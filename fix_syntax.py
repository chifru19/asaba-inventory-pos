init_path = "app/__init__.py"
with open(init_path, "r") as f:
    content = f.read()

# Fix the typo double closing brace
old_line = 'return jsonify({"error": "Product not found"}}, 404'
new_line = 'return jsonify({"error": "Product not found"}), 404'

if old_line in content:
    content = content.replace(old_line, new_line)
    with open(init_path, "w") as f:
        f.write(content)
    print("Successfully fixed jsonify syntax error!")
else:
    # General regex fix if exact line differs slightly
    import re
    content = re.sub(r'jsonify\(\{"error": "Product not found"\}\}\s*,\s*404\)', 'jsonify({"error": "Product not found"}), 404', content)
    with open(init_path, "w") as f:
        f.write(content)
    print("Applied regex fix for jsonify error!")
