from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    products = Product.query.all()
    print(f"📦 Distributing stock equally for {len(products)} products across 3 shops...")
    
    for p in products:
        # Get current main stock (fallback to 0 if not set)
        main_stock = getattr(p, 'stock', 0) or 0
        
        # Divide equally among 3 shops (integer division)
        per_shop = main_stock // 3
        
        # Assign equal shares to each shop
        p.shop1_stock = per_shop
        p.shop2_stock = per_shop
        p.shop3_stock = per_shop
        
        # Note: The remainder naturally stays in the main stock column or total pool
        
    db.session.commit()
    print("✅ Successfully distributed inventory equally to all shops!")

    # Verify a few items
    for p in Product.query.limit(5).all():
        main_qty = getattr(p, 'stock', 0)
        print(f"- {p.name}: Main={main_qty} | Shop1={p.shop1_stock}, Shop2={p.shop2_stock}, Shop3={p.shop3_stock}")
