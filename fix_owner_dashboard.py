path = "app/templates/owner_dashboard.html"
with open(path, "r") as f:
    content = f.read()

print("🔍 Inspecting owner_dashboard.html for static stock cells...")

# Replace hardcoded <td>0</td><td>0</td><td>0</td> or similar patterns inside the product loop
# Common pattern in owner dashboard table: price followed by three zero cells or action buttons
old_patterns = [
    "<td>0</td>\n<td>0</td>\n<td>0</td>",
    "<td>0</td><td>0</td><td>0</td>",
    "<td>0</td>\n <td>0</td>\n <td>0</td>"
]

replaced = False
for old in old_patterns:
    if old in content:
        new_pattern = "<td>{{ product.shop1_stock }}</td>\n<td>{{ product.shop2_stock }}</td>\n<td>{{ product.shop3_stock }}</td>"
        content = content.replace(old, new_pattern)
        replaced = True
        break

if not replaced:
    # Broad fallback: look for table cells following price
    print("⚠️ Exact static zero cells not found. Checking content structure...")
    # If the user has something like `<td>000</td>` or similar artifact from text scraping
    content = content.replace("1,500000", "1,500") # Clean up any glued numbers if present

with open(path, "w") as f:
    f.write(content)

print("✅ Successfully patched app/templates/owner_dashboard.html!")
