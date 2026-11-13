from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='worker')

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
