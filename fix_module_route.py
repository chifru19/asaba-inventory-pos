import re

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# Remove all occurrences of allocate_stock
code = re.sub(r'@app\.route\(\'/api/allocate_stock\'[\s\S]*?def allocate_stock\(\)[\s\S]*?(?=\n\s*@app\.route|\n\s*def |\n\s*if __name__|\Z)', '', code)

# Clean up extra blank lines
code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)

# Define allocate_stock correctly as a standalone route right before 'return app'
standalone_route = '''
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

if "return app" in code:
    # Place it right before return app with zero indentation (module level)
    code = code.replace("return app", standalone_route + "\n    return app")
    with open(init_path, "w") as f:
        f.write(code)
    print("Successfully moved allocate_stock to module level!")
else:
    print("Error: Could not find 'return app'")
