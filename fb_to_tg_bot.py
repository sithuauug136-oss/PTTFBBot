import os
import json
import logging
import requests
from flask import Flask, request, jsonify
from datetime import datetime

# ─── Configuration ─────────────────────────────────────────────────────────────
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "EAAjH0SfJsrcBRBOin0kfHO4uQ3oadIe2q8ILTsZC0Iamd8OvZCIwq1kfI2xx3AY4EvI7ZBZAdZBhHJugjp0a6bI9hMtcoUdZBj79felZAeHCP6pXawlyN9NiJKWP1ZAnLG7MPZAFx123ECL2wd3yyIDDcxVnPlDLuiaYWP9milADveOtkLLp40C0CDXsDFNLSfurFkuZAPsJDbtDEjekpyxcvJsbO6")
FB_VERIFY_TOKEN      = os.environ.get("FB_VERIFY_TOKEN", "PTTFBBot_verify_2024_secure")
FB_PAGE_ID           = os.environ.get("FB_PAGE_ID", "104789059168866")
TG_BOT_TOKEN         = os.environ.get("TG_BOT_TOKEN", "8645961201:AAGDAHX0oIzTgJq-w1EALX3lcy7Poo-Fv0A")
TG_BAHT_GROUP        = os.environ.get("TG_BAHT_GROUP", "@ptttbath")
TG_KYAT_GROUP        = os.environ.get("TG_KYAT_GROUP", "-1003848910699")

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "PTTFBBot Webhook is running! 🤖", 200

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == FB_VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    # Facebook Messenger webhook logic (Image receiving + forwarding)
    data = request.get_json()
    logger.info(f"📨 Received webhook: {data}")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
