import os

models_path = "app/models.py"
if os.path.exists(models_path):
    with open(models_path, "r") as f:
        code = f.read()
    
    if "main_stock" not in code:
        # Inject fields into Product model
        code = code.replace(
            "db.Model):",
            "db.Model):\n    main_stock = db.Column(db.Integer, default=0)\n    shop1_stock = db.Column(db.Integer, default=0)\n    shop2_stock = db.Column(db.Integer, default=0)\n    shop3_stock = db.Column(db.Integer, default=0)"
        )
        with open(models_path, "w") as f:
            f.write(code)
        print("Added multi-shop columns to Product model!")

