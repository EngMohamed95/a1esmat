# A1esmat booking implementation

## Run locally

```powershell
npm start
```

Open `http://127.0.0.1:8000`. The local server stores test leads and bookings in
`.local-data/bookings.json` and enforces slot conflicts.

Regenerate the complete site with the official source build:

```powershell
python build.py
```

The conversion homepage, shared booking component, ad landing page, mortgage
calculator and privacy pages are all part of `build.py` and `templates.py`.
`postbuild.js`, `static/booking.js` and `static/booking.css` are an old experimental
layer that is no longer used and must not be run.

To build somewhere other than `dist/` (for example when `dist/` is open in another
program), set `A1_OUT`:

```powershell
$env:A1_OUT = "C:\temp\a1-dist"; python build.py
```

Checks: `npm run check` (syntax, backend logic against fake Google services, and
links/structure of the built pages).

## Production booking setup (Google Calendar + Google Sheets)

1. Create a Google Sheet and copy its ID from the URL.
2. Open `script.google.com`, create a project, then copy in:
   - `backend/google-apps-script/Code.gs`
   - `backend/google-apps-script/appsscript.json`
3. In **Project settings → Script properties**, add:
   - `SHEET_ID`
   - `CALENDAR_ID` (usually Ahmed's Google account email)
   - `OWNER_EMAIL` (or the legacy name `NOTIFY_EMAIL`)
   - `BUSY_CALENDAR_IDS` if Ahmed's personal events live in a different calendar
     from `CALENDAR_ID` (see `backend/google-apps-script/README.md`)
4. Optional availability overrides:
   - `WORKING_DAYS` = `1,2,3,4,5,6`
   - `START` = `10:00`
   - `END` = `19:00`
   - `BLOCKED_DATES` = `2026-12-02,2026-12-03`
   - `SLOT_MINUTES` = `30`
   - `BUFFER_MINUTES` = `15`
   - `MIN_NOTICE_HOURS` = `3`
   - `HORIZON_DAYS` = `14`
5. Enable the **Google Calendar API** advanced service. This creates Google Meet
   links for video bookings.
6. Deploy as a Web app: execute as the owner; access for anyone. Copy the `/exec`
   URL into `BOOKING_ENDPOINT` in `config.py`, then run `python build.py`.
7. Create a time-driven trigger for `sendReminders` every 15 minutes.
8. Make one English and one Arabic test booking. Verify the Calendar event,
   Sheet row, owner email, client confirmation and reminder flags.

### WhatsApp (optional, official WhatsApp Cloud API)

Script Properties: `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_OWNER_NUMBER`.
Messages a business starts need a template approved in Meta Business Manager:

- `WHATSAPP_OWNER_TEMPLATE`: new-lead alert to Ahmed, one body variable (the summary).
  Without it the alert is sent as free text, which WhatsApp only delivers inside a
  24-hour chat window.
- `WHATSAPP_REMINDER_TEMPLATE`: client reminder 24 h and 1 h before, two body variables
  (name, date and time). Approve it in `en` and `ar`.

Without these, email notifications and reminders and the visitor's WhatsApp fallback
still work.

### Meta Conversions API (optional)

Script Properties: `META_PIXEL_ID`, `META_CAPI_TOKEN` (Events Manager → Settings →
Conversions API → Generate access token), and `META_TEST_EVENT_CODE` only while testing.
`Lead` and `Schedule` are sent with the same `event_id` as the browser Pixel, so Meta
de-duplicates them. Phone, email, name and lead ID are SHA-256 hashed. Nothing is sent
unless the visitor accepted analytics cookies.

### Per-IP rate limit (optional proxy)

Apps Script cannot see visitor IPs. `backend/cloudflare-worker/` is a small Cloudflare
Worker that rate-limits writes per IP and passes the IP to the Conversions API:

1. `npx wrangler deploy` inside `backend/cloudflare-worker/`.
2. `npx wrangler secret put APPS_SCRIPT_URL` (the `/exec` URL) and
   `npx wrangler secret put PROXY_SECRET` (any long random string).
3. Add the same `PROXY_SECRET` as a Script Property.
4. Put the Worker URL (not the Apps Script URL) in `BOOKING_ENDPOINT`, then rebuild.

## Analytics

Set these in `config.py`, then run `python build.py`:

- `GA4_ID`
- `META_PIXEL_ID`
- `CLARITY_ID` (optional)

Analytics scripts load only after cookie consent. Implemented events are
`PageView`, `ViewContent`, `Lead`, `Schedule`, `Contact`, and `CalculatorUsed`.
UTM fields, `fbclid`, `_fbp` and `_fbc` are saved with every lead.

## Content that switches on from `config.py`

These are built and tested, and appear on the site as soon as they are filled in:

- `FAQ_FEE_EN/AR`, `FAQ_ABU_DHABI_EN/AR`: the two FAQs that need Ahmed's answers. Each is
  published only when both languages are filled in (homepage, landing page, FAQ schema).
- `TIER_BEDROOMS`: bedroom range under each price tier.
- `LEGAL_ENTITY_EN/AR` (+ `EMAIL`): shown in the privacy notice, replacing the
  "to be completed" note, and as `legalName` in the schema.
- `ADDRESS_STREET`: adds the address to the `ProfessionalService` schema.
- `LICENSE_LINE_EN/AR`: footer licence line on every page.

## Real-estate guides (brief 5.3)

`content_guides.py` holds the nine guides in both languages as **drafts for Ahmed's review**.
They use only the figures in the brief and results calculated from them. To publish a guide,
edit its text if needed, set `"approved": True` and fill `"date"` in both languages. A guide
is published only when it is approved and both languages are complete; the first published
guide also adds "Buying guides" to the menu and creates `/guides/` and `/ar/guides/`.
Preview unfinished guides with `A1_DRAFTS=1 python build.py` (drafts are `noindex` and
never in the sitemap).

## Calculators (brief 5.2)

- `/cash-needed-calculator/`: down payment, 4% registration, mortgage registration.
- `/mortgage-calculator/`: loan, monthly payment, required income.

Both accept the down payment in AED or as loan-to-value, enforce the Central Bank caps,
and fire `CalculatorUsed` only when the visitor presses Calculate. The caps and fees are
in `MORTGAGE_RULES` at the top of the calculator code in `static/js/site.js`.

## Information still required before publishing

- Confirmed working days/hours, meeting types and buffer.
- Google account/calendar and Sheet to connect.
- Meta Pixel ID, GA4 ID and optional Clarity ID (and a CAPI token if wanted).
- Legal entity, BRN, ORN and trade-licence number in Arabic and English.
- Confirmed developer list, whether Modon is intended, and permission for names/logos.
- True answers about Ahmed's fee, Abu Dhabi foreign ownership, and bedroom ranges.
- Verified project prices, payment plans, handover data and last-checked dates.
- Approved developer renders or Ahmed-owned photos.
- Final real-estate guide copy.

The implementation deliberately does not invent or publish any of these facts.
