# Import the create_app function from the app package
from app import create_app

# Create the Flask application instance using the factory function
app = create_app()

# Entry point for running the application
if __name__ == '__main__':
    """
    Run the Flask application in debug mode on port 8000.
    """
    app.run(debug=True, port=8000)
