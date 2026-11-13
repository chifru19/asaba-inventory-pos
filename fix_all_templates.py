import os

owner_dashboard_code = '''<!DOCTYPE html>
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

        <!-- Central Stock Transfer to Shops Widget -->
        <div class="bg-white rounded-2xl shadow-xl border border-stone-200 p-6 mb-6">
            <h3 class="text-lg font-black text-stone-800 uppercase tracking-wider mb-2">📦 Central Stock Transfer to Shops</h3>
            <p class="text-xs text-stone-500 mb-4">Select an item from main inventory and instantly distribute quantities to Shop 1, Shop 2, or Shop 3.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                <div>
                    <label class="block text-xs font-bold uppercase text-stone-600 mb-1">Select Product</label>
                    <select id="transferProductId" class="w-full px-4 py-3 rounded-xl border border-stone-200 bg-stone-50 text-sm font-semibold text-stone-800">
                        {% for p in products %}
                        <option value="{{ p.id }}">{{ p.name.replace("(SHOP1)", "").replace("(SHOP2)", "").replace("(SHOP3)", "").strip() }} (Main: {{ p.main_stock | default(p.stock, true) }})</option>
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
                        <th class="py-3 px-4 text-teal-700">Shop 1 (Stock / Sold)</th>
                        <th class="py-3 px-4 text-teal-700">Shop 2 (Stock / Sold)</th>
                        <th class="py-3 px-4 text-teal-700">Shop 3 (Stock / Sold)</th>
                        <th class="py-3 px-4">Action</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-stone-100 text-sm">
                    {% for p in products %}
                    <tr>
                        <td class="py-4 px-4 font-bold text-stone-800">{{ p.name.replace("(SHOP1)", "").replace("(SHOP2)", "").replace("(SHOP3)", "").strip() }}</td>
                        <td class="py-4 px-4 font-semibold text-stone-600">{{ p.main_stock | default(p.stock, true) }}</td>
                        <td class="py-4 px-4 font-semibold text-stone-600">{{ "{:,.0f}".format(p.price) }}</td>
                        <td class="py-4 px-4 font-bold text-teal-900">{{ p.shop1_stock | default(p.stock, true) }} / <span class="text-red-600">{{ p.shop1_sold | default(0) }} sold</span></td>
                        <td class="py-4 px-4 font-bold text-teal-900">{{ p.shop2_stock | default(0) }} / <span class="text-red-600">{{ p.shop2_sold | default(0) }} sold</span></td>
                        <td class="py-4 px-4 font-bold text-teal-900">{{ p.shop3_stock | default(0) }} / <span class="text-red-600">{{ p.shop3_sold | default(0) }} sold</span></td>
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

pos_html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asaba Ngu POS</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-stone-100 min-h-screen font-sans">
    <div class="max-w-7xl mx-auto p-4 md:p-8">
        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-center mb-6 bg-white p-5 rounded-2xl shadow-sm border border-stone-200">
            <h1 class="text-xl font-black text-stone-800 tracking-tight">Asaba Ngu POS</h1>
            <div class="flex space-x-6 text-xs font-bold uppercase tracking-widest text-stone-600 mt-3 md:mt-0">
                <a href="/owner_dashboard" class="hover:text-teal-950 transition">Dashboard</a>
                <a href="/inventory" class="hover:text-teal-950 transition">Inventory</a>
                <a href="/pos" class="text-teal-950 underline">Checkout (POS)</a>
            </div>
        </div>

        <!-- Layout Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Left 2 Columns: Products & Search -->
            <div class="lg:col-span-2 space-y-6">
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-stone-200">
                    <input type="text" id="searchInput" placeholder="Search items..." onkeyup="filterProducts()" class="w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:border-teal-900 text-sm bg-stone-50">
                </div>

                <!-- Product Cards Grid -->
                <div id="productGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {% for p in products %}
                    <div class="product-card bg-white p-5 rounded-2xl shadow-sm border border-stone-200 flex flex-col justify-between" data-name="{{ p.name | lower }}">
                        <div>
                            <h3 class="font-black text-stone-800 text-base mb-1">{{ p.name }}</h3>
                            <p class="text-xs text-stone-500 mb-1">Price: CFA {{ "{:,.1f}".format(p.price) }}</p>
                            <p class="text-xs font-bold text-teal-700 mb-4">Stock: {{ p.shop1_stock | default(p.stock, true) }}</p>
                        </div>
                        
                        <div class="space-y-3">
                            <!-- Plus & Minus Quantity Controls -->
                            <div class="flex items-center justify-between bg-stone-50 px-3 py-2 rounded-xl border border-stone-200">
                                <span class="text-xs font-bold text-stone-600">Qty:</span>
                                <div class="flex items-center space-x-2">
                                    <button type="button" onclick="adjustCardQty('{{ p.id }}', -1)" class="w-8 h-8 bg-red-100 text-red-700 font-black rounded-lg flex items-center justify-center hover:bg-red-200 transition text-sm">-</button>
                                    <input type="number" id="qty-{{ p.id }}" value="1" min="1" class="w-12 text-center font-bold text-stone-800 bg-white border border-stone-300 rounded-lg py-1 text-xs">
                                    <button type="button" onclick="adjustCardQty('{{ p.id }}', 1)" class="w-8 h-8 bg-teal-100 text-teal-900 font-black rounded-lg flex items-center justify-center hover:bg-teal-200 transition text-sm">+</button>
                                </div>
                            </div>
                            <button onclick="addToCart('{{ p.id }}', '{{ p.name }}', {{ p.price }})" class="w-full bg-teal-800 text-white py-3 rounded-xl font-bold uppercase text-[10px] tracking-widest hover:bg-teal-900 transition shadow-md">
                                Add to Sale
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Right Column: Sales Summary & Cart -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 sticky top-6">
                    <h3 class="text-lg font-black text-stone-800 uppercase tracking-wider mb-2">Current Sale</h3>
                    <div id="cartItems" class="space-y-2 mb-4 max-h-60 overflow-y-auto text-xs text-stone-700">
                        <p class="text-stone-400 italic">No items added yet.</p>
                    </div>
                    <p class="text-sm font-semibold text-stone-600 mb-6">Total: CFA <span id="cartTotal">0</span></p>
                    <button onclick="completeSale()" class="w-full bg-blue-600 text-white py-4 rounded-xl font-black uppercase text-xs tracking-widest hover:bg-blue-700 transition shadow-md mb-6">
                        Complete Sale
                    </button>
                    <hr class="border-stone-100 my-6">
                    <h4 class="text-sm font-black text-stone-800 uppercase tracking-wider mb-3">Sold Today</h4>
                    <p class="text-xs text-stone-400 italic">No sales recorded yet today.</p>
                </div>
            </div>
        </div>
    </div>

    <script>
    let cart = [];

    function adjustCardQty(itemId, change) {
        const input = document.getElementById('qty-' + itemId);
        let val = parseInt(input.value) || 1;
        val += change;
        if (val < 1) val = 1;
        input.value = val;
    }

    function addToCart(id, name, price) {
        const qtyInput = document.getElementById('qty-' + id);
        const qty = parseInt(qtyInput.value) || 1;
        
        const existing = cart.find(item => item.id === id);
        if (existing) {
            existing.qty += qty;
        } else {
            cart.push({ id, name, price, qty });
        }
        updateCartDisplay();
        qtyInput.value = 1;
    }

    function updateCartDisplay() {
        const container = document.getElementById('cartItems');
        const totalEl = document.getElementById('cartTotal');
        if (cart.length === 0) {
            container.innerHTML = '<p class="text-stone-400 italic">No items added yet.</p>';
            totalEl.innerText = '0';
            return;
        }

        let html = '';
        let total = 0;
        cart.forEach(item => {
            let itemTotal = item.price * item.qty;
            total += itemTotal;
            html += `<div class="flex justify-between items-center bg-stone-50 p-2 rounded-lg border border-stone-200">
                <div>
                    <span class="font-bold text-stone-800">${item.name}</span>
                    <p class="text-[10px] text-stone-500">${item.qty} x CFA ${item.price}</p>
                </div>
                <span class="font-bold text-teal-900">CFA ${itemTotal}</span>
            </div>`;
        });
        container.innerHTML = html;
        totalEl.innerText = total.toLocaleString();
    }

    function completeSale() {
        if (cart.length === 0) {
            alert("Cart is empty!");
            return;
        }
        alert("Sale completed successfully!");
        cart = [];
        updateCartDisplay();
    }

    function filterProducts() {
        let query = document.getElementById('searchInput').value.toLowerCase();
        let cards = document.getElementsByClassName('product-card');
        for (let card of cards) {
            let name = card.getAttribute('data-name');
            if (name.includes(query)) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }
        }
    }
    </script>
</body>
</html>
'''

os.makedirs("app/templates", exist_ok=True)
with open("app/templates/owner_dashboard.html", "w") as f:
    f.write(owner_dashboard_code)

with open("app/templates/pos.html", "w") as f:
    f.write(pos_html_code)

print("Successfully restored full templates for owner dashboard and POS!")
