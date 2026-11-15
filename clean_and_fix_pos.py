import os

path = "app/templates/pos.html"
if not os.path.exists(path):
    print("Error: pos.html not found!")
    exit(1)

with open(path, "r") as f:
    content = f.read()

# Strip out any accidental python script pollution if present
if "cat <<" in content or "with open(" in content:
    # If the file got polluted with python code, let's clean it up or reset
    print("Detected script pollution in HTML. Resetting file via git...")
    os.system("git checkout app/templates/pos.html")
    with open(path, "r") as f:
        content = f.read()

# 1. Add Search Bar if missing
if 'id="productSearch"' not in content:
    search_html = '''
    <!-- Search Bar -->
    <div class="mb-4">
        <input type="text" id="productSearch" placeholder="🔍 Search products by name..." 
               class="w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500 shadow-sm"
               onkeyup="filterProducts()">
    </div>
    '''
    if '<div class="grid' in content:
        content = content.replace('<div class="grid', search_html + '\n    <div class="grid', 1)

# 2. Add valid JavaScript functions before </body>
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

print("Successfully cleaned and updated pos.html!")
