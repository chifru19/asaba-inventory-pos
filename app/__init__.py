import os
from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'asaba-secret-key-2026'

    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, 'asaba.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # IMPORTANT: Import models FIRST so metadata registers the tables
        from app.models import Product, Sale, SaleItem
        from app.routes import init_routes

        db.create_all()

        # Automatically seed initial inventory if empty
        if db.session.scalar(db.select(Product).limit(1)) is None:
            products_data = [
                Product(name='Drinking Water (3L)', sku='DOUS-3L', purchase_price=150.0, selling_price=250.0, stock_quantity=50, min_threshold=5),
                Product(name='Refined Garri (5kg)', sku='GARR-5K', purchase_price=1200.0, selling_price=1500.0, stock_quantity=20, min_threshold=3),
                Product(name='Palm Oil (1L)', sku='PLM-1L', purchase_price=800.0, selling_price=1000.0, stock_quantity=15, min_threshold=3),
                Product(name='Nigerian Rice (50kg)', sku='RICE-50K', purchase_price=45000.0, selling_price=52000.0, stock_quantity=10, min_threshold=2),
                Product(name='Honey Beans (5kg)', sku='BENS-5K', purchase_price=3500.0, selling_price=4200.0, stock_quantity=25, min_threshold=4),
                Product(name='Tomato Paste (Sachet)', sku='TOMA-SCH', purchase_price=120.0, selling_price=180.0, stock_quantity=100, min_threshold=10)
            ]
            db.session.add_all(products_data)
            db.session.commit()
            print('✅ Database automatically created and seeded with initial products!')

        init_routes(app)

    return app
