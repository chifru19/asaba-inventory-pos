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
            products = [
                Product(name="Balea Deo Mn Fresh & Exdry", sku="BAL-001", purchase_price=7000.0, selling_price=10000.0, stock_quantity=10, min_threshold=2),
                Product(name="Balea Deo Mn Inv & Sens", sku="BAL-002", purchase_price=7000.0, selling_price=10000.0, stock_quantity=10, min_threshold=2),
                Product(name="Balea SPRAY 4 Wm 48H", sku="BAL-003", purchase_price=6000.0, selling_price=9000.0, stock_quantity=10, min_threshold=2),
                Product(name="Balea DEO ROLLON Mn", sku="BAL-004", purchase_price=5000.0, selling_price=7000.0, stock_quantity=10, min_threshold=2),
                Product(name="Balea DEO ROLLON WN", sku="BAL-005", purchase_price=5000.0, selling_price=7000.0, stock_quantity=10, min_threshold=2),
                Product(name="Balea Bodylotion", sku="BAL-006", purchase_price=10000.0, selling_price=13000.0, stock_quantity=10, min_threshold=2),
                Product(name="Balea Bodymilk", sku="BAL-007", purchase_price=10000.0, selling_price=13000.0, stock_quantity=10, min_threshold=2),
                Product(name="Cien Spray 4Men", sku="CIEN-102", purchase_price=10000.0, selling_price=1460000.0, stock_quantity=10, min_threshold=2),
                Product(name="Cien Dusgel 1L", sku="CIEN-105", purchase_price=12000.0, selling_price=18000.0, stock_quantity=10, min_threshold=2),
                Product(name="Toilet roll-10/3lag", sku="HH-001", purchase_price=40000.0, selling_price=60000.0, stock_quantity=10, min_threshold=2),
                Product(name="Doussy 3L", sku="HH-002", purchase_price=800000.0, selling_price=1120000.0, stock_quantity=10, min_threshold=2),
                Product(name="Kuschelweich 1L", sku="HH-003", purchase_price=1000000.0, selling_price=1488000.0, stock_quantity=10, min_threshold=2),
                Product(name="Dash powder -100", sku="HH-004", purchase_price=3000000.0, selling_price=3900000.0, stock_quantity=10, min_threshold=2)
            ]
            db.session.add_all(products)
            db.session.commit()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    import json
    app.jinja_env.filters['from_json'] = json.loads

    return app