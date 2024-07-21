from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Load default configuration
    app.config.from_object('app.config.Config')

    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
