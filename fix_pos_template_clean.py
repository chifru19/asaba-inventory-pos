path = "app/templates/pos.html"
with open(path, "r") as f:
    content = f.read()

# Replace the broken get_stock call with direct product.stock access
old_snippet = """<span class="font-bold {% if get_stock(product, store_id) > 0 %}text-green-600{% else %}text-red-500{% endif %}">
                                    {{ get_stock(product, store_id) }}"""

new_snippet = """<span class="font-bold {% if product.stock > 0 %}text-green-600{% else %}text-red-500{% endif %}">
                                    {{ product.stock }}"""

if old_snippet in content:
    content = content.replace(old_snippet, new_snippet)
    with open(path, "w") as f:
        f.write(content)
    print("✅ Successfully replaced get_stock with product.stock in pos.html!")
else:
    print("⚠️ Exact get_stock snippet not found, performing broad replacement...")
    content = content.replace("get_stock(product, store_id)", "product.stock")
    with open(path, "w") as f:
        f.write(content)
    print("✅ Broad replacement completed!")
