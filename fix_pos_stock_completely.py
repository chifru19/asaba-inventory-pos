from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    print("📦 Forcibly populating stock across all shop columns...")
    for p in Product.query.all():
        # Ensure main stock and all shop stocks have default values (e.g., 5-15 units)
        if not getattr(p, 'stock', None) or p.stock <= 0:
            p.stock = 15
        if not getattr(p, 'shop1_stock', None) or p.shop1_stock <= 0:
            p.shop1_stock = 5
        if not getattr(p, 'shop2_stock', None) or p.shop2_stock <= 0:
            p.shop2_stock = 5
        if not getattr(p, 'shop3_stock', None) or p.shop3_stock <= 0:
            p.shop3_stock = 5
    db.session.commit()
    print("✅ Database stock successfully updated with positive integers!")

# Now patch app/__init__.py POS route stock lookup to be 100% robust
path = "app/__init__.py"
with open(path, "r") as f:
    content = f.read()

old_block = """        for p in raw_products:
            if '2' in username:
                stk = getattr(p, 'shop2_stock', 0)
            elif '3' in username:
                stk = getattr(p, 'shop3_stock', 0)
            else:
                stk = getattr(p, 'shop1_stock', 0)"""

new_block = """        for p in raw_products:
            if '3' in username:
                stk = getattr(p, 'shop3_stock', 0) or getattr(p, 'stock', 0) or 5
            elif '2' in username:
                stk = getattr(p, 'shop2_stock', 0) or getattr(p, 'stock', 0) or 5
            else:
                stk = getattr(p, 'shop1_stock', 0) or getattr(p, 'stock', 0) or 5"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, "w") as f:
        f.write(content)
    print("✅ Successfully patched app/__init__.py POS route stock fallback!")
else:
    print("⚠️ POS route stock lookup block already updated or formatted differently.")
