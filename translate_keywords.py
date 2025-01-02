from googletrans import Translator
import pandas as pd

# Funzione per tradurre le parole chiave
def translate_keywords(keywords, target_languages):
    translator = Translator()
    translations = {lang: [] for lang in target_languages}
    for keyword in keywords:
        for lang in target_languages:
            try:
                translated = translator.translate(keyword, dest=lang).text
                translations[lang].append(translated)
            except Exception as e:
                translations[lang].append(f"Error: {e}")
    return translations

# Lingue di destinazione
languages = ['it', 'fr', 'es', 'ja', 'hi', 'zh-cn']

# Parole chiave di esempio
keywords_to_translate = ["AI tools", "machine learning", "solar panels"]

# Traduzione delle parole chiave
translated_keywords = translate_keywords(keywords_to_translate, languages)

# Salva i risultati in un file CSV
df_translations = pd.DataFrame(translated_keywords)
df_translations.to_csv("translated_keywords.csv", index=False)

print("Parole chiave tradotte salvate in 'translated_keywords.csv'")
