import config as C

P = lambda *xs: "".join(f"<p>{x}</p>" for x in xs)
UL = lambda *xs: "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"

LANDING = [
# ---------------------------------------------------------------- EN
{
 "lang": "en", "path": "/off-plan-properties-dubai/", "alt": "/ar/villas-installments-dubai/",
 "crumb": "Off plan properties Dubai",
 "title": "Off Plan Properties in Dubai: How to Choose the Right Project",
 "meta": "Off-plan villas and townhouses in Dubai compared by payment plan, handover, supply and risk — and matched to your investor profile, not a sales target.",
 "h1": "Off Plan Properties in Dubai, Assessed for Your Profile",
 "intro": P("Off plan properties in Dubai let you secure a home at today's price and pay in stages while it's built. That structure can suit a patient investor well. It can also tie up capital for years in a market cycle nobody can predict.",
            "This page covers villa and townhouse developments currently worth examining, how their payment plans affect your cash flow, and how to decide whether off-plan fits your situation at all. There are no scores here and no claim that any project is the best — only who each one may suit, and who it may not."),
 "cats": ["offplan"], "cards_h2": "Off-plan developments under analysis",
 "sections": [
  ("What off-plan really means for your cash flow", P(
   "Buying off-plan means committing to a total price now and paying it over a schedule the developer sets. A typical structure is a booking payment, instalments during construction, and a larger payment at handover. Some projects add post-handover instalments.",
   "The question that matters is not the headline price. It is how much of that price you will have paid before you receive the keys, and whether your income and savings can carry that schedule if something changes — a job move, a slower business year, or a handover that slips by a few quarters.",
   "When we assess a project, we translate its payment plan into a simple timeline of cash out and the earliest date you could realistically earn rent or sell. That timeline is usually more useful than any brochure yield.")),
  ("When off-plan makes sense — and when it doesn't", P("Off-plan tends to make sense when:") + UL(
   "your horizon is five years or more, so you are not relying on selling before or right after handover",
   "the payment schedule fits your cash flow with room to spare",
   "you are buying into a community whose future supply you understand",
   "capital growth, not immediate income, is the main goal") + P("It tends not to make sense when you need rental income soon, when you may need the money back within two or three years, or when the only reason to buy is a launch-day deadline.")),
  ("Payment plans: what's paid before the keys", P(
   "Developers describe plans as ratios such as 60/40 or 70/30. Read those as the share paid before and after handover. A plan with a large share after handover lowers the pressure during construction but extends your commitment afterwards.",
   "Also budget for costs outside the plan: the Dubai Land Department registration fee, service charges once the community is handed over, furnishing if you plan to rent, and agency fees on resale. Confirm current fees at the time you buy, as they can change.")),
  ("Risks to price in", UL(
   "<b>Handover delay.</b> Dates are targets. A delay pushes back rent and resale options.",
   "<b>Supply at handover.</b> Large communities hand over many similar units at once, which affects rents and resale prices.",
   "<b>Market cycle.</b> Off-plan locks you in for years. Prices can move either way over that period.",
   "<b>Liquidity.</b> Selling before handover depends on the developer's rules and on demand at that moment.")),
  ("How to buy off-plan in Dubai, step by step", "<ol class='steps'>"
   "<li><b>Define the goal</b>Growth, income, a family home, or diversification.</li>"
   "<li><b>Set a cash-flow limit</b>The maximum you can pay before handover without strain.</li>"
   "<li><b>Shortlist by fit</b>Communities and projects that match the goal and limit.</li>"
   "<li><b>Compare on the same criteria</b>Developer, location, plan, handover, supply, liquidity and risks.</li>"
   "<li><b>Verify and document</b>Current price, plan and dates confirmed in writing before you book.</li></ol>"),
 ],
 "faqs": [
  ("Is off plan property in Dubai a good investment?", "It can be for investors with a long horizon and a payment plan that fits their cash flow. It is a poor fit for anyone who needs income soon or may need to sell quickly."),
  ("What is the difference between off plan and ready property in Dubai?", "Off-plan is bought before completion on a payment plan; ready property is completed and can be lived in or rented immediately. Off-plan usually has a lower entry price and higher delivery risk."),
  ("Can I sell an off plan property before handover?", "Often yes, but it depends on the developer's resale rules, how much you have paid, and demand at that time. Check the rules before you buy, not when you want to sell."),
  ("What are the best off plan developments in Dubai?", "There is no universal best. The right project depends on your capital, horizon and risk tolerance. The investor assessment matches projects to your profile."),
  ("What does DXB off plan mean?", "It is simply shorthand for off-plan property in Dubai — homes sold by developers before construction is complete."),
 ],
 "related": [("/off-plan-villas-dubai/", "Off plan villas in Dubai"), ("/off-plan-townhouses-dubai/", "Off plan townhouses in Dubai"), ("/new-off-plan-projects-dubai/", "New off plan projects in Dubai")],
},
{
 "lang": "en", "path": "/off-plan-villas-dubai/", "alt": "/ar/buy-villa-dubai/",
 "crumb": "Off plan villas Dubai",
 "title": "Off Plan Villas for Sale in Dubai: Payment Plans & Investor Fit",
 "meta": "Off-plan villas in Dubai with developer payment plans. Compare communities, handover dates and risks, and see which projects suit your goals and timeline.",
 "h1": "Off Plan Villas in Dubai: Choose by Fit, Not by Launch",
 "intro": P("Buying one of the off plan villas in Dubai usually means a developer payment plan, a handover several years out, and a community that is still taking shape. Those are the same facts whether they suit you or not.",
            "Below are villa projects we are analysing, with their stage and the investor profiles they may suit — and the ones they may not. Use it to shortlist, then test the shortlist against your own numbers."),
 "cats": ["villa"], "cards_h2": "Off-plan villa projects worth examining",
 "sections": [
  ("Payment plans compared", P(
   "Villa payment plans in Dubai vary more than most buyers expect. Some are front-loaded during construction; others push a large share to handover or beyond. Two villas at the same price can place very different pressure on your cash flow.",
   "When comparing, write down three numbers for each project: the amount due in the next 12 months, the total due before handover, and what remains after. If you are looking for a villa for sale in Dubai with a payment plan, or to buy a villa in Dubai on instalments, those three numbers tell you more than the ratio in the brochure.")),
  ("Freehold ownership explained", P(
   "Most new villa communities in Dubai are in designated freehold areas, where foreign buyers can own property outright and register it with the Dubai Land Department. A freehold villa for sale in Dubai gives you full ownership of the unit and its plot, subject to community rules and service charges.",
   "Ownership rules and visa eligibility linked to property value can change, so confirm the current position for your situation before relying on it.")),
  ("Villa vs townhouse: which fits your goal", P(
   "Villas usually offer more land, more privacy and a smaller pool of competing units — which can help at resale. They also cost more to buy and maintain. Townhouses offer a lower entry price and steady family demand, but communities often launch many similar units.",
   "If capital growth and long-term family use are the goal, a villa in a well-located community often fits. If a lower entry price and rental demand matter most, compare the townhouse options too.")),
  ("Risks specific to off-plan villas", UL(
   "Handover dates can move, delaying the point where the villa earns or can be sold.",
   "Large villa communities hand over in waves; resale prices can soften when many similar villas complete together.",
   "Service charges and maintenance for larger plots are higher than most buyers budget for.",
   "Community amenities shown in the master plan may arrive years after your handover.")),
 ],
 "faqs": [
  ("Can foreigners buy off plan villas in Dubai?", "Yes, in designated freehold areas, which include most new villa communities. Confirm the status of the specific project."),
  ("How much do I pay before handover on an off plan villa?", "It depends on the payment plan. Many plans require a large share before handover; some spread payments after it. Calculate the exact amount for the specific project."),
  ("Which off plan villa projects are available in Dubai?", "Projects we are currently analysing include The Valley, DAMAC Lagoons, Tilal Al Ghaf, The Oasis, Nad Al Sheba Gardens and Palm Jebel Ali villas."),
  ("Is it better to buy a ready villa or off plan?", "Ready villas offer certainty and immediate rent; off-plan offers a lower entry and a payment plan with delivery risk. The right choice depends on your horizon and cash flow."),
 ],
 "related": [("/villa-projects-dubai/", "Villa projects in Dubai by community"), ("/off-plan-townhouses-dubai/", "Off plan townhouses in Dubai"), ("/off-plan-properties-dubai/", "Off plan properties in Dubai")],
},
{
 "lang": "en", "path": "/off-plan-townhouses-dubai/", "alt": "/ar/townhouses-for-sale-dubai/",
 "crumb": "Off plan townhouses Dubai",
 "title": "Off Plan Townhouses in Dubai: Projects, Payment Plans & Risks",
 "meta": "Off-plan townhouses in Dubai compared by entry price, payment plan, handover and rental potential. Find the townhouse projects that match your investor profile.",
 "h1": "Off Plan Townhouses in Dubai",
 "intro": P("An off plan townhouse in Dubai is often the most practical entry into the city's family communities: a lower starting price than a villa, and demand from families who want space without villa running costs.",
            "The trade-off is that many communities launch large numbers of similar units, which matters when you come to rent or resell. Here's how to weigh that, and which townhouse projects we are analysing."),
 "cats": ["townhouse"], "cards_h2": "Townhouse projects under analysis",
 "sections": [
  ("Why investors look at townhouses", P(
   "Townhouses sit between apartments and villas. They give tenants a garden and more space, which keeps family demand steady, while keeping the purchase price and service charges below villa levels. For many investors they are the first step into Dubai's villa communities.")),
  ("Townhouse or villa: the trade-offs", "<div class='tscroll'><table><thead><tr><th></th><th>Townhouse</th><th>Villa</th></tr></thead><tbody>"
   "<tr><td>Entry price</td><td>Lower</td><td>Higher</td></tr>"
   "<tr><td>Competing units at resale</td><td>Usually many</td><td>Usually fewer</td></tr>"
   "<tr><td>Running costs</td><td>Lower</td><td>Higher</td></tr>"
   "<tr><td>Typical buyer</td><td>First-time family buyer, investor</td><td>Established family, long-term owner</td></tr>"
   "</tbody></table></div>"),
  ("Payment plans and cash flow", P(
   "Townhouses for sale in Dubai with a payment plan follow the same logic as villas: check the total due before handover, the amount due in the next year, and any post-handover instalments. Lower prices make these plans easier to carry, which is part of the appeal.")),
  ("Supply risk in townhouse communities", P(
   "This is the risk most buyers underestimate. When a cluster of several hundred similar townhouses hands over in the same quarter, many owners list for rent at once. Rents and resale prices in that window can be softer than the brochure suggests.",
   "Before buying, find out how many comparable units hand over near yours in the same year, and whether your unit has anything that sets it apart — a corner plot, a park view, a larger layout.")),
 ],
 "faqs": [
  ("Are off plan townhouses in Dubai a good investment?", "They can be for investors seeking a lower entry into family communities with a multi-year horizon. Supply at handover is the main risk to test."),
  ("Which areas have off plan townhouses in Dubai?", "Communities we are analysing include The Valley, DAMAC Lagoons, Tilal Al Ghaf and Nad Al Sheba Gardens."),
  ("Do townhouses rent well in Dubai?", "Family demand for townhouses is generally steady, but rents depend heavily on how many similar units are available at the same time."),
  ("Townhouse or villa for a first investment?", "A townhouse lowers the entry price and running costs; a villa usually faces less resale competition. Match the choice to your budget and horizon."),
 ],
 "related": [("/off-plan-villas-dubai/", "Off plan villas in Dubai"), ("/off-plan-properties-dubai/", "Off plan properties in Dubai")],
},
{
 "lang": "en", "path": "/new-off-plan-projects-dubai/", "alt": "/ar/new-projects-dubai/",
 "crumb": "New off plan projects Dubai",
 "title": f"New Off Plan Projects in Dubai (Updated {C.UPDATED_MONTH_EN})",
 "meta": "New villa and townhouse launches in Dubai, reviewed monthly. What's launched, the stage, and who each project suits — without \"best project\" hype.",
 "h1": "New Off Plan Projects in Dubai, Reviewed for Investors",
 "intro": P(f"<b>Last updated: {C.UPDATED_MONTH_EN}.</b>",
            "New off plan projects in Dubai move fast, and launch day is designed to create urgency. This page is updated monthly with villa and townhouse projects, the key facts, and an honest view of who each suits.",
            "On the best off plan projects in Dubai: there isn't one. There's the one that fits your capital, horizon and risk."),
 "cats": ["offplan"], "cards_h2": "Projects on our watch list",
 "sections": [
  ("Latest launches this month", UL(
   "<b>Palm Jebel Ali (Nakheel).</b> In August 2026 Nakheel released 44 beachfront villas on Frond F from its Beach and Coral collections, and said phased handover of the first villas begins in late 2026 and runs through 2027. <a href='/projects/palm-jebel-ali-villas/'>See our Palm Jebel Ali villas assessment</a>.",
   "<b>The Oasis (Emaar).</b> Emaar continues to release sub-communities in its Dubailand waterfront community. <a href='/projects/the-oasis-emaar/'>See our The Oasis assessment</a>.") +
   P("Each new property launch in Dubai is added here once the key facts can be checked against the developer's own announcement.")),
  ("Is there a \"best\" off-plan project?", P(
   "Search results are full of lists of the best off plan projects in Dubai. They rarely say best for whom. A project that suits an investor looking for capital growth over seven years may be a poor choice for someone who needs rental income in two. That is why the projects on this site show who they may suit and who they may not, rather than a score.")),
  ("Launch pricing vs later phases", P(
   "Launch prices are often lower than later phases of the same community, which is the main argument for buying early. The trade-off is uncertainty: at launch, less of the community exists, and you carry more delivery and market risk for longer. Later phases cost more but show you more of what you are buying.")),
  ("How to assess a new launch in 30 minutes", "<ol class='steps'>"
   "<li><b>Developer record</b>Past delivery times and build quality in comparable projects.</li>"
   "<li><b>Location reality</b>What exists nearby today versus what is only planned.</li>"
   "<li><b>Cash-flow test</b>What you pay before the keys, and when.</li>"
   "<li><b>Supply check</b>Similar units handing over nearby in the same period.</li>"
   "<li><b>Exit test</b>Who buys this from you in five years, and why.</li></ol>"),
 ],
 "faqs": [
  ("How often is this page updated?", "Monthly. The date at the top shows the last review."),
  ("What are the best off plan projects in Dubai right now?", "The best project depends on your goals, horizon and budget. Use the investor assessment to see which projects match your profile."),
  ("Is it better to buy at launch?", "Launch pricing can be lower, but you take on more uncertainty for longer. It suits patient buyers with flexible cash flow."),
  ("How do I hear about new property launches in Dubai?", "Check this page monthly or message Ahmed with your criteria to be told when a matching project is released."),
 ],
 "related": [("/off-plan-properties-dubai/", "Off plan properties in Dubai"), ("/villa-projects-dubai/", "Villa projects in Dubai")],
},
{
 "lang": "en", "path": "/villa-projects-dubai/", "alt": "/ar/villas-for-sale-dubai/",
 "crumb": "Villa projects Dubai",
 "title": "Villa Projects in Dubai: New & Upcoming Villa Communities",
 "meta": "A guide to new and upcoming villa communities in Dubai — location, developer, stage and investor fit — to help you shortlist with a clear head.",
 "h1": "Villa Projects in Dubai: A Community-by-Community View",
 "intro": P("When you look at a villa project in Dubai, the community matters more than the villa. Two similar homes can perform very differently depending on infrastructure, schools, future supply and who lives there.",
            "This guide covers new villa communities and upcoming villa projects by area and stage, so you can shortlist by location and fit before looking at floor plans."),
 "cats": ["villa"], "cards_h2": "New villa communities",
 "sections": [
  ("How community maturity affects value", P(
   "A new villa community goes through stages: launch, construction, handover, and several years of settling in as schools, retail and landscaping arrive. Prices and rents usually behave differently at each stage.",
   "Early buyers take more uncertainty in exchange for a lower price. Buyers in a maturing community pay more but can see what they are getting. Neither is right or wrong. The question is which stage matches your horizon.")),
  ("Matching a community to your goal", UL(
   "<b>Central location and lower delivery risk:</b> Nad Al Sheba Gardens, Sobha Hartland.",
   "<b>Lagoon lifestyle and long-term growth:</b> Tilal Al Ghaf, The Oasis.",
   "<b>Lower entry into a branded community:</b> The Valley, DAMAC Lagoons.",
   "<b>Beachfront and scarcity, long horizon:</b> Palm Jebel Ali, Elysian Mansions.") +
   P("These groupings are a starting point, not a recommendation. Your capital, timeline and risk tolerance decide the shortlist.")),
  ("Upcoming villa projects in Dubai", P(
   "New villa launches are added to our monthly review once their key facts can be verified. See <a href='/new-off-plan-projects-dubai/'>new off plan projects in Dubai</a> for the latest.")),
 ],
 "faqs": [
  ("What are the new villa communities in Dubai?", "Communities we are analysing include The Valley, DAMAC Lagoons, Tilal Al Ghaf, The Oasis, Nad Al Sheba Gardens and Palm Jebel Ali."),
  ("Which Dubai villa community is best for families?", "It depends on commute, schools and budget. Central options include Nad Al Sheba Gardens and Sobha Hartland; lower-entry options include The Valley."),
  ("Are new villa projects in Dubai a good investment?", "They can be for buyers with a long horizon who understand the community's future supply. Short-term buyers carry more risk."),
 ],
 "related": [("/off-plan-villas-dubai/", "Off plan villas in Dubai"), ("/new-off-plan-projects-dubai/", "New off plan projects in Dubai")],
},
# ---------------------------------------------------------------- AR
{
 "lang": "ar", "path": "/ar/villas-for-sale-dubai/", "alt": "/villa-projects-dubai/",
 "crumb": "فلل للبيع في دبي",
 "title": "فلل للبيع في دبي — مشاريع جديدة وجاهزة حسب هدفك الاستثماري",
 "meta": "فلل للبيع في دبي في مجتمعات جديدة وجاهزة، مع خطط دفع مختلفة. قارن المشاريع واعرف أيها يناسب رأس مالك ومدة استثمارك قبل أن تقرر.",
 "h1": "فلل للبيع في دبي: اختر حسب هدفك، لا حسب الإعلان",
 "intro": P("تجد فلل للبيع في دبي في كل مستوى سعري تقريباً، في مجتمعات جاهزة وأخرى قيد الإنشاء. لكن الفيلا المناسبة لا تُحدد بالمساحة أو التشطيب فقط، بل بهدفك ورأس مالك والمدة التي تستطيع الانتظار فيها.",
            "في هذه الصفحة مجموعة مختارة من مشاريع الفلل، مع مرحلة كل مشروع ولمن يناسب ولمن لا يناسب. لا نعطي أي مشروع درجة، ولا نقول إن مشروعاً ما هو الأفضل."),
 "cats": ["villa"], "cards_h2": "مشاريع فلل ندرسها حالياً",
 "sections": [
  ("أسعار الفلل في دبي: ما الذي يحددها؟", P(
   "اسعار الفلل في دبي تحددها عوامل أكثر من المساحة: الموقع والمسافة إلى مناطق العمل، ومرحلة المجتمع (جديد أم ناضج)، واسم المطور، وحجم الأرض، والمعروض القادم في المنطقة نفسها.",
   "فيلا للبيع في دبي بسعر أقل في مجتمع بعيد قد تكون خياراً ممتازاً لعائلة تبحث عن مساحة، وخياراً ضعيفاً لمستثمر يحتاج إلى دخل إيجاري سريع. لذلك نبدأ دائماً بهدفك قبل السعر.")),
  ("فيلا جاهزة أم قيد الإنشاء؟", "<div class='tscroll'><table><thead><tr><th></th><th>جاهزة</th><th>قيد الإنشاء</th></tr></thead><tbody>"
   "<tr><td>السعر</td><td>أعلى عادة</td><td>أقل عادة عند الإطلاق</td></tr>"
   "<tr><td>الدفع</td><td>دفعة كاملة أو تمويل بنكي</td><td>خطة دفع من المطور على سنوات</td></tr>"
   "<tr><td>الدخل الإيجاري</td><td>فوري</td><td>بعد التسليم</td></tr>"
   "<tr><td>المخاطر</td><td>أقل في التسليم</td><td>تأخير التسليم وتغيّر السوق</td></tr>"
   "</tbody></table></div>"),
  ("كيف تختار المجتمع المناسب", UL(
   "<b>موقع مركزي ومخاطر تسليم أقل:</b> حدائق ند الشبا، شوبا هارتلاند.",
   "<b>بحيرات ونمو طويل المدى:</b> تلال الغاف، The Oasis.",
   "<b>مدخل أقل كلفة إلى مجتمع معروف:</b> The Valley، داماك لاجونز.",
   "<b>شاطئ وندرة على مدى طويل:</b> نخلة جبل علي، Elysian Mansions.") +
   P("هذه نقطة بداية وليست توصية. رأس مالك ومدتك ومستوى المخاطرة هي ما يحدد القائمة النهائية.")),
  ("مخاطر يجب أن تعرفها", UL(
   "تأخر التسليم في المشاريع قيد الإنشاء يؤخر الدخل وإمكانية البيع.",
   "تسليم عدد كبير من الفلل المتشابهة في وقت واحد يضغط على الإيجارات وأسعار إعادة البيع.",
   "رسوم الخدمات والصيانة للفلل أعلى مما يتوقعه كثير من المشترين.",
   "المرافق المعروضة في المخطط قد تصل بعد سنوات من استلامك.")),
 ],
 "faqs": [
  ("ما هي أفضل مناطق فلل للبيع في دبي؟", "لا توجد منطقة أفضل للجميع. المناطق المركزية أنسب لمن يريد قرباً ومخاطر أقل، والمجتمعات الجديدة الأبعد أنسب لمن يريد سعر دخول أقل ويستطيع الانتظار."),
  ("كم أسعار الفلل في دبي؟", "تختلف كثيراً حسب المنطقة والمطور والمرحلة. نؤكد السعر الحالي لكل مشروع عند الطلب لأن الأسعار تتغير مع كل إصدار."),
  ("هل يستطيع الأجنبي شراء فيلا للبيع في دبي؟", "نعم في مناطق التملك الحر، وتشمل معظم مجتمعات الفلل الجديدة. تأكد من وضع المشروع المحدد."),
  ("هل توجد بيوت للبيع في دبي بأسعار مناسبة للعائلات؟", "نعم، خاصة التاون هاوس في المجتمعات الجديدة. راجع صفحة التاون هاوس للبيع في دبي للمقارنة."),
  ("هل أشتري فيلا جاهزة أم على الخارطة؟", "الجاهزة تعطي يقيناً ودخلاً فورياً، وقيد الإنشاء تعطي سعر دخول أقل مع مخاطر تسليم. الاختيار يعتمد على مدتك وتدفقك النقدي."),
 ],
 "related": [("/ar/townhouses-for-sale-dubai/", "تاون هاوس للبيع في دبي"), ("/ar/villas-installments-dubai/", "فلل للبيع في دبي بالتقسيط"), ("/ar/buy-villa-dubai/", "تملك فيلا في دبي")],
},
{
 "lang": "ar", "path": "/ar/townhouses-for-sale-dubai/", "alt": "/off-plan-townhouses-dubai/",
 "crumb": "تاون هاوس للبيع في دبي",
 "title": "تاون هاوس للبيع في دبي — مشاريع وخطط دفع ولمن تناسب",
 "meta": "تاون هاوس للبيع في دبي في مجتمعات عائلية جديدة وجاهزة، بعضها بالتقسيط. قارن المراحل وخطط الدفع والمخاطر، واعرف ما يناسب ملفك الاستثماري.",
 "h1": "تاون هاوس للبيع في دبي",
 "intro": P("التاون هاوس للبيع في دبي مدخل عملي إلى المجتمعات العائلية: سعر أقل من الفيلا، وطلب مستمر من العائلات التي تريد مساحة أكبر من الشقة.",
            "في المقابل، تطرح بعض المجتمعات أعداداً كبيرة من الوحدات المتشابهة، وهذا يؤثر عند التأجير أو إعادة البيع. هنا نعرض المشاريع ونوضح كيف توازن بين هذه العوامل."),
 "cats": ["townhouse"], "cards_h2": "مشاريع تاون هاوس ندرسها",
 "sections": [
  ("لماذا يختار المستثمرون التاون هاوس؟", P(
   "التاون هاوس يقع بين الشقة والفيلا: حديقة ومساحة أكبر للمستأجر، مع سعر شراء ورسوم خدمات أقل من الفلل. لذلك هو الخطوة الأولى لكثير من المستثمرين في مجتمعات الفلل في دبي.")),
  ("تاون هاوس أم فيلا؟", "<div class='tscroll'><table><thead><tr><th></th><th>تاون هاوس</th><th>فيلا</th></tr></thead><tbody>"
   "<tr><td>سعر الدخول</td><td>أقل</td><td>أعلى</td></tr>"
   "<tr><td>المنافسة عند إعادة البيع</td><td>وحدات متشابهة كثيرة عادة</td><td>أقل عادة</td></tr>"
   "<tr><td>تكاليف التشغيل</td><td>أقل</td><td>أعلى</td></tr>"
   "<tr><td>المشتري المعتاد</td><td>عائلة تشتري لأول مرة، مستثمر</td><td>عائلة مستقرة، مالك طويل المدى</td></tr>"
   "</tbody></table></div>"),
  ("التقسيط وخطط الدفع", P(
   "إذا كنت تبحث عن تاون هاوس للبيع بالتقسيط في دبي، فالقاعدة نفسها تنطبق: اعرف المبلغ المطلوب قبل التسليم، والمبلغ المستحق خلال السنة القادمة، وأي أقساط بعد الاستلام. السعر الأقل يجعل خطة الدفع أسهل، وهذا جزء من جاذبية التاون هاوس دبي للبيع.")),
  ("المعروض القادم وأثره على الإيجار وإعادة البيع", P(
   "هذه أكثر مخاطرة يقلل المشترون من شأنها. عندما تُسلَّم مجموعة فيها مئات الوحدات المتشابهة في ربع واحد، يعرض كثير من الملاك وحداتهم للإيجار في الوقت نفسه، فتضعف الإيجارات والأسعار مؤقتاً.",
   "قبل الشراء، اعرف عدد الوحدات المشابهة التي تُسلَّم قرب وحدتك في السنة نفسها، وما الذي يميز وحدتك: زاوية، أو إطلالة على حديقة، أو مساحة أكبر.")),
 ],
 "faqs": [
  ("هل التاون هاوس في دبي استثمار جيد؟", "قد يكون كذلك لمن يريد مدخلاً أقل كلفة إلى المجتمعات العائلية ويخطط لعدة سنوات. المعروض عند التسليم هو المخاطرة الأهم."),
  ("أين أجد تاون هاوس بالتقسيط في دبي؟", "من المجتمعات التي ندرسها: The Valley وداماك لاجونز وتلال الغاف وحدائق ند الشبا."),
  ("هل التاون هاوس يؤجَّر بسهولة في دبي؟", "الطلب العائلي عليه مستقر عموماً، لكن الإيجار يعتمد كثيراً على عدد الوحدات المشابهة المعروضة في الوقت نفسه."),
  ("تاون هاوس أم فيلا كأول استثمار؟", "التاون هاوس يخفض سعر الدخول والتكاليف، والفيلا تواجه منافسة أقل عند إعادة البيع عادة. اختر حسب ميزانيتك ومدتك."),
 ],
 "related": [("/ar/villas-for-sale-dubai/", "فلل للبيع في دبي"), ("/ar/villas-installments-dubai/", "فلل للبيع في دبي بالتقسيط")],
},
{
 "lang": "ar", "path": "/ar/villas-installments-dubai/", "alt": "/off-plan-properties-dubai/",
 "crumb": "فلل للبيع في دبي بالتقسيط",
 "title": "فلل للبيع في دبي بالتقسيط — خطط الدفع ومتى تناسبك",
 "meta": "فلل للبيع في دبي بالتقسيط عبر خطط دفع من المطورين. اعرف كم تدفع قبل الاستلام، وما المخاطر، وأي مشروع يتوافق مع دخلك ومدة استثمارك.",
 "h1": "فلل للبيع في دبي بالتقسيط: خطة الدفع جزء من القرار",
 "intro": P("معظم الفلل للبيع في دبي بالتقسيط هي فلل قيد الإنشاء تُباع بخطط دفع من المطور: دفعة أولى، ثم أقساط خلال البناء، وأحياناً أقساط بعد الاستلام.",
            "هذه المرونة مفيدة، لكنها تعني أيضاً التزاماً مالياً لسنوات. قبل أن تختار مشروعاً، من المهم أن تعرف كم ستدفع قبل استلام المفتاح، وهل يتوافق ذلك مع دخلك وخططك."),
 "cats": ["offplan"], "cards_h2": "مشاريع فلل بخطط دفع ندرسها",
 "sections": [
  ("كيف تعمل خطط الدفع في دبي", P(
   "يصف المطورون الخطط بنسب مثل 60/40 أو 70/30، وتعني الجزء المدفوع قبل التسليم والجزء المدفوع بعده. خطة فيها جزء كبير بعد التسليم تخفف الضغط أثناء البناء، لكنها تمد التزامك لسنوات بعد الاستلام.",
   "تُسمى هذه العقارات أيضاً عقارات على الخارطة، والفكرة واحدة: تشتري اليوم بسعر محدد وتدفع على مراحل مرتبطة بالبناء.")),
  ("التقسيط قبل التسليم وبعده", P(
   "عند المقارنة بين فلل بالتقسيط في دبي، اكتب ثلاثة أرقام لكل مشروع: المبلغ المستحق خلال 12 شهراً، والمبلغ الإجمالي قبل التسليم، والمتبقي بعده. هذه الأرقام الثلاثة تخبرك أكثر من النسبة المكتوبة في الكتيب.",
   "وخصص ميزانية لتكاليف خارج الخطة: رسوم التسجيل في دائرة الأراضي والأملاك، ورسوم الخدمات بعد التسليم، والتأثيث إن كنت ستؤجر. تأكد من الرسوم الحالية عند الشراء لأنها قد تتغير.")),
  ("هل التقسيط مناسب لك؟", P("التقسيط يناسبك غالباً إذا:") + UL(
   "كانت مدة استثمارك خمس سنوات أو أكثر",
   "كان جدول الدفع أقل من قدرتك بهامش واضح",
   "كان هدفك نمو رأس المال لا الدخل الفوري") +
   P("ولا يناسبك إذا كنت تحتاج إلى دخل إيجاري قريب، أو قد تحتاج إلى المال خلال سنتين أو ثلاث.")),
  ("مخاطر يجب حسابها", UL(
   "<b>تأخر التسليم:</b> يؤخر الدخل وإمكانية البيع، بينما تستمر الأقساط.",
   "<b>تغيّر دخلك:</b> الالتزام يمتد لسنوات، فاحسب هامش أمان.",
   "<b>المعروض عند التسليم:</b> وحدات كثيرة متشابهة تعني منافسة أكبر.",
   "<b>البيع قبل التسليم:</b> يخضع لشروط المطور ولحجم ما دفعته.")),
 ],
 "faqs": [
  ("كيف أشتري فيلا للبيع في دبي بالتقسيط؟", "تختار مشروعاً قيد الإنشاء، وتدفع دفعة حجز، ثم أقساطاً مرتبطة بمراحل البناء حسب خطة المطور، مع تسجيل العقد لدى دائرة الأراضي والأملاك."),
  ("هل يمكن شراء فلل للبيع بالتقسيط في دبي بدون بنك؟", "نعم، خطط الدفع من المطور لا تتطلب تمويلاً بنكياً في الغالب، لأنك تدفع للمطور مباشرة على مراحل."),
  ("كم الدفعة الأولى للفيلا بالتقسيط في دبي؟", "تختلف حسب المشروع والإصدار. نؤكد التفاصيل الحالية لكل مشروع عند الطلب."),
  ("هل يوجد تقسيط بعد الاستلام؟", "بعض المشاريع تقدم أقساطاً بعد التسليم. هذا يخفف الضغط أثناء البناء لكنه يمد التزامك."),
 ],
 "related": [("/ar/villas-for-sale-dubai/", "فلل للبيع في دبي"), ("/ar/townhouses-for-sale-dubai/", "تاون هاوس للبيع في دبي"), ("/ar/new-projects-dubai/", "مشاريع عقارية جديدة في دبي")],
},
{
 "lang": "ar", "path": "/ar/new-projects-dubai/", "alt": "/new-off-plan-projects-dubai/",
 "crumb": "مشاريع عقارية جديدة في دبي",
 "title": f"مشاريع عقارية جديدة في دبي — فلل وتاون هاوس (تحديث {C.UPDATED_MONTH_AR})",
 "meta": "أحدث مشاريع الفلل والتاون هاوس في دبي، بمراجعة شهرية: المطور، والموقع، والمرحلة، والتسليم، ولمن يناسب كل مشروع.",
 "h1": "مشاريع عقارية جديدة في دبي بعين المستثمر",
 "intro": P(f"<b>آخر تحديث: {C.UPDATED_MONTH_AR}.</b>",
            "تُطرح مشاريع عقارية جديدة في دبي باستمرار، ويوم الإطلاق مصمم عادة ليخلق إحساساً بالاستعجال. نراجع هذه الصفحة شهرياً ونعرض مشاريع الفلل والتاون هاوس، مع الحقائق الأساسية ورأي واضح في نوع المستثمر الذي يناسبه كل مشروع.",
            "الهدف أن تقرر بهدوء، لا تحت ضغط الإطلاق."),
 "cats": ["offplan"], "cards_h2": "مشاريع نتابعها",
 "sections": [
  ("أحدث المشاريع هذا الشهر", UL(
   "<b>نخلة جبل علي (نخيل):</b> في أغسطس 2026 طرحت نخيل 44 فيلا شاطئية على السعفة F، وأعلنت أن تسليم أولى الفلل يبدأ على مراحل من أواخر 2026 حتى 2027. <a href='/ar/projects/palm-jebel-ali-villas/'>اقرأ تقييمنا لفلل نخلة جبل علي</a>.",
   "<b>The Oasis (إعمار):</b> تواصل إعمار طرح مجتمعات فرعية في مشروعها على الواجهة المائية في دبي لاند. <a href='/ar/projects/the-oasis-emaar/'>اقرأ تقييمنا لـ The Oasis</a>.") +
   P("نضيف أي مشاريع فلل جديدة في دبي هنا بعد التحقق من الحقائق الأساسية من إعلان المطور نفسه.")),
  ("سعر الإطلاق أم المراحل اللاحقة؟", P(
   "سعر الإطلاق أقل غالباً من المراحل اللاحقة في المجتمع نفسه، وهذه أهم حجة للشراء المبكر. المقابل هو عدم اليقين: عند الإطلاق يكون الموجود من المجتمع أقل، وتتحمل مخاطر التسليم والسوق لفترة أطول.")),
  ("كيف تقيّم مشروعاً جديداً قبل الحجز", "<ol class='steps'>"
   "<li><b>سجل المطور</b>مدة التسليم وجودة البناء في مشاريع مشابهة.</li>"
   "<li><b>حقيقة الموقع</b>ما الموجود اليوم وما المخطط فقط.</li>"
   "<li><b>اختبار التدفق النقدي</b>كم تدفع قبل المفتاح ومتى.</li>"
   "<li><b>فحص المعروض</b>وحدات مشابهة تُسلَّم قربك في الفترة نفسها.</li>"
   "<li><b>اختبار الخروج</b>من سيشتري منك بعد خمس سنوات، ولماذا.</li></ol>"),
  ("لماذا لا نقول \"أفضل مشروع\"", P(
   "المشروع الذي يناسب مستثمراً يبحث عن نمو رأس المال خلال سبع سنوات قد لا يناسب من يحتاج إلى دخل خلال سنتين. لذلك نعرض لمن يناسب كل مشروع ولمن لا يناسب، بدلاً من الترتيب.")),
 ],
 "faqs": [
  ("كم مرة تُحدَّث هذه الصفحة؟", "شهرياً، والتاريخ في أعلى الصفحة يوضح آخر مراجعة."),
  ("ما أفضل مشاريع عقارية جديدة في دبي الآن؟", "الأفضل يعتمد على هدفك ومدتك وميزانيتك. التقييم الاستثماري يطابق المشاريع مع ملفك."),
  ("هل الشراء عند الإطلاق أفضل؟", "قد يكون السعر أقل، لكنك تتحمل عدم يقين أكبر لفترة أطول. يناسب المشتري الصبور ذا التدفق النقدي المرن."),
  ("ما معنى عقارات على الخارطة في دبي؟", "عقارات تُباع قبل اكتمال البناء بخطة دفع على مراحل، وتُسمى أيضاً مشاريع قيد الإنشاء."),
 ],
 "related": [("/ar/villas-installments-dubai/", "فلل للبيع في دبي بالتقسيط"), ("/ar/villas-for-sale-dubai/", "فلل للبيع في دبي")],
},
{
 "lang": "ar", "path": "/ar/buy-villa-dubai/", "alt": "/off-plan-villas-dubai/",
 "crumb": "تملك فيلا في دبي",
 "title": "تملك فيلا في دبي: دليل الشراء خطوة بخطوة قبل أن تختار المشروع",
 "meta": "كل ما تحتاج معرفته قبل شراء فيلا في دبي: التملك الحر، والجاهز مقابل قيد الإنشاء، وخطط الدفع، والتكاليف، وكيف تختار المشروع المناسب لهدفك.",
 "h1": "تملك فيلا في دبي: ابدأ بالقرار قبل المشروع",
 "intro": P("تملك فيلا في دبي قرار كبير، ويبدأ عادة من السؤال الخطأ: أي مشروع أختار؟ السؤال الأول هو: هل الشراء الآن يخدم هدفك؟",
            "في هذا الدليل نشرح خطوات شراء فيلا في دبي، والتكاليف الإضافية، والفرق بين الفيلا الجاهزة والفيلا قيد الإنشاء، ثم نساعدك على تحديد المشروع المناسب."),
 "cats": ["villa"], "cards_h2": "مشاريع فلل ندرسها",
 "sections": [
  ("هل الشراء مناسب لك الآن؟", P(
   "أحياناً يحقق المال عائداً أفضل داخل عملك الحالي، أو يحتاج إلى البقاء سائلاً لخطط قريبة. إذا كنت ستحتاج إلى المال خلال سنتين، فمشروع يُسلَّم بعد أربع سنوات لا يناسبك مهما كانت مزاياه. نقول ذلك بوضوح حين يكون صحيحاً.")),
  ("التملك الحر في دبي", P(
   "معظم مجتمعات الفلل الجديدة تقع في مناطق التملك الحر، حيث يستطيع غير المواطنين تملك العقار بالكامل وتسجيله لدى دائرة الأراضي والأملاك. قواعد التملك وأهلية الإقامة المرتبطة بقيمة العقار قد تتغير، فتأكد من الوضع الحالي لحالتك.")),
  ("خطوات شراء فيلا", "<ol class='steps'>"
   "<li><b>تحديد الهدف</b>سكن، أو نمو رأس المال، أو دخل، أو تنويع.</li>"
   "<li><b>حد التدفق النقدي</b>أقصى ما تستطيع دفعه دون ضغط.</li>"
   "<li><b>قائمة مختصرة</b>مجتمعات ومشاريع تناسب الهدف والحد.</li>"
   "<li><b>مقارنة بمعايير ثابتة</b>المطور والموقع والخطة والتسليم والمعروض والمخاطر.</li>"
   "<li><b>التحقق والتوثيق</b>السعر والخطة والمواعيد مكتوبة قبل الحجز.</li>"
   "<li><b>التسجيل</b>تسجيل العقد لدى دائرة الأراضي والأملاك.</li></ol>"),
  ("التكاليف التي تتجاوز سعر الفيلا", UL(
   "رسوم التسجيل لدى دائرة الأراضي والأملاك.",
   "رسوم الخدمات السنوية بعد التسليم.",
   "عمولة الوسيط في الفلل الجاهزة وإعادة البيع.",
   "التأثيث والصيانة، وهي أعلى في الفلل منها في الشقق.") +
   P("تُراجع الرسوم والإجراءات وفق قواعد دائرة الأراضي والأملاك الحالية وقت الشراء.")),
  ("فلل جاهزة أم قيد الإنشاء؟", P(
   "فلل جاهزة للبيع في دبي تعطيك يقيناً ودخلاً فورياً لكن بسعر أعلى غالباً. الفلل قيد الإنشاء تعطي سعر دخول أقل وخطة دفع، مقابل مخاطر التسليم وتغيّر السوق. اختيارك يعتمد على مدتك وتدفقك النقدي.")),
 ],
 "faqs": [
  ("هل يستطيع الأجنبي تملك فيلا في دبي؟", "نعم في مناطق التملك الحر، وتشمل معظم مجتمعات الفلل الجديدة."),
  ("ما خطوات شراء فيلا في دبي؟", "تحديد الهدف، ثم حد التدفق النقدي، ثم قائمة مختصرة، ثم مقارنة، ثم التحقق من التفاصيل كتابياً، ثم التسجيل لدى دائرة الأراضي والأملاك."),
  ("ما التكاليف الإضافية عند شراء فيلا في دبي؟", "رسوم التسجيل، ورسوم الخدمات، والعمولة في الجاهز وإعادة البيع، والتأثيث والصيانة."),
  ("أين أجد فلل جاهزة للبيع في دبي؟", "من الخيارات الجاهزة أو شبه الجاهزة التي ندرسها فلل شوبا هارتلاند والمراحل المسلّمة في بعض المجتمعات الجديدة."),
 ],
 "related": [("/ar/villas-for-sale-dubai/", "فلل للبيع في دبي"), ("/ar/villas-installments-dubai/", "فلل للبيع في دبي بالتقسيط")],
},
]
