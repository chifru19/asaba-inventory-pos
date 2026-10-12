from flask import Flask
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'asaba_secure_owner_key_2026'

    db.init_app(app)
    migrate.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)

        with app.app_context():
        db.create_all()
        from app.models import Product
        if not Product.query.first():
            p1 = Product(name="Cashew Nuts (Medium)", sku="CSH-001", purchase_price=1200.0, selling_price=1800.0, stock_quantity=50, min_threshold=5)
            p2 = Product(name="Plantain Chips", sku="PLN-002", purchase_price=300.0, selling_price=500.0, stock_quantity=100, min_threshold=10)
            db.session.add_all([p1, p2])
            db.session.commit()

    return app
