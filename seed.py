from app import create_app
from app.models import db, Product

app = create_app()

with app.app_context():
    # Check if products already exist to avoid duplicates
    if Product.query.count() == 0:
        p1 = Product(name="Premium Rice 50kg", sku="RICE-50", purchase_price=35.00, selling_price=45.00, stock_quantity=15, min_threshold=5)
        p2 = Product(name="Vegetable Cooking Oil 5L", sku="OIL-05", purchase_price=12.00, selling_price=18.00, stock_quantity=3, min_threshold=5)
        p3 = Product(name="Refined Sugar 1kg", sku="SUGAR-01", purchase_price=1.20, selling_price=2.00, stock_quantity=40, min_threshold=10)
        
        db.session.add_all([p1, p2, p3])
        db.session.commit()
        print("Mock inventory data seeded successfully!")
    else:
        print("Inventory already contains products.")
