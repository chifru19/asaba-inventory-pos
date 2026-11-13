import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asaba_super_secret_key_2026')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pos.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.models import Product, User, Sale

    with app.app_context():
        db.create_all()

    
    @app.route('/health')
    def health_check():
        return {"status": "healthy"}, 200

    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') == 'owner':
            return redirect(url_for('owner_dashboard'))
        return redirect(url_for('pos'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.form if request.form else request.json
            username = data.get('username')
            password = data.get('password')
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                if request.is_json or request.headers.get('Content-Type') == 'application/json':
                    return jsonify({"success": True, "redirect": url_for('owner_dashboard' if user.role == 'owner' else 'pos')})
                return redirect(url_for('owner_dashboard' if user.role == 'owner' else 'pos'))
            return jsonify({"error": "Invalid username or password"}), 401
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/owner')
    def owner_dashboard():
        if session.get('role') != 'owner':
            return redirect(url_for('login'))
        products = Product.query.all()
        return render_template('owner_dashboard.html', products=products)

    @app.route('/pos')
    def pos():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        products = Product.query.all()
        from datetime import datetime, date
        today_start = datetime.combine(date.today(), datetime.min.time())
        sales = Sale.query.filter(Sale.timestamp >= today_start).order_by(Sale.timestamp.desc()).all()
        return render_template('pos.html', products=products, sales=sales)

    @app.route('/api/products', methods=['GET', 'POST'])
    def manage_products():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 401
        
        if request.method == 'POST':
            data = request.json or request.form
            name = data.get('name')
            price = float(data.get('price', 0))
            stock = int(data.get('stock', 0))
            
            product = Product(name=name, price=price, stock=stock, main_stock=stock)
            db.session.add(product)
            db.session.commit()
            return jsonify({"success": True, "message": "Product created successfully!"})
            
        products = Product.query.all()
        return jsonify([{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock, "main_stock": getattr(p, 'main_stock', p.stock)} for p in products])

    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
        try:
            data = request.json or {}
            product_id = int(data.get('product_id', 0))
            shop = data.get('shop', 'shop1')
            qty = int(data.get('qty', 0))
            
            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404
                
            main_stk = getattr(product, 'main_stock', getattr(product, 'stock', 0))
            if main_stk < qty:
                return jsonify({"error": f"Insufficient main stock ({main_stk} available)"}), 400
                
            if hasattr(product, 'main_stock'):
                product.main_stock = main_stk - qty
            elif hasattr(product, 'stock'):
                product.stock = main_stk - qty
                
            shop_attr = f"{shop}_stock"
            current_shop_stk = getattr(product, shop_attr, 0) or 0
            setattr(product, shop_attr, current_shop_stk + qty)
            
            db.session.commit()
            return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()}!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    
    @app.route('/api/sales', methods=['GET', 'POST'])
    def handle_sales():
        from datetime import datetime, date
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
            
        if request.method == 'POST':
            data = request.json or {}
            items = data.get('items', [])
            total = float(data.get('total', 0))
            shop = data.get('shop', 'shop1')
            
            import json
            sale = Sale(
                user_id=session.get('user_id'),
                shop=shop,
                items_json=json.dumps(items),
                total=total
            )
            
            # Deduct stock
            for item in items:
                p_id = item.get('id')
                qty = item.get('qty', 1)
                product = Product.query.get(p_id)
                if product:
                    shop_attr = f"{shop}_stock"
                    current_stk = getattr(product, shop_attr, getattr(product, 'stock', 0))
                    setattr(product, shop_attr, max(0, current_stk - qty))
            
            db.session.add(sale)
            db.session.commit()
            return jsonify({"success": True, "message": "Sale completed and recorded successfully!"})
            
        # GET today's sales
        today_start = datetime.combine(date.today(), datetime.min.time())
        sales = Sale.query.filter(Sale.timestamp >= today_start).order_by(Sale.timestamp.desc()).all()
        
        sales_list = []
        for s in sales:
            sales_list.append({
                "id": s.id,
                "total": s.total,
                "shop": s.shop,
                "timestamp": s.timestamp.strftime("%H:%M:%S") if s.timestamp else "",
                "items": json.loads(s.items_json) if s.items_json else []
            })
        return jsonify(sales_list)

    return app
