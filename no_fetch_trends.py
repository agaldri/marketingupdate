
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Configurazione Pytrends
def fetch_trends(keywords, timeframe="today 12-m", geo=""):
    """
    Raccoglie dati da Google Trends per un elenco di keyword.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    trends_data = {}
    
    for keyword in keywords:
        try:
            pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
            data = pytrends.interest_over_time()
            if not data.empty:
                trends_data[keyword] = data[keyword]
        except Exception as e:
            print(f"Errore con la keyword '{keyword}': {e}")
    
    return pd.DataFrame(trends_data)

# Elenco di Keyword di esempio
keywords = ["intelligenza artificiale", "energie rinnovabili", "e-commerce", "fitness"]

# Raccolta Dati
print("Raccolta dati in corso...")
data = fetch_trends(keywords)

# Visualizzazione dei Dati
if not data.empty:
    print("Dati raccolti:")
    print(data.head())
    
    # Salva i dati in un file CSV
    data.to_csv("trends_data.csv")
    print("Dati salvati in 'trends_data.csv'")
    
    # Grafico delle keyword
    data.plot(figsize=(12, 6), title="Trend delle Keyword")
    plt.xlabel("Data")
    plt.ylabel("Volume di Ricerca")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()
else:
    print("Nessun dato disponibile.")
