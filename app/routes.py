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










@main_bp.route('/api/restock', methods=['GET', 'POST'])
@main_bp.route('/restock', methods=['GET', 'POST'])
@login_required
def restock_product():
    if request.method == 'GET':
        return redirect(url_for('main.owner_dashboard'))
    try:
        # Only call get_json if the request is actually JSON, avoiding 415 errors entirely
        if request.is_json:
            data = request.get_json(silent=True) or {}
        else:
            data = request.form or request.values or {}
            
        product_id = data.get('product_id')
        raw_qty = data.get('qty') or data.get('quantity') or 0
        qty = int(raw_qty) if str(raw_qty).strip() else 0
        
        if not product_id:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Product ID missing'}), 400
            flash('Product ID is missing.', 'danger')
            return redirect(url_for('main.owner_dashboard'))
            
        product = Product.query.get(product_id)
        if not product:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Product not found'}), 404
            flash('Product not found.', 'danger')
            return redirect(url_for('main.owner_dashboard'))
            
        product.main_stock = (product.main_stock or 0) + qty
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': f'Successfully restocked {qty} units of {product.name}!'})
            
        flash(f'Successfully restocked {qty} units of {product.name}!', 'success')
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        flash(f'Error during restock: {str(e)}', 'danger')
        
    return redirect(url_for('main.owner_dashboard'))
