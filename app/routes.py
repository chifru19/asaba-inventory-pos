from flask import render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Product, Sale, SaleItem

def init_routes(app):
    @app.route('/')
    def index():
        products = Product.query.all()
        return render_template('index.html', products=products)

    @app.route('/owner', methods=['GET', 'POST'])
    def owner_dashboard():
        error = None
        if request.method == 'POST':
            password = request.form.get('password')
            if password == 'asaba2026owner':
                session['is_owner'] = True
                return redirect(url_for('owner_dashboard'))
            else:
                error = 'Invalid password. Access denied.'

        products = Product.query.all()
        sales = Sale.query.order_by(Sale.date_created.desc()).all()
        return render_template('owner.html', products=products, sales=sales, error=error)

    @app.route('/owner/add', methods=['POST'])
    def add_product():
        if not session.get('is_owner'):
            return redirect(url_for('owner_dashboard'))

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
            stock_quantity=stock_quantity,
            min_threshold=5
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('owner_dashboard'))

    @app.route('/owner/logout')
    def owner_logout():
        session.pop('is_owner', None)
        return redirect(url_for('owner_dashboard'))

    @app.route('/checkout', methods=['POST'])
    def checkout():
        # Create a new Sale record
        new_sale = Sale(total_amount=0.0)
        db.session.add(new_sale)
        db.session.flush() # Get the new_sale.id

        total_sale_amount = 0.0

        for key, value in request.form.items():
            if key.startswith('product_'):
                product_id = int(key.split('_')[1])
                qty_sold = int(value)

                if qty_sold > 0:
                    product = Product.query.get(product_id)
                    if product and product.stock_quantity >= qty_sold:
                        # Deduct stock
                        product.stock_quantity -= qty_sold
                        item_total = product.selling_price * qty_sold
                        total_sale_amount += item_total

                        # Record sale item
                        sale_item = SaleItem(
                            sale_id=new_sale.id,
                            product_id=product.id,
                            quantity=qty_sold,
                            price=product.selling_price
                        )
                        db.session.add(sale_item)

        new_sale.total_amount = total_sale_amount
        db.session.commit()
        return redirect(url_for('index'))