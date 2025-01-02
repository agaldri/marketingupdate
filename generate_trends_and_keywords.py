from pytrends.request import TrendReq
from googletrans import Translator
import pandas as pd
import itertools

# Configurazione pytrends e Google Translate
pytrends = TrendReq(hl='en-US', tz=360)
translator = Translator()

# Lingue di destinazione
languages = ['en', 'it', 'fr', 'es', 'ja', 'hi', 'zh-cn']

# Mercati e parole chiave principali
markets_keywords = {
    "Artificial Intelligence": ["AI tools", "machine learning", "neural networks"],
    "Automation": ["workflow automation", "business automation", "robotics"],
    "Cloud Computing": ["cloud storage", "AWS", "Google Cloud"],
    "Health and Wellness": ["yoga classes", "meditation", "self-care"],
    "Fitness and Sports": ["workout plans", "home fitness", "sports gear"],
    "Nutrition and Supplements": ["protein powder", "vitamin D", "healthy diet"],
    "Online Education": ["e-learning platforms", "online courses", "study online"],
    "Cybersecurity": ["VPN services", "password manager", "cyber protection"],
    "Virtual Reality (VR)": ["VR headset", "augmented reality", "VR games"],
    "E-commerce": ["online shopping", "dropshipping", "best deals"],
    "Dropshipping": ["dropshipping products", "best suppliers", "dropshipping niches"],
    "Renewable Energy": ["solar panels", "wind turbines", "green energy"],
    "Electric Vehicles": ["electric cars", "EV chargers", "Tesla"],
    "Mobile Apps": ["best apps", "productivity apps", "mobile games"],
    "Fintech": ["digital wallets", "online payments", "investment apps"],
    "Digital Marketing": ["SEO tools", "social media ads", "content marketing"],
    "Personal Finance": ["budgeting apps", "investing tips", "financial planning"],
    "Travel and Tourism": ["cheap flights", "holiday packages", "travel blogs"],
    "Tech Gadgets": ["smartphones", "smartwatches", "latest gadgets"],
    "Smart Home": ["smart home devices", "Alexa", "home automation"],
    "Streaming Services": ["Netflix", "streaming apps", "best movies"],
    "Gaming": ["video games", "eSports", "gaming consoles"],
    "Graphic Design": ["graphic design software", "Adobe Photoshop", "creative tools"],
    "Eco-friendly Products": ["eco-friendly packaging", "reusable products", "sustainable brands"],
    "Handmade Goods": ["handmade jewelry", "DIY crafts", "Etsy products"],
    "SaaS": ["SaaS tools", "business software", "cloud apps"],
    "Skin Care": ["natural skincare", "anti-aging cream", "skin routine"],
    "Online Consulting": ["consulting services", "freelance consulting", "business consulting"],
    "Creative Tools": ["photo editing tools", "video editing software", "creative apps"]
}

# Parole aggiuntive per generare variazioni
additional_terms = ["tools", "apps", "software", "solutions", "services", "platforms"]

# Funzione per generare combinazioni di keyword
def generate_keywords(base_terms, additional_terms, max_keywords=500):
    combinations = list(itertools.product(base_terms, additional_terms))
    keywords = [f"{base} {additional}" for base, additional in combinations]
    return keywords[:max_keywords]

# Funzione per raccogliere dati da Google Trends
def get_trends_data(keywords, timeframe='today 12-m', geo=''):
    trends_data = {}
    for keyword in keywords:
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
        data = pytrends.interest_over_time()
        if not data.empty:
            trends_data[keyword] = data[keyword]
    return pd.DataFrame(trends_data)

# Funzione per tradurre le keyword
def translate_keywords(keywords, target_languages):
    translations = {lang: [] for lang in target_languages}
    for keyword in keywords:
        for lang in target_languages:
            try:
                translated = translator.translate(keyword, dest=lang).text
                translations[lang].append(translated)
            except Exception as e:
                translations[lang].append(f"Error: {e}")
    return translations

# Elaborazione dei mercati
for market, base_terms in markets_keywords.items():
    print(f"Processing market: {market}...")
    # Genera keyword
    keywords = generate_keywords(base_terms, additional_terms, max_keywords=500)
    print(f"Generated {len(keywords)} keywords for {market}.")

    # Ottieni dati di tendenza da Google Trends
    try:
        trends_data = get_trends_data(keywords, timeframe='today 12-m', geo='IT')  # Cambia 'IT' per una regione diversa
        trends_data.to_csv(f"{market.replace(' ', '_').lower()}_trends.csv")
        print(f"Saved trends for {market} in {market.replace(' ', '_').lower()}_trends.csv")
    except Exception as e:
        print(f"Error fetching trends for {market}: {e}")

    # Traduci le keyword
    translated_keywords = translate_keywords(keywords, languages)
    df_translations = pd.DataFrame(translated_keywords)
    df_translations.to_csv(f"{market.replace(' ', '_').lower()}_translated_keywords.csv", index=False)
    print(f"Saved translated keywords for {market} in {market.replace(' ', '_').lower()}_translated_keywords.csv")

print("Process completed!")
