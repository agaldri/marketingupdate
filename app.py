
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
from pytrends.request import TrendReq
from googletrans import Translator
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
DB_NAME = "trends_data.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY,
            keyword TEXT,
            volume INTEGER,
            geo TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_to_database(data, geo):
    conn = sqlite3.connect(DB_NAME)
    data['geo'] = geo
    data.to_sql('trends', conn, if_exists='append', index=False)
    conn.close()

def fetch_top_keywords(geo, num_keywords=500):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=[], geo=geo)
    related_queries = pytrends.trending_searches(pn=geo)
    top_keywords = related_queries.head(num_keywords)
    return top_keywords

def fetch_trends(keywords, geo):
    pytrends = TrendReq(hl='en-US', tz=360)
    trends_data = {}
    for keyword in keywords:
        try:
            pytrends.build_payload([keyword], cat=0, timeframe="today 12-m", geo=geo, gprop='')
            data = pytrends.interest_over_time()
            if not data.empty:
                trends_data[keyword] = data[keyword]
        except Exception as e:
            print(f"Errore con la keyword {keyword}: {e}")
    return pd.DataFrame(trends_data)

def translate_keywords(keywords, languages):
    translator = Translator()
    translations = {lang: [] for lang in languages}
    for keyword in keywords:
        for lang in languages:
            try:
                translations[lang].append(translator.translate(keyword, dest=lang).text)
            except:
                translations[lang].append("Error")
    return pd.DataFrame(translations, index=keywords)

def send_email(subject, body, recipient):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = "your_email@gmail.com"
    EMAIL_PASSWORD = "your_password"
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
    except Exception as e:
        print(f"Errore invio email: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/top-keywords', methods=['GET', 'POST'])
def top_keywords():
    if request.method == 'POST':
        geo = request.form.get('geo')
        num_keywords = int(request.form.get('num_keywords'))
        keywords = fetch_top_keywords(geo, num_keywords)
        keywords.to_csv("top_keywords.csv", index=False)
        return render_template('top_keywords.html', data=keywords.to_html(index=False))
    return render_template('top_keywords.html')

@app.route('/select', methods=['GET', 'POST'])
def select_functionality():
    if request.method == 'POST':
        choice = request.form.get('functionality')
        if choice == "top-keywords":
            return redirect(url_for('top_keywords'))
        elif choice == "trends":
            return redirect(url_for('trends'))
        elif choice == "translate":
            return redirect(url_for('translate'))
        elif choice == "filters":
            return redirect(url_for('filters'))
        elif choice == "notifications":
            return redirect(url_for('notifications'))
    return render_template('select.html')

@app.route('/trends', methods=['GET', 'POST'])
def trends():
    if request.method == 'POST':
        geo = request.form.get('geo')
        keywords = request.form.get('keywords').split(',')
        data = fetch_trends(keywords, geo)
        save_to_database(data, geo)
        return render_template('trends.html', data=data.to_html())
    return render_template('trends.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        keywords = request.form.get('keywords').split(',')
        languages = ['it', 'fr', 'es', 'ja', 'hi', 'zh-cn']
        translations = translate_keywords(keywords, languages)
        translations.to_csv("translations.csv")
        return render_template('translate.html', translations=translations.to_html())
    return render_template('translate.html')

@app.route('/filters', methods=['GET', 'POST'])
def filters():
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT * FROM trends"
    if request.method == 'POST':
        min_volume = request.form.get('min_volume')
        if min_volume:
            query += f" WHERE volume >= {min_volume}"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return render_template('filters.html', data=data.to_html())

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    if request.method == 'POST':
        recipient = request.form.get('email')
        subject = "Notification from Web App"
        body = "Your selected trends data is ready."
        send_email(subject, body, recipient)
        return render_template('notifications.html', message="Email inviata con successo!")
    return render_template('notifications.html')

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
