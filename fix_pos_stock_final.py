import os
from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"🔗 Active Database URI: {db_uri}")
    
    products = Product.query.all()
    print(f"📦 Found {len(products)} products in active database.")
    
    for p in products:
        p.shop1_stock = 15
        p.shop2_stock = 25
        p.shop3_stock = 10
        if hasattr(p, 'stock'):
            p.stock = 15
            
    db.session.commit()
    print("✅ Successfully updated stock in the active Flask database!")
    
    # Verify first product
    sample = Product.query.first()
    if sample:
        print(f"Verification -> Product: {sample.name} | Shop 1 Stock: {sample.shop1_stock}")

