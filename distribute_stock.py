from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    products = Product.query.all()
    print(f"📦 Distributing stock across shops for {len(products)} products...")
    for p in products:
        # Assign distinct test quantities to each shop
        p.shop1_stock = 15
        p.shop2_stock = 25
        p.shop3_stock = 10
    db.session.commit()
    print("✅ Successfully distributed stock for all shops!")
    
    # Verify sample distribution
    for p in Product.query.limit(3).all():
        print(f"Product: {p.name} | Shop1: {p.shop1_stock} | Shop2: {p.shop2_stock} | Shop3: {p.shop3_stock}")
