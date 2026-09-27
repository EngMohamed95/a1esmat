# ============================================================
#  Images — files live in static/img/<key>-900.webp and <key>-1920.webp
#  Source: Unsplash (free licence). Generic mood images, NOT official
#  project photos — project pages label them "Illustrative image".
#  To use an official render: drop <key>-900.webp / -1920.webp into
#  static/img, add it below, and point the project slug at it.
# ============================================================

IMAGES = {
    "skyline-night":    {"en": "Downtown Dubai skyline at night", "ar": "أفق وسط دبي ليلاً", "credit": "Ahmed Galal"},
    "skyline-sunset":   {"en": "Dubai skyline at sunset across the water", "ar": "أفق دبي عند الغروب", "credit": "James Watson"},
    "skyline-storm":    {"en": "Burj Khalifa and Downtown Dubai under dramatic clouds", "ar": "برج خليفة ووسط دبي تحت سحب كثيفة", "credit": "Ahmed Aldaie"},
    "palm-aerial":      {"en": "Aerial view of palm island fronds lined with villas", "ar": "منظر جوي لسعفات جزيرة النخلة والفلل", "credit": "Ahmad Ossayli"},
    "palm-wide":        {"en": "Aerial view over a Dubai palm island", "ar": "منظر جوي لجزيرة نخلة في دبي", "credit": "Thomas Haas"},
    "interior-dark":    {"en": "Luxury living room with warm lighting", "ar": "غرفة معيشة فاخرة بإضاءة دافئة", "credit": "Aalo Lens"},
    "villa-palms":      {"en": "Modern luxury villa among palm trees", "ar": "فيلا فاخرة حديثة بين أشجار النخيل", "credit": "Tim Schmidbauer"},
    "villa-pool-wide":  {"en": "Contemporary villa with a long swimming pool", "ar": "فيلا عصرية بمسبح ممتد", "credit": "Salman Saqib"},
    "villa-lawn":       {"en": "Modern villa with landscaped garden", "ar": "فيلا حديثة بحديقة منسقة", "credit": "Salman Saqib"},
    "villa-white-pool": {"en": "White villa with private pool", "ar": "فيلا بيضاء بمسبح خاص", "credit": "John Fornander"},
    "villa-pergola":    {"en": "Modern family villa with pergola", "ar": "فيلا عائلية حديثة بمظلة خشبية", "credit": "Salman Saqib"},
    "villa-tropical":   {"en": "Villa with pitched roofs and palm trees", "ar": "فيلا بأسقف مائلة وأشجار نخيل", "credit": "Jusuf Bachtiar"},
    "townhouses-row":   {"en": "Row of contemporary townhouses with gardens", "ar": "صف من التاون هاوس العصرية بحدائق", "credit": "Joan Tran"},
    # Ahmed's own photos (from a1esmat.com) — widths differ from the Unsplash set
    "ahmed-esmat-dubai-advisor": {"en": "Ahmed Esmat, Dubai real estate and business advisor", "ar": "أحمد عصمت، مستشار عقاري واستثماري في دبي",
                                  "credit": None, "w": (600, 960), "h": 1},
    "ahmed-esmat-portrait": {"en": "Ahmed Esmat in Dubai", "ar": "أحمد عصمت في دبي", "credit": None, "w": (600, 1200), "h": 1},
}

# Brands Ahmed has worked with — static/img/clients/<slug>.webp
# tone: "light" = logo sits on a white tile, "dark" = light/white logo on a dark tile
CLIENTS = [
    ("hallmark-real-estate", "Hallmark Real Estate", "light"), ("arjan-real-estate-broker", "Arjan Real Estate Broker", "light"),
    ("rh-homes-real-estate", "RH Homes Real Estate", "light"), ("mivida-property", "Mivida Property", "dark"),
    ("sterling-homes-international", "Sterling Homes International", "dark"), ("mohamed-tharwat", "Mohamed Tharwat Real Estate", "dark"),
    ("toyota", "Toyota", "light"), ("kelloggs", "Kellogg's", "light"), ("tcl", "TCL", "light"),
    ("caribou-coffee", "Caribou Coffee", "light"), ("copthorne-lakeview", "Copthorne Lakeview Dubai", "light"),
    ("city-hospital", "City Hospital", "light"), ("mounjaro", "Mounjaro", "light"), ("pepes-piri-piri", "Pepe's Piri Piri", "light"),
    ("fix-dessert-chocolatier", "Fix Dessert Chocolatier", "light"), ("candivore", "Candivore", "light"),
    ("arabian-oud", "Arabian Oud", "light"), ("jaimie-jacobs", "Jaimie Jacobs", "light"), ("hazza-alghawi", "Hazza Alghawi", "dark"),
    ("power-star-marketing", "Power Star Marketing", "dark"), ("rento-car-rental", "RENTO Car Rental Dubai", "dark"),
    ("oro-car-rental", "ORO Car Rental", "dark"), ("illbe", "illbe", "light"), ("al-khan-restaurant", "Al Khan Restaurant", "dark"),
    ("koshary-el-tahrir", "Koshary El Tahrir", "light"), ("el-sayed-hanafy", "El Sayed Hanafy", "light"),
    ("el-baghl", "El Baghl Restaurants", "light"), ("al-malki", "Al Malki", "light"),
]

PROJECT_IMG = {
    "the-valley-emaar": "townhouses-row",
    "damac-lagoons": "villa-pool-wide",
    "tilal-al-ghaf": "villa-lawn",
    "elysian-mansions-tilal-al-ghaf": "villa-palms",
    "palm-jebel-ali-villas": "palm-aerial",
    "the-oasis-emaar": "villa-white-pool",
    "nad-al-sheba-gardens": "villa-pergola",
    "sobha-hartland-villas": "villa-tropical",
}

# page path -> hero image
PAGE_IMG = {
    "/off-plan-properties-dubai/": "villa-lawn", "/ar/villas-installments-dubai/": "villa-lawn",
    "/off-plan-villas-dubai/": "villa-white-pool", "/ar/buy-villa-dubai/": "villa-white-pool",
    "/off-plan-townhouses-dubai/": "townhouses-row", "/ar/townhouses-for-sale-dubai/": "townhouses-row",
    "/new-off-plan-projects-dubai/": "skyline-storm", "/ar/new-projects-dubai/": "skyline-storm",
    "/villa-projects-dubai/": "villa-palms", "/ar/villas-for-sale-dubai/": "villa-palms",
    "/projects/": "palm-wide", "/ar/projects/": "palm-wide",
    "/investor-assessment/": "interior-dark", "/ar/investor-assessment/": "interior-dark",
    "/book/": "skyline-sunset", "/ar/book/": "skyline-sunset",
    "/disclaimer/": "skyline-storm", "/ar/disclaimer/": "skyline-storm",
}

# home "opportunities" tiles, in order
OPP_IMG = ["villa-palms", "townhouses-row", "interior-dark", "villa-lawn"]
