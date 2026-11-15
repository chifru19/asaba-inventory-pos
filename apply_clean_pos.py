path = "app/templates/pos.html"
with open(path, "r") as f:
    content = f.read()

# Add Search bar right before the product grid if not present
search_html = '''
    <!-- Search Bar -->
    <div class="mb-4">
        <input type="text" id="productSearch" placeholder="🔍 Search products by name..." 
               class="w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500 shadow-sm"
               onkeyup="filterProducts()">
    </div>
'''

if 'id="productSearch"' not in content:
    if '<div class="grid' in content:
        content = content.replace('<div class="grid', search_html + '\n    <div class="grid', 1)

# Add filterProducts and changeQty JavaScript functions before closing body
js_code = '''
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
'''

if 'function filterProducts' not in content:
    if '</body>' in content:
        content = content.replace('</body>', js_code + '\n</body>')
    else:
        content += js_code

with open(path, "w") as f:
    f.write(content)

print("Successfully applied clean search and quantity controls to pos.html!")
