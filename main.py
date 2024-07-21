from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
app = Flask(__name__)
@app.route("/",methods=["GET"])

def home():
    return "<h1 style='text-align:center;'>Wink Wink</h1>"

@app.route('/webhook/', methods=['GET',"POST"])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")
        if mode and token:
            if mode == "subscribe" and token == os.getenv("VERIFY_TOKEN"):
                return challenge,200
            return "",403
            
    return "HI"

if __name__ == '__main__':
    app.run(debug=True,port=5000)
