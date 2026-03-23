import sqlite3
import os
import json
import logging
import requests
from flask import Flask, request
from datetime import datetime
try:
    from google import genai
    from google.genai import types
except ImportError:
    pass

# ─── Configuration ─────────────────────────────────────────────────────────────
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "EAAjH0SfJsrcBRBOin0kfHO4uQ3oadIe2q8ILTsZC0Iamd8OvZCIwq1kfI2xx3AY4EvI7ZBZAdZBhHJugjp0a6bI9hMtcoUdZBj79felZAeHCP6pXawlyN9NiJKWP1ZAnLG7MPZAFx123ECL2wd3yyIDDcxVnPlDLuiaYWP9milADveOtkLLp40C0CDXsDFNLSfurFkuZAPsJDbtDEjekpyxcvJsbO6")
FB_VERIFY_TOKEN      = os.environ.get("FB_VERIFY_TOKEN", "PTTFBBot_verify_2024_secure")
FB_PAGE_ID           = os.environ.get("FB_PAGE_ID", "104789059168866")
TG_BOT_TOKEN         = os.environ.get("TG_BOT_TOKEN", "8645961201:AAGDAHX0oIzTgJq-w1EALX3lcy7Poo-Fv0A")
GROUP_BAHT           = "@ptttbath"
GROUP_KYAT           = "-1003848910699"
GEMINI_KEY           = os.environ.get("GEMINI_API_KEY", "AIzaSyCBtmPDFMc11qjte7TfyayYmTLFexcf_0Y")

DB_PATH = "/app/data/slips.db"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = genai.Client(api_key=GEMINI_KEY) if 'genai' in globals() else None

def init_db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS slips (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tx_id TEXT UNIQUE,
                        sender TEXT,
                        amount REAL,
                        currency TEXT,
                        type TEXT,
                        date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO settings VALUES ('clear_time', ?)", (datetime.now().strftime("%H:%M %p"),))
    conn.commit()
    conn.close()

def get_totals(currency):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sum(amount) FROM slips WHERE currency = ? AND type = 'In'", (currency,))
    in_sum = cursor.fetchone()[0] or 0
    cursor.execute("SELECT sum(amount) FROM slips WHERE currency = ? AND type = 'Out'", (currency,))
    out_sum = cursor.fetchone()[0] or 0
    cursor.execute("SELECT value FROM settings WHERE key = 'clear_time'")
    clear_time = cursor.fetchone()[0]
    conn.close()
    return in_sum, out_sum, clear_time

@app.route("/", methods=["GET"])
def index(): return "PTTFBBot is running!", 200

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    # Logic to process FB image, analyze, save to DB, and send to TG
    # This part would be the full pipeline
    return "OK", 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
