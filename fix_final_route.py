import re

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# 1. Remove all old allocate_stock blocks completely
code = re.sub(r'@app\.route\(\'/api/allocate_stock\'[\s\S]*?def allocate_stock\(\)[\s\S]*?(?=\n@app\.route|\ndef |\nif __name__|\Z)', '', code)
code = re.sub(r'def allocate_stock\(\)[\s\S]*?(?=\n@app\.route|\ndef |\nif __name__|\Z)', '', code)

# 2. Clean up extra blank lines
code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)

# 3. Add the clean module-level route at the very bottom of the file
clean_module_route = '''

@app.route('/api/allocate_stock', methods=['POST'])
def allocate_stock():
    try:
        data = request.json or {}
        product_id = int(data.get('product_id', 0))
        shop = data.get('shop', 'shop1')
        qty = int(data.get('qty', 0))
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
            
        main_stk = getattr(product, 'main_stock', getattr(product, 'stock', 0))
        if main_stk < qty:
            return jsonify({"error": f"Insufficient main stock ({main_stk} available)"}), 400
            
        if hasattr(product, 'main_stock'):
            product.main_stock = main_stk - qty
        elif hasattr(product, 'stock'):
            product.stock = main_stk - qty
            
        shop_attr = f"{shop}_stock"
        current_shop_stk = getattr(product, shop_attr, 0) or 0
        setattr(product, shop_attr, current_shop_stk + qty)
        
        db.session.commit()
        return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()}!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
'''

code += clean_module_route

with open(init_path, "w") as f:
    f.write(code)

print("Successfully placed allocate_stock at the module level!")
