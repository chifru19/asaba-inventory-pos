import os

init_path = "app/__init__.py" if os.path.exists("app/__init__.py") else "app.py"
with open(init_path, "r") as f:
    code = f.read()

# Make sure owner_dashboard route passes consolidated products
print("Updating owner dashboard backend logic...")
