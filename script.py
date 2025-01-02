from pytrends.request import TrendReq
from googletrans import Translator
import pandas as pd

def fetch_trends(keywords):
    pytrends = TrendReq(hl='en-US', tz=360)
    trends_data = {}
    for keyword in keywords:
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
        data = pytrends.interest_over_time()
        if not data.empty:
            trends_data[keyword] = data[keyword]
    return pd.DataFrame(trends_data)

def translate_keywords(keywords, languages):
    translator = Translator()
    translations = {lang: [] for lang in languages}
    for keyword in keywords:
        for lang in languages:
            try:
                translations[lang].append(translator.translate(keyword, dest=lang).text)
            except Exception as e:
                translations[lang].append(f"Error: {e}")
    return translations

# Configurazione iniziale
keywords = ["artificial intelligence", "renewable energy", "e-commerce"]
languages = ['it', 'fr', 'es', 'ja', 'hi', 'zh-cn']

# Fetch trends
print("Fetching trends data...")
trends = fetch_trends(keywords)

# Translate keywords
print("Translating keywords...")
translations = translate_keywords(keywords, languages)

# Salva i risultati
trends.to_csv("trends_data.csv", index=False)
pd.DataFrame(translations).to_csv("translated_keywords.csv", index=False)

print("Dati salvati: 'trends_data.csv' e 'translated_keywords.csv'")
