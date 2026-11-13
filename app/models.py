from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    password = db.Column(db.String(255))
    main_stock = db.Column(db.Integer, default=0)
    shop1_stock = db.Column(db.Integer, default=0)
    shop2_stock = db.Column(db.Integer, default=0)
    shop3_stock = db.Column(db.Integer, default=0)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='worker') # 'owner' or 'worker'
    store_id = db.Column(db.String(50), nullable=False, default='shop1') # 'shop1', 'shop2', 'shop3'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    main_stock = db.Column(db.Integer, default=0)
    shop1_stock = db.Column(db.Integer, default=0)
    shop2_stock = db.Column(db.Integer, default=0)
    shop3_stock = db.Column(db.Integer, default=0)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    store_id = db.Column(db.String(50), nullable=False, default='shop1', index=True)

class Sale(db.Model):
    main_stock = db.Column(db.Integer, default=0)
    shop1_stock = db.Column(db.Integer, default=0)
    shop2_stock = db.Column(db.Integer, default=0)
    shop3_stock = db.Column(db.Integer, default=0)
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.String(50), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
