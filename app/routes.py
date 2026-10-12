from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.models import Product, Sale
from datetime import datetime

bp = Blueprint('main', __name__)

OWNER_PASSWORD = "asaba123"

@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@bp.route('/checkout', methods=['POST'])
def checkout():
    total_amount = 0
    sale_items = []

    for key, value in request.form.items():
        if key.startswith('product_'):
            try:
                qty = int(value)
                if qty > 0:
                    product_id = int(key.split('_')[1])
                    product = Product.query.get(product_id)
                    if product and product.stock_quantity >= qty:
                        product.stock_quantity -= qty
                        item_total = product.selling_price * qty
                        total_amount += item_total
                        sale_items.append(f"{product.name} (x{qty})")
            except (ValueError, TypeError):
                continue

    if total_amount > 0:
        db.session.commit()
        # Log sale record
        new_sale = Sale(total_amount=total_amount, items_sold=", ".join(sale_items), timestamp=datetime.utcnow())
        db.session.add(new_sale)
        db.session.commit()

    return redirect(url_for('main.index'))

@bp.route('/owner', methods=['GET', 'POST'])
def owner():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == OWNER_PASSWORD:
            session['owner_logged_in'] = True
            return redirect(url_for('main.owner'))
        else:
            return render_template('owner_login.html', error="Invalid password. Please try again.")

    if not session.get('owner_logged_in'):
        return render_template('owner_login.html')

    products = Product.query.all()
    
    # Calculate today's revenue and transactions
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_sales = Sale.query.filter(Sale.timestamp >= today_start).all()
    
    today_revenue = sum(s.total_amount for s in today_sales)
    today_transactions_count = len(today_sales)

    return render_template('owner.html', products=products, today_revenue=today_revenue, today_transactions_count=today_transactions_count)

@bp.route('/owner/logout')
def owner_logout():
    session.pop('owner_logged_in', None)
    return redirect(url_for('main.owner'))
