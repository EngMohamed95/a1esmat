# ============================================================
#  a1esmat.com — site settings
#  Fill the CONTACT fields before publishing, then run:  python3 build.py
# ============================================================

DOMAIN = "https://a1esmat.com"

# --- Contact (REQUIRED before going live) ---------------------------------
# WhatsApp number in international format, digits only, e.g. "971501234567"
WHATSAPP = "971547772515"
EMAIL = ""            # e.g. "hello@a1esmat.com"
INSTAGRAM = "https://www.instagram.com/a1esmat.investment/"
LINKEDIN = ""

# --- Licensing line shown in the footer (leave "" to hide) ---------------
# Example: "Transactions handled by XYZ Real Estate Brokers, RERA ORN 12345"
LICENSE_LINE_EN = ""
LICENSE_LINE_AR = ""

# --- Legal entity (privacy notice + structured data; leave "" until confirmed) ---
LEGAL_ENTITY_EN = ""   # e.g. "XYZ Real Estate Brokers LLC"
LEGAL_ENTITY_AR = ""
# Business address for the ProfessionalService schema. Leave STREET "" to omit it.
ADDRESS_STREET = ""
ADDRESS_LOCALITY = "Dubai"
ADDRESS_COUNTRY = "AE"

# --- Answers only Ahmed can give (brief 1.6, 1.8). Each appears on the site as soon
#     as BOTH languages are filled in; until then it is not published.
FAQ_FEE_EN = ""          # "Do you charge me a fee?"
FAQ_FEE_AR = ""          # "هل تتقاضى مني رسومًا؟"
FAQ_ABU_DHABI_EN = ""    # "Can I buy in Abu Dhabi as a foreigner?"
FAQ_ABU_DHABI_AR = ""    # "هل يمكنني الشراء في أبوظبي كأجنبي؟"
# Bedroom range per price tier, e.g. {"2.7-4": ("3–4 bedrooms", "3–4 غرف"), ...}
TIER_BEDROOMS = {}

# --- Data freshness --------------------------------------------------------
DATA_CHECKED_EN = "September 2026"
DATA_CHECKED_AR = "سبتمبر 2026"
UPDATED_MONTH_EN = "September 2026"
UPDATED_MONTH_AR = "سبتمبر 2026"
# Sitemap <lastmod>: the day the site is built (leave as is; set a fixed "YYYY-MM-DD" only to override)
import datetime as _dt
BUILD_DATE = _dt.date.today().isoformat()

# --- Analytics (optional) --------------------------------------------------
# Google Analytics 4 measurement ID, e.g. "G-XXXXXXX". Leave "" to disable.
GA4_ID = ""
# Meta Pixel ID and Microsoft Clarity project ID. Tracking is only loaded after
# the visitor accepts analytics cookies.
META_PIXEL_ID = ""
CLARITY_ID = ""

# Booking API. In production this is the deployed Google Apps Script Web App
# URL. Keep empty until the deployment in backend/google-apps-script is ready.
BOOKING_ENDPOINT = "https://script.google.com/macros/s/AKfycbzXcoR3yjdBISWs_VSIYxhjracljAFPeRB8QrcXVk-w50ekBDvwAy4fbUsm1JNmLT69cQ/exec"

# Availability defaults; the Apps Script backend is authoritative.
BOOKING_TIMEZONE = "Asia/Dubai"
BOOKING_DAYS = [1, 2, 3, 4, 5, 6]  # Monday-Saturday (JS weekday numbers)
BOOKING_START = "10:00"
BOOKING_END = "19:00"
BOOKING_SLOT_MINUTES = 30
BOOKING_BUFFER_MINUTES = 15
BOOKING_MIN_NOTICE_HOURS = 3
BOOKING_HORIZON_DAYS = 14
# Google Search Console HTML-tag verification code (content="..."). Optional.
GSC_VERIFICATION = ""
