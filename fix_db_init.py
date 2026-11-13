import os

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

if "db.create_all()" not in code:
    code = code.replace(
        "return app",
        "    with app.app_context():\n        db.create_all()\n    return app"
    )
    with open(init_path, "w") as f:
        f.write(code)
    print("Added db.create_all() inside create_app factory!")

