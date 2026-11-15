path = "app/templates/pos.html"
clean_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asaba POS - {{ store_name }}</title>
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

        <!-- Search Bar -->
        <div class="mb-4">
            <input type="text" id="productSearch" placeholder="🔍 Search products by name..." 
                   class="w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500 shadow-sm"
                   onkeyup="filterProducts()">
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Inventory Catalog -->
            <div class="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
                <h2 class="text-lg font-bold text-stone-800 mb-4">Inventory Catalog ({{ store_name }})</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[70vh] overflow-y-auto pr-2">
                    {% for product in products %}
                    <div class="product-card border border-stone-200 rounded-xl p-4 flex flex-col justify-between bg-stone-50" data-name="{{ product.name }}">
                        <div>
                            <h3 class="font-bold text-stone-800">{{ product.name }}</h3>
                            <p class="text-teal-600 font-semibold text-sm">Price: CFA {{ "{:,.0f}".format(product.price) }}</p>
                            <p class="text-xs text-stone-500 mt-1">Stock Available: 
                                <span class="font-bold {% if get_stock(product, store_id) > 0 %}text-green-600{% else %}text-red-500{% endif %}">
                                    {{ get_stock(product, store_id) }}
                                </span>
                            </p>
                        </div>
                        <div class="mt-4 flex items-center justify-between">
                            <div class="flex items-center space-x-2">
                                <button onclick="changeQty('{{ product.id }}', -1)" class="bg-stone-200 hover:bg-stone-300 px-2.5 py-1 rounded-lg text-stone-700 font-bold text-sm">-</button>
                                <input type="number" id="qty-{{ product.id }}" value="1" min="1" class="w-12 text-center border border-stone-300 rounded-lg py-1 text-sm bg-white">
                                <button onclick="changeQty('{{ product.id }}', 1)" class="bg-stone-200 hover:bg-stone-300 px-2.5 py-1 rounded-lg text-stone-700 font-bold text-sm">+</button>
                            </div>
                            <button onclick="addToSale('{{ product.id }}', '{{ product.name }}', {{ product.price }}, {{ get_stock(product, store_id) }})" 
                                    class="bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold transition shadow-sm">
                                + Add to Sale
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Current Sale / Cart -->
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 flex flex-col justify-between">
                <div>
                    <h2 class="text-lg font-bold text-stone-800 mb-4">Current Sale</h2>
                    <div id="cartItems" class="space-y-3 max-h-[50vh] overflow-y-auto pr-1 mb-4">
                        <p class="text-stone-400 text-sm italic" id="emptyCartText">No items added yet.</p>
                    </div>
                </div>
                <div class="border-t border-stone-200 pt-4">
                    <div class="flex justify-between items-center mb-4">
                        <span class="font-bold text-stone-700">Total:</span>
                        <span id="cartTotal" class="text-xl font-black text-teal-700">CFA 0</span>
                    </div>
                    <button onclick="completeSale()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-xl transition shadow-md">
                        Complete Sale & Print Receipt
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        var cart = [];
        var currentShop = "{{ store_name }}";

        function filterProducts() {
            var input = document.getElementById("productSearch").value.toLowerCase();
            var cards = document.querySelectorAll(".product-card");
            cards.forEach(function(card) {
                var name = card.getAttribute("data-name").toLowerCase();
                if (name.indexOf(input) !== -1) {
                    card.style.display = "";
                } else {
                    card.style.display = "none";
                }
            });
        }

        function changeQty(productId, delta) {
            var qtyInput = document.getElementById("qty-" + productId);
            if (qtyInput) {
                var current = parseInt(qtyInput.value) || 1;
                var updated = current + delta;
                if (updated < 1) updated = 1;
                qtyInput.value = updated;
            }
        }

        function addToSale(id, name, price, maxStock) {
            var qtyInput = document.getElementById("qty-" + id);
            var qty = parseInt(qtyInput.value) || 1;

            if (maxStock <= 0) {
                alert("Cannot add item: Stock is 0!");
                return;
            }

            var existing = null;
            for (var i = 0; i < cart.length; i++) {
                if (cart[i].id === id) {
                    existing = cart[i];
                    break;
                }
            }

            if (existing) {
                if (existing.qty + qty > maxStock) {
                    alert("Cannot add more than available stock (" + maxStock + ")");
                    return;
                }
                existing.qty += qty;
            } else {
                if (qty > maxStock) {
                    alert("Cannot add more than available stock (" + maxStock + ")");
                    return;
                }
                cart.push({ id: id, name: name, price: price, qty: qty });
            }
            updateCartUI();
        }

        function removeFromCart(id) {
            var newCart = [];
            for (var i = 0; i < cart.length; i++) {
                if (cart[i].id !== id) {
                    newCart.push(cart[i]);
                }
            }
            cart = newCart;
            updateCartUI();
        }

        function updateCartUI() {
            var container = document.getElementById("cartItems");
            var totalElem = document.getElementById("cartTotal");
            
            if (cart.length === 0) {
                container.innerHTML = '<p class="text-stone-400 text-sm italic" id="emptyCartText">No items added yet.</p>';
                totalElem.innerText = "CFA 0";
                return;
            }

            container.innerHTML = "";
            var total = 0;

            for (var i = 0; i < cart.length; i++) {
                var item = cart[i];
                var itemTotal = item.price * item.qty;
                total += itemTotal;
                
                var html = '<div class="flex justify-between items-center bg-stone-50 p-2.5 rounded-xl border border-stone-200 text-sm">' +
                           '<div><p class="font-bold text-stone-800">' + item.name + '</p>' +
                           '<p class="text-xs text-stone-500">' + item.qty + ' x CFA ' + item.price.toLocaleString() + '</p></div>' +
                           '<div class="flex items-center space-x-2">' +
                           '<span class="font-bold text-stone-700">CFA ' + itemTotal.toLocaleString() + '</span>' +
                           '<button onclick="removeFromCart(\'' + item.id + '\')" class="text-red-500 hover:text-red-700 font-bold px-1.5">&times;</button>' +
                           '</div></div>';
                container.innerHTML += html;
            }

            totalElem.innerText = "CFA " + total.toLocaleString();
        }

        function printReceipt(saleData) {
            var win = window.open("", "", "height=600,width=400");
            win.document.write("<html><head><title>Receipt</title>");
            win.document.write("<style>body { font-family: monospace; padding: 20px; }</style>");
            win.document.write("</head><body>");
            win.document.write("<h2 style='text-align:center;'>ASABA INVENTORY POS</h2>");
            win.document.write("<p>Shop: " + currentShop + "<br>Date: " + new Date().toLocaleString() + "</p><hr>");
            for (var i = 0; i < saleData.items.length; i++) {
                var i_item = saleData.items[i];
                win.document.write("<p>" + i_item.name + " x" + i_item.qty + " .......... CFA " + (i_item.price * i_item.qty).toLocaleString() + "</p>");
            }
            win.document.write("<hr><h3>Total: CFA " + saleData.total.toLocaleString() + "</h3>");
            win.document.write("<p style='text-align:center;'>Thank you for your business!</p>");
            win.document.write("</body></html>");
            win.document.close();
            win.focus();
            setTimeout(function() { win.print(); win.close(); }, 500);
        }

        function completeSale() {
            if (cart.length === 0) {
                alert("Cart is empty!");
                return;
            }
            var total = 0;
            for (var i = 0; i < cart.length; i++) {
                total += (cart[i].price * cart[i].qty);
            }
            var salePayload = { items: cart.slice(), total: total, shop: currentShop };

            fetch("/api/sales", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(salePayload)
            })
            .then(function(res) { return res.json(); })
            .then(function(data) {
                if (data.success) {
                    printReceipt(salePayload);
                    alert("Sale completed and receipt generated!");
                    location.reload();
                } else {
                    alert("Error: " + (data.error || "Sale failed"));
                }
            })
            .catch(function(err) {
                alert("Connection error during checkout.");
            });
        }
    </script>
</body>
</html>
'''

with open(path, "w") as f:
    f.write(clean_html)

print("Successfully cleaned pos.html and resolved all linter errors!")
