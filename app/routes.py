from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Product, Sale, SaleItem

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    today = date.today()
    # Daily sales calculation
    todays_sales = Sale.query.filter(db.func.date(Sale.created_at) == today).all()
    total_sales_today = sum(sale.total_amount for sale in todays_sales)
    
    # Reorder alerts (stock <= min_threshold)
    reorder_products = Product.query.filter(Product.stock_quantity <= Product.min_threshold).all()
    
    total_products = Product.query.count()
    
    return render_template('dashboard.html', 
                           total_sales_today=total_sales_today, 
                           todays_sales=todays_sales,
                           reorder_products=reorder_products,
                           total_products=total_products)

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        name = request.form.get('name')
        sku = request.form.get('sku')
        purchase_price = float(request.form.get('purchase_price'))
        selling_price = float(request.form.get('selling_price'))
        stock_quantity = int(request.form.get('stock_quantity'))
        min_threshold = int(request.form.get('min_threshold', 5))
        
        new_product = Product(
            name=name,
            sku=sku,
            purchase_price=purchase_price,
            selling_price=selling_price,
            stock_quantity=stock_quantity,
            min_threshold=min_threshold
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('main.inventory'))
        
    products = Product.query.all()
    return render_template('inventory.html', products=products)

@bp.route('/pos', methods=['GET', 'POST'])
def pos():
    if request.method == 'POST':
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        
        product = Product.query.get_or_404(product_id)
        if product.stock_quantity < quantity:
            return "Not enough stock available!", 400
            
        # Deduct stock
        product.stock_quantity -= quantity
        
        # Create sale record
        total_amount = product.selling_price * quantity
        sale = Sale(total_amount=total_amount)
        db.session.add(sale)
        db.session.commit()
        
        # Create sale item
        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.selling_price
        )
        db.session.add(sale_item)
        db.session.commit()
        
        return redirect(url_for('main.dashboard'))
        
    products = Product.query.all()
    return render_template('pos.html', products=products)
