import re

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    lines = f.readlines()

new_lines = []
inside_bad_route = False

for line in lines:
    # If we encounter the allocate_stock route, we want to strip leading whitespace from top-level definitions
    if "@app.route('/api/allocate_stock'" in line or "def allocate_stock():" in line:
        new_lines.append(line.lstrip())
    elif inside_bad_route and line.strip() == "":
        new_lines.append(line)
    else:
        new_lines.append(line)

# Let's do a complete clean rewrite of app/__init__.py to ensure zero indentation issues
with open(init_path, "r") as f:
    content = f.read()

# Remove any existing allocate_stock function entirely using regex
content = re.sub(r'([ \t]*)(@app\.route\(\'/api/allocate_stock\'[\s\S]*?)(?=\n@app\.route|\ndef |\nif __name__|\Z)', '', content)
content = re.sub(r'([ \t]*)(def allocate_stock\(\)[\s\S]*?)(?=\n@app\.route|\ndef |\nif __name__|\Z)', '', content)

# Clean up multiple blank lines
content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

# Append the strictly zero-indented module-level route at the very end
perfect_route = '''
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

content = content.strip() + "\n" + perfect_route

with open(init_path, "w") as f:
    f.write(content)

print("Successfully rewrote app/__init__.py with strict zero indentation for module-level route!")
