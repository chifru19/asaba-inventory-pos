import os
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
        try:
            if not User.query.filter_by(username='owner').first():
                db.session.add(User(username='owner', password_hash=generate_password_hash('owner123'), role='owner'))
            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='worker_shop2').first():
                db.session.add(User(username='worker_shop2', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='worker_shop3').first():
                db.session.add(User(username='worker_shop3', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='admin').first():
                db.session.add(User(username='admin', password_hash=generate_password_hash('admin123'), role='owner'))
            db.session.commit()

            if Product.query.count() == 0:
                sample_products = [
                    Product(name="DEO ROLLON mn", price=800, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="DEO ROLLON wn", price=800, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Bodylotion", price=1500, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Bodymilk", price=1500, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL Body coscos", price=2000, main_stock=150, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL/vital", price=2500, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                ]
                db.session.bulk_save_objects(sample_products)
                db.session.commit()
        except Exception as e:
            print("Seeding error:", e)
            db.session.rollback()

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
            if user and check_password_hash(user.password_hash, password):
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
        
        today = date.today()
        sales_today = Sale.query.filter(db.func.date(Sale.created_at) == today).all()
        
        shop_sales = {'shop1': 0, 'shop2': 0, 'shop3': 0}
        shop_revenue = {'shop1': 0.0, 'shop2': 0.0, 'shop3': 0.0}
        
        for s in sales_today:
            s_shop = getattr(s, 'store_id', 'shop1')
            if s_shop in shop_sales:
                shop_sales[s_shop] += 1
                shop_revenue[s_shop] += float(s.total_amount or 0)

        return render_template('owner_dashboard.html', products=products, shop_sales=shop_sales, shop_revenue=shop_revenue)

    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
        try:
            data = request.get_json() or {}
            product_id = data.get('product_id')
            shop = data.get('shop')
            qty = int(data.get('qty', 0))

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404

            main_stk = getattr(product, 'main_stock', 0) or 0
            if main_stk < qty:
                return jsonify({"error": "Insufficient main stock for transfer!"}), 400

            shop_attr = f"{shop}_stock"
            if not hasattr(product, shop_attr):
                return jsonify({"error": "Invalid shop target"}), 400

            product.main_stock = main_stk - qty
            current_shop_stk = getattr(product, shop_attr, 0) or 0
            setattr(product, shop_attr, current_shop_stk + qty)

            db.session.commit()
            return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()} from Main Stock!"})
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

                sale = Sale(total_amount=total, store_id=shop, user_id=session.get('user_id', 1), created_at=datetime.utcnow())
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
                "total": s.total_amount,
                "shop": s.store_id,
                "timestamp": s.created_at.strftime('%Y-%m-%d %H:%M:%S') if s.created_at else str(s.created_at)
            } for s in sales])


    @app.route('/api/products', methods=['POST'])
    def add_product():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 403
        try:
            data = request.get_json() or {}
            name = data.get('name')
            price = float(data.get('price', 0))
            main_stock = int(data.get('main_stock', 0))

            if not name or price <= 0:
                return jsonify({"error": "Invalid product name or price"}), 400

            new_prod = Product(
                name=name,
                price=price,
                main_stock=main_stock,
                shop1_stock=0,
                shop2_stock=0,
                shop3_stock=0,
                store_id='shop1'
            )
            db.session.add(new_prod)
            db.session.commit()
            return jsonify({"success": True, "message": "Product added successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/api/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 403
        try:
            prod = Product.query.get(product_id)
            if not prod:
                return jsonify({"error": "Product not found"}), 404
            
            db.session.delete(prod)
            db.session.commit()
            return jsonify({"success": True, "message": "Product deleted successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return app

