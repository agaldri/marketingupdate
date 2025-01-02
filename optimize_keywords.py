
import pandas as pd

# Legge i file principali
trends = pd.read_csv("top_trending_keywords.csv")
translations = pd.read_csv("all_translated_keywords.csv")

# Merge tra tendenze e traduzioni
merged = trends.merge(translations, left_on="Top Keyword", right_on="en", how="inner")

# Aggiunge una metrica di priorità (può essere personalizzata)
merged["Priority Score"] = merged["Average Volume"] * 100  # Moltiplicatore per enfatizzare

# Ordina per priorità
sorted_keywords = merged.sort_values(by="Priority Score", ascending=False)
sorted_keywords.to_csv("priority_keywords.csv", index=False)
print("Saved priority keywords in 'priority_keywords.csv'.")

# Mostra i risultati principali
print(sorted_keywords.head(10))
