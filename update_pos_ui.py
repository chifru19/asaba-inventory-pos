import os

path = "app/templates/pos.html"
if not os.path.exists(path):
    print("Error: pos.html not found!")
    exit(1)

with open(path, "r") as f:
    html = f.read()

# Check if search bar already exists
if 'id="productSearch"' not in html:
    # Insert search bar right above the catalog grid
    old_header = 'Inventory Catalog'
    search_bar_html = '''
    <!-- Search Bar -->
    <div class="mb-4">
        <input type="text" id="productSearch" placeholder="🔍 Search products by name..." 
               class="w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500 shadow-sm"
               onkeyup="filterProducts()">
    </div>
    '''
    # We will insert it near the inventory title header
    if '<div class="grid' in html:
        html = html.replace('<div class="grid', search_bar_html + '\n    <div class="grid', 1)
    elif 'Inventory Catalog' in html:
        html = html.replace('Inventory Catalog', 'Inventory Catalog\n' + search_bar_html, 1)

# Ensure script for search and quantity +/- is present
search_js = '''
<script>
function filterProducts() {
    let input = document.getElementById('productSearch').value.toLowerCase();
    let cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
        let name = card.getAttribute('data-name').toLowerCase();
        if (name.includes(input)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}

function changeQty(productId, delta) {
    let qtyInput = document.getElementById('qty-' + productId);
    if (qtyInput) {
        let current = parseInt(qtyInput.value) || 1;
        let updated = current + delta;
        if (updated < 1) updated = 1;
        qtyInput.value = updated;
    }
}
</script>
''';

if 'function filterProducts' not in html:
    if '</body>' in html:
        html = html.replace('</body>', search_js + '\n</body>')
    else:
        html += search_js

with open(path, "w") as f:
    f.write(html)

print("Successfully updated app/templates/pos.html with Search and Quantity controls!")
