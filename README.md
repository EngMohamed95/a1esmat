# موقع a1esmat.com — المرحلة الأولى

## ما في هذا الملف
- `dist/` — الموقع جاهز للرفع (36 صفحة: عربي + إنجليزي، sitemap.xml، robots.txt).
- `config.py` — بيانات التواصل والإعدادات. **املأها قبل الرفع.**
- `data_projects.py` — بيانات المشاريع الثمانية. أضف السعر وخطة الدفع هنا عند التحقق منها.
- `content_landing.py` و `content_pages.py` — نصوص الصفحات.
- `build.py` — يعيد توليد الموقع: `python3 build.py` (على ويندوز: `set PYTHONUTF8=1` ثم `python build.py`)
- `static/img/` — صور الموقع (كل صورة بمقاسين: `-900.webp` و `-1920.webp`)، تُنسخ تلقائياً إلى `dist/assets/img`.
- `data_images.py` — وصف الصور وأسماء المصورين، وأي صورة تظهر في أي صفحة/مشروع.
  الصور الحالية صور توضيحية مجانية من Unsplash (مكتوب عليها "صورة توضيحية")، وليست صوراً رسمية للمشاريع.
  لو عندك رندرات رسمية من المطور: ضعها في `static/img` بنفس نظام المقاسين، وغيّر اسمها في `PROJECT_IMG`.

## قبل الرفع (إلزامي)
1. في `config.py`: رقم الواتساب (`WHATSAPP`) والإيميل (`EMAIL`).
2. سطر الترخيص (`LICENSE_LINE_AR/EN`): اسم الوسيط المرخص ورقم RERA لو المعاملات بتتم من خلاله.
3. شغّل `python3 build.py` مرة واحدة بعد أي تعديل.

## الرفع (مجاني وسريع): Cloudflare Pages
1. أنشئ حساباً على dash.cloudflare.com ← Workers & Pages ← Create ← Pages ← Upload assets.
2. ارفع محتوى مجلد `dist` كما هو.
3. Custom domains ← أضف `a1esmat.com` و `www.a1esmat.com` واتبع تعليمات الـ DNS.
(بديل: Netlify ← Deploy manually ← اسحب مجلد dist.)

## بعد الرفع مباشرة
1. Google Search Console: أضف الدومين، ثم Sitemaps ← `https://a1esmat.com/sitemap.xml`.
2. اطلب فهرسة يدوية (URL Inspection) لصفحات المشاريع أولاً: هي أسرع صفحات هتظهر.
3. Google Business Profile باسم أحمد عصمت، والرابط للموقع.
4. حط رابط الموقع في Bio إنستجرام وكل حساباتك.

## التحديث الشهري (مهم للترتيب)
- صفحة المشاريع الجديدة: غيّر `UPDATED_MONTH_*` في config.py وحدّث قسم "أحدث المشاريع".
- `DATA_CHECKED_*`: تاريخ مراجعة البيانات.
