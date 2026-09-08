from app import create_app
from app.extensions import db
from app.models import Product

app = create_app()

with app.app_context():
    db.create_all()
    
    if Product.query.count() == 0:
        p1 = Product(name='Drinking Water (3L)', sku='DOUS-3L', purchase_price=150.0, selling_price=250.0, stock_quantity=50, min_threshold=5)
        p2 = Product(name='Refined Garri (5kg)', sku='GARR-5K', purchase_price=1200.0, selling_price=1500.0, stock_quantity=20, min_threshold=3)
        p3 = Product(name='Palm Oil (1L)', sku='PLM-1L', purchase_price=800.0, selling_price=1000.0, stock_quantity=15, min_threshold=3)

        db.session.add_all([p1, p2, p3])
        db.session.commit()
        print('✅ Database successfully created and seeded with initial products!')
    else:
        print('ℹ️ Database already contains products.')
