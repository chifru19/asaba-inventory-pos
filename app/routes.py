from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Product, Sale, SaleItem

def init_routes(app):
    @app.route('/')
    def index():
        products = Product.query.all()
        return render_template('index.html', products=products)

    @app.route('/owner', methods=['GET', 'POST'])
    def owner_dashboard():
        products = Product.query.all()
        sales = Sale.query.order_by(Sale.date_created.desc()).all()
        return render_template('owner.html', products=products, sales=sales)

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