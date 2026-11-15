from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    products = Product.query.all()
    print(f"Found {len(products)} products in active database.")
    for p in products:
        p.shop1_stock = 15
        p.shop2_stock = 25
        p.shop3_stock = 10
    db.session.commit()
    print("✅ Successfully updated stock in the active Flask database!")
