# Import necessary modules from dotenv, pathlib, and os
from dotenv import load_dotenv
from pathlib import Path
import os

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent
# Load environment variables from the .env file located in the base directory
load_dotenv(BASE_DIR / ".env")

class Config:
    """
    Configuration class for the Flask application.
    
    Attributes:
        SECRET_KEY (str): Secret key for the application, loaded from environment variables.
        SQLALCHEMY_DATABASE_URI (str): URI for the SQLAlchemy database connection.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to disable SQLAlchemy modification tracking.
    """
    # Load the secret key from the environment variables
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Define the database URI for SQLAlchemy (using SQLite database)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite3.db'
    # Disable SQLAlchemy modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
