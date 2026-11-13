import os

init_path = "app/__init__.py"

app_code = '''import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from .extensions import db
from .models import Product, Sale, User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asaba-secret-key-2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asaba.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='owner').first():
            owner = User(username='owner', password=generate_password_hash('owner123'), role='owner')
            db.session.add(owner)
        if not User.query.filter_by(username='worker_shop1').first():
            worker = User(username='worker_shop1', password=generate_password_hash('worker123'), role='worker')
            db.session.add(worker)
        db.session.commit()

    @app.route('/health')
    def health():
        return {"status": "healthy"}, 200

    @app.route('/')
    def index():
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user and user.role == 'owner':
                return redirect(url_for('owner_dashboard'))
            else:
                return redirect(url_for('pos'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['role'] = user.role
                if user.role == 'owner':
                    return redirect(url_for('owner_dashboard'))
                else:
                    return redirect(url_for('pos'))
            return render_template('login.html', error="Invalid username or password")
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/pos')
    def pos():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        products = Product.query.all()
        return render_template('pos.html', products=products)

    @app.route('/owner')
    def owner_dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        products = Product.query.all()
        return render_template('owner_dashboard.html', products=products)

    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
        try:
            data = request.get_json() or {}
            product_id = data.get('product_id')
            shop = data.get('shop') # 'shop1', 'shop2', 'shop3'
            qty = int(data.get('qty', 0))

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404

            shop_attr = f"{shop}_stock"
            if not hasattr(product, shop_attr):
                return jsonify({"error": "Invalid shop target"}), 400

            current_shop_stk = getattr(product, shop_attr, 0) or 0
            setattr(product, shop_attr, current_shop_stk + qty)

            db.session.commit()
            return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()}!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/api/sales', methods=['GET', 'POST'])
    def handle_sales():
        if request.method == 'POST':
            try:
                data = request.get_json() or {}
                items = data.get('items', [])
                total = data.get('total', 0)
                shop = data.get('shop', 'shop1')

                sale = Sale(total=total, shop=shop, timestamp=datetime.utcnow())
                db.session.add(sale)

                for item in items:
                    p_id = item.get('id')
                    q = int(item.get('qty', 1))
                    prod = Product.query.get(p_id)
                    if prod:
                        shop_attr = f"{shop}_stock"
                        current_stk = getattr(prod, shop_attr, 0) or 0
                        setattr(prod, shop_attr, max(0, current_stk - q))

                db.session.commit()
                return jsonify({"success": True, "message": "Sale recorded successfully!"})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
        else:
            sales = Sale.query.order_by(Sale.id.desc()).limit(20).all()
            return jsonify([{
                "id": s.id,
                "total": s.total,
                "shop": s.shop,
                "timestamp": s.strftime('%Y-%m-%d %H:%M:%S') if hasattr(s, 'strftime') else str(s.timestamp)
            } for s in sales])

    return app
'''

with open(init_path, "w") as f:
    f.write(app_code)

print("Successfully fixed app/__init__.py indentation!")
