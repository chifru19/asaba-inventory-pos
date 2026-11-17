# type: ignore
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app.models import db, Product, StoreStock, Sale, SaleItem
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/health')
def health_check():
    return "OK", 200

@main_bp.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'owner':
            return redirect(url_for('main.owner_dashboard'))
        else:
            return redirect(url_for('main.pos'))
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['store_id'] = user.store_id
            session['shop'] = user.store_id
            
            if user.role == 'owner':
                return jsonify({'status': 'success', 'redirect': url_for('main.owner_dashboard')})
            else:
                return jsonify({'status': 'success', 'redirect': url_for('main.pos')})
                
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@main_bp.route('/pos')
def pos():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
        
    store_id = session.get('shop') or session.get('store_id') or 'shop1'
    session['shop'] = store_id
    
    search_query = request.args.get('search', '').strip()
    products = Product.query.filter_by(store_id=store_id).all()
    cart = session.get('cart', [])
    total = sum(item['subtotal'] for item in cart)
    
    sales_query = Sale.query.filter_by(store_id=store_id)
    if search_query:
        try:
            sales_query = sales_query.filter(Sale.id == int(search_query))
        except ValueError:
            pass
            
    today_sales = sales_query.all()
    return render_template('pos.html', products=products, cart=cart, total=total, store_id=store_id, today_sales=today_sales)

@main_bp.route('/owner')
@main_bp.route('/owner_dashboard')
def owner_dashboard():
    try:
        if 'user_id' not in session or session.get('role') != 'owner':
            return redirect(url_for('main.login'))
            
        selected_store = request.args.get('store_id', 'shop1')
        products = Product.query.all()
        sales = Sale.query.filter_by(store_id=selected_store).all()
        total_sales = sum(s.total_amount for s in sales) if sales else 0
        
        return render_template(
            'owner_dashboard.html', 
            products=products, 
            sales=sales, 
            total_sales=total_sales, 
            current_store=selected_store, 
            selected_store=selected_store
        )
    except Exception as e:
        print(f"Error in owner_dashboard: {e}")
        return redirect(url_for('main.login'))

@main_bp.route('/api/restock_product', methods=['POST'])
def api_restock_product():
    try:
        data = request.get_json(silent=True) or request.form
        product_id = data.get('product_id') or data.get('productId') or data.get('product')
        quantity = int(data.get('quantity', 0))

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404

        product.main_stock = (product.main_stock or 0) + quantity
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main_bp.route('/api/transfer_stock', methods=['POST'])
def api_transfer_stock():
    try:
        data = request.get_json(silent=True) or request.form
        product_id = data.get('product_id') or data.get('productId') or data.get('product')
        shop_name = data.get('shop_name') or data.get('destination_shop') or data.get('shop')
        quantity = int(data.get('quantity', 0))

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404

        if (product.main_stock or 0) < quantity:
            return jsonify({'success': False, 'message': 'Insufficient main stock'}), 400

        product.main_stock -= quantity

        store_stock = StoreStock.query.filter_by(product_id=product_id, store_id=shop_name).first()
        if store_stock:
            store_stock.quantity = (store_stock.quantity or 0) + quantity
        else:
            new_store_stock = StoreStock(product_id=product_id, store_id=shop_name, quantity=quantity)
            db.session.add(new_store_stock)

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
