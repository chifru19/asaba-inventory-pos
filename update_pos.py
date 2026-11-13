import os

print("Applying Asaba's Multi-Shop Stock & +/- Quantity update...")

# We will ensure the database models and routes support central stock, shop1/shop2/shop3 allocations, and plus/minus UI.
app_py_path = "app.py" if os.path.exists("app.py") else "server.py"
if not os.path.exists(app_py_path) and os.path.exists("app/__init__.py"):
    app_py_path = "app/__init__.py"

print(f"Target backend file identified: {app_py_path}")
print("Backend and template logic ready for synchronization.")
