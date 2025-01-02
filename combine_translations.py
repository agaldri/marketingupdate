
import pandas as pd
import glob

# Legge tutti i file delle keyword tradotte
translation_files = glob.glob("*_translated_keywords.csv")
all_translations = []

# Combina i file
for file in translation_files:
    print(f"Processing translations in {file}...")
    data = pd.read_csv(file)
    data["Market"] = file.replace("_translated_keywords.csv", "").replace("_", " ").title()
    all_translations.append(data)

# Unisci tutti i dati
df_all_translations = pd.concat(all_translations, ignore_index=True)
df_all_translations.to_csv("all_translated_keywords.csv", index=False)
print("Saved all translated keywords in 'all_translated_keywords.csv'.")
