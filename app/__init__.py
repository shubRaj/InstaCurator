# Import necessary modules and functions from Flask and Flask extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy and Migrate objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """
    Factory function to create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    # Create a Flask application instance
    app = Flask(__name__, instance_relative_config=True)
    
    # Load default configuration from a Python object
    app.config.from_object('app.config.Config')
    
    # Initialize the SQLAlchemy extension with the app
    db.init_app(app)
    # Initialize the Migrate extension with the app and database
    migrate.init_app(app, db)
    
    # Import the main Blueprint from the app.routes module
    from app.routes import main
    # Register the main Blueprint with the app
    app.register_blueprint(main)
    
    # Return the configured Flask application instance
    return app
