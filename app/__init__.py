from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # Configure SQLite database for Asaba Ngu's inventory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asaba_inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'asaba-secure-inventory-key'
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints or routes later
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
