import os

# 1. Update app/__init__.py so worker accounts are named shop1, shop2, shop3
init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

old_users = '''            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='worker_shop2').first():
                db.session.add(User(username='worker_shop2', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='worker_shop3').first():
                db.session.add(User(username='worker_shop3', password_hash=generate_password_hash('worker123'), role='worker'))'''

new_users = '''            if not User.query.filter_by(username='shop1').first():
                db.session.add(User(username='shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='shop2').first():
                db.session.add(User(username='shop2', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='shop3').first():
                db.session.add(User(username='shop3', password_hash=generate_password_hash('worker123'), role='worker'))'''

if old_users in code:
    code = code.replace(old_users, new_users)

# Also update POS route to determine store_id from username dynamically
old_pos = '''    @app.route('/pos')
    def pos():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        products = Product.query.all()
        return render_template('pos.html', products=products)'''

new_pos = '''    @app.route('/pos')
    def pos():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        products = Product.query.all()
        # Determine store name based on username (e.g. shop1, shop2, shop3)
        store_name = user.username.upper() if user and user.role == 'worker' else 'SHOP 1'
        return render_template('pos.html', products=products, store_name=store_name, username=user.username if user else 'shop1')'''

if old_pos in code:
    code = code.replace(old_pos, new_pos)

with open(init_path, "w") as f:
    f.write(code)

print("Updated backend store routing successfully!")

# 2. Update pos.html template to display the specific shop name and target the correct inventory column
pos_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>POS - Asaba {{ store_name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-stone-100 min-h-screen font-sans">
    <div class="max-w-7xl mx-auto p-4 md:p-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-6 bg-white p-5 rounded-2xl shadow-sm border border-stone-200">
            <div>
                <h1 class="text-xl font-black text-stone-800 tracking-tight">Asaba POS</h1>
                <p class="text-xs font-bold text-teal-800 uppercase tracking-widest mt-0.5">Point of Sale — {{ store_name }}</p>
            </div>
            <a href="/logout" class="bg-red-100 text-red-700 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider hover:bg-red-200 transition">Logout</a>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Inventory Catalog -->
            <div class="lg:col-span-2 bg-white rounded-2xl shadow-xl border border-stone-200 p-6">
                <h2 class="text-lg font-black text-stone-800 uppercase tracking-wider mb-4">Inventory Catalog ({{ store_name }})</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[650px] overflow-y-auto pr-2">
                    {% for p in products %}
                    <div class="bg-stone-50 border border-stone-200 p-4 rounded-xl flex flex-col justify-between">
                        <div>
                            <h3 class="font-bold text-stone-800 text-sm">{{ p.name }}</h3>
                            <p class="text-xs text-stone-500 mt-1">Price: CFA {{ "{:,.0f}".format(p.price) }}</p>
                            <p class="text-xs font-semibold text-teal-700 mt-0.5">Stock Available: 
                                <span id="stock-{{ p.id }}">
                                    {% if username == 'shop2' %}
                                        {{ p.shop2_stock }}
                                    {% elif username == 'shop3' %}
                                        {{ p.shop3_stock }}
                                    {% else %}
                                        {{ p.shop1_stock }}
                                    {% endif %}
                                </span>
                            </p>
                        </div>
                        <div class="mt-4 flex items-center gap-2">
                            <input type="number" id="qty-{{ p.id }}" min="1" value="1" class="w-16 px-3 py-2 rounded-lg border border-stone-200 bg-white text-xs font-bold text-center">
                            <button onclick="addToSale({{ p.id }}, '{{ p.name }}', {{ p.price }})" class="flex-1 bg-teal-950 text-white py-2 px-3 rounded-lg font-bold uppercase text-[10px] tracking-wider hover:bg-teal-900 transition">
                                + Add to Sale
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Current Sale Cart -->
            <div class="bg-white rounded-2xl shadow-xl border border-stone-200 p-6 flex flex-col justify-between">
                <div>
                    <h2 class="text-lg font-black text-stone-800 uppercase tracking-wider mb-4">Current Sale</h2>
                    <div id="cartItems" class="space-y-3 mb-4 max-h-[350px] overflow-y-auto pr-1">
                        <p class="text-stone-400 text-xs italic">No items added yet.</p>
                    </div>
                </div>

                <div>
                    <div class="border-t border-stone-200 pt-4 mb-4 flex justify-between items-center">
                        <span class="font-bold text-stone-600 uppercase text-xs">Total:</span>
                        <span id="cartTotal" class="text-xl font-black text-teal-950">CFA 0</span>
                    </div>
                    <button onclick="completeSale()" class="w-full bg-emerald-700 text-white py-3 rounded-xl font-bold uppercase text-xs tracking-wider hover:bg-emerald-800 transition shadow-md">
                        Complete Sale & Print Receipt
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
    let cart = [];
    const currentShop = "{{ username }}";

    function addToSale(id, name, price) {
        const qtyInput = document.getElementById(`qty-${id}`);
        const qty = parseInt(qtyInput.value) || 1;
        
        const existing = cart.find(item => item.id === id);
        if (existing) {
            existing.qty += qty;
        } else {
            cart.push({ id: id, name: name, price: price, qty: qty });
        }
        renderCart();
    }

    function renderCart() {
        const container = document.getElementById("cartItems");
        const totalContainer = document.getElementById("cartTotal");
        
        if (cart.length === 0) {
            container.innerHTML = '<p class="text-stone-400 text-xs italic">No items added yet.</p>';
            totalContainer.innerText = "CFA 0";
            return;
        }

        let html = "";
        let total = 0;
        cart.forEach((item, index) => {
            const subtotal = item.price * item.qty;
            total += subtotal;
            html += `
                <div class="flex justify-between items-center bg-stone-50 p-3 rounded-xl border border-stone-200 text-xs">
                    <div>
                        <p class="font-bold text-stone-800">${item.name}</p>
                        <p class="text-stone-500">${item.qty} x CFA ${item.price.toLocaleString()}</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <span class="font-bold text-teal-900">CFA ${subtotal.toLocaleString()}</span>
                        <button onclick="removeFromCart(${index})" class="text-red-500 font-bold hover:text-red-700">✕</button>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
        totalContainer.innerText = `CFA ${total.toLocaleString()}`;
    }

    function removeFromCart(index) {
        cart.splice(index, 1);
        renderCart();
    }

    function completeSale() {
        if (cart.length === 0) {
            alert("Cart is empty!");
            return;
        }

        const total = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);

        fetch("/api/sales", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ items: cart, total: total, shop: currentShop })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Sale completed successfully!");
                location.reload();
            } else {
                alert("Error: " + (data.error || "Sale failed"));
            }
        })
        .catch(err => alert("Connection error during checkout."));
    }
    </script>
</body>
</html>
'''

with open("app/templates/pos.html", "w") as f:
    f.write(pos_html)

print("Updated POS template successfully!")
