from flask import render_template, request, redirect, url_for, flash, session
from app.models import Product, Sale, SaleItem
from app.extensions import db
from functools import wraps

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_owner'):
            flash('Owner access required.', 'danger')
            return redirect(url_for('owner_login'))
        return f(*args, **kwargs)
    return decorated_function

def init_routes(app):
    @app.route('/')
    def pos():
        products = Product.query.all()
        return render_template('pos.html', products=products)

    @app.route('/pos/checkout', methods=['POST'])
    def pos_checkout():
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        
        sale = Sale(total_amount=0.0)
        db.session.add(sale)
        total = 0.0
        items_sold = False

        for p_id, q_str in zip(product_ids, quantities):
            qty = int(q_str)
            if qty > 0:
                items_sold = True
                product = Product.query.get(int(p_id))
                if product:
                    if product.stock_quantity < qty:
                        flash(f'Insufficient stock for {product.name}. Available: {product.stock_quantity}', 'danger')
                        db.session.rollback()
                        return redirect(url_for('pos'))
                    
                    product.stock_quantity -= qty
                    line_total = product.selling_price * qty
                    total += line_total
                    
                    sale_item = SaleItem(
                        sale=sale,
                        product_id=product.id,
                        quantity=qty,
                        price_at_sale=product.selling_price
                    )
                    db.session.add(sale_item)
        
        if not items_sold:
            flash('No items selected for sale.', 'warning')
            db.session.rollback()
            return redirect(url_for('pos'))

        sale.total_amount = total
        db.session.commit()
        flash(f'Sale recorded successfully! Total: {total:,.2f}', 'success')
        return redirect(url_for('pos'))

    @app.route('/owner/login', methods=['GET', 'POST'])
    def owner_login():
        if request.method == 'POST':
            if request.form.get('passcode') == 'asaba2026owner':
                session['is_owner'] = True
                flash('Welcome, Owner!', 'success')
                return redirect(url_for('owner_dashboard'))
            flash('Incorrect passcode', 'danger')
        return render_template('owner_login.html')

    @app.route('/owner/logout')
    def owner_logout():
        session.pop('is_owner', None)
        flash('Logged out successfully.', 'info')
        return redirect(url_for('pos'))

    @app.route('/owner/dashboard')
    @owner_required
    def owner_dashboard():
        products = Product.query.all()
        return render_template('owner_dashboard.html', products=products)

    @app.route('/owner/product/add', methods=['POST'])
    @owner_required
    def owner_add_product():
        try:
            product = Product(
                name=request.form.get('name'),
                sku=request.form.get('sku'),
                purchase_price=float(request.form.get('purchase_price')),
                selling_price=float(request.form.get('selling_price')),
                stock_quantity=int(request.form.get('stock_quantity')),
                min_threshold=int(request.form.get('min_threshold', 3))
            )
            db.session.add(product)
            db.session.commit()
            flash('New product added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'danger')
        return redirect(url_for('owner_dashboard'))
