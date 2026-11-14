path = "app/templates/owner_dashboard.html"
with open(path, "r") as f:
    html = f.read()

restock_widget_html = '''
        <!-- 🔄 Restock Existing Main Stock -->
        <div class="bg-white rounded-2xl shadow-xl border border-stone-200 p-6 mb-6">
            <h3 class="text-lg font-black text-stone-800 uppercase tracking-wider mb-2">🔄 Restock Existing Main Stock</h3>
            <p class="text-xs text-stone-500 mb-4">Select an existing product from your central inventory and add newly received shipment quantities.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                <div>
                    <label class="block text-xs font-bold uppercase text-stone-600 mb-1">Select Existing Product</label>
                    <select id="restockProductId" class="w-full px-4 py-3 rounded-xl border border-stone-200 bg-stone-50 text-sm font-semibold text-stone-800">
                        {% for p in products %}
                        <option value="{{ p.id }}">{{ p.name.replace("(SHOP1)", "").replace("(SHOP2)", "").replace("(SHOP3)", "").strip() }} (Main: {{ p.main_stock | default(p.stock, true) }})</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-stone-600 mb-1">Quantity Received</label>
                    <input type="number" id="restockQty" min="1" value="10" class="w-full px-4 py-3 rounded-xl border border-stone-200 bg-stone-50 text-sm font-semibold text-stone-800">
                </div>
                <div>
                    <button onclick="executeRestock()" class="w-full bg-teal-950 text-white py-3 rounded-xl font-bold uppercase text-xs tracking-wider hover:bg-teal-900 transition shadow-md">
                        Restock Main Stock ➔
                    </button>
                </div>
            </div>
        </div>
'''

restock_js = '''
    function executeRestock() {
        const productId = document.getElementById("restockProductId").value;
        const qty = parseInt(document.getElementById("restockQty").value);

        if (!qty || qty <= 0) {
            alert("Please enter a valid quantity to restock.");
            return;
        }

        fetch("/api/restock_product", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ product_id: productId, qty: qty })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert("Error: " + (data.error || "Restock failed"));
            }
        })
        .catch(err => alert("Connection error during restock."));
    }
'''

if "Restock Existing Main Stock" not in html:
    # Insert before the Central Stock Transfer widget or near the bottom
    html = html.replace('<!-- Central Stock Transfer to Shops Widget -->', restock_widget_html + '\n        <!-- Central Stock Transfer to Shops Widget -->')
    # Insert JS before closing script tag
    html = html.replace('</script>\n</body>', restock_js + '\n    </script>\n</body>')
    with open(path, "w") as f:
        f.write(html)
    print("Successfully added restock widget to owner_dashboard.html!")
else:
    print("Restock widget already exists in owner_dashboard.html!")
