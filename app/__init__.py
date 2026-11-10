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
        
        # Create default users and shop data if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='owner', store_id='global')
            admin.set_password('admin123')
            db.session.add(admin)

        # Create workers for Shop 1, Shop 2, and Shop 3
        shops = ['shop1', 'shop2', 'shop3']
        for shop in shops:
            worker_username = f'worker_{shop}'
            if not User.query.filter_by(username=worker_username).first():
                worker = User(username=worker_username, role='worker', store_id=shop)
                worker.set_password('password123')
                db.session.add(worker)
            
            # Add sample products for each shop if none exist
            if not Product.query.filter_by(store_id=shop).first():
                p1 = Product(name=f'Item A ({shop.upper()})', price=1500.0, stock=50, store_id=shop)
                p2 = Product(name=f'Item B ({shop.upper()})', price=3000.0, stock=30, store_id=shop)
                db.session.add_all([p1, p2])

        db.session.commit()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
