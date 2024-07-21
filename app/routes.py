from flask import request, Blueprint,render_template
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def home():
    return "<h1 style='text-align:center;'>Wink Wink</h1>"

@main.route('/webhook/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")
        if mode and token:
            if mode == "subscribe" and token == os.getenv("VERIFY_TOKEN"):
                return challenge, 200
            return "", 403
    elif request.method == 'POST':
        data = request.get_json()
        message_instance = data["entry"][0]["messaging"][0]
        sender_id = message_instance["sender"]["id"]
        attachments = message_instance["message"].get("attachments")
        text = message_instance["message"].get("text")
        if attachments is not None:
            for attachment in attachments:
                if attachment["type"] != "ig_reel":
                    continue
                title = attachment["payload"]["title"]
                url = attachment["payload"]["url"]

        # Handle the JSON data received
        # Add your processing logic here

    return "HI"

@main.route("/privacy-policy/", methods=["GET"])
def privacy_policy():
    return render_template("privacy-policy.html")

@main.route("/terms-and-conditions/", methods=["GET"])
def terms_and_conditions():
    return render_template("terms-and-conditions.html")