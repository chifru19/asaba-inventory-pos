from flask import Flask
from app.extensions import db
from app.models import Product, Sale

def create_app():
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///asaba.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "supersecretkey"

db.init_app(app)

with app.app_context():
    db.create_all()
    if not Product.query.first():
        p1 = Product(name="Cashew Nuts (Medium)", sku="CSH-001", purchase_price=1200.0, selling_price=1800.0, stock_quantity=50, min_threshold=5)
        p2 = Product(name="Plantain Chips", sku="PLN-002", purchase_price=300.0, selling_price=500.0, stock_quantity=100, min_threshold=10)
        db.session.add_all([p1, p2])
        db.session.commit()

from app.routes import main_bp
app.register_blueprint(main_bp)

import json
app.jinja_env.filters['from_json'] = json.loads

return app
