# type: ignore
from functools import wraps
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app.models import db, Product, StoreStock, Sale, SaleItem, User
from datetime import datetime

main_bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Unauthorized'}), 401
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/restock', methods=['POST'])
@login_required
def restock_product():
    try:
        data = request.get_json(silent=True) or request.form
        product_id = data.get('product_id')
        qty = int(data.get('qty') or data.get('quantity') or 0)
        product = Product.query.get(product_id)
        if product:
            product.main_stock = (product.main_stock or 0) + qty
            db.session.commit()
            flash(f'Successfully restocked {qty} units of {product.name}!', 'success')
        else:
            flash('Product not found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error during restock: {str(e)}', 'danger')
    return redirect(url_for('main.owner_dashboard'))
@main_bp.route('/restock', methods=['POST'])
@login_required
def restock_product():
    try:
        data = request.get_json(silent=True) or request.form
        product_id = data.get('product_id')
        qty = int(data.get('qty') or data.get('quantity') or 0)
        product = Product.query.get(product_id)
        if product:
            product.main_stock = (product.main_stock or 0) + qty
            db.session.commit()
            flash(f'Successfully restocked {qty} units of {product.name}!', 'success')
        else:
            flash('Product not found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error during restock: {str(e)}', 'danger')
    return redirect(url_for('main.owner_dashboard'))
@login_required
def restock_product():
    try:
        data = request.get_json(silent=True) or request.form
        product_id = data.get('product_id')
        qty = int(data.get('qty') or data.get('quantity') or 0)
        product = Product.query.get(product_id)
        if product:
            product.main_stock = (product.main_stock or 0) + qty
            db.session.commit()
            flash(f'Restocked {qty} units!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'danger')
    return redirect(url_for('main.owner_dashboard'))
