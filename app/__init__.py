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
            from seed import seed_database
            try:
                seed_database()
            except Exception:
                pass

    return app
