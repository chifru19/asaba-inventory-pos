from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.models import Product, Sale
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main_bp.route('/checkout', methods=['POST'])
def checkout():
    # Gather items and calculate total from form submission
    total = float(request.form.get('total', 0))
    
    # Create and save Sale record
    new_sale = Sale(total_amount=total)
    db.session.add(new_sale)
    db.session.commit()
    
    return redirect(url_for('main.receipt'))

@main_bp.route('/receipt')
def receipt():
    sale = Sale.query.order_by(Sale.id.desc()).first()
    if not sale:
        flash('No recent sale found.', 'warning')
        return redirect(url_for('main.index'))
    return render_template('receipt.html', sale=sale)

@main_bp.route('/owner', methods=['GET', 'POST'])
def owner():
    if not session.get('owner_logged_in'):
        if request.method == 'POST':
            password = request.form.get('password')
            if password == 'admin123':
                session['owner_logged_in'] = True
                return redirect(url_for('main.owner'))
            else:
                flash('Incorrect password', 'danger')
        return render_template('owner_login.html')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_product':
            name = request.form.get('name')
            sku = request.form.get('sku')
            purchase_price = float(request.form.get('purchase_price', 0))
            selling_price = float(request.form.get('selling_price', 0))
            stock_quantity = int(request.form.get('stock_quantity', 0))
            
            new_product = Product(
                name=name,
                sku=sku,
                purchase_price=purchase_price,
                selling_price=selling_price,
                initial_stock=stock_quantity,
                stock_quantity=stock_quantity
            )
            db.session.add(new_product)
            db.session.commit()
            flash('New product added successfully!', 'success')
            
        elif action == 'update_product':
            product_id = request.form.get('product_id')
            product = Product.query.get(product_id)
            if product:
                product.selling_price = float(request.form.get('selling_price', product.selling_price))
                product.stock_quantity = int(request.form.get('stock_quantity', product.stock_quantity))
                db.session.commit()
                flash(f'Updated {product.name} successfully!', 'success')
                
        return redirect(url_for('main.owner'))

    products = Product.query.all()
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_sales = Sale.query.filter(Sale.timestamp >= today_start).all()
    return render_template('owner.html', products=products, today_sales=today_sales)

@main_bp.route('/owner/logout')
def owner_logout():
    session.pop('owner_logged_in', None)
    return redirect(url_for('main.owner'))
