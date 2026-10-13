#!/usr/bin/env python3
"""Build a1esmat.com into ./dist  —  run:  python3 build.py"""
import os, re, shutil, json
from html import escape
import config as C
from templates import (CSS, script_json, page, crumbs_html, crumbs_schema, faq_html, faq_schema,
                       person_schema, service_schema, website_schema, wa_link, img, illus, phero, booking_form)
from data_images import IMAGES, PROJECT_IMG, PAGE_IMG, OPP_IMG, CLIENTS
from data_projects import PROJECTS, BY_SLUG
from content_landing import LANDING
from content_pages import HOME, ASSESS, BOOK, DISCLAIMER
from content_articles import ARTICLES
from content_guides import GUIDES, is_ready
import templates
from content_conversion import HOME_CONVERSION, LANDING_CONVERSION, PRIVACY, EXTRA_FAQS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("A1_OUT") or os.path.join(ROOT, "dist")  # A1_OUT: build elsewhere for testing
SITEMAP = []  # (path, alt_path or None)

def write(path, html, alt=None, sitemap=True):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    if sitemap:
        SITEMAP.append((path, alt))

T = {
 "en": {"home": "Home", "projects": "Projects", "may_suit": "May suit", "may_not": "May not suit", "view": "Read the assessment",
        "dev": "Developer", "loc": "Location", "type": "Unit types", "stage": "Stage", "handover": "Expected handover", "price": "Starting price",
        "on_req": "Requires current developer confirmation", "plan": "Payment plan", "glance": "At a glance", "suits_h": "Who this project may suit", "not_h": "Who it may not suit",
        "pay_h": "Payment plan and cash flow", "loc_h": "Location and community", "app_h": "Capital appreciation factors",
        "rent_h": "Rental and income considerations", "sup_h": "Supply and liquidity", "str_h": "Main strengths", "risk_h": "Main risks",
        "cmp_h": "Compare {p} with", "faq_h": "Questions about {p}", "faq": "Frequently asked questions",
        "cta_p": "Not sure {p} fits your plans? Build your profile first.", "start": "Start your investment assessment", "talk": "Talk to Ahmed",
        "checked": "Data checked in {d}. Ahmed Esmat is not affiliated with {dev} unless stated.",
        "pending": "The current price and payment plan change with each release. Ask for the latest confirmed figures before you compare.",
        "ask_plan": "Ask for the current payment plan", "book_project": "Book a consultation about this project", "related": "Related guides",
        "mini_h": "Which of these might fit you?", "mini_p": "Answer five short questions and see the projects that match your goal, horizon and budget.",
        "idx_title": "Dubai Villa & Townhouse Projects: Investor Assessments",
        "idx_meta": "Independent assessments of Dubai villa and townhouse projects: location, stage, strengths, risks, and who each project may suit.",
        "idx_h1": "Dubai villa and townhouse projects, assessed", "idx_lede": "Each project shows who it may suit and who it may not. No scores, no \"best project\" claims.",
        "by": "by"},
 "ar": {"home": "الرئيسية", "projects": "المشاريع", "may_suit": "قد يناسب", "may_not": "قد لا يناسب", "view": "اقرأ التقييم",
        "dev": "المطور", "loc": "الموقع", "type": "أنواع الوحدات", "stage": "المرحلة", "handover": "التسليم المتوقع", "price": "السعر يبدأ من",
        "on_req": "يتطلب تأكيدًا حاليًا من المطور", "plan": "خطة الدفع", "glance": "المشروع باختصار", "suits_h": "لمن قد يناسب هذا المشروع", "not_h": "لمن قد لا يناسب",
        "pay_h": "خطة الدفع والتدفق النقدي", "loc_h": "الموقع والمجتمع", "app_h": "عوامل نمو القيمة",
        "rent_h": "اعتبارات الإيجار والدخل", "sup_h": "المعروض والسيولة", "str_h": "أبرز نقاط القوة", "risk_h": "أبرز المخاطر",
        "cmp_h": "قارن {p} مع", "faq_h": "أسئلة حول {p}", "faq": "أسئلة شائعة",
        "cta_p": "لست متأكداً أن {p} يناسب خططك؟ ابدأ بملفك الاستثماري.", "start": "ابدأ تقييمك الاستثماري", "talk": "تحدث مع أحمد",
        "checked": "البيانات مراجعة في {d}. أحمد عصمت غير مرتبط بـ{dev} ما لم يُذكر خلاف ذلك.",
        "pending": "السعر الحالي وخطة الدفع يتغيران مع كل إصدار. اطلب آخر الأرقام المؤكدة قبل المقارنة.",
        "ask_plan": "اطلب خطة الدفع الحالية", "book_project": "احجز استشارة عن هذا المشروع", "related": "أدلة ذات صلة",
        "mini_h": "أي هذه المشاريع قد يناسبك؟", "mini_p": "أجب عن خمسة أسئلة قصيرة وشاهد المشاريع التي تتوافق مع هدفك ومدتك وميزانيتك.",
        "idx_title": "مشاريع فلل وتاون هاوس في دبي: تقييمات للمستثمرين",
        "idx_meta": "تقييمات مستقلة لمشاريع الفلل والتاون هاوس في دبي: الموقع والمرحلة ونقاط القوة والمخاطر ولمن يناسب كل مشروع.",
        "idx_h1": "مشاريع الفلل والتاون هاوس في دبي بعين المستثمر", "idx_lede": "كل مشروع يوضح لمن قد يناسب ولمن قد لا يناسب. بلا درجات، وبلا ادعاء \"أفضل مشروع\".",
        "by": "من"},
}

def ppath(p, lang):
    return ("/ar" if lang == "ar" else "") + f"/projects/{p['slug']}/"

def card(p, lang):
    d, t = p[lang], T[lang]
    checked = C.DATA_CHECKED_AR if lang == "ar" else C.DATA_CHECKED_EN
    price = p["price_from"] or ("السعر الحالي يُؤكد من المطور" if lang == "ar" else "Current price requires developer confirmation")
    handover_label = "التسليم" if lang == "ar" else "Handover"
    checked_label = "آخر مراجعة" if lang == "ar" else "Last checked"
    return (f'<article class="pcard"><a class="ph" href="{ppath(p, lang)}" tabindex="-1" aria-hidden="true">'
            f'{img(PROJECT_IMG[p["slug"]], lang, sizes="(max-width:760px) 100vw, 400px")}{illus(lang)}</a>'
            f'<div class="pb"><h3><a href="{ppath(p, lang)}">{escape(d["name"])}</a></h3>'
            f'<p class="meta">{escape(d["developer"])} · {escape(d["area"])}</p>'
            f'<p>{escape(d["types"])}</p>'
            f'<p><b>{escape(str(price))}</b><br><span class="note">{handover_label}: {escape(d["handover"])} · {checked_label}: {escape(checked)}</span></p>'
            f'<p class="fit"><b>{t["may_suit"]}:</b> {escape(d["suits"][0])}</p>'
            f'<p class="fit no"><b>{t["may_not"]}:</b> {escape(d["not_for"][0])}</p>'
            f'<a class="more" href="{ppath(p, lang)}">{t["view"]}</a></div></article>')

def band(lang, heading, buttons, bg="skyline-sunset"):
    to_form = lambda u: "#contact" if (C.WHATSAPP and u.endswith("/book/")) else u
    btns = "".join(f'<a class="btn{" ghost" if i else ""}" href="{to_form(u)}">{escape(l)}</a>' for i, (u, l) in enumerate(buttons))
    return (f'<section class="band">{img(bg, lang, "cover")}<div class="wrap"><h2>{escape(heading)}</h2>'
            f'<div class="actions">{btns}</div></div></section>')

def clients_html(lang):
    if lang == "ar":
        h, p, alt = "أعمال التسويق", "علامات تجارية عمل معها أحمد في التسويق وجذب العملاء وتحسين التحويل. لا تمثل هذه الشعارات اعتمادًا لخدمات الاستشارة العقارية.", "شعار {}"
    else:
        h, p, alt = "Marketing work", "Brands Ahmed has worked with in performance marketing, customer acquisition and conversion. These logos are not endorsements of the property-advisory service.", "{} logo"
    items = "".join(f'<li class="{tone}"><img src="/assets/img/clients/{s}.webp" width="240" height="100" alt="{escape(alt.format(n))}" loading="lazy" decoding="async"></li>'
                    for s, n, tone in CLIENTS)
    return f'<section id="clients"><h2 class="sec-h">{h}</h2><p>{p}</p><ul class="clients">{items}</ul></section>'

def articles_teaser(lang):
    if lang != "ar":
        return ""
    return ('<section id="articles"><h2 class="sec-h">أحدث المقالات</h2>'
            f'<div class="plist">{"".join(acard(a) for a in ARTICLES)}</div>'
            '<div class="actions"><a class="btn ghost" href="/blog/">كل المقالات</a></div></section>')

def hero_inner(crumbs, lang, h1, lede=""):
    return crumbs_html(crumbs, lang) + f"<h1>{escape(h1)}</h1>" + (f'<p class="lede">{escape(lede)}</p>' if lede else "")


def extra_faqs(lang):
    """Brief 1.8: FAQs added to the homepage and ad landing page."""
    qs = {"fee": ("Do you charge me a fee?", "هل تتقاضى مني رسومًا؟"),
          "abu_dhabi": ("Can I buy in Abu Dhabi as a foreigner?", "هل يمكنني الشراء في أبوظبي كأجنبي؟")}
    out = []
    for key, (q_en, q_ar) in qs.items():
        en, ar = getattr(C, f"FAQ_{key.upper()}_EN", ""), getattr(C, f"FAQ_{key.upper()}_AR", "")
        if en and ar:  # never publish one language without the other
            out.append((q_ar, ar) if lang == "ar" else (q_en, en))
    return out + EXTRA_FAQS[lang]

def tier_cards(lang, h, href):
    """Price tiers (brief 1.6); bedroom range shown only once Ahmed confirms it in config."""
    out = []
    for tier, title, desc in h["tiers"]:
        beds = C.TIER_BEDROOMS.get(tier)
        beds_html = f'<p class="note">{escape(beds[1] if lang == "ar" else beds[0])}</p>' if beds else ""
        out.append(f'<article class="tier-card"><h3>{escape(title)}</h3><p>{escape(desc)}</p>{beds_html}<a class="more" href="{href(tier)}">{escape(h["see"])}</a></article>')
    return "".join(out)

# ------------------------------------------------------------------ HOME
def build_home(lang):
    old, h = HOME[lang], HOME_CONVERSION[lang]
    faqs = old["faqs"] + extra_faqs(lang)
    benefits = "".join(f'<article class="benefit-card"><span class="num">0{i}</span><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i, (a, b) in enumerate(h["benefits"], 1))
    audience = "".join(f'<article class="audience-card"><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for a, b in h["audience"])
    landing = "/ar/villas-townhouses-dubai-abu-dhabi/" if lang == "ar" else "/villas-townhouses-dubai-abu-dhabi/"
    tiers = tier_cards(lang, h, lambda tier: f"{landing}?tier={tier}")
    steps = "".join(f"<li><b>{escape(a)}</b>{escape(b)}</li>" for a, b in h["steps"])
    developers = "".join(f"<li>{escape(name)}</li>" for name in h["developers"])
    featured = "".join(card(BY_SLUG[s], lang) for s in ["the-valley-emaar", "tilal-al-ghaf", "palm-jebel-ali-villas"])
    all_p = ('/ar/projects/', 'كل المشاريع') if lang == 'ar' else ('/projects/', 'All projects')
    body = f"""
<section class="hero">{img('skyline-night', lang, 'cover', eager=True)}<div class="wrap hero-grid">
 <div><p class="eyebrow">{escape(h['eyebrow'])}</p><h1>{escape(h['h1'])}</h1><p class="lede">{escape(h['sub'])}</p><p class="note">{escape(h['trust'])}</p></div>
 {booking_form(lang, compact=True, anchor='hero-booking')}
</div><span class="scroll-cue" aria-hidden="true"></span></section>
<div class="wrap">
<section id="developers"><h2>{escape(h['developers_h'])}</h2><ul class="developer-strip">{developers}</ul><p>{escape(h['developers_note'])}</p></section>
<section id="services"><h2>{escape(h['benefits_h'])}</h2><div class="benefit-grid">{benefits}</div><p class="market-line">{escape(h['markets'])}</p></section>
<section><h2>{escape(h['audience_h'])}</h2><div class="audience-grid">{audience}</div></section>
<section><h2>{escape(h['tiers_h'])}</h2><div class="tier-grid">{tiers}</div></section>
<section id="how-it-works"><h2>{escape(h['steps_h'])}</h2><ol class="steps">{steps}</ol></section>
<h2>{escape(h['projects_h'])}</h2><div class="plist">{featured}</div>
<div class="actions"><a class="btn ghost" href="{all_p[0]}">{all_p[1]}</a></div>
<section class="split" id="about"><div class="frame">{img('ahmed-esmat-dubai-advisor', lang, 'cover top', sizes='(max-width:860px) 100vw, 560px')}</div>
 <div><h2>{escape(old['bio_h'])}</h2>{''.join(f'<p>{escape(x)}</p>' for x in old['bio'])}<p><strong>{escape(h['about_line'])}</strong></p></div></section>
{clients_html(lang)}
{articles_teaser(lang)}
{faq_html(faqs, old['faq_h'])}
</div>
"""
    schemas = [person_schema(), service_schema(), website_schema(), faq_schema(faqs)]
    write(old["path"], page(lang=lang, path=old["path"], title=h["title"], description=h["meta"], body=body, alt_path=old["alt"], schemas=schemas, home_page=True,
                            lead_heading=h["bottom_h"]), old["alt"])

# ------------------------------------------------------------------ LANDING
def mini(lang):
    t = T[lang]
    u = "/ar/investor-assessment/" if lang == "ar" else "/investor-assessment/"
    return f'<section class="mini"><h2>{t["mini_h"]}</h2><p>{t["mini_p"]}</p><a class="btn" href="{u}">{t["start"]}</a></section>'

def build_landing(L):
    lang, t = L["lang"], T[L["lang"]]
    home = "/ar/" if lang == "ar" else "/"
    crumbs = [(home, t["home"]), (L["path"], L["crumb"])]
    cards = "".join(card(p, lang) for p in PROJECTS if set(p["cats"]) & set(L["cats"]))
    secs = "".join(f"<h2>{escape(h)}</h2>{html}" for h, html in L["sections"])
    related = "".join(f'<li><a href="{u}">{escape(n)}</a></li>' for u, n in L["related"])
    key = PAGE_IMG[L["path"]]
    body = f"""{phero(key, lang, hero_inner(crumbs, lang, L['h1']))}
<div class="wrap">
<div class="lede-block">{L['intro']}</div>
<h2>{escape(L['cards_h2'])}</h2><div class="plist">{cards}</div>
{secs}
{mini(lang)}
{faq_html(L['faqs'], t['faq'])}
<h2>{t['related']}</h2><ul class="related">{related}</ul>
</div>
{band(lang, HOME[lang]['band_h'], HOME[lang]['band'])}"""
    schemas = [crumbs_schema(crumbs), faq_schema(L["faqs"])]
    write(L["path"], page(lang=lang, path=L["path"], title=L["title"], description=L["meta"], body=body, alt_path=L["alt"], schemas=schemas, og_img=key), L["alt"])

# ------------------------------------------------------------------ PROJECTS
def build_index(lang):
    t = T[lang]
    path = "/ar/projects/" if lang == "ar" else "/projects/"
    alt = "/projects/" if lang == "ar" else "/ar/projects/"
    home = "/ar/" if lang == "ar" else "/"
    crumbs = [(home, t["home"]), (path, t["projects"])]
    cards = "".join(card(p, lang) for p in PROJECTS)
    body = f"""{phero(PAGE_IMG[path], lang, hero_inner(crumbs, lang, t['idx_h1'], t['idx_lede']))}
<div class="wrap"><div class="plist">{cards}</div>{mini(lang)}</div>{band(lang, HOME[lang]['band_h'], HOME[lang]['band'])}"""
    write(path, page(lang=lang, path=path, title=t["idx_title"], description=t["idx_meta"], body=body, alt_path=alt, schemas=[crumbs_schema(crumbs)], og_img=PAGE_IMG[path]), alt)

def build_project(p, lang):
    d, t = p[lang], T[lang]
    path, alt = ppath(p, lang), ppath(p, "en" if lang == "ar" else "ar")
    home = "/ar/" if lang == "ar" else "/"
    name = d["name"]
    if lang == "en":
        title = f"{name} by {d['developer']}: Investor Fit, Location & Risks"
        if len(title) > 62: title = f"{name} by {d['developer']}: Investor Fit & Risks"
        h1 = f"{name} by {d['developer']}"
        meta = f"{name} by {d['developer']}, {d['area']}. {d['summary']}"
    else:
        title = f"مشروع {name} من {d['developer']}: لمن يناسب والمخاطر"
        if len(title) > 60: title = f"{name} من {d['developer']}: لمن يناسب"
        h1 = f"مشروع {name} من {d['developer']}"
        meta = f"مشروع {name} من {d['developer']} في {d['area']}. {d['summary']}"
    if len(meta) > 158:
        meta = meta[:155].rsplit(" ", 1)[0].rstrip("،,.:") + "…"
    crumbs = [(home, t["home"]), (("/ar" if lang == "ar" else "") + "/projects/", t["projects"]), (path, name)]
    price = p["price_from"] or t["on_req"]
    plan = p["payment_plan"] or t["on_req"]
    facts = [(t["dev"], d["developer"]), (t["loc"], d["area"]), (t["type"], d["types"]), (t["stage"], d["stage"]),
             (t["handover"], d["handover"]), (t["price"] + " / " + t["plan"], price if price == plan else f"{price} / {plan}")]
    facts_html = '<dl class="facts">' + "".join(f"<div><dt>{a}</dt><dd>{escape(str(b))}</dd></div>" for a, b in facts) + "</dl>"
    ul = lambda xs: "<ul>" + "".join(f"<li>{escape(x)}</li>" for x in xs) + "</ul>"
    ask = f'<a class="btn" href="#contact">{t["book_project"]}</a>'
    pct = ""
    if p["pct_before_handover"]:
        pct = (f"<p>نحو {p['pct_before_handover']}٪ من السعر يُدفع قبل استلام الوحدة.</p>" if lang == "ar"
               else f"<p>About {p['pct_before_handover']}% is paid before you receive the keys.</p>")
    cmp_links = "".join(f'<li><a href="{ppath(BY_SLUG[s], lang)}">{escape(BY_SLUG[s][lang]["name"])}</a></li>' for s in p["en"]["compare"])
    key = PROJECT_IMG[p["slug"]]
    body = f"""{phero(key, lang, hero_inner(crumbs, lang, h1, d['summary']), badge=True)}
<div class="wrap">
{facts_html}
<div class="actions">{ask}<a class="btn ghost" href="{'/ar/investor-assessment/' if lang=='ar' else '/investor-assessment/'}">{t['start']}</a></div>
<div class="fitgrid">
 <section class="fitbox yes"><h2>{t['suits_h']}</h2>{ul(d['suits'])}</section>
 <section class="fitbox no"><h2>{t['not_h']}</h2>{ul(d['not_for'])}</section>
</div>
<h2>{t['pay_h']}</h2><p class="pending">{t['pending']}</p>{pct}
<h2>{t['loc_h']}</h2><p>{escape(d['location'])}</p>
<h2>{t['app_h']}</h2>{ul(d['appreciation'])}
<h2>{t['rent_h']}</h2><p>{escape(d['rental'])}</p>
<h2>{t['sup_h']}</h2><p>{escape(d['supply'])}</p>
<section class="strengths"><h2>{t['str_h']}</h2>{ul(d['strengths'])}</section>
<section class="risks"><h2>{t['risk_h']}</h2>{ul(d['risks'])}</section>
<h2>{t['cmp_h'].format(p=escape(name))}</h2><ul class="related">{cmp_links}</ul>
{faq_html(d['faqs'], t['faq_h'].format(p=name))}
<p class="note">{escape(t['checked'].format(d=C.DATA_CHECKED_AR if lang=='ar' else C.DATA_CHECKED_EN, dev=d['developer']))}</p>
</div>
{band(lang, t['cta_p'].format(p=name), [('/ar/investor-assessment/' if lang=='ar' else '/investor-assessment/', t['start']), ('/ar/book/' if lang=='ar' else '/book/', t['talk'])])}"""
    place = {"@context": "https://schema.org", "@type": "Place", "name": f"{p['en']['name']} ({p['en']['developer']})",
             "alternateName": p["ar"]["name"], "url": C.DOMAIN + path, "description": d["summary"],
             "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE", "streetAddress": p["en"]["area"]}}
    schemas = [crumbs_schema(crumbs), place, faq_schema(d["faqs"])]
    topic = (f"مهتم بمشروع {name}، أريد آخر سعر وخطة دفع." if lang == "ar" else f"Interested in {name}. Please send the latest price and payment plan.")
    write(path, page(lang=lang, path=path, title=title, description=meta, body=body, alt_path=alt, schemas=schemas, og_img=key,
                     lead_topic=topic, lead_interest=2), alt)

# ------------------------------------------------------------------ ASSESSMENT
def build_assess(lang):
    a, t = ASSESS[lang], T[lang]
    fs = ""
    for key, q, opts in a["qs"]:
        o = "".join(f'<label><input type="radio" name="{key}" value="{v}" required><span>{escape(l)}</span></label>' for v, l in opts)
        fs += f'<fieldset><legend>{escape(q)}</legend><div class="opts">{o}</div></fieldset>'
    projects = {p["slug"]: {"name": p[lang]["name"], "url": ppath(p, lang), "suit": p[lang]["suits"][0]} for p in PROJECTS}
    labels = {k: {v: l for v, l in opts} for k, q, opts in a["qs"]}
    qtext = {k: q for k, q, opts in a["qs"]}
    msgs = {
     "en": {"short": "With a 2–3 year horizon, most off-plan projects are a mismatch: handover and resale may not happen in time. Ready property, or keeping the capital liquid, may fit better.",
            "income": "For income, completed communities with real rental evidence usually fit better than launches.",
            "none": "No project on our current list is a clear match. A conversation will help define the right option — which may not be property.",
            "head": "Projects that may fit", "wa_intro": "Hi Ahmed, here is my investor profile:"},
     "ar": {"short": "مع مدة سنتين أو ثلاث، معظم المشاريع قيد الإنشاء لا تناسبك: قد لا يتم التسليم أو البيع في الوقت المطلوب. العقار الجاهز، أو إبقاء المال سائلاً، قد يكون أنسب.",
            "income": "إذا كان هدفك الدخل، فالمجتمعات المكتملة ذات بيانات الإيجار الحقيقية أنسب عادة من الإطلاقات الجديدة.",
            "none": "لا يوجد مشروع في قائمتنا الحالية يتطابق بوضوح. المحادثة ستساعد على تحديد الخيار المناسب، وقد لا يكون عقاراً.",
            "head": "مشاريع قد تناسبك", "wa_intro": "مرحباً أحمد، هذا ملفي الاستثماري:"},
    }[lang]
    wa = wa_link("") or ""
    book = "/ar/book/" if lang == "ar" else "/book/"
    script = """
<script>
(function(){
var P=%s, L=%s, Q=%s, M=%s, WA=%s;
// Indicative budget bands — adjust as current prices change.
var BUD={b1:["the-valley-emaar","damac-lagoons"],b2:["the-valley-emaar","damac-lagoons","nad-al-sheba-gardens","tilal-al-ghaf","sobha-hartland-villas"],
 b3:["tilal-al-ghaf","the-oasis-emaar","nad-al-sheba-gardens","sobha-hartland-villas"],b4:["elysian-mansions-tilal-al-ghaf","palm-jebel-ali-villas","the-oasis-emaar","tilal-al-ghaf"]};
var READY=["sobha-hartland-villas","the-valley-emaar","damac-lagoons","tilal-al-ghaf"];
var LONG=["palm-jebel-ali-villas","the-oasis-emaar","elysian-mansions-tilal-al-ghaf"];
var f=document.getElementById('assess'),r=document.getElementById('result');
f.addEventListener('submit',function(e){e.preventDefault();
 var a={};new FormData(f).forEach(function(v,k){a[k]=v});
 var c=(BUD[a.budget]||[]).slice(),notes=[];
 if(a.horizon==='short'){notes.push(M.short);c=c.filter(function(s){return READY.indexOf(s)>-1})}
 if(a.stage==='ready'||a.risk==='low'){c=c.filter(function(s){return LONG.indexOf(s)<0})}
 if(a.goal==='income'){notes.push(M.income);c=c.filter(function(s){return LONG.indexOf(s)<0})}
 c=c.slice(0,3);
 var h='<h2>'+%s+'</h2><ul>';Object.keys(a).forEach(function(k){h+='<li>'+Q[k]+': <b>'+L[k][a[k]]+'</b></li>'});h+='</ul>';
 notes.forEach(function(n){h+='<p>'+n+'</p>'});
 if(c.length){h+='<h3>'+M.head+'</h3><ul>';c.forEach(function(s){h+='<li><a href="'+P[s].url+'">'+P[s].name+'</a> — '+P[s].suit+'</li>'});h+='</ul>'}else{h+='<p>'+M.none+'</p>'}
 var txt=M.wa_intro+'\\n';Object.keys(a).forEach(function(k){txt+='- '+Q[k]+': '+L[k][a[k]]+'\\n'});
 h+='<div class="actions">'+(WA?'<a class="btn" rel="noopener" href="'+WA+'?text='+encodeURIComponent(txt)+'">'+%s+'</a>':'')+'<a class="btn ghost" href="%s">'+%s+'</a></div><p class="note">'+%s+'</p>';
 r.innerHTML=h;r.classList.add('show');r.focus();
});})();
</script>""" % (script_json(projects), script_json(labels), script_json(qtext),
                script_json(msgs), script_json(wa), script_json(a["result_h"]),
                script_json(a["send"]), book, script_json(a["book"]), script_json(a["note"]))
    home = "/ar/" if lang == "ar" else "/"
    crumbs = [(home, t["home"]), (a["path"], a["h1"])]
    body = f"""{phero(PAGE_IMG[a['path']], lang, hero_inner(crumbs, lang, a['h1'], a['lede']))}<div class="wrap">
<form id="assess" class="mini">{fs}<button class="btn" type="submit">{escape(a['submit'])}</button></form>
<div id="result" class="result" tabindex="-1" aria-live="polite"></div></div>{script}"""
    write(a["path"], page(lang=lang, path=a["path"], title=a["title"], description=a["meta"], body=body, alt_path=a["alt"], schemas=[crumbs_schema(crumbs)]), a["alt"])

def build_book(lang):
    b, t = BOOK[lang], T[lang]
    wa = wa_link("مرحباً أحمد، أريد استشارة" if lang == "ar" else "Hi Ahmed, I'd like to book a consultation")
    btns = ""
    if wa: btns += f'<a class="btn" href="{wa}" rel="noopener">{b["wa"]}</a>'
    if C.EMAIL: btns += f'<a class="btn ghost" href="mailto:{C.EMAIL}">{b["mail"]}</a>'
    if not btns:
        btns = f'<p class="pending">{b["missing"]}</p><a class="btn" href="{"/ar/investor-assessment/" if lang=="ar" else "/investor-assessment/"}">{t["start"]}</a>'
    home = "/ar/" if lang == "ar" else "/"
    crumbs = [(home, t["home"]), (b["path"], b["h1"])]
    body = f"""{phero(PAGE_IMG[b['path']], lang, hero_inner(crumbs, lang, b['h1'], b['lede']))}<div class="wrap">
<section class="split rev"><div class="frame">{img('ahmed-esmat-portrait', lang, 'cover top', sizes='(max-width:860px) 100vw, 560px')}</div>
 <div><h2>{escape(b['bring'])}</h2><ul>{''.join(f'<li>{escape(x)}</li>' for x in b['bring_list'])}</ul></div></section>
<div id="contact" class="book-form">{booking_form(lang, compact=True)}</div></div>"""
    write(b["path"], page(lang=lang, path=b["path"], title=b["title"], description=b["meta"], body=body, alt_path=b["alt"], schemas=[crumbs_schema(crumbs), person_schema()], og_img="ahmed-esmat-portrait", lead=False), b["alt"])

def build_disclaimer(lang):
    d = DISCLAIMER[lang]
    credits = ", ".join(sorted({v["credit"] for v in IMAGES.values() if v["credit"]}))
    photo_note = (f"صور المشاريع والمدن في هذا الموقع صور توضيحية من Unsplash وليست صوراً رسمية للمشاريع. تصوير: {credits}. الشعارات ملك أصحابها." if lang == "ar"
                  else f"Project and city photos on this site are illustrative images from Unsplash, not official project imagery. Photography: {credits}. Logos belong to their owners.")
    body = (phero(PAGE_IMG[d["path"]], lang, f'<h1>{escape(d["h1"])}</h1>') + '<div class="wrap"><div class="lede-block">'
            + "".join(f"<p>{escape(x)}</p>" for x in d["body"]) + f'<p class="note">{escape(photo_note)}</p></div></div>')
    write(d["path"], page(lang=lang, path=d["path"], title=d["title"], description=d["meta"], body=body, alt_path=d["alt"]), d["alt"])

def build_privacy(lang):
    d = PRIVACY[lang]
    home = "/ar/" if lang == "ar" else "/"
    label = "الخصوصية" if lang == "ar" else "Privacy"
    entity = (C.LEGAL_ENTITY_AR if lang == "ar" else C.LEGAL_ENTITY_EN) if (C.LEGAL_ENTITY_EN and C.LEGAL_ENTITY_AR) else ""
    secs = list(d["sections"])
    if entity:  # the "to be completed" note is replaced by the real controller details
        contact = " ".join(x for x in (C.EMAIL, "+" + C.WHATSAPP if C.WHATSAPP else "") if x)
        secs = secs[:-1] + [(d["controller_h"], d["controller"].format(entity=entity, contact=contact))]
    sections = "".join(f'<section><h2>{escape(h)}</h2><p>{escape(p)}</p></section>' for h, p in secs)
    body = f'{phero("skyline-storm", lang, hero_inner([(home, "الرئيسية" if lang=="ar" else "Home"), (d["path"], label)], lang, d["h1"], d["updated"]))}<div class="wrap narrow prose">{sections}</div>'
    write(d["path"], page(lang=lang, path=d["path"], title=d["title"], description=d["meta"], body=body, alt_path=d["alt"],
                          schemas=[crumbs_schema([(home, "Home"), (d["path"], label)])]), d["alt"])

def build_conversion_landing(lang):
    d, h = LANDING_CONVERSION[lang], HOME_CONVERSION[lang]
    faqs = HOME[lang]["faqs"] + extra_faqs(lang)
    benefits = "".join(f'<article class="benefit-card"><span class="num">0{i}</span><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i, (a, b) in enumerate(h["benefits"], 1))
    tiers = tier_cards(lang, h, lambda tier: f'{d["path"]}?tier={tier}#contact')
    questions = "".join(f'<li><b>{i}.</b> {escape(q)}</li>' for i, q in enumerate(d["questions"], 1))
    body = f"""<section class="hero">{img('villa-palms', lang, 'cover', eager=True)}<div class="wrap hero-grid"><div><h1>{escape(d['h1'])}</h1><p class="lede">{escape(d['sub'])}</p></div>{booking_form(lang, compact=True)}</div></section>
<div class="wrap"><section id="services"><h2>{escape(h['benefits_h'])}</h2><div class="benefit-grid">{benefits}</div></section>
<section><h2>{escape(h['tiers_h'])}</h2><div class="tier-grid">{tiers}</div></section>
<section><h2>{escape(d['questions_h'])}</h2><ol class="steps">{questions}</ol></section>
{faq_html(faqs, HOME[lang]['faq_h'])}</div>"""
    write(d["path"], page(lang=lang, path=d["path"], title=d["title"], description=d["meta"], body=body, alt_path=d["alt"],
                          schemas=[service_schema(), faq_schema(faqs)], home_page=True, minimal_header=True,
                          lead_heading=h["bottom_h"]), d["alt"])

CALCS = {
    "cash": {"path": "/cash-needed-calculator/", "img": "interior-dark",
             "title": ("Cash Needed to Buy Property in Dubai: Calculator", "حاسبة الكاش المطلوب لشراء عقار في دبي"),
             "h1": ("How much cash do you need to buy?", "كم كاش تحتاج للشراء؟"),
             "lede": ("Down payment, 4% registration and mortgage registration for a Dubai property, before agency commission and bank fees.",
                      "الدفعة المقدمة ورسم التسجيل 4% وتسجيل الرهن لعقار في دبي، قبل عمولة الوسيط ورسوم البنك."),
             "results": ["down", "registration", "mortgage", "cash"], "fields": ["price", "buyer", "property", "down", "ltv"]},
    "monthly": {"path": "/mortgage-calculator/", "img": "villa-pool-wide",
                "title": ("UAE Mortgage Calculator: Monthly Payment", "حاسبة القسط الشهري للتمويل العقاري في الإمارات"),
                "h1": ("What will the monthly payment be?", "كم سيكون القسط الشهري؟"),
                "lede": ("Monthly mortgage payment and the income banks usually expect, for a Dubai property.",
                         "القسط الشهري للتمويل العقاري والدخل الذي تتوقعه البنوك عادةً، لعقار في دبي."),
                "results": ["loan", "monthly", "income"], "fields": ["price", "buyer", "property", "down", "ltv", "rate", "term"]},
}

def calc_path(kind, lang):
    return ("/ar" if lang == "ar" else "") + CALCS[kind]["path"]

def build_calculator(lang, kind):
    """Brief 5.2: two calculators (cash needed, monthly payment); each ends with the booking CTA."""
    ar, c = lang == "ar", CALCS[kind]
    i = 1 if ar else 0
    path, alt = calc_path(kind, lang), calc_path(kind, "en" if ar else "ar")
    other = "monthly" if kind == "cash" else "cash"
    note = "تقدير توضيحي. شروط البنوك والرسوم تختلف، والنتيجة ليست عرض تمويل." if ar else "Illustrative. Banks and fees vary; this is not a finance offer."
    L = {
        "price": "سعر العقار (درهم)" if ar else "Property price (AED)", "buyer": "فئة المشتري" if ar else "Buyer category",
        "expat": "وافد مقيم" if ar else "Expatriate resident", "national": "مواطن إماراتي" if ar else "UAE national", "nonresident": "غير مقيم (تقديري حسب البنك)" if ar else "Non-resident (bank-dependent estimate)",
        "property": "حالة الشراء" if ar else "Purchase type", "first": "أول منزل جاهز للسكن" if ar else "First completed owner-occupied home", "second": "عقار ثانٍ أو استثماري" if ar else "Second / investment property", "offplan": "عقار قيد الإنشاء" if ar else "Off-plan property",
        "down_in": "الدفعة المقدمة (درهم)" if ar else "Down payment (AED)", "ltv": "نسبة التمويل %" if ar else "Loan-to-value %", "rate": "الفائدة السنوية %" if ar else "Annual interest %", "term": "مدة التمويل بالسنوات" if ar else "Loan term (years)", "button": "احسب" if ar else "Calculate",
        "down": "الدفعة المقدمة" if ar else "Down payment", "loan": "قيمة التمويل" if ar else "Loan amount", "registration": "رسم التسجيل 4%" if ar else "Registration fee (4%)", "mortgage": "تسجيل الرهن" if ar else "Mortgage registration",
        "cash": "الكاش المطلوب (قبل العمولة ورسوم البنك)" if ar else "Cash needed (before commission and bank fees)", "monthly": "القسط الشهري" if ar else "Monthly payment", "income": "الدخل الشهري المطلوب تقديريًا" if ar else "Illustrative required monthly income",
    }
    inputs = {
        "price": f'<label>{L["price"]}<input name="price" type="number" min="100000" step="any" value="2700000" required inputmode="numeric"></label>',
        "buyer": f'<label>{L["buyer"]}<select name="buyer"><option value="expat">{L["expat"]}</option><option value="national">{L["national"]}</option><option value="nonresident">{L["nonresident"]}</option></select></label>',
        "property": f'<label>{L["property"]}<select name="property_type"><option value="first">{L["first"]}</option><option value="second">{L["second"]}</option><option value="offplan">{L["offplan"]}</option></select></label>',
        "down": f'<label>{L["down_in"]}<input name="down" type="number" min="0" step="any" inputmode="numeric"></label>',
        "ltv": f'<label>{L["ltv"]}<input name="ltv" type="number" min="0" max="100" step="any" value="80"></label>',
        "rate": f'<label>{L["rate"]}<input name="rate" type="number" min="3.75" max="5.5" step="any" value="4.5"></label>',
        "term": f'<label>{L["term"]}<input name="term" type="number" min="1" max="25" step="1" value="25"></label>',
    }
    fields = "".join(inputs[f] for f in c["fields"])
    results = "".join(f'<div><span>{L[r]}</span><strong data-result="{r}">—</strong></div>' for r in c["results"])
    other_link = (f'<p><a href="{calc_path(other, lang)}">{escape(CALCS[other]["h1"][i])}</a></p>')
    body = f"""{phero(c['img'], lang, f'<h1>{escape(c["h1"][i])}</h1><p class="lede">{escape(c["lede"][i])}</p>')}
<div class="wrap narrow"><form class="calculator" data-lang="{lang}" data-kind="{kind}" novalidate><div class="calc-grid">{fields}</div>
<p class="note calc-cap" aria-live="polite" hidden></p>
<button class="btn" type="submit">{L['button']}</button><p class="note">{escape(note)}</p>
<div class="calc-results" aria-live="polite">{results}</div></form>
<div class="actions"><a class="btn" href="#contact">{'احجز استشارة لمراجعة أرقامك' if ar else 'Book a consultation to check your numbers'}</a></div>
{other_link}</div>"""
    write(path, page(lang=lang, path=path, title=c["title"][i], description=c["lede"][i], body=body, alt_path=alt,
                     schemas=[service_schema()], og_img=c["img"]), alt)

# ------------------------------------------------------------------ GUIDES (real estate, brief 5.3)
DRAFTS = bool(os.environ.get("A1_DRAFTS"))

def guide_list():
    return [g for g in GUIDES if is_ready(g) or DRAFTS]

def guide_path(g, lang):
    return ("/ar" if lang == "ar" else "") + f"/guides/{g['slug']}/"

def build_guide(g, lang):
    ar, i = lang == "ar", (1 if lang == "ar" else 0)
    d, title = g[lang], g["title"][i]
    path, alt = guide_path(g, lang), guide_path(g, "en" if ar else "ar")
    home, idx = ("/ar/" if ar else "/"), ("/ar/guides/" if ar else "/guides/")
    crumbs = [(home, "الرئيسية" if ar else "Home"), (idx, "أدلة الشراء" if ar else "Buying guides"), (path, title)]
    draft = not is_ready(g)
    intro = d["intro"] or ("النص النهائي لهذا الدليل لم يصل بعد." if ar else "The final text for this guide has not been supplied yet.")
    points = "".join(f"<li><b>{escape(h)}</b>{escape(t)}</li>" for h, t in d["points"])
    calc = (f'<section class="mini"><h2>{escape(CALCS[g["calc"]]["h1"][i])}</h2><a class="btn ghost" href="{calc_path(g["calc"], lang)}">'
            f'{"افتح الحاسبة" if ar else "Open the calculator"}</a></section>') if g["calc"] else ""
    others = "".join(f'<li><a href="{guide_path(o, lang)}">{escape(o["title"][i])}</a></li>' for o in guide_list() if o is not g)
    banner = f'<p class="pending">{"مسودة: لا تُنشر حتى يكتمل النص باللغتين." if ar else "Draft: not published until the text is complete in both languages."}</p>' if draft else ""
    body = f"""{phero('townhouses-row', lang, hero_inner(crumbs, lang, title))}
<div class="wrap narrow prose">{banner}<p class="lede">{escape(intro)}</p>
{f'<ol class="steps">{points}</ol>' if points else ''}
{calc}
{faq_html(d['faqs'], 'أسئلة شائعة' if ar else 'Frequently asked questions') if d['faqs'] else ''}
{f'<h2>{"أدلة أخرى" if ar else "More guides"}</h2><ul class="related">{others}</ul>' if others else ''}</div>"""
    schemas = [crumbs_schema(crumbs), {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": intro,
               "inLanguage": lang, "mainEntityOfPage": C.DOMAIN + path, "author": {"@id": C.DOMAIN + "/#ahmed"},
               "publisher": {"@id": C.DOMAIN + "/#ahmed"}, **({"datePublished": d["date"]} if d["date"] else {})}]
    if d["faqs"]: schemas.append(faq_schema(d["faqs"]))
    html = page(lang=lang, path=path, title=f"{title} | {'أحمد عصمت' if ar else 'Ahmed Esmat'}", description=intro[:155], body=body,
                alt_path=alt, schemas=schemas, og_type="article", og_img="townhouses-row")
    if draft: html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    write(path, html, alt, sitemap=not draft)

def build_guides_index(lang):
    ar = lang == "ar"
    path, alt = ("/ar/guides/" if ar else "/guides/"), ("/guides/" if ar else "/ar/guides/")
    home = "/ar/" if ar else "/"
    crumbs = [(home, "الرئيسية" if ar else "Home"), (path, "أدلة الشراء" if ar else "Buying guides")]
    h1 = "أدلة شراء الفلل والتاون هاوس" if ar else "Guides to buying a villa or townhouse"
    lede = "إجابات عملية بالأرقام قبل أن تلتزم." if ar else "Practical answers, with numbers, before you commit."
    items = "".join(f'<li><a href="{guide_path(g, lang)}">{escape(g["title"][1 if ar else 0])}</a></li>' for g in guide_list())
    body = f"""{phero('townhouses-row', lang, hero_inner(crumbs, lang, h1, lede))}<div class="wrap narrow"><ul class="guide-list">{items}</ul></div>"""
    html = page(lang=lang, path=path, title=f"{h1} | {'أحمد عصمت' if ar else 'Ahmed Esmat'}", description=lede, body=body,
                alt_path=alt, schemas=[crumbs_schema(crumbs)], og_img="townhouses-row")
    published = any(is_ready(g) for g in GUIDES)
    if not published: html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    write(path, html, alt, sitemap=published)

def build_guides():
    templates.GUIDES_LIVE = any(is_ready(g) for g in GUIDES)
    if not guide_list():
        return
    for lang in ("en", "ar"):
        build_guides_index(lang)
        for g in guide_list(): build_guide(g, lang)

# ------------------------------------------------------------------ ARTICLES (Arabic, migrated from WordPress)
AR_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
for _a in ARTICLES:
    IMAGES[_a["img"]] = {"ar": _a["img_alt"], "en": _a["img_alt"], "credit": None, "w": (600, 900), "h": 600 / 933}

def ar_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {AR_MONTHS[int(m) - 1]} {y}"

def acard(a):
    u = f"/{a['slug']}/"
    return (f'<article class="pcard"><a class="ph" href="{u}" tabindex="-1" aria-hidden="true">'
            f'{img(a["img"], "ar", sizes="(max-width:760px) 100vw, 400px")}</a>'
            f'<div class="pb"><p class="meta"><time datetime="{a["date"]}">{ar_date(a["date"])}</time></p>'
            f'<h3><a href="{u}">{escape(a["title"])}</a></h3><p>{escape(a["desc"])}</p>'
            f'<a class="more" href="{u}">اقرأ المقال</a></div></article>')

def build_blog():
    path = "/blog/"
    crumbs = [("/ar/", "الرئيسية"), (path, "المقالات")]
    body = (phero("skyline-storm", "ar", hero_inner(crumbs, "ar", "مقالات في التسويق ونمو الأعمال",
            "خبرة عملية من داخل التسويق الرقمي وجذب العملاء ورفع معدلات التحويل، بلغة مباشرة وأمثلة قابلة للتطبيق.")) +
            f'<div class="wrap"><div class="plist">{"".join(acard(a) for a in ARTICLES)}</div></div>'
            + band("ar", HOME["ar"]["band_h"], HOME["ar"]["band"]))
    write(path, page(lang="ar", path=path, title="مقالات أحمد عصمت في التسويق ونمو الأعمال",
                     description="مقالات أحمد عصمت في التسويق الرقمي والبراندينج والسرد القصصي ومحتوى النمو والمبيعات، مع أمثلة عملية لأصحاب الأعمال.",
                     body=body, schemas=[crumbs_schema(crumbs)], og_img="skyline-storm", lead_interest=3))

def build_article(a):
    path = f"/{a['slug']}/"
    crumbs = [("/ar/", "الرئيسية"), ("/blog/", "المقالات"), (path, a["title"])]
    others = "".join(acard(o) for o in ARTICLES if o is not a)
    byline = (f'<div class="byline"><img src="/assets/img/ahmed-esmat-dubai-advisor-600.webp" width="600" height="600" alt="أحمد عصمت" loading="lazy">'
              f'<div><b>أحمد عصمت</b><span>مستشار تسويق ونمو أعمال · <time datetime="{a["date"]}">{ar_date(a["date"])}</time></span></div></div>')
    body = f"""<div class="wrap narrow">{crumbs_html(crumbs, 'ar')}
<header class="ahead"><h1>{escape(a['h1'])}</h1><p class="lede">{escape(a['desc'])}</p>{byline}</header>
<figure class="acover">{img(a['img'], 'ar', eager=True, sizes='(max-width:860px) 100vw, 820px')}</figure>
<div class="prose">{a['html']}</div>
<section class="mini"><h2>هل تريد تطبيق هذا على عملك؟</h2><p>تحدث مع أحمد عن التسويق وجذب العملاء ورفع معدل التحويل في مشروعك.</p><a class="btn" href="#contact">تحدث مع أحمد</a></section>
</div>
<div class="wrap"><h2>مقالات أخرى</h2><div class="plist">{others}</div></div>"""
    posting = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["h1"], "description": a["desc"],
               "image": C.DOMAIN + f"/assets/img/{a['img']}-900.webp", "datePublished": a["date"], "dateModified": a["modified"],
               "inLanguage": "ar", "mainEntityOfPage": C.DOMAIN + path, "author": {"@id": C.DOMAIN + "/#ahmed"},
               "publisher": {"@id": C.DOMAIN + "/#ahmed"}}
    html = page(lang="ar", path=path, title=f"{a['title']} | أحمد عصمت", description=a["desc"], body=body,
                schemas=[crumbs_schema(crumbs), posting, person_schema()], og_type="article", og_img=a["img"], lead_interest=3)
    html = html.replace("</head>", f'<meta property="article:published_time" content="{a["date"]}">\n'
                                    f'<meta property="article:modified_time" content="{a["modified"]}">\n</head>', 1)
    write(path, html)

def build_404():
    body = ('<div class="wrap"><h1>Page not found</h1><p>The page you were looking for has moved or does not exist.</p>'
            '<div class="actions"><a class="btn" href="/">Go to the home page</a><a class="btn ghost" href="/ar/">الصفحة الرئيسية بالعربية</a></div></div>')
    html = page(lang="en", path="/404.html", title="Page not found — Ahmed Esmat", description="Page not found.", body=body, lead=False)
    html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
    write("/404.html", html, sitemap=False)

# Old WordPress URLs -> closest page on the new site (301 keeps their search ranking)
OLD_REDIRECTS = [
    ("services", "/ar/"), ("الاستشارات-التسويقية-الاستراتيجية", "/ar/"), ("الإنتاج-الإبداعي-والمحتوى-الإعلاني", "/ar/"),
    ("الإعلانات-الممولة-وادارة-الحملات", "/ar/"), ("بناء-الهوية-الشخصية", "/ar/"), ("about-us", "/ar/"), ("about-me", "/ar/"),
    ("contact", "/ar/book/"), ("thank-you", "/ar/"), ("faq", "/ar/"), ("pricing", "/ar/book/"),
    ("blog-card", "/blog/"), ("blog-card-sidebar", "/blog/"), ("blog-default", "/blog/"), ("blog-list-left-thumb", "/blog/"),
    ("blog-list-right-thumb", "/blog/"), ("blog-list-random-thumb", "/blog/"), ("home-slider", "/ar/"), ("creative-agency", "/ar/"),
    ("personal-page", "/ar/"), ("works-list-style", "/ar/"), ("works-grid", "/ar/"), ("works-grid-style-2", "/ar/"),
    ("works-masonry-grid", "/ar/"), ("shop", "/ar/"), ("shop-2", "/ar/"), ("shop-2-2", "/ar/"), ("checkout-2", "/ar/"),
    ("my-account-2", "/ar/"), ("my-account-2-2", "/ar/"), ("cart-2", "/ar/"), ("sample-page", "/ar/"), ("sample-page-2", "/ar/"),
]

def csp():
    """Content-Security-Policy: own files, the booking backend and the analytics vendors loaded after consent."""
    from urllib.parse import urlparse
    endpoint = urlparse(C.BOOKING_ENDPOINT)
    booking = f"{endpoint.scheme}://{endpoint.netloc}" if endpoint.netloc else ""
    connect = " ".join(x for x in ["'self'", "https://script.google.com", "https://script.googleusercontent.com", booking,
                                     "https://*.google-analytics.com", "https://*.analytics.google.com", "https://www.googletagmanager.com",
                                     "https://www.facebook.com", "https://connect.facebook.net", "https://*.clarity.ms"] if x)
    return ("default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://connect.facebook.net https://www.clarity.ms https://*.clarity.ms; "
            f"connect-src {connect}; img-src 'self' data: blob: https:; style-src 'self' 'unsafe-inline'; font-src 'self'; "
            "frame-src 'none'; frame-ancestors 'self'; base-uri 'self'; object-src 'none'; form-action 'self'")

def htaccess():
    rules = "\n".join(f"RewriteRule ^{re.escape(o)}/?$ {n} [R=301,L]" for o, n in OLD_REDIRECTS)
    return f"""# Generated by build.py — static site (replaces WordPress)
DirectoryIndex index.html
Options -Indexes
ErrorDocument 404 /404.html
AddDefaultCharset utf-8

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
# http -> https (also behind a TLS-terminating proxy, without looping) and www -> non-www
RewriteCond %{{HTTPS}} !=on
RewriteCond %{{HTTP:X-Forwarded-Proto}} !https
RewriteRule ^(.*)$ https://a1esmat.com/$1 [R=301,L]
RewriteCond %{{HTTP_HOST}} ^www[.]a1esmat[.]com$ [NC]
RewriteRule ^(.*)$ https://a1esmat.com/$1 [R=301,L]
# The old WordPress install is gone: its scripts and admin paths answer 410 Gone, even if files were left on the server
RewriteRule ^(wp-admin|wp-includes|wp-content)(/.*)?$ - [G,L]
RewriteRule ^(wp-login|xmlrpc|wp-cron|wp-config|wp-settings|wp-load|wp-signup|wp-trackback|wp-mail|wp-links-opml|wp-activate|wp-blog-header|wp-comments-post)[.]php$ - [G,L]
{rules}
# WordPress feeds, archives and sitemaps
RewriteRule ^(feed|comments/feed)(/.*)?$ /blog/ [R=301,L]
RewriteRule ^(category|tag)/.*$ /blog/ [R=301,L]
RewriteRule ^author/.*$ /ar/ [R=301,L]
RewriteRule ^(sitemap_index|wp-sitemap|page-sitemap|post-sitemap)[.]xml$ /sitemap.xml [R=301,L]
</IfModule>

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()"
Header always set Content-Security-Policy "{csp()}"
</IfModule>

<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/html "access plus 0 seconds"
ExpiresByType text/css "access plus 1 year"
ExpiresByType text/javascript "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/x-icon "access plus 1 year"
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript application/json application/xml text/xml image/svg+xml
</IfModule>
"""

def build_static():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "site.css"), "w", encoding="utf-8") as f: f.write(CSS.strip())
    shutil.copytree(os.path.join(ROOT, "static", "img"), os.path.join(OUT, "assets", "img"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(ROOT, "static", "icons"), os.path.join(OUT, "assets", "icons"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(ROOT, "static", "fonts"), os.path.join(OUT, "assets", "fonts"), ignore=shutil.ignore_patterns("*.css"), dirs_exist_ok=True)
    js_src = os.path.join(ROOT, "static", "js")
    if os.path.isdir(js_src):
        shutil.copytree(js_src, os.path.join(OUT, "assets", "js"), dirs_exist_ok=True)
    shutil.copy(os.path.join(ROOT, "static", "icons", "favicon.ico"), os.path.join(OUT, "favicon.ico"))
    with open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8", newline="\n") as f:
        f.write(htaccess())
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {C.DOMAIN}/sitemap.xml\n")
    urls = []
    for path, alt in SITEMAP:
        lines = [f"  <url>\n    <loc>{C.DOMAIN}{path}</loc>\n    <lastmod>{C.BUILD_DATE}</lastmod>"]
        if alt:
            en_p, ar_p = (alt, path) if path.startswith("/ar/") else (path, alt)
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{C.DOMAIN}{en_p}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="ar" href="{C.DOMAIN}{ar_p}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{C.DOMAIN}{en_p}"/>')
        lines.append("  </url>")
        urls.append("\n".join(lines))
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + "\n".join(urls) + "\n</urlset>\n")
    # Cloudflare Pages / Netlify: security + caching headers
    with open(os.path.join(OUT, "_headers"), "w", encoding="utf-8", newline="\n") as f:
        f.write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n"
                "  Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
                "  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()\n"
                f"  Content-Security-Policy: {csp()}\n"
                "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n")

def main():
    # A1_NO_CLEAN=1 overwrites dist/ in place instead of deleting it first (useful when a file in it is held open)
    if os.path.exists(OUT) and not os.environ.get("A1_NO_CLEAN"): shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    templates.GUIDES_LIVE = any(is_ready(g) for g in GUIDES)
    for lang in ("en", "ar"):
        build_home(lang); build_index(lang); build_assess(lang); build_book(lang); build_disclaimer(lang)
        build_privacy(lang); build_conversion_landing(lang); build_calculator(lang, "cash"); build_calculator(lang, "monthly")
        for p in PROJECTS: build_project(p, lang)
    for L in LANDING: build_landing(L)
    build_guides()
    build_blog()
    for a in ARTICLES: build_article(a)
    build_404(); build_static()
    print(f"Built {len(SITEMAP)} indexable pages into {OUT}")

if __name__ == "__main__":
    main()
