from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import time
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file located in the parent directory of the current file's parent directory
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True,exist_ok=True)
load_dotenv(BASE_DIR / ".env")

# Retrieve environment variables for PAGE_ID and ACCESS_TOKEN
PAGE_ID = os.getenv("PAGE_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Set up logging
logger = logging.getLogger("LOLify")
logger.setLevel(logging.DEBUG)

# Create a StreamHandler for console output
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Create a RotatingFileHandler for logging to a file with rotation
log_file = BASE_DIR / 'app.log'
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

class FacebookAPI:
    """Class to interact with the Facebook Graph API."""
    
    _HOST = "https://graph.facebook.com/v20.0"
    
    def __init__(self):
        """Initialize the FacebookAPI class and set up a requests session."""
        logger.debug("Initializing FacebookAPI class")
        session = requests.Session()
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        self._session = session
    
    def get_session(self):
        """Get the current session."""
        return self._session
    
    def get_host(self):
        """Get the host URL."""
        return self._HOST
    
    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context related to this object, closing the session."""
        logger.debug("Exiting FacebookAPI context")
        self.get_session().close()
    
    def get_instagram_id(self):
        """Get the Instagram Business Account ID linked to the Facebook Page."""
        logger.debug("Fetching Instagram Business Account ID")
        params = {
            "fields": "instagram_business_account",
            "access_token": ACCESS_TOKEN
        }
        response = self.get_session().get(f"{self.get_host()}/{PAGE_ID}", params=params)
        if response.status_code != 200:
            logger.error(f"Failed to get Instagram ID: {response.status_code}")
            return None
        data = response.json()
        instagram_business_account = data.get("instagram_business_account")
        if not instagram_business_account:
            logger.warning("No Instagram Business Account linked to the Facebook Page")
            return None
        return instagram_business_account["id"]

class InstagramAPI:
    """Class to interact with the Instagram Graph API."""
    
    _HOST = "https://graph.instagram.com"
    _WAIT_INTERVAL = 5

    def __init__(self):
        """Initialize the InstagramAPI class and set up a requests session."""
        logger.debug("Initializing InstagramAPI class")
        session = requests.Session()
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        self._session = session
        with FacebookAPI() as fapi:
            self._instagram_id = fapi.get_instagram_id()
    
    def get_wait_interval(self):
        """Get the wait interval time between retries."""
        return self._WAIT_INTERVAL

    def get_session(self):
        """Get the current session."""
        return self._session
    
    def get_host(self):
        """Get the host URL."""
        return self._HOST
    
    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context related to this object, closing the session."""
        logger.debug("Exiting InstagramAPI context")
        self.get_session().close()
    
    def get_instagram_id(self):
        """Get the Instagram Business Account ID."""
        return self._instagram_id
    
    def _create_container(self, URL, caption="", media_type="image"):
        """Create a media container for posting."""
        logger.debug(f"Creating media container: URL={URL}, caption={caption}, media_type={media_type}")
        params = {
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }
        if media_type.lower() == "image":
            params["image_url"] = URL
        elif media_type.lower() == "reels":
            params["video_url"] = URL
            params["media_type"] = "REELS"
        
        response = self.get_session().post(f"{FacebookAPI._HOST}/{self.get_instagram_id()}/media", params=params)
        container_id = response.json().get("id")
        if container_id:
            logger.info(f"Created media container with ID: {container_id}")
        else:
            logger.error("Failed to create media container")
        return container_id
    
    def get_publishing_limit(self):
        """Get the publishing limit for the Instagram Business Account."""
        logger.debug("Fetching content publishing limit")
        params = {
            "access_token": ACCESS_TOKEN
        }
        response = self.get_session().get(f"{FacebookAPI._HOST}/{self.get_instagram_id()}/content_publishing_limit", params=params)
        quota_usage = response.json()["data"][0]["quota_usage"]
        logger.info(f"Current publishing limit usage: {quota_usage}")
        return quota_usage
    
    def _check_container_status(self, container_id):
        """Check the status of the media container."""
        logger.debug(f"Checking container status for ID: {container_id}")
        params = {
            "fields": "status_code",
            "access_token": ACCESS_TOKEN
        }
        response = self.get_session().get(f"{FacebookAPI._HOST}/{container_id}", params=params)
        status_code = response.json().get("status_code", "").lower()
        logger.info(f"Container ID {container_id} status: {status_code}")
        return status_code
    
    def _publish_container(self, container_id):
        """Publish the created media container."""
        logger.debug(f"Publishing container with ID: {container_id}")
        params = {
            "creation_id": container_id,
            "access_token": ACCESS_TOKEN
        }
        while True:
            container_status = self._check_container_status(container_id)
            if container_status == "finished":
                response = self.get_session().post(f"{FacebookAPI._HOST}/{self.get_instagram_id()}/media_publish", params=params)
                logger.info(f"Published container ID: {container_id}")
                break
            elif container_status == "error":
                logger.error(f"Error publishing container ID: {container_id}")
                break
            else: 
                time.sleep(self.get_wait_interval())
    
    def make_post(self, URL, caption="", media_type="image"):
        """Create and publish a post on Instagram."""
        logger.debug(f"Making post: URL={URL}, caption={caption}, media_type={media_type}")
        container_id = self._create_container(URL, caption=caption, media_type=media_type)
        if container_id:
            self._publish_container(container_id)

if __name__ == "__main__":
    with InstagramAPI() as iapi:
        iapi.make_post("https://d.rapidcdn.app/snapinsta?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJodHRwczovL3Njb250ZW50LmNkbmluc3RhZ3JhbS5jb20vbzEvdi90MTYvZjEvbTg2L0ExNDVDMTQ4ODUzMjFBRUY5NEE3MkU1MTJCOEY5M0E1X3ZpZGVvX2Rhc2hpbml0Lm1wND9lZmc9ZXlKeFpWOW5jbTkxY0hNaU9pSmJYQ0pwWjE5M1pXSmZaR1ZzYVhabGNubGZkblJ6WDI5MFpsd2lYU0lzSW5abGJtTnZaR1ZmZEdGbklqb2lkblJ6WDNadlpGOTFjbXhuWlc0dVkyeHBjSE11WXpJdU56QTBMbUpoYzJWc2FXNWxJbjAmX25jX2h0PXNjb250ZW50LmNkbmluc3RhZ3JhbS5jb20mX25jX2NhdD0xJnZzPTQ2OTU2MjQ2MjM4MTk4NV8xMjY1OTE0NjkmX25jX3ZzPUhCa3NGUUlZVW1sblgzaHdkbDl5WldWc2MxOXdaWEp0WVc1bGJuUmZjM0pmY0hKdlpDOUJNVFExUXpFME9EZzFNekl4UVVWR09UUkJOekpGTlRFeVFqaEdPVE5CTlY5MmFXUmxiMTlrWVhOb2FXNXBkQzV0Y0RRVkFBTElBUUFWQWhnNmNHRnpjM1JvY205MVoyaGZaWFpsY25OMGIzSmxMMGRGYmtJMFVuSjFaR1poWVVoNlRXUkJUM2R4TkhCUk1YaDBZMUJpY1Y5RlFVRkJSaFVDQXNnQkFDZ0FHQUFiQUJVQUFDYmMwODdidUx2SlB4VUNLQUpETXl3WFFBcThhbjc1MnlNWUVtUmhjMmhmWW1GelpXeHBibVZmTVY5Mk1SRUFkZjRIQUElM0QlM0QmY2NiPTktNCZvaD0wMF9BWUFQbGxFLWVnczRkTVd1cWtUTVZOMm9rVWpGWUhQZHdSZEpPYWdQTHVrZC1nJm9lPTY2OUQzNEUxJl9uY19zaWQ9MTBkMTNiIiwiZmlsZW5hbWUiOiJTbmFwaW5zdGEuYXBwX3ZpZGVvX0ExNDVDMTQ4ODUzMjFBRUY5NEE3MkU1MTJCOEY5M0E1X3ZpZGVvX2Rhc2hpbml0Lm1wNCJ9.-ULWqno5hH-uKGna0oRjlfVmtpsf4E_uT8UBQFfGszw&dl=1&dl=1", caption="Video Here", media_type="REELS")
