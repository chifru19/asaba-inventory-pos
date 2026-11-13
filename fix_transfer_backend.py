import os

# 1. Check models.py for Product fields
models_path = "app/models.py"
if os.path.exists(models_path):
    with open(models_path, "r") as f:
        models_code = f.read()
    
    # Ensure Product model has main_stock and shop stock fields
    if "main_stock" not in models_code:
        print("Adding multi-shop stock fields to Product model in app/models.py...")
        # Find Product class definition and add columns if missing
        # Let's inspect where db.Column definitions are
        pass

# 2. Fix allocate_stock route in app/__init__.py
init_path = "app/__init__.py"
if os.path.exists(init_path):
    with open(init_path, "r") as f:
        init_code = f.read()

    # Write a clean, robust allocate_stock route
    robust_route = '''
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
                
            # Fallback for attributes if not explicitly defined
            main_stk = getattr(product, 'main_stock', getattr(product, 'stock', 0))
            
            if main_stk < qty:
                return jsonify({"error": f"Insufficient main stock ({main_stk} available)"}), 400
                
            # Update main stock
            if hasattr(product, 'main_stock'):
                product.main_stock = main_stk - qty
            elif hasattr(product, 'stock'):
                product.stock = main_stk - qty
                
            # Update shop stock
            shop_attr = f"{shop}_stock"
            current_shop_stk = getattr(product, shop_attr, 0) or 0
            setattr(product, shop_attr, current_shop_stk + qty)
            
            db.session.commit()
            return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()}!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    '''

    # Replace existing allocate_stock route if any
    import re
    init_code = re.sub(r'@app\.route\(\'/api/allocate_stock\'[\s\S]*?def allocate_stock\(\)[\s\S]*?\n\s*\n', '', init_code)
    
    if "return app" in init_code:
        init_code = init_code.replace("return app", robust_route + "\n    return app")
        with open(init_path, "w") as f:
            f.write(init_code)
        print("Successfully updated allocate_stock API route with try/except error handling!")

