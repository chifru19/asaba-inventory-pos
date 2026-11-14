import os

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# Add automatic product seeding alongside user seeding in app_context
old_context = '''    with app.app_context():
        db.create_all()
        try:
            if not User.query.filter_by(username='owner').first():
                db.session.add(User(username='owner', password_hash=generate_password_hash('owner123'), role='owner'))
            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='admin').first():
                db.session.add(User(username='admin', password_hash=generate_password_hash('admin123'), role='owner'))
            db.session.commit()
        except Exception:
            db.session.rollback()'''

new_context = '''    with app.app_context():
        db.create_all()
        try:
            if not User.query.filter_by(username='owner').first():
                db.session.add(User(username='owner', password_hash=generate_password_hash('owner123'), role='owner'))
            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='admin').first():
                db.session.add(User(username='admin', password_hash=generate_password_hash('admin123'), role='owner'))
            db.session.commit()

            # Auto-seed sample products if table is empty
            if Product.query.count() == 0:
                sample_products = [
                    Product(name="DEO ROLLON mn", price=800, main_stock=100, shop1_stock=72, shop2_stock=30, shop3_stock=20),
                    Product(name="DEO ROLLON wn", price=800, main_stock=100, shop1_stock=120, shop2_stock=40, shop3_stock=25),
                    Product(name="BL-Bodylotion", price=1500, main_stock=200, shop1_stock=168, shop2_stock=50, shop3_stock=40),
                    Product(name="BL-Bodymilk", price=1500, main_stock=200, shop1_stock=165, shop2_stock=60, shop3_stock=30),
                    Product(name="BL Body coscos", price=2000, main_stock=150, shop1_stock=100, shop2_stock=30, shop3_stock=20),
                    Product(name="BL/vital", price=2500, main_stock=100, shop1_stock=10, shop2_stock=25, shop3_stock=15),
                ]
                db.session.bulk_save_objects(sample_products)
                db.session.commit()
        except Exception as e:
            print("Seeding error:", e)
            db.session.rollback()'''

if old_context in code:
    code = code.replace(old_context, new_context)
    with open(init_path, "w") as f:
        f.write(code)
    print("Successfully added automatic product seeding to app/__init__.py!")
else:
    print("Could not find target context block, checking file structure.")

