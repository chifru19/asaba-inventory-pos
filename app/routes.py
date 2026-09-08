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
