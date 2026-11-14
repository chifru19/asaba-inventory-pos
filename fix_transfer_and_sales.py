import os

# 1. Update app/__init__.py for proper stock deduction and daily sales calculation
init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# Replace allocate_stock route
old_allocate = '''    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
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
            return jsonify({"error": str(e)}), 500'''

new_allocate = '''    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
        try:
            data = request.get_json() or {}
            product_id = data.get('product_id')
            shop = data.get('shop') # 'shop1', 'shop2', 'shop3'
            qty = int(data.get('qty', 0))

            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404

            main_stk = getattr(product, 'main_stock', 0) or 0
            if main_stk < qty:
                return jsonify({"error": "Insufficient main stock for transfer!"}), 400

            shop_attr = f"{shop}_stock"
            if not hasattr(product, shop_attr):
                return jsonify({"error": "Invalid shop target"}), 400

            # Deduct from main and add to shop
            product.main_stock = main_stk - qty
            current_shop_stk = getattr(product, shop_attr, 0) or 0
            setattr(product, shop_attr, current_shop_stk + qty)

            db.session.commit()
            return jsonify({"success": True, "message": f"Successfully transferred {qty} units to {shop.upper()} from Main Stock!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500'''

if old_allocate in code:
    code = code.replace(old_allocate, new_allocate)

# Update owner_dashboard route to pass daily sales/revenue
old_owner = '''    @app.route('/owner')
    def owner_dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        products = Product.query.all()
        return render_template('owner_dashboard.html', products=products)'''

new_owner = '''    @app.route('/owner')
    def owner_dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        products = Product.query.all()
        
        today = date.today()
        sales_today = Sale.query.filter(db.func.date(Sale.created_at) == today).all()
        
        shop_sales = {'shop1': 0, 'shop2': 0, 'shop3': 0}
        shop_revenue = {'shop1': 0.0, 'shop2': 0.0, 'shop3': 0.0}
        
        for s in sales_today:
            s_shop = getattr(s, 'store_id', 'shop1')
            if s_shop in shop_sales:
                shop_sales[s_shop] += 1
                shop_revenue[s_shop] += float(s.total_amount or 0)

        return render_template('owner_dashboard.html', products=products, shop_sales=shop_sales, shop_revenue=shop_revenue)'''

if old_owner in code:
    code = code.replace(old_owner, new_owner)

with open(init_path, "w") as f:
    f.write(code)

print("Updated app/__init__.py successfully!")

# 2. Update owner_dashboard.html to display daily sales/revenue metrics
dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Owner Dashboard - Asaba POS</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-stone-100 min-h-screen font-sans">
    <div class="max-w-7xl mx-auto p-4 md:p-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-6 bg-white p-5 rounded-2xl shadow-sm border border-stone-200">
            <h1 class="text-xl font-black text-stone-800 tracking-tight">Owner Dashboard (Multi-Store Admin)</h1>
            <a href="/logout" class="bg-red-100 text-red-700 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider hover:bg-red-200 transition">Logout</a>
        </div>

        <!-- Daily Sales Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
                <h3 class="text-xs font-black uppercase text-stone-400 tracking-wider">Shop 1 Sales Today</h3>
                <p class="text-2xl font-black text-teal-900 mt-2">{{ shop_sales.get('shop1', 0) }} orders</p>
                <p class="text-sm font-bold text-stone-600 mt-1">Revenue: XAF {{ "{:,.0f}".format(shop_revenue.get('shop1', 0)) }}</p>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
                <h3 class="text-xs font-black uppercase text-stone-400 tracking-wider">Shop 2 Sales Today</h3>
                <p class="text-2xl font-black text-teal-900 mt-2">{{ shop_sales.get('shop2', 0) }} orders</p>
                <p class="text-sm font-bold text-stone-600 mt-1">Revenue: XAF {{ "{:,.0f}".format(shop_revenue.get('shop2', 0)) }}</p>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
                <h3 class="text-xs font-black uppercase text-stone-400 tracking-wider">Shop 3 Sales Today</h3>
                <p class="text-2xl font-black text-teal-900 mt-2">{{ shop_sales.get('shop3', 0) }} orders</p>
                <p class="text-sm font-bold text-stone-600 mt-1">Revenue: XAF {{ "{:,.0f}".format(shop_revenue.get('shop3', 0)) }}</p>
            </div>
        </div>

        <!-- Central Stock Transfer to Shops Widget -->
        <div class="bg-white rounded-2xl shadow-xl border border-stone-200 p-6 mb-6">
            <h3 class="text-lg font-black text-stone-800 uppercase tracking-wider mb-2">📦 Central Stock Transfer to Shops</h3>
            <p class="text-xs text-stone-500 mb-4">Select an item from main inventory, deduct from warehouse, and instantly distribute quantities to Shop 1, Shop 2, or Shop 3.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                <div>
                    <label class="block text-xs font-bold uppercase text-stone-600 mb-1">Select Product</label>
                    <select id="transferProductId" class="w-full px-4 py-3 rounded-xl border border-stone-200 bg-stone-50 text-sm font-semibold text-stone-800">
                        {% for p in products %}
                        <option value="{{ p.id }}">{{ p.name }} (Main: {{ p.main_stock }})</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-stone-600 mb-1">Destination Shop</label>
                    <select id="transferShop" class="w-full px-4 py-3 rounded-xl border border-stone-200 bg-stone-50 text-sm font-semibold text-stone-800">
                        <option value="shop1">Shop 1</option>
                        <option value="shop2">Shop 2</option>
                        <option value="shop3">Shop 3</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-stone-600 mb-1">Quantity to Transfer</label>
                    <input type="number" id="transferQty" min="1" value="10" class="w-full px-4 py-3 rounded-xl border border-stone-200 bg-stone-50 text-sm font-semibold text-stone-800">
                </div>
                <div>
                    <button onclick="executeStockTransfer()" class="w-full bg-teal-950 text-white py-3 rounded-xl font-bold uppercase text-xs tracking-wider hover:bg-teal-900 transition shadow-md">
                        Transfer Stock ➔
                    </button>
                </div>
            </div>
        </div>

        <!-- Central Stock & Multi-Shop Allocation Table -->
        <div class="overflow-x-auto bg-white rounded-2xl shadow-xl border border-stone-200 p-6">
            <h3 class="text-lg font-black text-stone-800 uppercase tracking-wider mb-4">Central Stock & Multi-Shop Allocation</h3>
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="border-b border-stone-200 text-[10px] uppercase tracking-widest text-stone-500">
                        <th class="py-3 px-4">Item Name</th>
                        <th class="py-3 px-4">Main Stock</th>
                        <th class="py-3 px-4">Price (XAF)</th>
                        <th class="py-3 px-4 text-teal-700">Shop 1 Stock</th>
                        <th class="py-3 px-4 text-teal-700">Shop 2 Stock</th>
                        <th class="py-3 px-4 text-teal-700">Shop 3 Stock</th>
                        <th class="py-3 px-4">Action</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-stone-100 text-sm">
                    {% for p in products %}
                    <tr>
                        <td class="py-4 px-4 font-bold text-stone-800">{{ p.name }}</td>
                        <td class="py-4 px-4 font-semibold text-stone-600">{{ p.main_stock }}</td>
                        <td class="py-4 px-4 font-semibold text-stone-600">{{ "{:,.0f}".format(p.price) }}</td>
                        <td class="py-4 px-4 font-bold text-teal-900">{{ p.shop1_stock }}</td>
                        <td class="py-4 px-4 font-bold text-teal-900">{{ p.shop2_stock }}</td>
                        <td class="py-4 px-4 font-bold text-teal-900">{{ p.shop3_stock }}</td>
                        <td class="py-4 px-4">
                            <button onclick="executeStockTransferModal({{ p.id }})" class="bg-teal-950 text-white px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider hover:bg-teal-900 transition">Share Stock</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
    function executeStockTransfer() {
        const productId = document.getElementById("transferProductId").value;
        const shop = document.getElementById("transferShop").value;
        const qty = parseInt(document.getElementById("transferQty").value);

        fetch("/api/allocate_stock", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ product_id: productId, shop: shop, qty: qty })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert("Error: " + (data.error || "Transfer failed"));
            }
        })
        .catch(err => alert("Connection error during transfer."));
    }

    function executeStockTransferModal(productId) {
        document.getElementById("transferProductId").value = productId;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    </script>
</body>
</html>
'''

with open("app/templates/owner_dashboard.html", "w") as f:
    f.write(dashboard_html)

print("Updated owner_dashboard.html successfully!")
