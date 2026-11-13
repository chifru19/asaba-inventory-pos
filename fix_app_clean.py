import re

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# Remove all existing allocate_stock definitions to avoid duplicates or bad indents
code = re.sub(r'@app\.route\(\'/api/allocate_stock\'[\s\S]*?def allocate_stock\(\)[\s\S]*?(?=\n\s*@app\.route|\n\s*return app|\Z)', '', code)

# Clean up multiple consecutive newlines
code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)

clean_route = '''
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
    code = code.replace("return app", clean_route + "\n    return app")
    with open(init_path, "w") as f:
        f.write(code)
    print("Successfully rebuilt app/__init__.py with clean indentation!")
else:
    print("Error: Could not find 'return app' in app/__init__.py")
