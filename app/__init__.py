from flask import Flask
from app.extensions import db
from app.models import User, Product

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asaba-pos-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        
        # Create default owner if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='owner', store_id='global')
            admin.set_password('admin123')
            db.session.add(admin)

        # Define custom inventory for your shops
        shop_inventories = {
            'shop1': [
                {'name': 'Item A (SHOP1)', 'price': 1500.0, 'stock': 50},
                {'name': 'Item B (SHOP1)', 'price': 3000.0, 'stock': 30}
            ],
            'shop2': [
                {'name': 'Item A (SHOP2)', 'price': 1500.0, 'stock': 40},
                {'name': 'Item B (SHOP2)', 'price': 3000.0, 'stock': 25}
            ],
            'shop3': [
                {'name': 'Item A (SHOP3)', 'price': 1500.0, 'stock': 50},
                {'name': 'Item B (SHOP3)', 'price': 3000.0, 'stock': 30}
            ]
        }

        # Create workers and populate inventory for each shop
        for shop, items in shop_inventories.items():
            worker_username = f'worker_{shop}'
            if not User.query.filter_by(username=worker_username).first():
                worker = User(username=worker_username, role='worker', store_id=shop)
                worker.set_password('password123')
                db.session.add(worker)
            
            # Populate products if none exist for this shop
            if not Product.query.filter_by(store_id=shop).first():
                for item in items:
                    p = Product(name=item['name'], price=item['price'], stock=item['stock'], store_id=shop)
                    db.session.add(p)

        db.session.commit()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
