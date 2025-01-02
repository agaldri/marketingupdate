from pytrends.request import TrendReq
import pandas as pd

# Configura pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Funzione per ottenere i dati di Google Trends
def get_trends_data(keywords, timeframe='today 12-m', geo=''):
    trends_data = {}
    for keyword in keywords:
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
        data = pytrends.interest_over_time()
        if not data.empty:
            trends_data[keyword] = data[keyword]
    return pd.DataFrame(trends_data)

# Parole chiave di esempio
markets_keywords = {
    "Artificial Intelligence": ["AI tools", "machine learning", "neural networks"],
    "E-commerce": ["online shopping", "dropshipping", "best deals"],
    "Renewable Energy": ["solar panels", "wind turbines", "green energy"]
}

# Raccolta dati
results = {}
for market, keywords in markets_keywords.items():
    print(f"Fetching trends for {market}...")
    results[market] = get_trends_data(keywords)

# Salvataggio dei dati
for market, data in results.items():
    filename = f"{market.replace(' ', '_').lower()}_trends.csv"
    data.to_csv(filename)
    print(f"Saved data for {market} to {filename}")

print("Raccolta completata!")
