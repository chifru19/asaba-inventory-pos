from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.extensions import db
from app.models import User, Product, Sale

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'owner':
            return redirect(url_for('main.owner_dashboard'))
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
            
            if user.role == 'owner':
                return jsonify({'status': 'success', 'redirect': url_for('main.owner_dashboard')})
            else:
                return jsonify({'status': 'success', 'redirect': url_for('main.pos')})
                
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main_bp.route('/pos')
def pos():
    if 'user_id' not in session or session.get('role') != 'worker':
        return redirect(url_for('main.login'))
    store_id = session.get('store_id')
    products = Product.query.filter_by(store_id=store_id).all()
    return render_template('pos.html', products=products, store_id=store_id)

@main_bp.route('/owner')
def owner_dashboard():
    if 'user_id' not in session or session.get('role') != 'owner':
        return redirect(url_for('main.login'))
    
    selected_store = request.args.get('store_id', 'shop1')
    products = Product.query.filter_by(store_id=selected_store).all()
    sales = Sale.query.filter_by(store_id=selected_store).all()
    total_sales = sum(s.total_amount for s in sales)
    
    return render_template('owner.html', products=products, sales=sales, total_sales=total_sales, selected_store=selected_store)

@main_bp.route('/api/sell', methods=['POST'])
def api_sell():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json()
    items = data.get('items', []) # List of {product_id, quantity}
    store_id = session.get('store_id')
    
    if session.get('role') == 'owner':
        store_id = data.get('store_id', 'shop1')

    total_amount = 0
    sale_items = []

    for item in items:
        product = Product.query.filter_by(id=item['product_id'], store_id=store_id).first()
        if not product or product.stock < item['quantity']:
            return jsonify({'error': f'Insufficient stock or product not found'}), 400
        
        product.stock -= item['quantity']
        subtotal = product.price * item['quantity']
        total_amount += subtotal

    new_sale = Sale(total_amount=total_amount, store_id=store_id, user_id=session['user_id'])
    db.session.add(new_sale)
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
