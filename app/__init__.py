import os
from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'asaba-secret-key-2026'

    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, 'asaba.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from app.models import Product, Sale, SaleItem
        from app.routes import init_routes

        db.create_all()

        # Automatically seed initial inventory if empty
        if db.session.scalar(db.select(Product).limit(1)) is None:
            products_data = [
                Product(name='Balea Deo Men Fresh & Dry', sku='BL-DEO-MN', purchase_price=667.0, selling_price=1000.0, stock_quantity=50, min_threshold=5),
                Product(name='Balea Bodylotion Bloomy Kiss', sku='BL-LCR-BK', purchase_price=667.0, selling_price=1500.0, stock_quantity=40, min_threshold=5),
                Product(name='Balea Bodycream Shea Butter', sku='BL-BC-SHEA', purchase_price=671.25, selling_price=2500.0, stock_quantity=30, min_threshold=3),
                Product(name='Cien Spray 4 Men', sku='CIEN-SP-MN', purchase_price=667.50, selling_price=1000.0, stock_quantity=50, min_threshold=5),
                Product(name='Dentalux Complex 3 Toothpaste', sku='LD-DENT-3', purchase_price=667.36, selling_price=800.0, stock_quantity=175, min_threshold=20),
                Product(name='Doussy Softener 3L', sku='DOUS-3L-SF', purchase_price=672.46, selling_price=5000.0, stock_quantity=56, min_threshold=10),
                Product(name='W5 Glass Cleaner', sku='W5-GLS-CLN', purchase_price=667.56, selling_price=1500.0, stock_quantity=50, min_threshold=10),
                Product(name='Dash Washing Powder 100W', sku='DASH-PWD-100', purchase_price=675.66, selling_price=13000.0, stock_quantity=15, min_threshold=3),
                Product(name='Irving Rice Cooker 2.2L', sku='IRV-RC-2L', purchase_price=66710.0, selling_price=25000.0, stock_quantity=15, min_threshold=2),
                Product(name='Airfryer Pro', sku='AIRFRY-PRO', purchase_price=6676.67, selling_price=15000.0, stock_quantity=5, min_threshold=1)
            ]
            db.session.add_all(products_data)
            db.session.commit()
            print('✅ Database seeded with complete imported catalog!')

        init_routes(app)

    return app