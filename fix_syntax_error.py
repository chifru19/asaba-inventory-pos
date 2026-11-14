import re

with open("app/__init__.py", "r") as f:
    code = f.read()

clean_context = '''    with app.app_context():
        db.create_all()
        try:
            if not User.query.filter_by(username='owner').first():
                db.session.add(User(username='owner', password_hash=generate_password_hash('owner123'), role='owner'))
            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='admin').first():
                db.session.add(User(username='admin', password_hash=generate_password_hash('admin123'), role='owner'))
            db.session.commit()

            if Product.query.count() == 0:
                sample_products = [
                    Product(name="DEO ROLLON mn", price=800, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="DEO ROLLON wn", price=800, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Bodylotion", price=1500, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Bodymilk", price=1500, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL Body coscos", price=2000, main_stock=150, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL/vital", price=2500, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                ]
                db.session.bulk_save_objects(sample_products)
                db.session.commit()
        except Exception as e:
            print("Seeding error:", e)
            db.session.rollback()'''

code = re.sub(r'with app\.app_context\(\):[\s\S]*?except Exception as e:[\s\S]*?db\.session\.rollback\(\)', clean_context, code)

with open("app/__init__.py", "w") as f:
    f.write(code)

print("Successfully repaired app/__init__.py syntax error!")
