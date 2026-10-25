# Google Apps Script booking backend

## Quick start (about 15 minutes, from Ahmed's Google account)

1. script.google.com → New project. Project settings → tick "Show appsscript.json manifest file".
2. Paste `Code.gs` and `appsscript.json` from this folder over the editor's files and save.
3. Select `setup` in the toolbar → Run → allow access. It creates the "A1esmat Leads" sheet, uses
   your default calendar and email, and installs the reminder trigger (steps 1, 3, 4, 5 and 8 below).
4. Deploy → New deployment → Web app → Execute as: Me, Who has access: Anyone → copy the `/exec` URL
   into `BOOKING_ENDPOINT` in `config.py`, then push.

## Manual setup (reference)

1. Create a Google Sheet (the script adds a `Leads` tab with headers on first use).
2. Create an Apps Script project and paste `Code.gs` and `appsscript.json` into it.
3. In **Project settings → Script properties**, add:
   - `CALENDAR_ID`: the calendar bookings are written to (usually Ahmed's Google account email).
   - `SHEET_ID`
   - `OWNER_EMAIL`
   - `BUSY_CALENDAR_IDS` (optional): comma-separated extra calendars whose events also block
     slots, for example a personal calendar. Each must be shared with the account that deploys
     the script ("See all event details" is enough). If `CALENDAR_ID` is already Ahmed's main
     calendar, his own events block slots without this.
   - `OWNER_WHATSAPP` (optional, digits only): used in the "Change the time" links. Defaults to the site number.
   - `BLOCKED_DATES` (optional), such as `2026-12-02,2026-12-03`
4. Set the Apps Script project time zone to `Asia/Dubai`.
5. Enable the Google Calendar advanced service (used for Google Meet links).
6. Deploy as **Web app**, execute as the owner, accessible to anyone.
7. Put the deployment URL in `config.py` as `BOOKING_ENDPOINT` and rebuild.
8. Add a 15-minute time trigger for `sendReminders`.

Availability can be edited using Script Properties: `WORKING_DAYS` (`1,2,3,4,5,6`, where
1 = Monday and 7 = Sunday), `START`, `END`, `SLOT_MINUTES`, `BUFFER_MINUTES`,
`MIN_NOTICE_HOURS`, `HORIZON_DAYS`, and comma-separated `BLOCKED_DATES`. If you change the
working days or hours, change `BOOKING_DAYS`/`BOOKING_START`/`BOOKING_END` in `config.py` too
(there `0` = Sunday) so the day picker greys out the same days.

Optional integrations (WhatsApp Cloud API alerts and reminder templates, Meta
Conversions API, the per-IP rate-limit proxy in `backend/cloudflare-worker/`) are
described in `IMPLEMENTATION.md`.

The public endpoint validates fields, uses a honeypot, rate-limits by a hash of
the submitted phone/lead identifier, locks booking writes, re-checks calendar
availability, keeps one Sheet row per lead (stored as plain text so phones, dates
and names are never reinterpreted by Sheets), creates the event, and emails the
owner and client.

Test the script logic locally with `node tests/backend.test.js`.
