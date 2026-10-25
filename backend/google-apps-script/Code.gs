/**
 * A1esmat booking backend for Google Apps Script.
 * Script Properties (required): CALENDAR_ID, SHEET_ID, OWNER_EMAIL (legacy name: NOTIFY_EMAIL).
 * Optional: BUSY_CALENDAR_IDS (comma-separated extra calendars whose events block slots,
 * e.g. Ahmed's personal calendar), ALL_DAY_BLOCKS ("true" to let all-day events block whole days),
 * OWNER_WHATSAPP (digits only), BLOCKED_DATES (YYYY-MM-DD,...), WORKING_DAYS (1=Mon..7=Sun),
 * START, END, SLOT_MINUTES, BUFFER_MINUTES, MIN_NOTICE_HOURS, HORIZON_DAYS, SITE_HOST (default a1esmat.com).
 * Meta Conversions API (optional): META_PIXEL_ID, META_CAPI_TOKEN, META_TEST_EVENT_CODE (only while testing).
 * WhatsApp Cloud API (optional): WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_OWNER_NUMBER,
 * WHATSAPP_OWNER_TEMPLATE (1 body variable: the lead summary), WHATSAPP_REMINDER_TEMPLATE
 * (2 body variables: client name, date and time), WHATSAPP_LANG_EN / WHATSAPP_LANG_AR (template
 * language codes exactly as approved, default "en" / "ar").
 * Proxy (optional, for per-IP rate limiting): PROXY_SECRET, shared with backend/cloudflare-worker.
 * Once PROXY_SECRET is set, writes that do not come through the proxy are refused.
 * Deploy as a Web App executed as the owner and accessible to anyone.
 *
 * Quick start: run setup() once from the editor. It fills the required properties
 * (a new "A1esmat Leads" sheet, your default calendar, your email) and installs the reminder trigger.
 */
const SETTINGS = {
  timezone: 'Asia/Dubai', workingDays: [1, 2, 3, 4, 5, 6],
  start: '10:00', end: '19:00', slotMinutes: 30, bufferMinutes: 15,
  minNoticeHours: 3, horizonDays: 14, ownerWhatsapp: '971547772515', siteHost: 'a1esmat.com'
};
// Abuse limits (per rolling window held in CacheService).
const LIMITS = { perPhone: 12, perIp: 30, leadsPer10Min: 40, booksPer10Min: 20, ownerMailsPer6h: 40, activeBookingsPerPhone: 2 };

function settings_() {
  const p = props_(), s = Object.assign({}, SETTINGS);
  if (p.getProperty('WORKING_DAYS')) s.workingDays = p.getProperty('WORKING_DAYS').split(',').map(Number).filter(n => n >= 1 && n <= 7);
  if (p.getProperty('START')) s.start = p.getProperty('START');
  if (p.getProperty('END')) s.end = p.getProperty('END');
  if (p.getProperty('OWNER_WHATSAPP')) s.ownerWhatsapp = p.getProperty('OWNER_WHATSAPP').replace(/\D/g, '');
  if (p.getProperty('SITE_HOST')) s.siteHost = p.getProperty('SITE_HOST');
  [['SLOT_MINUTES', 'slotMinutes'], ['BUFFER_MINUTES', 'bufferMinutes'], ['MIN_NOTICE_HOURS', 'minNoticeHours'], ['HORIZON_DAYS', 'horizonDays']]
    .forEach(x => { if (p.getProperty(x[0])) s[x[1]] = Number(p.getProperty(x[0])); });
  return s;
}

function json_(value) {
  return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);
}
// Only these error codes reach the browser; anything else is logged and reported as server_error.
const PUBLIC_ERRORS = ['invalid_action', 'invalid_name', 'invalid_phone', 'invalid_email', 'invalid_field', 'consent_required', 'rate_limited',
  'slot_taken', 'busy_try_again', 'too_many_bookings', 'invalid_date', 'invalid_datetime', 'forbidden'];
function fail_(err) {
  const code = String((err && err.message) || err);
  if (PUBLIC_ERRORS.indexOf(code) !== -1) return json_({ ok: false, error: code, code: code });
  console.error(err);
  return json_({ ok: false, error: 'server_error' });
}
/** Run a side effect that must never turn a saved booking into an error for the visitor. */
function safely_(label, fn) { try { fn(); } catch (e) { console.error(label + ' failed', e); } }

function doGet(e) {
  try {
    const action = e && e.parameter.action;
    if (action === 'days') return json_({ ok: true, days: availableDays_() });
    if (action === 'slots') return json_({ ok: true, date: e.parameter.date, slots: availableSlots_(e.parameter.date) });
    return json_({ ok: false, error: 'invalid_action' });
  } catch (err) { return fail_(err); }
}

function doPost(e) {
  try {
    const raw = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) throw new Error('invalid_action');
    if (raw.website || raw.honeypot) return json_({ ok: true }); // honeypot: silently discard
    trustProxy_(raw);
    const data = clean_(raw);
    if (data.client_ip) rateLimit_('ip:' + data.client_ip, LIMITS.perIp);
    rateLimit_('phone:' + data.phone, LIMITS.perPhone);
    if (data.action === 'lead') return lead_(data);
    if (data.action === 'book') return book_(data);
    throw new Error('invalid_action');
  } catch (err) { return fail_(err); }
}

function lead_(data) {
  rateLimit_('global:lead', LIMITS.leadsPer10Min);
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) throw new Error('busy_try_again');
  let saved;
  try { saved = upsertLead_(data, 'Lead'); } finally { lock.releaseLock(); }
  // pressing Continue again must not re-notify
  if (saved.isNew) { safely_('owner notify', () => notifyOwner_(data, false)); safely_('capi', () => sendMetaEvent_('Lead', data)); }
  return json_({ ok: true, lead_id: data.lead_id });
}

function book_(data) {
  if (!data.date || !data.time || !data.meeting_type) throw new Error('invalid_datetime');
  rateLimit_('global:book', LIMITS.booksPer10Min);
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) throw new Error('busy_try_again');
  const s = settings_(), start = dubaiDate_(data.date, data.time), end = new Date(start.getTime() + s.slotMinutes * 60000);
  let previousEvent = '';
  try {
    if (availableSlots_(data.date).indexOf(data.time) === -1) throw new Error('slot_taken'); // re-checked on the server at submit time
    if (activeBookings_(data.phone, data.lead_id) >= LIMITS.activeBookingsPerPhone) throw new Error('too_many_bookings');
    const event = createEvent_(data, start, end);
    data.booking_id = event.id; data.meet_link = event.meetLink || '';
    previousEvent = upsertLead_(data, 'Booked').previousEvent;
  } finally { lock.releaseLock(); }
  CacheService.getScriptCache().remove('days-v1');
  // The booking exists now: nothing below may report failure to the visitor.
  if (previousEvent && previousEvent !== data.booking_id) safely_('remove replaced event', () => deleteEvent_(previousEvent));
  safely_('owner notify', () => notifyOwner_(data, true));
  safely_('client email', () => sendClientConfirmation_(data));
  safely_('capi', () => sendMetaEvent_('Schedule', data));
  return json_({ ok: true, booking_id: data.booking_id, lead_id: data.lead_id, start_iso: start.toISOString(), end_iso: end.toISOString(), meet_link: data.meet_link });
}

function props_() { return PropertiesService.getScriptProperties(); }
function calendar_() {
  const id = props_().getProperty('CALENDAR_ID');
  if (!id) throw new Error('calendar_not_configured');
  const cal = CalendarApp.getCalendarById(id); if (!cal) throw new Error('calendar_not_found'); return cal;
}
/** The booking calendar plus every calendar listed in BUSY_CALENDAR_IDS. A missing one fails closed (no double bookings). */
function busyCalendars_() {
  const extra = (props_().getProperty('BUSY_CALENDAR_IDS') || '').split(',').map(x => x.trim()).filter(Boolean);
  return [calendar_()].concat(extra.map(id => {
    const cal = CalendarApp.getCalendarById(id);
    if (!cal) throw new Error('busy_calendar_not_found: ' + id); // share it with the deploying account
    return cal;
  }));
}
function deleteEvent_(id) { const ev = calendar_().getEventById(id); if (ev) ev.deleteEvent(); }

const HEADERS = ['Created', 'Updated', 'Lead ID', 'Status', 'Name', 'Phone', 'Email', 'Interest', 'Emirate', 'Budget', 'Purpose', 'Timeline', 'Date', 'Time', 'Meeting type', 'Topic',
  'UTM source', 'UTM medium', 'UTM campaign', 'UTM content', 'fbclid', '_fbp', '_fbc', 'Landing URL', 'Language', 'Calendar event ID', 'Reminder 24h', 'Reminder 1h', 'Tier', 'Meet link'];
const COL = { leadId: 2, status: 3, name: 4, phone: 5, email: 6, date: 12, time: 13, language: 24, eventId: 25, rem24: 26, rem1: 27 };
function sheet_() {
  const id = props_().getProperty('SHEET_ID'); if (!id) throw new Error('sheet_not_configured');
  const ss = SpreadsheetApp.openById(id); let sh = ss.getSheetByName('Leads');
  if (!sh) { sh = ss.insertSheet('Leads'); sh.appendRow(HEADERS); sh.setFrozenRows(1); }
  return sh;
}
/** Force plain text: keeps "+971…" phones and "2026-10-06" dates as typed, and stops "=…" being run as a formula. */
function text_(v) { return v === undefined || v === null || v === '' ? '' : "'" + String(v).slice(0, 500); }
/** Read a date/time cell back as text even if Sheets turned it into a Date. */
function cellText_(v, pattern) { return v instanceof Date ? Utilities.formatDate(v, SETTINGS.timezone, pattern) : String(v || ''); }

// Every choice field must be one of the form's own values; labels are derived here, never trusted from the browser.
const CHOICES = {
  interest: { villa: 'Villa', townhouse: 'Townhouse', offplan: 'Off-plan launch', unsure: 'Not sure' },
  emirate: { dubai: 'Dubai', 'abu-dhabi': 'Abu Dhabi', both: 'Both' },
  budget: { 'under-2': 'Under 2M', '2-3': '2M–3M', '3-5': '3M–5M', '5-8': '5M–8M', '8-12': '8M–12M', 'over-12': 'Over 12M' },
  purpose: { live: 'Live in it', invest: 'Invest', both: 'Both' },
  timeline: { '0-3': 'Within 3 months', '3-6': '3–6 months', '6-12': '6–12 months', exploring: 'Just exploring' },
  meeting_type: { phone: 'Phone / WhatsApp call', video: 'Video call', person: 'In person (Dubai)' },
  language: { en: 'English', ar: 'Arabic' },
  tier: { '2.7-4': 'AED 2.7M–4M', '4-6': 'AED 4M–6M', '6-9': 'AED 6M–9M', '9-12': 'AED 9M–12M' }
};
const FREE_TEXT = { topic: 200, utm_source: 100, utm_medium: 100, utm_campaign: 150, utm_content: 150, fbclid: 300, _fbp: 200, _fbc: 400,
  landing_url: 500, client_user_agent: 400, event_id: 100, client_ip: 64 };
/** Build the record from an allow-list only: unknown keys are dropped, lengths are capped, choices are checked. */
function clean_(raw) {
  const str = v => (v === undefined || v === null ? '' : String(v)).trim();
  const d = { action: str(raw.action) };
  d.name = str(raw.name).replace(/\s+/g, ' ');
  // Letters, spaces and . ' - only: no links or numbers that could be turned into phishing text in emails.
  // Dots are allowed in initials ("J.R. Smith"), never before a word as in a domain ("evil.co").
  if (!/^[\p{L}\p{M}][\p{L}\p{M} .'’-]{1,79}$/u.test(d.name) || /\.[\p{L}\p{M}]{2}/u.test(d.name)) throw new Error('invalid_name');
  d.phone = str(raw.phone);
  const digits = d.phone.replace(/\D/g, '');
  if (!/^\+?[\d\s()-]+$/.test(d.phone) || digits.length < 8 || digits.length > 15) throw new Error('invalid_phone');
  d.phone = '+' + digits;
  d.email = str(raw.email).toLowerCase();
  if (d.email && (d.email.length > 120 || !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(d.email))) throw new Error('invalid_email');
  if (!raw.consent) throw new Error('consent_required');
  Object.keys(CHOICES).forEach(k => {
    const v = str(raw[k]);
    if (v && !Object.prototype.hasOwnProperty.call(CHOICES[k], v)) throw new Error('invalid_field');
    d[k] = v; if (v) d[k + '_label'] = CHOICES[k][v];
  });
  Object.keys(FREE_TEXT).forEach(k => { d[k] = str(raw[k]).slice(0, FREE_TEXT[k]); });
  d.lead_id = /^[A-Za-z0-9-]{8,64}$/.test(str(raw.lead_id)) ? str(raw.lead_id) : Utilities.getUuid();
  d.date = str(raw.date); d.time = str(raw.time);
  if (d.date && !/^\d{4}-\d{2}-\d{2}$/.test(d.date)) throw new Error('invalid_date');
  if (d.time && !/^\d{2}:\d{2}$/.test(d.time)) throw new Error('invalid_datetime');
  d.analytics_consent = raw.analytics_consent === true || raw.analytics_consent === 'true';
  return d;
}
function rateLimit_(key, max, seconds) {
  const digest = Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(key))).slice(0, 24);
  const cache = CacheService.getScriptCache(), k = 'rl-' + digest, count = Number(cache.get(k) || 0) + 1;
  if (count > max) throw new Error('rate_limited'); cache.put(k, String(count), seconds || 600);
}
/** Apps Script cannot see the visitor's IP; the optional proxy adds it, signed with PROXY_SECRET. */
function trustProxy_(d) {
  const secret = props_().getProperty('PROXY_SECRET');
  if (secret && d.proxy_secret !== secret) throw new Error('forbidden'); // the per-IP limit cannot be bypassed
  if (!secret) delete d.client_ip;
  delete d.proxy_secret;
}
function sha256_(v) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(v).trim().toLowerCase(), Utilities.Charset.UTF_8)
    .map(b => ((b + 256) % 256).toString(16).padStart(2, '0')).join('');
}
/** Meta Conversions API, de-duplicated with the browser Pixel through the shared event_id. */
function sendMetaEvent_(name, d) {
  const p = props_(), pixel = p.getProperty('META_PIXEL_ID'), token = p.getProperty('META_CAPI_TOKEN');
  if (!pixel || !token || !d.analytics_consent) return; // only with the visitor's analytics consent
  const host = settings_().siteHost;
  let url = 'https://' + host + '/';
  try { if (new RegExp('^https://(www\\.)?' + host.replace(/\./g, '\\.') + '/').test(d.landing_url)) url = d.landing_url; } catch (e) { /* keep the default */ }
  const first = d.name.split(' ')[0];
  const user = { ph: [sha256_(d.phone.replace(/\D/g, ''))], em: d.email ? [sha256_(d.email)] : undefined, fn: first ? [sha256_(first)] : undefined,
    fbc: d._fbc || undefined, fbp: d._fbp || undefined, client_user_agent: d.client_user_agent || undefined, client_ip_address: d.client_ip || undefined,
    external_id: [sha256_(d.lead_id)] };
  const custom = { budget_band: d.budget, interest: d.interest, emirate: d.emirate, meeting_type: d.meeting_type || undefined, content_name: d.topic || undefined };
  const body = { data: [{ event_name: name, event_time: Math.floor(Date.now() / 1000), event_id: d.event_id, action_source: 'website',
    event_source_url: url, user_data: user, custom_data: custom }] };
  if (p.getProperty('META_TEST_EVENT_CODE')) body.test_event_code = p.getProperty('META_TEST_EVENT_CODE');
  UrlFetchApp.fetch('https://graph.facebook.com/v22.0/' + pixel + '/events?access_token=' + encodeURIComponent(token),
    { method: 'post', contentType: 'application/json', payload: JSON.stringify(body), muteHttpExceptions: true });
}
function dubaiDate_(date, time) { if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time)) throw new Error('invalid_datetime'); return new Date(date + 'T' + time + ':00+04:00'); }
function minutes_(s) { const p = s.split(':').map(Number); return p[0] * 60 + p[1]; }
function isoDay_(d) { return Utilities.formatDate(d, SETTINGS.timezone, 'yyyy-MM-dd'); }

/** Busy intervals [start, end] (ms) across every busy calendar between two instants. */
function busyBetween_(from, to) {
  const allDayBlocks = props_().getProperty('ALL_DAY_BLOCKS') === 'true', busy = [];
  busyCalendars_().forEach(cal => cal.getEvents(from, to).forEach(ev => {
    if (ev.getMyStatus && ev.getMyStatus() === CalendarApp.GuestStatus.NO) return; // declined invitations do not block
    if (!allDayBlocks && ev.isAllDayEvent && ev.isAllDayEvent()) return;          // birthdays, holidays, working location
    busy.push([ev.getStartTime().getTime(), ev.getEndTime().getTime()]);
  }));
  return busy;
}
/** Free slots for one day given precomputed busy intervals. */
function slotsFor_(date, busy, s, now) {
  const blocked = (props_().getProperty('BLOCKED_DATES') || '').split(',').map(x => x.trim());
  if (blocked.indexOf(date) !== -1) return [];
  const noon = new Date(date + 'T12:00:00+04:00'), weekday = Number(Utilities.formatDate(noon, s.timezone, 'u'));
  if (s.workingDays.indexOf(weekday) === -1) return [];
  if (noon.getTime() > now + s.horizonDays * 86400000 || noon.getTime() < now - 86400000) return [];
  const out = [], first = minutes_(s.start), last = minutes_(s.end), step = s.slotMinutes + s.bufferMinutes, pad = s.bufferMinutes * 60000;
  for (let m = first; m + s.slotMinutes <= last; m += step) {
    const time = String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0');
    const start = dubaiDate_(date, time).getTime(), end = start + s.slotMinutes * 60000;
    if (start < now + s.minNoticeHours * 3600000) continue;
    if (!busy.some(b => b[0] < end + pad && b[1] > start - pad)) out.push(time);
  }
  return out;
}
function availableSlots_(date) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error('invalid_date');
  const s = settings_(), pad = s.bufferMinutes * 60000;
  const busy = busyBetween_(new Date(dubaiDate_(date, s.start).getTime() - pad), new Date(dubaiDate_(date, s.end).getTime() + pad));
  return slotsFor_(date, busy, s, Date.now());
}
/** Every day of the horizon in one calendar read (one request per visitor), cached for a minute. */
function availableDays_() {
  const cache = CacheService.getScriptCache(), hit = cache.get('days-v1');
  if (hit) return JSON.parse(hit);
  const s = settings_(), now = Date.now(), from = new Date(now), to = new Date(now + (s.horizonDays + 1) * 86400000);
  const busy = busyBetween_(from, to), days = {};
  for (let i = 0; i <= s.horizonDays; i++) { const date = isoDay_(new Date(now + i * 86400000)); days[date] = slotsFor_(date, busy, s, now); }
  cache.put('days-v1', JSON.stringify(days), 60);
  return days;
}

/** Bookings still ahead for this phone, other than this lead's own. */
function activeBookings_(phone, leadId) {
  const rows = sheet_().getDataRange().getValues(), today = isoDay_(new Date());
  return rows.slice(1).filter(r => r[COL.status] === 'Booked' && String(r[COL.phone]) === phone && String(r[COL.leadId]) !== leadId
    && cellText_(r[COL.date], 'yyyy-MM-dd') >= today).length;
}

function createEvent_(d, start, end) {
  // The client is NOT added as a guest: Google invites would let anyone make Ahmed's calendar email arbitrary addresses.
  // The client gets our own confirmation email instead, so the description can carry Ahmed's internal notes.
  const title = 'Consultation: ' + d.name + ' · ' + (d.budget_label || '-') + ' · ' + (d.interest_label || '-');
  const description = ['Phone: ' + d.phone, 'Email: ' + (d.email || '-'), 'Interest: ' + (d.interest_label || '-'), 'Emirate: ' + (d.emirate_label || '-'),
    'Budget: ' + (d.budget_label || '-'), 'Purpose: ' + (d.purpose_label || '-'), 'Timeline: ' + (d.timeline_label || '-'), 'Meeting: ' + (d.meeting_type_label || '-'),
    d.topic ? 'Topic: ' + d.topic : '', d.tier ? 'Tier: ' + d.tier_label : '', 'Language: ' + (d.language || '-'),
    'Source: ' + [d.utm_source, d.utm_medium, d.utm_campaign, d.utm_content].filter(Boolean).join(' / '), 'Page: ' + d.landing_url, 'Lead ID: ' + d.lead_id]
    .filter(Boolean).join('\n');
  if (d.meeting_type === 'video' && typeof Calendar !== 'undefined') {
    const resource = {
      summary: title, description: description,
      start: { dateTime: start.toISOString(), timeZone: SETTINGS.timezone }, end: { dateTime: end.toISOString(), timeZone: SETTINGS.timezone },
      reminders: { useDefault: false, overrides: [{ method: 'email', minutes: 1440 }, { method: 'popup', minutes: 60 }] },
      conferenceData: { createRequest: { requestId: d.lead_id + '-' + start.getTime(), conferenceSolutionKey: { type: 'hangoutsMeet' } } }
    };
    const created = Calendar.Events.insert(resource, props_().getProperty('CALENDAR_ID'), { conferenceDataVersion: 1, sendUpdates: 'none' });
    // Store the iCalUID: it is the id CalendarApp.getEventById understands, so a re-booking can delete this event.
    return { id: created.iCalUID || created.id, meetLink: created.hangoutLink || '' };
  }
  const event = calendar_().createEvent(title, start, end, { description: description });
  event.addEmailReminder(60); event.addEmailReminder(1440);
  return { id: event.getId(), meetLink: '' };
}
/**
 * Insert or update the lead's row (call with the script lock held).
 * A lead_id only matches a row with the same phone, so nobody can overwrite another person's row.
 * Returns { isNew, previousEvent } (previousEvent: the calendar event this booking replaces).
 */
function upsertLead_(d, status) {
  const sh = sheet_(), rows = sh.getDataRange().getValues(), now = new Date(); let row = 0;
  for (let i = 1; i < rows.length; i++) if (String(rows[i][COL.leadId]) === d.lead_id) { row = i + 1; break; }
  if (row && String(rows[row - 1][COL.phone]) !== d.phone) { d.lead_id = Utilities.getUuid(); row = 0; }
  const old = row ? rows[row - 1] : [];
  if (row && status === 'Lead' && old[COL.status] === 'Booked') return { isNew: false, previousEvent: '' }; // never downgrade a booked lead
  const rebooked = row && status === 'Booked' && old[COL.status] === 'Booked';
  const keepFlags = row && !rebooked;
  const values = [row ? old[0] : now, now, text_(d.lead_id), status, text_(d.name), text_(d.phone), text_(d.email), text_(d.interest_label), text_(d.emirate_label),
    text_(d.budget_label), text_(d.purpose_label), text_(d.timeline_label), text_(d.date), text_(d.time), text_(d.meeting_type_label), text_(d.topic),
    text_(d.utm_source), text_(d.utm_medium), text_(d.utm_campaign), text_(d.utm_content), text_(d.fbclid), text_(d._fbp), text_(d._fbc),
    text_(d.landing_url), text_(d.language), text_(d.booking_id), keepFlags ? old[COL.rem24] === true : false, keepFlags ? old[COL.rem1] === true : false,
    text_(d.tier_label), text_(d.meet_link)];
  if (row) sh.getRange(row, 1, 1, values.length).setValues([values]); else sh.appendRow(values);
  return { isNew: !row, previousEvent: rebooked ? String(old[COL.eventId] || '') : '' };
}
const AR_DAYS = ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد'];
const AR_MONTHS = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'];
function whenText_(d, ar) {
  const noon = dubaiDate_(d.date, '12:00'), f = p => Utilities.formatDate(noon, SETTINGS.timezone, p);
  if (ar) return AR_DAYS[Number(f('u')) - 1] + ' ' + Number(f('d')) + ' ' + AR_MONTHS[Number(f('M')) - 1] + ' ' + f('yyyy') + ' الساعة ' + d.time + ' بتوقيت دبي';
  return f('EEEE d MMMM yyyy') + ' at ' + d.time + ' (Dubai time)';
}
function notifyOwner_(d, booked) {
  const email = props_().getProperty('OWNER_EMAIL') || props_().getProperty('NOTIFY_EMAIL');
  const when = booked ? whenText_(d, false) + ' · ' + d.meeting_type_label : 'not booked yet';
  const summary = 'New lead: ' + d.name + ', ' + (d.budget_label || '-') + ', ' + (d.interest_label || '-') + ', ' + when;
  const body = [summary, '', 'Phone/WhatsApp: ' + d.phone, 'Email: ' + (d.email || '-'), 'Emirate: ' + (d.emirate_label || '-'), 'Purpose: ' + (d.purpose_label || '-'),
    'Timeline: ' + (d.timeline_label || '-'), d.topic ? 'Topic: ' + d.topic : '', d.meet_link ? 'Meet: ' + d.meet_link : '',
    'Source: ' + [d.utm_source, d.utm_medium, d.utm_campaign].filter(Boolean).join(' / '), 'Page: ' + d.landing_url,
    '', 'WhatsApp the client: https://wa.me/' + d.phone.replace(/\D/g, '')].filter(x => x !== '').join('\n');
  // A flood of fake leads must not use up the daily MailApp quota needed for real confirmations.
  let mailAllowed = true;
  try { rateLimit_('owner-mail', LIMITS.ownerMailsPer6h, 21600); } catch (e) { mailAllowed = false; }
  if (email && mailAllowed) MailApp.sendEmail(email, (booked ? 'Booked: ' : 'New lead: ') + d.name, body);
  notifyOwnerWhatsApp_(summary);
}
function changeLink_(d, ar) {
  const msg = (ar ? 'مرحباً أحمد، أريد تغيير موعد الاستشارة: ' : 'Hi Ahmed, I need to change my consultation time: ') + d.name + ' · ' + d.date + ' ' + d.time;
  return 'https://wa.me/' + settings_().ownerWhatsapp + '?text=' + encodeURIComponent(msg);
}
function sendClientConfirmation_(d) {
  if (!d.email) return;
  const ar = d.language === 'ar';
  const meeting = { phone: ar ? 'مكالمة هاتف / واتساب' : 'Phone / WhatsApp call', video: ar ? 'مكالمة فيديو' : 'Video call', person: ar ? 'مقابلة شخصية في دبي' : 'In person (Dubai)' }[d.meeting_type];
  const lines = ar
    ? ['مرحباً ' + d.name + '،', '', 'تم حجز استشارتك مع أحمد عصمت: ' + whenText_(d, true) + '.', 'نوع المقابلة: ' + meeting,
       d.meet_link ? 'رابط مكالمة الفيديو: ' + d.meet_link : '', d.meeting_type === 'person' ? 'سيؤكد أحمد مكان اللقاء على واتساب.' : '',
       '', 'غيّر الموعد: ' + changeLink_(d, true), '', 'أحمد عصمت · a1esmat.com']
    : ['Hi ' + d.name + ',', '', 'Your consultation with Ahmed Esmat is booked: ' + whenText_(d, false) + '.', 'Meeting type: ' + meeting,
       d.meet_link ? 'Video call link: ' + d.meet_link : '', d.meeting_type === 'person' ? 'Ahmed will confirm the meeting place on WhatsApp.' : '',
       '', 'Change the time: ' + changeLink_(d, false), '', 'Ahmed Esmat · a1esmat.com'];
  MailApp.sendEmail(d.email, ar ? 'تأكيد استشارتك مع أحمد عصمت' : 'Your consultation with Ahmed Esmat', lines.filter((x, i, a) => x !== '' || a[i - 1] !== '').join('\n'));
}
function whatsApp_(to, message) {
  const p = props_(), token = p.getProperty('WHATSAPP_TOKEN'), phoneId = p.getProperty('WHATSAPP_PHONE_NUMBER_ID');
  if (!token || !phoneId || !to) return false;
  const payload = Object.assign({ messaging_product: 'whatsapp', to: String(to).replace(/\D/g, '') }, message);
  try {
    const r = UrlFetchApp.fetch('https://graph.facebook.com/v22.0/' + phoneId + '/messages', { method: 'post', contentType: 'application/json',
      headers: { Authorization: 'Bearer ' + token }, payload: JSON.stringify(payload), muteHttpExceptions: true });
    return r.getResponseCode() < 300;
  } catch (e) { console.error('WhatsApp failed', e); return false; }
}
function templateLang_(ar) { return props_().getProperty(ar ? 'WHATSAPP_LANG_AR' : 'WHATSAPP_LANG_EN') || (ar ? 'ar' : 'en'); }
function template_(name, lang, params) {
  return { type: 'template', template: { name: name, language: { code: lang }, components: [{ type: 'body', parameters: params.map(t => ({ type: 'text', text: String(t) })) }] } };
}
/** Owner alert. Business-initiated messages need an approved template; free text only works inside a 24h chat window. */
function notifyOwnerWhatsApp_(text) {
  const p = props_(), to = p.getProperty('WHATSAPP_OWNER_NUMBER'), tpl = p.getProperty('WHATSAPP_OWNER_TEMPLATE');
  whatsApp_(to, tpl ? template_(tpl, templateLang_(false), [text]) : { type: 'text', text: { body: text } });
}
/** Install a time-driven trigger to run this function every 15 minutes. */
function sendReminders() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return; // the next run (15 min) picks the reminders up
  try {
    const sh = sheet_(), rows = sh.getDataRange().getValues(), now = Date.now(), waTemplate = props_().getProperty('WHATSAPP_REMINDER_TEMPLATE');
    for (let i = 1; i < rows.length; i++) {
      try { // one bad row must not stop the others
        const r = rows[i]; if (r[COL.status] !== 'Booked' || !r[COL.date] || !r[COL.time] || (!r[COL.email] && !waTemplate)) continue;
        const d = { name: r[COL.name], phone: r[COL.phone], date: cellText_(r[COL.date], 'yyyy-MM-dd'), time: cellText_(r[COL.time], 'HH:mm'), language: r[COL.language] };
        const hours = (dubaiDate_(d.date, d.time).getTime() - now) / 3600000, ar = d.language === 'ar';
        const subject = ar ? 'تذكير بموعد استشارتك' : 'Consultation reminder';
        const remind = (col, text) => {
          sh.getRange(i + 1, col + 1).setValue(true); // mark first: a failure must not cause repeated sends
          if (r[COL.email]) safely_('reminder email', () => MailApp.sendEmail(r[COL.email], subject, text));
          if (waTemplate) whatsApp_(d.phone, template_(waTemplate, templateLang_(ar), [d.name, whenText_(d, ar)]));
        };
        if (hours > 23.75 && hours <= 24.25 && r[COL.rem24] !== true)
          remind(COL.rem24, (ar ? 'تذكير: استشارتك مع أحمد عصمت غدًا، ' : 'Reminder: your consultation with Ahmed Esmat is tomorrow, ') + whenText_(d, ar) + '.\n\n' + (ar ? 'غيّر الموعد: ' : 'Change the time: ') + changeLink_(d, ar));
        if (hours > .75 && hours <= 1.25 && r[COL.rem1] !== true)
          remind(COL.rem1, (ar ? 'تذكير: استشارتك مع أحمد عصمت بعد ساعة، ' : 'Reminder: your consultation with Ahmed Esmat is in one hour, ') + whenText_(d, ar) + '.');
      } catch (e) { console.error('reminder row ' + (i + 1), e); }
    }
  } finally { lock.releaseLock(); }
}

/**
 * One-time setup. Run it from the Apps Script editor (select "setup", click Run, allow access).
 * Safe to run again: it only fills what is missing and never creates a second trigger.
 */
function setup() {
  const p = props_(), done = [];
  if (!p.getProperty('SHEET_ID')) {
    const ss = SpreadsheetApp.create('A1esmat Leads');
    p.setProperty('SHEET_ID', ss.getId()); done.push('Created the sheet: ' + ss.getUrl());
  }
  if (!p.getProperty('CALENDAR_ID')) {
    p.setProperty('CALENDAR_ID', CalendarApp.getDefaultCalendar().getId()); done.push('Bookings go to calendar: ' + p.getProperty('CALENDAR_ID'));
  }
  if (!p.getProperty('OWNER_EMAIL') && !p.getProperty('NOTIFY_EMAIL')) {
    p.setProperty('OWNER_EMAIL', Session.getEffectiveUser().getEmail()); done.push('Lead emails go to: ' + p.getProperty('OWNER_EMAIL'));
  }
  sheet_(); // creates the Leads tab with its headers
  if (!ScriptApp.getProjectTriggers().some(t => t.getHandlerFunction() === 'sendReminders')) {
    ScriptApp.newTrigger('sendReminders').timeBased().everyMinutes(15).create(); done.push('Reminders run every 15 minutes');
  }
  const today = isoDay_(new Date());
  done.push('Free times today (' + today + '): ' + (availableSlots_(today).join(', ') || 'none'));
  console.log(done.join('\n') + '\nNext: Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone) and copy the /exec URL.');
  return done;
}
