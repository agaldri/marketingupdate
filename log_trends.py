
from pytrends.request import TrendReq
import pandas as pd
import logging
from datetime import datetime

# Configurazione Logging
LOG_FILE = "trends_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Funzione per Raccolta Dati Google Trends
def fetch_trends(keywords):
    pytrends = TrendReq(hl='en-US', tz=360)
    trends_data = {}
    for keyword in keywords:
        try:
            pytrends.build_payload([keyword], cat=0, timeframe="today 12-m", geo='', gprop='')
            data = pytrends.interest_over_time()
            if not data.empty:
                trends_data[keyword] = data[keyword]
        except Exception as e:
            logging.error(f"Errore con la keyword '{keyword}': {e}")
    return pd.DataFrame(trends_data)

# Funzione per Aggiungere Notifica al Log
def log_notification(message):
    logging.info(message)
    print(message)  # Opzionale: Visualizza il messaggio anche in console.

# Esecuzione dello Script
if __name__ == "__main__":
    keywords = ["intelligenza artificiale", "energie rinnovabili", "e-commerce"]
    log_notification("Inizio della raccolta dati da Google Trends...")
    
    # Raccolta dati
    data = fetch_trends(keywords)

    if not data.empty:
        # Salva i dati in un file CSV
        file_name = f"trends_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        data.to_csv(file_name)
        log_notification(f"Dati salvati in '{file_name}'.")
    else:
        log_notification("Nessun dato disponibile per le keyword specificate.")
