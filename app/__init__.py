from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'asaba-secret-key-2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asaba.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from app.models import Product, Sale, SaleItem
        from app.routes import init_routes
        init_routes(app)
        db.create_all()

    return app
