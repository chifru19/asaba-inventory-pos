import os

pos_path = "app/templates/pos.html"
with open(pos_path, "r") as f:
    content = f.read()

# Make sure completeSale fetches sales or updates the DOM directly, and add a loadSales function on startup
updated_js = '''
    <script>
    function adjustCardQty(itemId, change) {
        const input = document.getElementById('qty-' + itemId);
        if (!input) return;
        let val = parseInt(input.value) || 1;
        val += change;
        if (val < 1) val = 1;
        input.value = val;
    }

    let cart = [];

    function addToCart(id, name, price) {
        const input = document.getElementById('qty-' + id);
        let qty = input ? parseInt(input.value) || 1 : 1;
        
        let existing = cart.find(item => item.id === id);
        if (existing) {
            existing.qty += qty;
        } else {
            cart.push({ id: id, name: name, price: price, qty: qty });
        }
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
            html += `<div class="flex justify-between items-center bg-stone-50 p-2 rounded-lg border border-stone-200 mb-2">
                <div>
                    <span class="font-bold text-stone-800 text-xs">${item.name}</span>
                    <p class="text-[10px] text-stone-500">${item.qty} x CFA ${item.price.toLocaleString()}</p>
                </div>
                <span class="font-bold text-teal-900 text-xs">CFA ${itemTotal.toLocaleString()}</span>
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
        fetch('/api/sales', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ items: cart, total: total, shop: 'shop1' })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Sale completed successfully!");
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

    // Load sales on page load
    window.onload = function() {
        loadTodaySales();
    };
    </script>
'''

# Replace script block in pos.html
if "<script>" in content:
    parts = content.split("<script>")
    content = parts[0] + updated_js

    with open(pos_path, "w") as f:
        f.write(content)
    print("Successfully updated pos.html with dynamic AJAX sales loading!")

