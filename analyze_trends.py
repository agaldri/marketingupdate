
import pandas as pd
import glob

# Legge tutti i file delle tendenze
trend_files = glob.glob("*_trends.csv")  # Assicurati che i file abbiano questa estensione
top_keywords = []

# Analizza ciascun file
for file in trend_files:
    print(f"Analyzing trends in {file}...")
    data = pd.read_csv(file)
    # Identifica le keyword con il volume medio più alto
    mean_values = data.mean().sort_values(ascending=False)
    top_keywords.append({
        "Market": file.replace("_trends.csv", "").replace("_", " ").title(),
        "Top Keyword": mean_values.idxmax(),
        "Average Volume": mean_values.max()
    })

# Risultati in un DataFrame
df_top_keywords = pd.DataFrame(top_keywords)
df_top_keywords.to_csv("top_trending_keywords.csv", index=False)
print("Saved top trending keywords in 'top_trending_keywords.csv'.")

# Mostra i risultati principali
print(df_top_keywords)
