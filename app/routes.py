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
    import json
    items_list = []
    total_val = 0.0

    products = Product.query.all()
    for product in products:
        qty_str = request.form.get(f'product_{product.id}', '0')
        try:
            qty = int(qty_str)
        except (ValueError, TypeError):
            qty = 0

        if qty > 0:
            product.stock_quantity = max(0, product.stock_quantity - qty)
            subtotal = float(product.selling_price) * qty
            total_val += subtotal
            items_list.append({
                "name": product.name,
                "price": float(product.selling_price),
                "quantity": qty,
                "subtotal": subtotal
            })

    if not items_list:
        total_val = float(request.form.get('total', 0.0))

    sale_items_json = json.dumps(items_list) if items_list else None
    new_sale = Sale(total_amount=total_val, items_sold=sale_items_json)
    db.session.add(new_sale)
    db.session.commit()
    return redirect(url_for('main.receipt', sale_id=new_sale.id))

@main_bp.route('/receipt')
def receipt():
    sale_id = request.args.get('sale_id')
    if sale_id:
        sale = Sale.query.get(sale_id)
    else:
        sale = Sale.query.order_by(Sale.id.desc()).first()
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

@main_bp.route('/owner/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if not session.get('owner_logged_in'):
        flash('Please log in first.', 'danger')
        return redirect(url_for('main.owner'))
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{product.name}" deleted successfully!', 'success')
    return redirect(url_for('main.owner'))

@main_bp.route('/owner/logout')
def owner_logout():
    session.pop('owner_logged_in', None)
    return redirect(url_for('main.owner'))

@main_bp.route('/sales-report')
def sales_report():
    sales = Sale.query.order_by(Sale.timestamp.desc()).all()
    total_revenue = sum(s.total_amount for s in sales)
    return render_template('sales_report.html', sales=sales, total_revenue=total_revenue)