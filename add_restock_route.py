with open("app/__init__.py", "r") as f:
    code = f.read()

restock_code = '''
    @app.route('/api/restock_product', methods=['POST'])
    def restock_product():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 403
        try:
            data = request.get_json() or {}
            product_id = data.get('product_id')
            qty = int(data.get('qty', 0))

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404

            if qty <= 0:
                return jsonify({"error": "Quantity must be greater than zero"}), 400

            product.main_stock = (product.main_stock or 0) + qty
            db.session.commit()
            
            return jsonify({
                "success": True, 
                "message": f"Successfully restocked {qty} units of {product.name}. New Main Stock: {product.main_stock}"
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

'''

if "restock_product" not in code:
    if "return app" in code:
        code = code.replace("    return app", restock_code + "\n    return app")
        with open("app/__init__.py", "w") as f:
            f.write(code)
        print("Successfully added restock_product route to app/__init__.py!")
    else:
        print("Could not find 'return app' in app/__init__.py")
else:
    print("restock_product route already exists!")
