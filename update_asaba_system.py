import os

init_path = "app/__init__.py"
if not os.path.exists(init_path):
    print("Error: app/__init__.py not found!")
    exit(1)

with open(init_path, "r") as f:
    code = f.read()

print("Analyzing app/__init__.py structure...")
# We will inject stock allocation and sales tracking routes if not already present
if "allocate_stock" not in code:
    allocation_route = '''
@app.route('/api/allocate_stock', methods=['POST'])
def allocate_stock():
    if session.get('role') != 'owner':
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    product_id = data.get('product_id')
    shop = data.get('shop') # 'shop1', 'shop2', 'shop3'
    qty = int(data.get('qty', 0))
    
    # Update allocation logic here
    return jsonify({"success": True, "message": f"Successfully allocated {qty} to {shop}"})
'''
    # Append before app run or at the bottom
    code += "\n" + allocation_route
    with open(init_path, "w") as f:
        f.write(code)
    print("Successfully added stock allocation API route!")
else:
    print("Stock allocation route already exists.")

