(function () {
  "use strict";
  var cfg = window.A1CFG || {};

  // Storage can throw (private mode, blocked site data); the site must work without it.
  function store(kind) {
    return {
      get: function (k) { try { return window[kind].getItem(k); } catch (e) { return null; } },
      set: function (k, v) { try { window[kind].setItem(k, v); } catch (e) { /* ignore */ } },
      remove: function (k) { try { window[kind].removeItem(k); } catch (e) { /* ignore */ } }
    };
  }
  var local = store("localStorage"), session = store("sessionStorage");

  function track(name, params) {
    params = params || {};
    if (typeof window.gtag === "function") window.gtag("event", name, params);
    if (typeof window.fbq === "function") window.fbq(name === "CalculatorUsed" ? "trackCustom" : "track", name, params, { eventID: params.event_id || undefined });
  }
  window.a1Track = track;

  function loadTracking() {
    if (window.__a1TrackingLoaded) return;
    window.__a1TrackingLoaded = true;
    if (cfg.ga4) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", cfg.ga4, { anonymize_ip: true });
      var gs = document.createElement("script");
      gs.async = true;
      gs.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(cfg.ga4);
      document.head.appendChild(gs);
    }
    if (cfg.meta) {
      window.fbq = function () { window.fbq.callMethod ? window.fbq.callMethod.apply(window.fbq, arguments) : window.fbq.queue.push(arguments); };
      window.fbq.queue = []; window.fbq.loaded = true; window.fbq.version = "2.0";
      var fs = document.createElement("script"); fs.async = true; fs.src = "https://connect.facebook.net/en_US/fbevents.js"; document.head.appendChild(fs);
      window.fbq("init", cfg.meta); window.fbq("track", "PageView");
    }
    if (cfg.clarity) {
      window.clarity = window.clarity || function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
      var cs = document.createElement("script"); cs.async = true; cs.src = "https://www.clarity.ms/tag/" + encodeURIComponent(cfg.clarity); document.head.appendChild(cs);
    }
  }

  var cookie = document.querySelector(".cookie-banner");
  var consent = local.get("a1-consent");
  if (consent === "analytics") loadTracking();
  if (cookie && !consent) cookie.hidden = false;
  if (cookie) {
    cookie.querySelector(".cookie-accept").addEventListener("click", function () { local.set("a1-consent", "analytics"); cookie.hidden = true; loadTracking(); });
    cookie.querySelector(".cookie-reject").addEventListener("click", function () { local.set("a1-consent", "essential"); cookie.hidden = true; });
  }

  var header = document.querySelector(".site-head");
  var burger = header && header.querySelector(".burger");
  if (burger) burger.addEventListener("click", function () { var open = header.classList.toggle("open"); burger.setAttribute("aria-expanded", String(open)); });
  if (header) header.querySelectorAll(".nav a").forEach(function (a) { a.addEventListener("click", function () { header.classList.remove("open"); if (burger) burger.setAttribute("aria-expanded", "false"); }); });
  if (header && document.body.classList.contains("home")) {
    var setHeader = function () { header.classList.toggle("scrolled", window.scrollY > 40); };
    setHeader(); addEventListener("scroll", setHeader, { passive: true });
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href^='https://wa.me/']");
    if (a) track("Contact", { method: "whatsapp" });
  });
  if (/\/projects\/[^/]+\//.test(location.pathname)) track("ViewContent", { content_name: document.querySelector("h1") ? document.querySelector("h1").textContent : document.title });

  function languageOffer() {
    if (session.get("a1-lang-offered")) return;
    var browserArabic = (navigator.language || "").toLowerCase().indexOf("ar") === 0;
    var pageArabic = document.documentElement.lang === "ar";
    if (browserArabic === pageArabic) return;
    var alternate = document.querySelector('link[rel="alternate"][hreflang="' + (browserArabic ? "ar" : "en") + '"]');
    if (!alternate) return;
    var box = document.createElement("div"); box.className = "lang-offer"; box.dir = browserArabic ? "rtl" : "ltr";
    var p = document.createElement("p"); p.textContent = browserArabic ? "هذه الصفحة متاحة بالعربية." : "This page is available in English.";
    var a = document.createElement("a"); a.className = "btn small"; a.href = alternate.href; a.textContent = browserArabic ? "العربية" : "English";
    var close = document.createElement("button"); close.type = "button"; close.setAttribute("aria-label", "Close"); close.textContent = "×";
    close.addEventListener("click", function () { session.set("a1-lang-offered", "1"); box.remove(); });
    box.appendChild(p); box.appendChild(a); box.appendChild(close); document.body.appendChild(box);
  }
  languageOffer();

  // ------------------------------------------------------------ booking
  // Dubai is UTC+4 all year (no daylight saving), so slot instants are fixed offsets.
  var TZ = cfg.timezone || "Asia/Dubai", OFFSET = "+04:00", DUBAI_MS = 4 * 3600000;
  var visitorZone = (Intl.DateTimeFormat().resolvedOptions().timeZone) || "";
  var sameZone = !visitorZone || visitorZone === TZ || new Date().getTimezoneOffset() === -240;

  function pad(n) { return String(n).padStart(2, "0"); }
  function slotInstant(date, time) { return new Date(date + "T" + time + ":00" + OFFSET); }
  function dubaiToday() { var d = new Date(Date.now() + DUBAI_MS); return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()); }
  function isoDay(utcMidnight) { var d = new Date(utcMidnight); return d.getUTCFullYear() + "-" + pad(d.getUTCMonth() + 1) + "-" + pad(d.getUTCDate()); }
  function locale(form) { return form.dataset.lang === "ar" ? "ar-AE-u-nu-latn" : "en-GB"; }
  function longDate(form, date) { return new Intl.DateTimeFormat(locale(form), { timeZone: TZ, weekday: "long", day: "numeric", month: "long" }).format(slotInstant(date, "12:00")); }
  function localTime(form, date, time) {
    var at = slotInstant(date, time), opts = { hour: "2-digit", minute: "2-digit" };
    if (new Intl.DateTimeFormat("en-CA", { year: "numeric", month: "2-digit", day: "2-digit" }).format(at) !== date) opts.weekday = "short"; // e.g. Monday evening in Los Angeles
    return new Intl.DateTimeFormat(locale(form), opts).format(at);
  }

  // National number lengths for the codes in the form, used to spot "971501234567" typed while +971 is selected.
  var NATIONAL_LENGTH = { "971": 9, "966": 9, "20": 10, "974": 8, "965": 8, "973": 8, "968": 8, "91": 10, "44": 10, "1": 10 };
  function normalisePhone(code, raw) {
    raw = String(raw || "").trim();
    var digits = raw.replace(/\D/g, ""), cc = String(code || "").replace(/\D/g, "");
    if (raw.charAt(0) === "+") return "+" + digits;
    if (digits.indexOf("00") === 0) return "+" + digits.slice(2);
    if (cc && digits.indexOf(cc) === 0 && digits.length - cc.length === NATIONAL_LENGTH[cc]) return "+" + digits;
    return "+" + cc + digits.replace(/^0+/, "");
  }
  // Same rules as the server (letters only, no links); built at runtime so old browsers without \p{} do not fail to parse the file.
  var NAME_OK = null, NAME_LINK = null;
  try { NAME_OK = new RegExp("^[\\p{L}\\p{M}][\\p{L}\\p{M} .'\u2019-]{1,79}$", "u"); NAME_LINK = new RegExp("\\.[\\p{L}\\p{M}]{2}", "u"); } catch (e) { /* server still validates */ }
  function nameValid(name) { name = String(name || "").trim().replace(/\s+/g, " "); return name.length >= 2 && (!NAME_OK || (NAME_OK.test(name) && !NAME_LINK.test(name))); }
  function emailValid(email) { return !email || /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email); }
  function values(form) {
    var out = {}; new FormData(form).forEach(function (v, k) { out[k] = v; });
    out.phone_raw = out.phone || "";
    out.phone = normalisePhone(out.country_code, out.phone);
    out.landing_url = location.href; out.language = form.dataset.lang;
    out._fbp = (document.cookie.match(/(?:^|; )_fbp=([^;]*)/) || [])[1] || "";
    out._fbc = (document.cookie.match(/(?:^|; )_fbc=([^;]*)/) || [])[1] || "";
    if (!out._fbc && out.fbclid) out._fbc = "fb.1." + Date.now() + "." + out.fbclid;
    out.client_user_agent = navigator.userAgent;
    out.analytics_consent = local.get("a1-consent") === "analytics"; // the server only sends CAPI events with consent
    return out;
  }
  function setStep(form, step) {
    form.querySelectorAll(".booking-step").forEach(function (el) { el.hidden = Number(el.dataset.step) !== step; });
    form.querySelectorAll(".booking-progress span").forEach(function (el, i) { el.classList.toggle("on", i < step); });
    var focusTarget = form.querySelector('[data-step="' + step + '"] h2');
    if (focusTarget) { focusTarget.setAttribute("tabindex", "-1"); focusTarget.focus({ preventScroll: true }); }
  }
  function showError(step, message) { var el = step.querySelector(".booking-error"); el.textContent = message; el.hidden = false; }
  function clearError(step) { var el = step.querySelector(".booking-error"); if (el) { el.textContent = ""; el.hidden = true; } }
  function post(endpoint, body) {
    return fetch(endpoint, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(body), redirect: "follow" }).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
  }
  // Used only when the live calendar cannot be reached: same rules as the backend, without the busy calendar.
  function fallbackSlots(date) {
    var slots = [], start = (cfg.start || "10:00").split(":"), end = (cfg.end || "19:00").split(":"), len = Number(cfg.slot || 30), step = len + Number(cfg.buffer || 15);
    var first = Number(start[0]) * 60 + Number(start[1]), last = Number(end[0]) * 60 + Number(end[1]), earliest = Date.now() + Number(cfg.notice || 3) * 3600000;
    for (var m = first; m + len <= last; m += step) {
      var t = pad(Math.floor(m / 60)) + ":" + pad(m % 60);
      if (slotInstant(date, t).getTime() >= earliest) slots.push(t);
    }
    return slots;
  }
  function icsText(s) { return String(s || "").replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/[,;]/g, "\\$&"); }
  function stamp(d) { return d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, ""); }
  function makeIcs(b) {
    return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//A1esmat//Consultation//EN", "BEGIN:VEVENT", "UID:" + b.id + "@a1esmat.com", "DTSTAMP:" + stamp(new Date()),
      "DTSTART:" + stamp(b.start), "DTEND:" + stamp(b.end), "SUMMARY:" + icsText(b.title), "DESCRIPTION:" + icsText(b.details), "END:VEVENT", "END:VCALENDAR"].join("\r\n");
  }
  function googleCalendarUrl(b) {
    return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + encodeURIComponent(b.title) + "&dates=" + stamp(b.start) + "/" + stamp(b.end) +
      "&details=" + encodeURIComponent(b.details) + "&ctz=" + encodeURIComponent(TZ);
  }
  // mode: "booked" (live booking confirmed), "change" (asks to move it), otherwise a plain request (fallback).
  function whatsappUrl(form, data, mode) {
    var ar = form.dataset.lang === "ar", lines = [];
    if (mode === "change") lines.push(ar ? "مرحباً أحمد، أريد تغيير موعد الاستشارة." : "Hi Ahmed, I need to change my consultation time.");
    else if (mode === "booked") lines.push(ar ? "مرحباً أحمد، حجزت استشارة." : "Hi Ahmed, I booked a consultation.");
    else lines.push(ar ? "مرحباً أحمد، أريد استشارة. ميزانيتي " + data.budget_label + "." : "Hi Ahmed, I'd like a consultation. My budget is " + data.budget_label + ".");
    lines.push(data.name, data.phone, data.interest_label + " · " + data.emirate_label);
    if (data.date) lines.push((mode ? "" : (ar ? "الموعد المفضل: " : "Preferred time: ")) + longDate(form, data.date) + " " + data.time + (ar ? " بتوقيت دبي" : " Dubai time"));
    if (data.topic) lines.push(data.topic);
    return "https://wa.me/" + form.dataset.wa + "?text=" + encodeURIComponent(lines.join("\n"));
  }
  function optionLabel(form, name) { var el = form.elements[name]; return el && el.selectedOptions && el.selectedOptions[0] ? el.selectedOptions[0].textContent : ""; }

  var params = new URLSearchParams(location.search);
  if (params.get("tier")) document.querySelectorAll("a.lang").forEach(function (a) { var u = new URL(a.href); u.searchParams.set("tier", params.get("tier")); a.href = u.toString(); });
  // Price tier (AED millions) -> closest budget band in the form.
  var TIER_BUDGET = { "2.7-4": "3-5", "4-6": "5-8", "6-9": "5-8", "9-12": "8-12" };

  document.querySelectorAll(".booking-form").forEach(function (form, formIndex) {
    var labels = JSON.parse(form.dataset.labels), endpoint = form.dataset.endpoint || cfg.bookingEndpoint || "", selectedDate = "", selectedTime = "", booked = null;
    var ar = form.dataset.lang === "ar";
    if (!endpoint && /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) endpoint = "/api";
    var saved = {};
    try { saved = JSON.parse(session.get("a1-booking") || "{}"); } catch (e) { saved = {}; }
    Object.keys(saved).forEach(function (k) { var el = form.elements[k]; if (el && el.type !== "radio" && el.type !== "checkbox" && el.type !== "hidden" && k !== "phone") el.value = saved[k]; });
    if (saved.phone_raw && form.elements.phone) form.elements.phone.value = saved.phone_raw;
    var cc = form.elements.country_code;
    if (cc) {
      // Closed: flag + code only, so it never gets cut off. Open: full country names.
      var expand = function () { Array.prototype.forEach.call(cc.options, function (o) { o.textContent = o.dataset.full; }); };
      var collapse = function () { expand(); var o = cc.selectedOptions[0]; if (o) { o.textContent = o.value; cc.dataset.flag = o.dataset.flag; } };
      cc.addEventListener("mousedown", expand); cc.addEventListener("focus", expand); cc.addEventListener("keydown", expand);
      cc.addEventListener("change", collapse); cc.addEventListener("blur", collapse); collapse();
    }
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "fbclid"].forEach(function (k) { if (form.elements[k]) form.elements[k].value = params.get(k) || saved[k] || ""; });
    if (form.elements.tier) form.elements.tier.value = params.get("tier") || saved.tier || "";
    if (form.elements.lead_id) form.elements.lead_id.value = saved.lead_id || (window.crypto && crypto.randomUUID ? crypto.randomUUID() : "lead-" + Date.now() + "-" + formIndex + "-" + Math.random().toString(36).slice(2));
    if (TIER_BUDGET[params.get("tier")] && form.elements.budget) form.elements.budget.value = TIER_BUDGET[params.get("tier")];
    if (form.elements.landing_url) form.elements.landing_url.value = location.href;
    form.querySelector(".visitor-zone").textContent = sameZone ? "" : " · " + (ar ? "وبين القوسين بتوقيتك (" : "your time in brackets (") + visitorZone + ")";
    form.addEventListener("input", function () { session.set("a1-booking", JSON.stringify(values(form))); });

    var days = form.querySelector(".day-chips"), slots = form.querySelector(".slot-chips"), status = form.querySelector(".slot-status"), cache = {}, daysPromise = null;
    function api(query) { return fetch(endpoint + (endpoint.indexOf("?") > -1 ? "&" : "?") + query, { redirect: "follow" }).then(function (r) { return r.json(); }); }
    // Whole horizon in one request; null when the backend does not offer it (then each day is asked separately).
    function loadDays() {
      if (!endpoint) return Promise.resolve(null);
      if (!daysPromise) daysPromise = api("action=days").then(function (x) { return x && x.ok && x.days ? x.days : null; }).catch(function () { return null; });
      return daysPromise;
    }
    function fetchSlots(date) {
      if (cache[date]) return cache[date];
      cache[date] = loadDays().then(function (all) {
        if (all && Object.prototype.hasOwnProperty.call(all, date)) return { list: all[date], live: true };
        if (!endpoint) return { list: fallbackSlots(date), live: false };
        return api("action=slots&date=" + encodeURIComponent(date)).then(function (x) { if (!x || x.ok === false) throw new Error((x && x.error) || "slots_failed"); return { list: x.slots || [], live: true }; });
      }).catch(function () { delete cache[date]; return { list: fallbackSlots(date), live: false, failed: true }; });
      return cache[date];
    }
    function refreshSlots(date) { delete cache[date]; daysPromise = null; return fetchSlots(date); }
    function renderSlots(date, result) {
      slots.innerHTML = "";
      var list = result.list;
      status.hidden = list.length > 0 && !result.failed;
      status.textContent = result.failed ? labels.fallback : (list.length ? "" : (ar ? "لا توجد مواعيد متاحة في هذا اليوم." : "No available times on this day."));
      list.forEach(function (time) {
        var s = document.createElement("button"); s.type = "button"; s.className = "slot-chip"; s.dataset.time = time; s.setAttribute("aria-pressed", "false");
        s.textContent = time + (sameZone ? "" : " (" + localTime(form, date, time) + ")");
        s.addEventListener("click", function () { selectedTime = this.dataset.time; slots.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", "false"); }); this.setAttribute("aria-pressed", "true"); });
        slots.appendChild(s);
      });
    }

    var today = dubaiToday();
    for (var i = 0; i < Number(cfg.horizon || 14); i++) {
      var midnight = today + i * 86400000, key = isoDay(midnight), weekday = new Date(midnight).getUTCDay();
      var btn = document.createElement("button"); btn.type = "button"; btn.className = "day-chip"; btn.dataset.date = key; btn.setAttribute("aria-pressed", "false");
      btn.textContent = new Intl.DateTimeFormat(locale(form), { timeZone: TZ, weekday: "short", day: "numeric", month: "short" }).format(slotInstant(key, "12:00"));
      btn.disabled = Array.isArray(cfg.days) && cfg.days.indexOf(weekday) === -1;
      btn.addEventListener("click", function () {
        var date = this.dataset.date; selectedDate = date; selectedTime = "";
        days.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", "false"); }); this.setAttribute("aria-pressed", "true");
        slots.innerHTML = ""; status.hidden = false; status.textContent = labels.loading;
        fetchSlots(date).then(function (result) { if (selectedDate === date) renderSlots(date, result); });
      });
      days.appendChild(btn);
    }
    // Grey out days that have no free slot at all (brief 2.2), checked in the background.
    var availabilityChecked = false;
    function checkAvailability() {
      if (availabilityChecked || !endpoint) return; availabilityChecked = true;
      loadDays().then(function (all) {
        days.querySelectorAll("button:not(:disabled)").forEach(function (b) {
          var check = all ? Promise.resolve({ list: all[b.dataset.date] || [], failed: !(b.dataset.date in all) }) : fetchSlots(b.dataset.date);
          check.then(function (r) { if (!r.failed && !r.list.length) { b.disabled = true; if (selectedDate === b.dataset.date) { selectedDate = ""; status.textContent = labels.pick_day; } } });
        });
      });
    }

    function describe(data) {
      data.budget_label = optionLabel(form, "budget"); data.interest_label = optionLabel(form, "interest"); data.emirate_label = optionLabel(form, "emirate");
      return data;
    }

    form.querySelector(".booking-next").addEventListener("click", function () {
      var step = form.querySelector('[data-step="1"]'), data = describe(values(form)), digits = data.phone.replace(/\D/g, ""); clearError(step);
      var phoneOk = digits.length >= 8 && digits.length <= 15 && data.phone_raw.replace(/\D/g, "").length >= 6;
      if (data.website) return; // honeypot
      if (!nameValid(data.name)) { showError(step, labels.name_invalid); return; }
      if (!phoneOk || !data.consent || !emailValid(data.email)) { showError(step, labels.required); return; }
      data.action = "lead"; data.event_id = "lead-" + data.lead_id;
      track("Lead", { budget_band: data.budget, interest: data.interest, event_id: data.event_id });
      if (endpoint) post(endpoint, data).then(function (res) {
        // The server issues a new id if this one belongs to someone else's row.
        if (res && res.ok && res.lead_id && res.lead_id !== form.elements.lead_id.value) { form.elements.lead_id.value = res.lead_id; session.set("a1-booking", JSON.stringify(values(form))); }
      }).catch(function () { /* the WhatsApp fallback in step 3 still works */ });
      setStep(form, 2); checkAvailability();
    });
    form.querySelector(".booking-back").addEventListener("click", function () { setStep(form, 1); });
    form.querySelector(".booking-change").addEventListener("click", function () {
      if (booked) { window.open(whatsappUrl(form, booked, "change"), "_blank", "noopener"); return; }
      setStep(form, 2);
    });
    form.querySelector(".booking-confirm-btn").addEventListener("click", function () {
      var step = form.querySelector('[data-step="2"]'), meeting = form.querySelector('input[name="meeting_type"]:checked'); clearError(step);
      if (!selectedDate || !selectedTime || !meeting) { showError(step, labels.slot_required); return; }
      var data = describe(values(form)); data.action = "book"; data.date = selectedDate; data.time = selectedTime; data.meeting_type = meeting.value; data.event_id = "schedule-" + data.lead_id;
      var finish = function (result, live) {
        setStep(form, 3); var copy = form.querySelector(".confirmation-copy"), when = longDate(form, selectedDate) + (ar ? " الساعة " : " at ") + selectedTime;
        copy.textContent = live ? labels.booked + ": " + when + " (" + labels.dubai_time + ")." : labels.request + ". " + labels.fallback;
        var wa = form.querySelector(".wa-confirm"); wa.href = whatsappUrl(form, data, live ? "booked" : "");
        if (!live) return;
        booked = data;
        track("Schedule", { day_offset: Math.round((Date.parse(selectedDate + "T00:00:00Z") - dubaiToday()) / 86400000), meeting_type: data.meeting_type, event_id: data.event_id });
        var start = slotInstant(selectedDate, selectedTime), b = {
          id: result.booking_id || data.lead_id, start: start, end: new Date(start.getTime() + Number(cfg.slot || 30) * 60000),
          title: ar ? "استشارة مع أحمد عصمت" : "Consultation with Ahmed Esmat",
          details: [meeting.parentNode.textContent.trim(), result.meet_link || "", "WhatsApp: https://wa.me/" + form.dataset.wa].filter(Boolean).join("\n")
        };
        var ics = form.querySelector(".ics-link"); ics.href = URL.createObjectURL(new Blob([makeIcs(b)], { type: "text/calendar;charset=utf-8" })); ics.hidden = false;
        var gl = form.querySelector(".google-link"); gl.href = googleCalendarUrl(b); gl.hidden = false;
        session.remove("a1-booking");
      };
      if (!endpoint) { finish({}, false); return; }
      var btn = this; btn.disabled = true;
      var attempt = function (retries) {
        return post(endpoint, data).then(function (result) { if (!result.ok) throw new Error(result.error || "booking_failed"); finish(result, true); })
          .catch(function (err) {
            var code = String(err.message);
            if (code === "busy_try_again" && retries > 0) return new Promise(function (r) { setTimeout(r, 1500); }).then(function () { return attempt(retries - 1); });
            if (code === "slot_taken") { showError(step, labels.taken); refreshSlots(selectedDate).then(function (r) { selectedTime = ""; renderSlots(selectedDate, r); }); }
            else if (code === "too_many_bookings") showError(step, labels.too_many);
            else finish({}, false);
          });
      };
      attempt(1).finally(function () { btn.disabled = false; });
    });
  });

  // ------------------------------------------------------------ calculator
  // UAE Central Bank mortgage caps (brief 5.2). Editable because the rules can change.
  var MORTGAGE_RULES = {
    firstHome: { expat: [80, 70], national: [85, 75], nonresident: [50, 50] }, // [up to the price threshold, above it]
    priceThreshold: 5000000,
    secondHome: { expat: 60, national: 65, nonresident: 50 },
    offPlan: 50,
    registrationFee: 0.04, mortgageRegistration: 0.0025, mortgageRegistrationFixed: 290,
    debtBurden: { expat: 0.5, national: 0.5, nonresident: 0.5 } // brief 5.2: 50% of income for all obligations
  };
  document.querySelectorAll(".calculator").forEach(function (form) {
    var el = form.elements, R = MORTGAGE_RULES, kind = form.dataset.kind || "monthly", capNote = form.querySelector(".calc-cap");
    var fmt = new Intl.NumberFormat(form.dataset.lang === "ar" ? "ar-AE-u-nu-latn" : "en-AE", { style: "currency", currency: "AED", maximumFractionDigits: 0 });
    function price() { return Number(el.price.value || 0); }
    function maxLtv() {
      if (el.property_type.value === "offplan") return R.offPlan;
      if (el.property_type.value === "second") return R.secondHome[el.buyer.value];
      return R.firstHome[el.buyer.value][price() <= R.priceThreshold ? 0 : 1];
    }
    // Down payment (AED) and loan-to-value (%) are two views of the same number.
    function downFromLtv() { el.down.value = Math.round(price() * (1 - Number(el.ltv.value) / 100)); }
    function ltvFromDown() { var p = price(); if (p > 0) el.ltv.value = Math.max(0, Math.round((1 - Number(el.down.value || 0) / p) * 10000) / 100); }
    function enforceCap() {
      var cap = maxLtv(), over = Number(el.ltv.value) > cap;
      if (over) { el.ltv.value = cap; downFromLtv(); }
      capNote.hidden = !over;
      if (over) capNote.textContent = (form.dataset.lang === "ar" ? "الحد الأقصى للتمويل في هذه الحالة " + cap + "%، أي دفعة مقدمة لا تقل عن " : "The maximum loan here is " + cap + "%, so the down payment is at least ") + fmt.format(price() * (1 - cap / 100)) + ".";
    }
    function resetToCap() { el.ltv.value = maxLtv(); downFromLtv(); capNote.hidden = true; }
    function calculate(fire) {
      enforceCap();
      var p = price(), down = el.down.value === "" ? p * (1 - Number(el.ltv.value) / 100) : Number(el.down.value), loan = Math.max(0, p - down); // the AED amount is exact; the % is rounded
      if (!(p > 0)) return;
      var registration = p * R.registrationFee, mortgage = loan > 0 ? loan * R.mortgageRegistration + R.mortgageRegistrationFixed : 0, out = { down: down, loan: loan, registration: registration, mortgage: mortgage, cash: down + registration + mortgage };
      if (el.rate && el.term) {
        // Keep inputs inside the brief's ranges (rate 3.75–5.5%, term up to 25 years); the fields show the corrected value.
        [el.rate, el.term].forEach(function (x) { var v = Number(x.value); if (x.value !== "" && !isNaN(v)) x.value = Math.min(Math.max(v, Number(x.min)), Number(x.max)); });
        var rate = Number(el.rate.value) / 1200, months = Math.round(Number(el.term.value) * 12);
        if (!(rate > 0 && months > 0 && months <= 300)) return;
        out.monthly = loan > 0 ? loan * rate * Math.pow(1 + rate, months) / (Math.pow(1 + rate, months) - 1) : 0;
        out.income = out.monthly / R.debtBurden[el.buyer.value];
      }
      Object.keys(out).forEach(function (k) { var r = form.querySelector('[data-result="' + k + '"]'); if (r) r.textContent = fmt.format(out[k]); });
      if (fire) track("CalculatorUsed", { calculator: kind === "cash" ? "cash_needed" : "monthly_payment", price_band: p < 3000000 ? "under_3m" : p < 5000000 ? "3_5m" : p < 8000000 ? "5_8m" : "8m_plus" });
    }
    [el.buyer, el.property_type].forEach(function (x) { x.addEventListener("change", resetToCap); });
    el.price.addEventListener("change", function () { if (Number(el.ltv.value) > maxLtv()) resetToCap(); else downFromLtv(); });
    el.ltv.addEventListener("input", downFromLtv);
    el.down.addEventListener("input", ltvFromDown);
    form.addEventListener("submit", function (e) { e.preventDefault(); calculate(true); });
    resetToCap(); calculate(false); // show the worked example without counting it as a use
  });

  window.addEventListener("pageshow", function () { document.querySelectorAll(".booking-confirm-btn").forEach(function (b) { b.disabled = false; }); });
})();
