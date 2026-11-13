import os

pos_html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asaba POS - Point of Sale</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-stone-100 min-h-screen font-sans">
    <!-- Navbar -->
    <nav class="bg-teal-950 text-white px-6 py-4 flex justify-between items-center shadow-md">
        <div class="flex items-center space-x-3">
            <span class="text-xl font-black tracking-wider uppercase">Asaba POS</span>
            <span class="bg-teal-800 text-teal-200 text-xs px-3 py-1 rounded-full font-semibold">Shop Worker</span>
        </div>
        <div class="flex items-center space-x-4">
            <a href="/logout" class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition shadow">Logout</a>
        </div>
    </nav>

    <!-- Main Container -->
    <div class="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Left 2 Columns: Product Catalog -->
        <div class="lg:col-span-2 space-y-6">
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-stone-200 flex items-center justify-between">
                <h2 class="text-lg font-black text-stone-800">Inventory Catalog</h2>
                <input type="text" id="searchInput" placeholder="Search products..." onkeyup="filterProducts()" class="px-4 py-2 bg-stone-50 border border-stone-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-800 w-64">
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="productGrid">
                {% for p in products %}
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-stone-200 flex flex-col justify-between product-card" 
                     data-name="{{ p.name | lower }}"
                     data-id="{{ p.id }}"
                     data-itemname="{{ p.name }}"
                     data-price="{{ p.price }}">
                    <div>
                        <h3 class="font-black text-stone-800 text-base mb-1">{{ p.name }}</h3>
                        <p class="text-xs text-stone-500 mb-1">Price: CFA {{ "{:,.0f}".format(p.price) }}</p>
                        <p class="text-xs font-bold text-teal-700 mb-4">Stock: {{ p.shop1_stock | default(p.stock, true) }}</p>
                    </div>

                    <div class="space-y-3">
                        <div class="flex items-center justify-between bg-stone-50 px-3 py-2 rounded-xl border border-stone-200">
                            <span class="text-xs font-bold text-stone-600">Qty:</span>
                            <div class="flex items-center space-x-2">
                                <button type="button" onclick="adjustQty(this, -1)" class="w-8 h-8 bg-red-100 text-red-700 font-black rounded-lg flex items-center justify-center hover:bg-red-200 transition text-sm">-</button>
                                <input type="number" value="1" min="1" class="item-qty-input w-12 text-center font-bold text-stone-800 bg-white border border-stone-300 rounded-lg text-sm">
                                <button type="button" onclick="adjustQty(this, 1)" class="w-8 h-8 bg-teal-100 text-teal-900 font-black rounded-lg flex items-center justify-center hover:bg-teal-200 transition text-sm">+</button>
                            </div>
                        </div>
                        <button onclick="addCardToCart(this)" class="w-full bg-teal-800 text-white py-3 rounded-xl font-bold uppercase text-[10px] tracking-widest hover:bg-teal-900 transition shadow-md">
                            Add to Sale
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Right Column: Cart & Sales Summary -->
        <div class="space-y-6">
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 sticky top-6">
                <h3 class="text-lg font-black text-stone-800 mb-4">Current Sale</h3>
                
                <div id="cartItems" class="space-y-3 mb-6 max-h-72 overflow-y-auto">
                    <p class="text-xs text-stone-400 italic">No items added yet.</p>
                </div>

                <div class="border-t border-stone-100 pt-4 mb-6">
                    <div class="flex justify-between items-center text-base font-black text-stone-800">
                        <span>Total:</span>
                        <span class="text-teal-900">CFA <span id="cartTotal">0</span></span>
                    </div>
                </div>

                <button onclick="completeSale()" class="w-full bg-blue-600 text-white py-4 rounded-xl font-black uppercase text-xs tracking-widest hover:bg-blue-700 transition shadow-md mb-4">
                    Complete Sale & Print Receipt
                </button>

                <hr class="border-stone-100 my-6">
                <h4 class="text-sm font-black text-stone-800 uppercase tracking-wider mb-3">Sold Today</h4>
                <div id="soldTodayContainer">
                    <p class="text-xs text-stone-400 italic">No sales recorded yet today.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Hidden Printable Receipt Template -->
    <div id="receiptModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white p-6 rounded-2xl max-w-sm w-full space-y-4 shadow-2xl">
            <div id="printableReceipt" class="p-4 text-stone-800 text-xs space-y-3 font-mono">
                <div class="text-center">
                    <h2 class="font-bold text-base uppercase">Asaba Inventory POS</h2>
                    <p class="text-[10px] text-stone-500">Official Sales Receipt</p>
                    <p class="text-[10px] text-stone-500" id="receiptDate"></p>
                </div>
                <div class="border-t border-dashed border-stone-400 my-2"></div>
                <div id="receiptItemsList" class="space-y-1"></div>
                <div class="border-t border-dashed border-stone-400 my-2"></div>
                <div class="flex justify-between font-bold text-sm">
                    <span>TOTAL:</span>
                    <span id="receiptTotal"></span>
                </div>
                <div class="text-center text-[10px] text-stone-500 mt-4">
                    <p>Thank you for your patronage!</p>
                </div>
            </div>
            <div class="flex space-x-3">
                <button onclick="window.print()" class="flex-1 bg-teal-900 text-white py-2 rounded-xl font-bold uppercase text-xs hover:bg-teal-800 transition">Print</button>
                <button onclick="closeReceipt()" class="flex-1 bg-stone-200 text-stone-800 py-2 rounded-xl font-bold uppercase text-xs hover:bg-stone-300 transition">Close</button>
            </div>
        </div>
    </div>

    <script>
    function adjustQty(btn, change) {
        let card = btn.closest('.product-card');
        let input = card.querySelector('.item-qty-input');
        if (!input) return;
        let val = parseInt(input.value) || 1;
        val += change;
        if (val < 1) val = 1;
        input.value = val;
    }

    let cart = [];

    function addCardToCart(btn) {
        let card = btn.closest('.product-card');
        let id = parseInt(card.getAttribute('data-id'));
        let name = card.getAttribute('data-itemname');
        let price = parseFloat(card.getAttribute('data-price'));
        let input = card.querySelector('.item-qty-input');
        let qty = input ? parseInt(input.value) || 1 : 1;
        
        let existing = cart.find(item => item.id === id);
        if (existing) {
            existing.qty += qty;
        } else {
            cart.push({ id: id, name: name, price: price, qty: qty });
        }
        updateCart();
    }

    function updateCartItemQty(id, change) {
        let item = cart.find(i => i.id === id);
        if (item) {
            item.qty += change;
            if (item.qty <= 0) {
                cart = cart.filter(i => i.id !== id);
            }
        }
        updateCart();
    }

    function removeFromCart(id) {
        cart = cart.filter(i => i.id !== id);
        updateCart();
    }

    function updateCart() {
        let container = document.getElementById('cartItems');
        let totalEl = document.getElementById('cartTotal');
        if (!container || !totalEl) return;
        
        if (cart.length === 0) {
            container.innerHTML = '<p class="text-xs text-stone-400 italic">No items added yet.</p>';
            totalEl.innerText = '0';
            return;
        }

        let html = '';
        let total = 0;
        cart.forEach(item => {
            let itemTotal = item.price * item.qty;
            total += itemTotal;
            html += `<div class="bg-stone-50 p-3 rounded-xl border border-stone-200 flex flex-col space-y-2 mb-2">
                <div class="flex justify-between items-center">
                    <span class="font-bold text-stone-800 text-xs">${item.name}</span>
                    <button onclick="removeFromCart(${item.id})" class="text-red-500 hover:text-red-700 font-bold text-xs">✕</button>
                </div>
                <div class="flex justify-between items-center">
                    <div class="flex items-center space-x-1">
                        <button onclick="updateCartItemQty(${item.id}, -1)" class="w-6 h-6 bg-red-100 text-red-700 font-black rounded flex items-center justify-center text-xs">-</button>
                        <span class="w-8 text-center font-bold text-xs">${item.qty}</span>
                        <button onclick="updateCartItemQty(${item.id}, 1)" class="w-6 h-6 bg-teal-100 text-teal-900 font-black rounded flex items-center justify-center text-xs">+</button>
                    </div>
                    <span class="font-bold text-teal-900 text-xs">CFA ${itemTotal.toLocaleString()}</span>
                </div>
            </div>`;
        });
        container.innerHTML = html;
        totalEl.innerText = total.toLocaleString();
    }

    function loadTodaySales() {
        fetch('/api/sales', { credentials: 'include' })
        .then(res => res.json())
        .then(sales => {
            let soldTodayContainer = document.getElementById('soldTodayContainer');
            if (!soldTodayContainer) return;
            
            if (!sales || sales.length === 0) {
                soldTodayContainer.innerHTML = '<p class="text-xs text-stone-400 italic">No sales recorded yet today.</p>';
                return;
            }

            let html = '<div class="space-y-3 max-h-60 overflow-y-auto">';
            sales.forEach(s => {
                html += `<div class="bg-stone-50 p-3 rounded-xl border border-stone-200 text-xs">
                    <div class="flex justify-between font-bold text-stone-800 mb-1">
                        <span>Sale #${s.id}</span>
                        <span class="text-teal-900">CFA ${s.total.toLocaleString()}</span>
                    </div>
                    <p class="text-[10px] text-stone-500">${s.timestamp} (${s.shop})</p>
                </div>`;
            });
            html += '</div>';
            soldTodayContainer.innerHTML = html;
        })
        .catch(err => console.error("Error loading sales:", err));
    }

    function completeSale() {
        if (cart.length === 0) {
            alert("Cart is empty!");
            return;
        }
        let total = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
        let currentCart = [...cart];

        fetch('/api/sales', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ items: currentCart, total: total, shop: 'shop1' })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showReceipt(currentCart, total);
                cart = [];
                updateCart();
                loadTodaySales();
            } else {
                alert("Error recording sale: " + (data.error || "Unknown error"));
            }
        })
        .catch(err => {
            alert("Connection error while completing sale.");
            console.error(err);
        });
    }

    function showReceipt(items, total) {
        document.getElementById('receiptDate').innerText = new Date().toLocaleString();
        let listHtml = '';
        items.forEach(i => {
            listHtml += `<div class="flex justify-between">
                <span>${i.qty}x ${i.name}</span>
                <span>CFA ${(i.price * i.qty).toLocaleString()}</span>
            </div>`;
        });
        document.getElementById('receiptItemsList').innerHTML = listHtml;
        document.getElementById('receiptTotal').innerText = 'CFA ' + total.toLocaleString();
        document.getElementById('receiptModal').classList.remove('hidden');
    }

    function closeReceipt() {
        document.getElementById('receiptModal').classList.add('hidden');
        location.reload();
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

    window.onload = function() {
        loadTodaySales();
    };
    </script>
</body>
</html>
'''

os.makedirs("app/templates", exist_ok=True)
with open("app/templates/pos.html", "w") as f:
    f.write(pos_html_code)

print("Successfully wrote complete pos.html!")
