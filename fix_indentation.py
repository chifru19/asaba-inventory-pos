import re

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    content = f.read()

# Clean up any malformed allocate_stock route
content = re.sub(r'@app\.route\(\'/api/allocate_stock\'[\s\S]*?return jsonify\([^)]+\)\s*\n\s*', '', content)

# Correctly indented allocate_stock route
correct_route = '''
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

if "return app" in content:
    content = content.replace("return app", correct_route + "\n    return app")
    with open(init_path, "w") as f:
        f.write(content)
    print("Successfully fixed indentation and updated allocate_stock route!")
else:
    print("Could not find 'return app' in app/__init__.py")
