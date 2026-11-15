import re

with open("app/__init__.py", "r") as f:
    code = f.read()

old_allocate = """def allocate_stock():
        try:
            data = request.get_json() or {}
            product_id = data.get('product_id')
            shop = data.get('shop')
            qty = int(data.get('qty', 0))

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404

            shop_attr = f"{shop}_stock"
            if not hasattr(product, shop_attr):
                return jsonify({"error": "Invalid shop target"}), 400

            current_shop_stk = getattr(product, shop_attr, 0) or 0
            setattr(product, shop_attr, current_shop_stk + qty)

            db.session.commit()
            return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()}!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500"""

new_allocate = """def allocate_stock():
        try:
            data = request.get_json() or {}
            product_id = data.get('product_id')
            shop = data.get('shop')
            qty = int(data.get('qty', 0))

            if qty <= 0:
                return jsonify({"error": "Transfer quantity must be greater than zero."}), 400

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404

            if product.main_stock < qty:
                return jsonify({"error": f"Insufficient main stock! Available: {product.main_stock}"}), 400

            shop_attr = f"{shop}_stock"
            if not hasattr(product, shop_attr):
                return jsonify({"error": "Invalid shop target"}), 400

            # Deduct from central main stock and add to target shop stock
            product.main_stock -= qty
            current_shop_stk = getattr(product, shop_attr, 0) or 0
            setattr(product, shop_attr, current_shop_stk + qty)

            db.session.commit()
            return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()}! Main stock updated."})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500"""

if old_allocate in code:
    code = code.replace(old_allocate, new_allocate)
    with open("app/__init__.py", "w") as f:
        f.write(code)
    print("Successfully updated allocate_stock route in app/__init__.py!")
else:
    print("Could not find exact allocate_stock block to replace.")
