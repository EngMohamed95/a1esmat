// Runs backend/google-apps-script/Code.gs against in-memory fakes of Calendar, Sheets, Mail, Cache and UrlFetch.
// The fake sheet converts typed values the way Google Sheets does (dates, numbers, formulas).
const fs = require('fs'), vm = require('vm'), assert = require('assert'), crypto = require('crypto');
const code = fs.readFileSync(require('path').join(__dirname, '..', 'backend', 'google-apps-script', 'Code.gs'), 'utf8');

let NOW = Date.parse('2026-10-05T06:00:00Z'); // Monday 10:00 Dubai
const RealDate = Date;
class FakeDate extends RealDate { constructor(...a) { if (a.length === 0) super(NOW); else super(...a); } static now() { return NOW; } }

const mails = [], fetches = [], own = [], personal = [];
const props = { CALENDAR_ID: 'cal', SHEET_ID: 'sh', OWNER_EMAIL: 'owner@x.com', BUSY_CALENDAR_IDS: 'personal', BLOCKED_DATES: '2026-10-08',
  META_PIXEL_ID: 'PX1', META_CAPI_TOKEN: 'TOK', WHATSAPP_TOKEN: 'WT', WHATSAPP_PHONE_NUMBER_ID: 'PN', WHATSAPP_OWNER_NUMBER: '971500000000',
  WHATSAPP_REMINDER_TEMPLATE: 'consult_reminder' };
let failMail = false, uuid = 0;

function conv(v) {
  if (typeof v !== 'string') return v;
  if (v.startsWith("'")) return v.slice(1);
  if (/^\d{4}-\d{2}-\d{2}$/.test(v)) return new RealDate(v + 'T00:00:00+04:00');
  if (/^\d{2}:\d{2}$/.test(v)) return new RealDate('1899-12-30T' + v + ':00+04:00');
  if (/^\+?\d+$/.test(v)) return Number(v);
  if (v.startsWith('=')) return 'FORMULA!';
  return v;
}
const rows = [];
const sheet = { appendRow: r => rows.push(r.map(conv)), setFrozenRows() {}, getDataRange: () => ({ getValues: () => rows.map(r => r.slice()) }),
  getRange: (r, c) => ({ setValues: v => { rows[r - 1] = v[0].map(conv); }, setValue: v => { rows[r - 1][c - 1] = v; } }) };
let nextEvent = 0;
function cal(list) {
  return {
    getEvents: (a, b) => list.filter(e => !e.deleted && e.s < b && e.e > a).map(e => ({ getStartTime: () => e.s, getEndTime: () => e.e,
      getMyStatus: () => e.status || 'YES', isAllDayEvent: () => !!e.allDay })),
    createEvent: (t, s, e, o) => { const ev = { id: 'ev' + (++nextEvent), s, e, t, o }; list.push(ev); return { getId: () => ev.id, addEmailReminder() {} }; },
    getEventById: id => { const ev = list.find(x => x.id === id); return ev && { deleteEvent: () => { ev.deleted = true; } }; },
  };
}
const cache = {};
const ctx = { Date: FakeDate, console: { error() {}, log() {} }, JSON, Math, String, Number, Object, Array, Boolean, RegExp, Error, encodeURIComponent,
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k] || null }) },
  CalendarApp: { GuestStatus: { NO: 'NO' }, getCalendarById: id => id === 'cal' ? cal(own) : id === 'personal' ? cal(personal) : null },
  SpreadsheetApp: { openById: () => ({ getSheetByName: () => rows.length ? sheet : null, insertSheet: () => sheet }) },
  MailApp: { sendEmail: (to, s, b) => { if (failMail) throw new Error('Service invoked too many times: email'); mails.push({ to, s, b }); } },
  ContentService: { createTextOutput: t => ({ setMimeType: () => JSON.parse(t) }), MimeType: { JSON: 1 } },
  LockService: { getScriptLock: () => ({ tryLock: () => true, releaseLock() {} }) },
  CacheService: { getScriptCache: () => ({ get: k => cache[k], put: (k, v) => { cache[k] = v; }, remove: k => { delete cache[k]; } }) },
  Utilities: { Charset: { UTF_8: 1 }, base64EncodeWebSafe: b => Buffer.from(b).toString('base64'), DigestAlgorithm: { SHA_256: 1 },
    computeDigest: (a, s) => [...crypto.createHash('sha256').update(s).digest()], getUuid: () => 'server-uuid-' + (++uuid),
    formatDate: (d, tz, p) => {
      const x = new RealDate(d.getTime() + 4 * 3600000), pad = n => String(n).padStart(2, '0');
      const D = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const M = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      return p.replace('EEEE', D[x.getUTCDay()]).replace('MMMM', M[x.getUTCMonth()]).replace('yyyy', x.getUTCFullYear()).replace('MM', pad(x.getUTCMonth() + 1))
        .replace('dd', pad(x.getUTCDate())).replace('HH', pad(x.getUTCHours())).replace('mm', pad(x.getUTCMinutes()))
        .replace(/\bu\b/, x.getUTCDay() || 7).replace(/\bd\b/, x.getUTCDate()).replace(/\bM\b/, x.getUTCMonth() + 1);
    } },
  UrlFetchApp: { fetch: (url, o) => { fetches.push({ url, body: JSON.parse(o.payload) }); return { getResponseCode: () => 200 }; } },
  // Advanced Calendar service (video calls): its event id differs from the iCalUID that CalendarApp uses.
  Calendar: { Events: { insert: (res) => { const ev = { id: 'ev' + (++nextEvent), s: new RealDate(res.start.dateTime), e: new RealDate(res.end.dateTime), t: res.summary, o: res };
    own.push(ev); return { id: 'api-' + ev.id, iCalUID: ev.id, hangoutLink: 'https://meet.google.com/abc' }; } } } };
vm.createContext(ctx); vm.runInContext(code, ctx);

// --- setup(): fills only missing properties and installs one reminder trigger
{
  const saved = { ...props }, triggers = [];
  Object.keys(props).forEach(k => delete props[k]);
  ctx.PropertiesService = { getScriptProperties: () => ({ getProperty: k => props[k] || null, setProperty: (k, v) => { props[k] = v; } }) };
  ctx.SpreadsheetApp = { ...ctx.SpreadsheetApp, create: () => ({ getId: () => 'new-sheet', getUrl: () => 'https://docs.google.com/x' }) };
  ctx.CalendarApp = { ...ctx.CalendarApp, getDefaultCalendar: () => ({ getId: () => 'cal' }) };
  ctx.Session = { getEffectiveUser: () => ({ getEmail: () => 'ahmed@x.com' }) };
  ctx.ScriptApp = { getProjectTriggers: () => triggers, newTrigger: h => ({ timeBased: () => ({ everyMinutes: () => ({ create: () => triggers.push({ getHandlerFunction: () => h }) }) }) }) };
  ctx.setup(); ctx.setup();
  assert.deepStrictEqual([props.SHEET_ID, props.CALENDAR_ID, props.OWNER_EMAIL], ['new-sheet', 'cal', 'ahmed@x.com'], 'setup fills the required properties');
  assert.strictEqual(triggers.length, 1, 'running setup twice installs one trigger');
  Object.keys(props).forEach(k => delete props[k]); Object.assign(props, saved);
  rows.length = 0; // setup created the sheet header; the tests below start from an empty sheet
}

const slots = date => ctx.doGet({ parameter: { action: 'slots', date } });
const post = d => ctx.doPost({ postData: { contents: JSON.stringify(d) } });
const clearLimits = () => Object.keys(cache).forEach(k => delete cache[k]);
const sha = v => crypto.createHash('sha256').update(v).digest('hex');
const base = { action: 'lead', lead_id: 'lead-0001', name: 'Sara Ali', phone: '+971501234567', consent: 'on', budget: '3-5', interest: 'villa',
  emirate: 'dubai', purpose: 'live', timeline: '0-3', language: 'en', email: 'c@x.com', topic: '=HYPERLINK("x")' };

// --- availability
let r = slots('2026-10-05'); assert(r.ok, JSON.stringify(r));
assert.deepStrictEqual(r.slots.slice(0, 2), ['13:00', '13:45'], 'min notice 3h from 10:00 -> first slot 13:00');
assert.deepStrictEqual(slots('2026-10-11').slots, [], 'Sunday closed');
assert.deepStrictEqual(slots('2026-10-08').slots, [], 'blocked date');
assert.deepStrictEqual(slots('2026-10-25').slots, [], 'beyond horizon');
personal.push({ s: new RealDate('2026-10-06T11:00:00+04:00'), e: new RealDate('2026-10-06T12:00:00+04:00') });
personal.push({ s: new RealDate('2026-10-06T16:00:00+04:00'), e: new RealDate('2026-10-06T17:00:00+04:00'), status: 'NO' });
personal.push({ s: new RealDate('2026-10-07T00:00:00+04:00'), e: new RealDate('2026-10-08T00:00:00+04:00'), allDay: true });
const tue = slots('2026-10-06').slots;
assert(!tue.includes('11:30') && !tue.includes('10:45'), 'personal event + buffer blocks');
assert(tue.includes('16:00'), 'declined event does not block');
assert(slots('2026-10-07').slots.length > 0, 'all-day event (birthday) does not block the day');
const days = ctx.doGet({ parameter: { action: 'days' } });
assert(days.ok && days.days['2026-10-06'].join() === tue.join() && days.days['2026-10-11'].length === 0, 'days endpoint matches per-day slots');
props.BUSY_CALENDAR_IDS = 'personal,missing@x.com';
assert.strictEqual(slots('2026-10-06').error, 'server_error', 'unreadable busy calendar fails closed, internals not leaked');
props.BUSY_CALENDAR_IDS = 'personal';

// --- lead
assert(post(base).ok); assert(post(base).ok);
assert.strictEqual(mails.filter(m => m.to === 'owner@x.com').length, 1, 'owner notified once for repeated Continue');
assert.strictEqual(rows[1][5], '+971501234567', 'phone kept as text');
assert.strictEqual(rows[1][15], '=HYPERLINK("x")', 'free text never runs as a formula');
assert.strictEqual(rows[1][9], '3M–5M', 'labels come from the server, not the browser');

// --- validation (security review #1)
assert.strictEqual(post({ ...base, lead_id: 'lead-0099', name: 'Verify your account at evil.co' }).error, 'invalid_name', 'no links in names');
assert.strictEqual(post({ ...base, lead_id: 'lead-0099', budget: '<script>' }).error, 'invalid_field', 'choices must be form values');
assert.strictEqual(post({ ...base, lead_id: 'lead-0099', email: 'a@b' }).error, 'invalid_email');
assert.strictEqual(post([1, 2]).error, 'invalid_action', 'non-object body rejected');

// --- book
r = post({ ...base, action: 'book', date: '2026-10-06', time: '13:00', meeting_type: 'phone', injected: 'x'.repeat(5000) }); assert(r.ok, JSON.stringify(r));
const ev = own.find(e => e.id === r.booking_id);
assert(!ev.o.guests && !ev.o.sendInvites, 'client is never added as a calendar guest (no invites sent from Ahmed\'s account)');
assert(!ev.o.description.includes('injected') && ev.o.description.length < 1000, 'unknown keys never reach the event');
r = post({ ...base, lead_id: 'lead-0002', phone: '+971509999999', action: 'book', date: '2026-10-06', time: '13:00', meeting_type: 'phone' });
assert.strictEqual(r.error, 'slot_taken');
assert(!slots('2026-10-06').slots.includes('13:00') && slots('2026-10-06').slots.includes('13:45'), 'booked slot removed, next slot after buffer kept');
assert.strictEqual(rows.filter(x => x[2] === 'lead-0001').length, 1, 'one row per lead'); assert.strictEqual(rows[1][3], 'Booked');
const client = mails.find(m => m.to === 'c@x.com');
assert(client && /Tuesday 6 October 2026 at 13:00/.test(client.b) && /Change the time: https:\/\/wa.me\//.test(client.b), client && client.b);
assert(post(base).ok); assert.strictEqual(rows[1][3], 'Booked', 'lead resubmit does not downgrade');

// --- a failing email after the event exists must still confirm the booking (code review #1)
failMail = true;
r = post({ ...base, lead_id: 'lead-0003', phone: '+971504444444', action: 'book', date: '2026-10-06', time: '14:30', meeting_type: 'phone' });
failMail = false;
assert(r.ok, 'booking confirmed even when MailApp quota is exhausted: ' + JSON.stringify(r));

// --- re-booking the same lead replaces its old event instead of orphaning it
const firstEvent = rows[1][25];
r = post({ ...base, action: 'book', date: '2026-10-06', time: '15:15', meeting_type: 'phone' }); assert(r.ok, JSON.stringify(r));
assert(own.find(e => e.id === firstEvent).deleted, 'old event removed'); assert(slots('2026-10-06').slots.includes('13:00'), 'old slot freed');

// --- video bookings: Meet link returned, and a re-booking deletes the old video event too
r = post({ ...base, lead_id: 'lead-video', phone: '+971508888888', action: 'book', date: '2026-10-07', time: '13:00', meeting_type: 'video' });
assert(r.ok && r.meet_link === 'https://meet.google.com/abc', JSON.stringify(r));
const videoEvent = r.booking_id;
r = post({ ...base, lead_id: 'lead-video', phone: '+971508888888', action: 'book', date: '2026-10-07', time: '13:45', meeting_type: 'video' }); assert(r.ok);
assert(own.find(e => e.id === videoEvent).deleted, 'old video event removed on re-booking');

// --- names: initials pass, domains do not
assert(post({ ...base, lead_id: 'lead-names', phone: '+971507777777', name: 'J.R. Smith' }).ok, 'initials allowed');
assert(post({ ...base, lead_id: 'lead-names2', phone: '+971507777778', name: 'أحمد عبدُ الله' }).ok, 'Arabic names with diacritics allowed');

// --- someone else's lead_id cannot overwrite their row
post({ ...base, phone: '+971505555555', name: 'Attacker Name' });
assert.strictEqual(rows[1][4], 'Sara Ali', 'row with a different phone is never overwritten');

// --- per-phone cap on future bookings
clearLimits();
const many = i => post({ ...base, lead_id: 'lead-cap-' + i, phone: '+971506666666', action: 'book', date: '2026-10-09', time: ['10:00', '10:45', '11:30'][i], meeting_type: 'phone' });
assert(many(0).ok && many(1).ok); assert.strictEqual(many(2).error, 'too_many_bookings');

// --- rate limits
clearLimits();
let limited = 0; for (let i = 0; i < 15; i++) if (post({ ...base, lead_id: 'lead-rl-' + i }).error === 'rate_limited') limited++;
assert(limited >= 3, 'per-phone limit applies');
clearLimits();
limited = 0; for (let i = 0; i < 45; i++) if (post({ ...base, lead_id: 'lead-g-' + i, phone: '+9715070' + String(10000 + i) }).error === 'rate_limited') limited++;
assert(limited >= 5, 'global lead cap applies even when phones rotate');
clearLimits();

// --- reminders
const row1 = rows[1];
NOW = Date.parse('2026-10-05T11:15:00Z'); ctx.sendReminders(); // 24h before 15:15 Dubai
assert.strictEqual(row1[26], true, '24h reminder sent');
NOW = Date.parse('2026-10-06T10:15:00Z'); ctx.sendReminders();
assert.strictEqual(row1[27], true, '1h reminder sent');
rows.push(['x', 'x', 'bad', 'Booked', 'Bad Row', '+97150', 'bad@x.com', '', '', '', '', '', 'not-a-date', '10:00']);
row1[27] = false; ctx.sendReminders();
assert.strictEqual(row1[27], true, 'a bad row does not stop the other reminders');
rows.pop();

// --- Meta Conversions API
NOW = Date.parse('2026-10-05T06:00:00Z'); clearLimits();
assert.deepStrictEqual(fetches.filter(f => f.url.includes('/PX1/events')).length, 0, 'no CAPI without analytics consent');
const lead2 = { ...base, lead_id: 'lead-0010', phone: '+971502222222', analytics_consent: true, event_id: 'lead-lead-0010', client_user_agent: 'UA', landing_url: 'https://evil.example/' };
assert(post(lead2).ok);
r = post({ ...lead2, action: 'book', date: '2026-10-07', time: '10:00', meeting_type: 'phone', event_id: 'schedule-lead-0010' }); assert(r.ok, JSON.stringify(r));
const sent = fetches.filter(f => f.url.includes('/PX1/events')).map(f => f.body.data[0]);
assert.deepStrictEqual(sent.map(e => e.event_name + ':' + e.event_id), ['Lead:lead-lead-0010', 'Schedule:schedule-lead-0010']);
assert.strictEqual(sent[0].user_data.ph[0], sha('971502222222'), 'phone hashed');
assert(!JSON.stringify(sent).includes('+971502222222'), 'no plain phone in CAPI');
assert.strictEqual(sent[0].event_source_url, 'https://a1esmat.com/', 'foreign landing URLs are not forwarded');

// --- proxy: once PROXY_SECRET is set, direct calls are refused and the signed IP is used
props.PROXY_SECRET = 's3cret'; fetches.length = 0;
assert.strictEqual(post({ ...lead2, lead_id: 'lead-0011' }).error, 'forbidden', 'direct calls bypassing the proxy are refused');
assert(post({ ...lead2, lead_id: 'lead-0012', phone: '+971503333333', proxy_secret: 's3cret', client_ip: '1.2.3.4' }).ok);
assert.strictEqual(fetches.find(f => f.url.includes('/PX1/events')).body.data[0].user_data.client_ip_address, '1.2.3.4', 'IP trusted from the proxy');
delete props.PROXY_SECRET;

// --- WhatsApp reminder template in the client's language, with a configurable language code
fetches.length = 0; row1[26] = false; props.WHATSAPP_LANG_EN = 'en_US';
NOW = Date.parse('2026-10-05T11:15:00Z'); ctx.sendReminders();
const wa = fetches.find(f => f.url.includes('/PN/messages') && f.body.type === 'template');
assert(wa && wa.body.to === '971501234567' && wa.body.template.name === 'consult_reminder' && wa.body.template.language.code === 'en_US', JSON.stringify(wa));

console.log('ALL BACKEND TESTS PASSED');
