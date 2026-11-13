import os

models_path = "app/models.py"
if os.path.exists(models_path):
    with open(models_path, "r") as f:
        content = f.read()

    if "password =" not in content and "password_hash =" not in content:
        # Add password column to User model
        content = content.replace(
            "class User(db.Model):",
            "class User(db.Model):\n    password = db.Column(db.String(255))"
        )
        with open(models_path, "w") as f:
            f.write(content)
        print("Successfully added password column to User model in app/models.py!")
    else:
        print("Password column already exists in models.py.")
