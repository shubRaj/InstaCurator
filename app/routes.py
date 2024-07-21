# Import necessary modules and functions from Flask, dotenv, pathlib, os, and custom modules
from flask import request, Blueprint, render_template
from dotenv import load_dotenv
from pathlib import Path
import os
from app.crud import create_post, get_post_by_hashed
from app.core import get_hash_from_video, InstagramAPI

# Load environment variables from the .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Initialize a Blueprint for the main routes
main = Blueprint('main', __name__)

# Define the home route
@main.route("/", methods=["GET"])
def home():
    """
    Home route that returns a simple HTML response.
    
    Returns:
        str: HTML content displaying a centered "Wink Wink" message.
    """
    return "<h1 style='text-align:center;'>Wink Wink</h1>"

# Define the webhook route
@main.route('/webhook/', methods=['GET', 'POST'])
def webhook():
    """
    Webhook route to handle GET and POST requests.
    
    Handles subscription verification and processes received messages.
    
    Returns:
        str: A challenge token for GET requests or a simple response for POST requests.
        int: HTTP status code (200 for successful verification, 403 for forbidden access).
    """
    if request.method == 'GET':
        # Handle GET request for subscription verification
        mode = request.args.get("hub.mode")  # Mode of the subscription request
        challenge = request.args.get("hub.challenge")  # Challenge token to be returned
        token = request.args.get("hub.verify_token")  # Verification token
        
        # Verify the subscription mode and token
        if mode and token:
            if mode == "subscribe" and token == os.getenv("VERIFY_TOKEN"):
                return challenge, 200  # Return the challenge token if verification is successful
            return "", 403  # Return 403 Forbidden if verification fails

    elif request.method == 'POST':
        # Handle POST request to process incoming messages
        data = request.get_json()  # Parse the JSON payload from the request
        message_instance = data["entry"][0]["messaging"][0]  # Extract the message instance
        sender_id = message_instance["sender"]["id"]  # Extract the sender ID
        attachments = message_instance["message"].get("attachments")  # Extract message attachments if any
        text = message_instance["message"].get("text")  # Extract text message if any

        if attachments:
            # Process each attachment in the message
            for attachment in attachments:
                if attachment["type"] != "ig_reel":
                    continue  # Skip non-reel attachments
                
                title = attachment["payload"]["title"]  # Extract the title of the reel
                url = attachment["payload"]["url"]  # Extract the URL of the reel
                hashed = get_hash_from_video(url)  # Generate a hash from the video URL
                
                # Check if the post already exists in the database
                if get_post_by_hashed(hashed):
                    return "Already Exists"  
                else:
                    with InstagramAPI() as iapi:
                        # Make a post to Instagram using the API
                        iapi.make_post(url, caption=title, media_type="REELS")
                        # Create a new post entry in the database
                        create_post(caption=title, hashed=hashed)
                        return "Successful"

        # Add additional processing logic here if needed
    """
        Further Will be Done
    
    """
    return "Hi"

# Define the privacy policy route
@main.route("/privacy-policy/", methods=["GET"])
def privacy_policy():
    """
    Route to render the privacy policy page.
    
    Returns:
        str: Rendered HTML template for the privacy policy page.
    """
    return render_template("privacy-policy.html")

# Define the terms and conditions route
@main.route("/terms-and-conditions/", methods=["GET"])
def terms_and_conditions():
    """
    Route to render the terms and conditions page.
    
    Returns:
        str: Rendered HTML template for the terms and conditions page.
    """
    return render_template("terms-and-conditions.html")
