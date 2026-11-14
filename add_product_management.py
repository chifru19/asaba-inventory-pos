import os

# 1. Update app/__init__.py to include product creation and deletion endpoints
init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# Add product CRUD routes before return app
crud_routes = '''
    @app.route('/api/products', methods=['POST'])
    def add_product():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 403
        try:
            data = request.get_json() or {}
            name = data.get('name')
            price = float(data.get('price', 0))
            main_stock = int(data.get('main_stock', 0))

            if not name or price <= 0:
                return jsonify({"error": "Invalid product name or price"}), 400

            new_prod = Product(
                name=name,
                price=price,
                main_stock=main_stock,
                shop1_stock=0,
                shop2_stock=0,
                shop3_stock=0,
                store_id='shop1'
            )
            db.session.add(new_prod)
            db.session.commit()
            return jsonify({"success": True, "message": "Product added successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/api/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 403
        try:
            prod = Product.query.get(product_id)
            if not prod:
                return jsonify({"error": "Product not found"}), 404
            
            db.session.delete(prod)
            db.session.commit()
            return jsonify({"success": True, "message": "Product deleted successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return app
'''

code = code.replace("    return app", crud_routes)

with open(init_path, "w") as f:
    f.write(code)

print("Added product CRUD APIs to app/__init__.py!")
