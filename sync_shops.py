from app import create_app
from app.extensions import db
from app.models import Product

app = create_app()
with app.app_context():
    shop1_products = Product.query.filter_by(store_id='shop1').all()
    print(f"Found {len(shop1_products)} products in Shop 1.")
    
    for store in ['shop2', 'shop3']:
        added_count = 0
        for p in shop1_products:
            existing = Product.query.filter_by(name=p.name, store_id=store).first()
            if not existing:
                new_product = Product(
                    name=p.name,
                    price=p.price,
                    stock=p.stock,
                    store_id=store
                )
                db.session.add(new_product)
                added_count += 1
        db.session.commit()
        print(f"Successfully added {added_count} products to {store}!")
