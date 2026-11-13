import os

init_path = "app/__init__.py" if os.path.exists("app/__init__.py") else "app.py"
with open(init_path, "r") as f:
    code = f.read()

# Ensure the allocate_stock route properly subtracts from main stock and adds to the target shop
new_route = '''
    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 401
        data = request.json
        product_id = data.get('product_id')
        shop = data.get('shop') # 'shop1', 'shop2', 'shop3'
        qty = int(data.get('qty', 0))
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}}, 404
            
        main_stk = getattr(product, 'main_stock', product.stock)
        if main_stk < qty:
            return jsonify({"error": "Insufficient main stock for transfer"}), 400
            
        # Deduct from main stock and add to target shop
        product.main_stock = main_stk - qty
        if shop == 'shop1':
            product.shop1_stock = getattr(product, 'shop1_stock', 0) + qty
        elif shop == 'shop2':
            product.shop2_stock = getattr(product, 'shop2_stock', 0) + qty
        elif shop == 'shop3':
            product.shop3_stock = getattr(product, 'shop3_stock', 0) + qty
            
        db.session.commit()
        return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop}!"})
'''

if "def allocate_stock" in code:
    # Replace existing route with robust version
    import re
    code = re.sub(r'@app\.route\(\'/api/allocate_stock\'[\s\S]*?return jsonify\([^)]+\)\s*\n\s*', '', code)

if "return app" in code:
    code = code.replace("return app", new_route + "\n    return app")
    with open(init_path, "w") as f:
        f.write(code)
    print("Successfully updated backend stock transfer logic!")

