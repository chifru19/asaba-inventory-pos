import re

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    content = f.read()

# Remove the incorrectly placed global route block if it exists at the bottom
content = re.sub(r'\n@app\.route\(\'/api/allocate_stock\'[\s\S]*?return jsonify\([^)]+\)\s*\n', '', content)

# Find where app is returned or near the end of create_app, and insert the route before 'return app'
allocate_code = '''
    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 401
        data = request.json
        product_id = data.get('product_id')
        shop = data.get('shop') # 'shop1', 'shop2', 'shop3'
        qty = int(data.get('qty', 0))
        return jsonify({"success": True, "message": f"Successfully allocated {qty} to {shop}"})
'''

if "def allocate_stock" not in content:
    if "return app" in content:
        content = content.replace("return app", allocate_code + "\n    return app")
        with open(init_path, "w") as f:
            f.write(content)
        print("Successfully repositioned allocate_stock route inside create_app()!")
    else:
        print("Could not find 'return app' in app/__init__.py")
else:
    print("allocate_stock is already defined.")
