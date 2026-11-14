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
            if not User.query.filter_by(username='shop1').first():
                db.session.add(User(username='shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='shop2').first():
                db.session.add(User(username='shop2', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='shop3').first():
                db.session.add(User(username='shop3', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='admin').first():
                db.session.add(User(username='admin', password_hash=generate_password_hash('admin123'), role='owner'))
            db.session.commit()

            if Product.query.count() == 0:
                master_products = [
                    Product(name="DEO ROLLON mn", price=1500, main_stock=72, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="DEO ROLLON WN", price=1500, main_stock=120, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL/ urea/ Q10", price=3500, main_stock=70, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Bcream-Sheabut", price=3500, main_stock=1632, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Bl-Bcream-vanille/SheaB", price=3500, main_stock=96, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Dgel H&M 750ml", price=2500, main_stock=3060, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL men Dusgel 300ml", price=1000, main_stock=86, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Bl Savon H&M", price=1000, main_stock=29, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Denkmit Duftspary", price=1500, main_stock=612, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Enthaarungs creame", price=2000, main_stock=1236, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Rossmann facelle clasic", price=1500, main_stock=390, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Cien Spray 4Men", price=1500, main_stock=1460, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="cein seduction spray mn", price=1500, main_stock=220, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="LD-Dentalux-Complex 3", price=1000, main_stock=4200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Complex 8", price=1500, main_stock=204, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Dentalux 5FACH", price=1500, main_stock=192, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Cien Dgel 300ml 3x colour", price=1500, main_stock=360, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Cein Schauma Shampo", price=1500, main_stock=108, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Cein seduction 3-1 dusgel", price=1500, main_stock=240, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="cien savon", price=2000, main_stock=240, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Cein Blotion Q10", price=3000, main_stock=252, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Ld Mundspulung 750ml", price=2500, main_stock=600, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Doussy 3L", price=6000, main_stock=224, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Kuschelweich 1Ldorsey", price=3500, main_stock=744, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Softland fresh 2L", price=3000, main_stock=120, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="LD-dentalux Tbrush kids-Gc", price=1500, main_stock=1350, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Simpre PLiners 45", price=2000, main_stock=330, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="W5 Glas reinigen", price=1500, main_stock=500, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="W5 Dischwasser", price=1500, main_stock=360, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Hot chocolate", price=6000, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="chocolate", price=5000, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Dash powder -100", price=15000, main_stock=300, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Cornflakes 500g", price=3000, main_stock=120, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="LACUNA Blotion", price=2500, main_stock=300, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Biocura Spray M", price=1500, main_stock=600, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Tbrush aldi", price=1200, main_stock=1200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Tbrush-kids- Aldi good", price=1500, main_stock=882, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Biocura Rollon Mix", price=1200, main_stock=640, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Nivea Bodylotion", price=7000, main_stock=40, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Pure Rollon", price=1200, main_stock=304, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Softrans weichspuler", price=3500, main_stock=240, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Tbrush big", price=1200, main_stock=858, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Irvering 3L H20 bioler", price=12000, main_stock=180, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Irvering plastic mixer", price=20000, main_stock=60, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Irvering Glas mixer 800w", price=25000, main_stock=60, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="irvering 3,2L Rice cooker", price=35000, main_stock=20, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="COMPRESSOR Fridge", price=50000, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Long Fridge 1.8", price=100000, main_stock=2, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Short Fridge 1.5", price=75000, main_stock=6, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Tabletop", price=50000, main_stock=10, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Gasherd", price=50000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="kitchen fridge ecofrost", price=100000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Ladder", price=20000, main_stock=5, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Gas herd Beko 5head", price=300000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Pressing iron 5+", price=10000, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="27 zoll monitor", price=25000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="glasses", price=5000, main_stock=2, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="H20bioler -used", price=5000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Airfryer", price=25000, main_stock=5, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="8 black staple chairs", price=5000, main_stock=8, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="ironing board", price=20000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="crunches", price=5000, main_stock=4, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Babywalker", price=20000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="child bett", price=15000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="child bicycle", price=10000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Pots", price=5000, main_stock=10, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Fryingpan", price=5000, main_stock=12, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Used Professional Iron", price=20000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Gehrad-age bicycle", price=10000, main_stock=5, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Chaire red 3-2 Vinc", price=150000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Brown ch 3-2-1", price=200000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="English Material", price=150000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="mopo centre table", price=50000, main_stock=1, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Tyres 8*4 800", price=10000, main_stock=600, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Catalan", price=10000, main_stock=2, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="PC Screens 20-22", price=15000, main_stock=143, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="PC Screens 24-26Z VIP red", price=15000, main_stock=61, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="matrasse", price=20000, main_stock=2, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="Carpet 15k", price=20000, main_stock=2, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                ]
                db.session.bulk_save_objects(master_products)
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
        user = User.query.get(session['user_id'])
        raw_products = Product.query.all()
        username = user.username if user else 'shop1'
        store_name = username.upper()
        
        products = []
        for p in raw_products:
            if username == 'shop2':
                stk = p.shop2_stock
            elif username == 'shop3':
                stk = p.shop3_stock
            else:
                stk = p.shop1_stock
                
            products.append({
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "stock": stk
            })

        return render_template('pos.html', products=products, store_name=store_name, username=username)

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


    @app.route('/api/restock_product', methods=['POST'])
    def restock_product():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 403
        try:
            data = request.get_json() or {}
            product_id = data.get('product_id')
            qty = int(data.get('qty', 0))

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404

            if qty <= 0:
                return jsonify({"error": "Quantity must be greater than zero"}), 400

            product.main_stock = (product.main_stock or 0) + qty
            db.session.commit()
            
            return jsonify({
                "success": True, 
                "message": f"Successfully restocked {qty} units of {product.name}. New Main Stock: {product.main_stock}"
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


    return app
