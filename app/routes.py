from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.extensions import db
from app.models import User, Product, Sale
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
            session['shop'] = user.store_id
            session['shop'] = user.store_id
            
            if user.role == 'owner':
                return jsonify({'status': 'success', 'redirect': url_for('main.owner_dashboard')})
            else:
                return jsonify({'status': 'success', 'redirect': url_for('main.pos')})
                
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@main_bp.route('/pos')
def pos():
    store_id = session.get('shop') or session.get('store_id') or 'shop1'
    session['shop'] = store_id
    products = Product.query.filter_by(store_id=store_id).all()
    cart = session.get('cart', [])
    total = sum(item['subtotal'] for item in cart)
    from datetime import datetime
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_sales = Sale.query.filter_by(store_id=store_id).all()
    return render_template('pos.html', products=products, cart=cart, total=total, store_id=store_id, today_sales=today_sales)
@main_bp.route('/owner_dashboard')
def owner_dashboard():
    if 'user_id' not in session or session.get('role') != 'owner':
        return redirect(url_for('main.login'))
    selected_store = request.args.get('store_id', 'shop1')
    products = Product.query.filter_by(store_id=selected_store).all()
    sales = Sale.query.filter_by(store_id=selected_store).all()
    total_sales = sum(s.total_amount for s in sales)
    return render_template('owner_dashboard.html', products=products, sales=sales, total_sales=total_sales, current_store=selected_store, selected_store=selected_store)
@main_bp.route('/api/sell', methods=['POST'])
def sell():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    items = data.get('items', [])
    store_id = session.get('store_id') or request.args.get('store_id', 'shop1')
    if session.get('role') == 'owner':
        store_id = request.args.get('store_id', 'shop1')

    total_amount = 0
    for item in items:
        product = Product.query.get(item['product_id'])
        if product and product.stock >= item['quantity']:
            product.stock -= item['quantity']
            total_amount += product.price * item['quantity']
        else:
            return jsonify({'error': f"Insufficient stock for {product.name if product else 'item'}"}), 400

    sale = Sale(total_amount=total_amount, store_id=store_id, user_id=session['user_id'])
    db.session.add(sale)
    db.session.commit()

    return jsonify({'success': True, 'total_amount': total_amount})

@main_bp.route('/api/products', methods=['POST'])
def add_product():
    if 'user_id' not in session or session.get('role') != 'owner':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    store_id = data.get('store_id', 'shop1')

    product = Product(name=name, price=price, stock=stock, store_id=store_id)
    db.session.add(product)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Product added successfully'})

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main_bp.route('/pos/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    cart = session.get('cart', [])
    product = Product.query.get_or_404(product_id)
    
    # Check if item already in cart
    found = False
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            item['subtotal'] = item['quantity'] * product.price
            found = True
            break
    if not found:
        cart.append({
            'product_id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'subtotal': product.price
        })
    session['cart'] = cart
    return redirect(url_for('main.pos'))

@main_bp.route('/pos/complete', methods=['POST'])
def complete_sale():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('main.pos'))
    
    store_id = session.get('shop') or session.get('store_id') or 'shop1'
    total_amount = sum(item['subtotal'] for item in cart)
    
    # Create sale record
    sale = Sale(total_amount=total_amount, store_id=store_id, user_id=session['user_id'])
    db.session.add(sale)
    
    # Deduct stock
    for item in cart:
        product = Product.query.get(item['product_id'])
        if product:
            product.stock = max(0, product.stock - item['quantity'])
            
    db.session.commit()
    session.pop('cart', None)
    return redirect(url_for('main.pos'))
