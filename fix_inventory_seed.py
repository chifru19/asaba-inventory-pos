import os

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# Replace the product seeding block with clean pool-based initial stock
old_seed_block = code[code.find("if Product.query.count() == 0:"):code.find("if Product.query.count() == 0:") + 750]

new_seed_block = '''if Product.query.count() == 0:
                sample_products = [
                    Product(name="DEO ROLLON mn", price=800, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="DEO ROLLON wn", price=800, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Bodylotion", price=1500, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL-Bodymilk", price=1500, main_stock=200, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL Body coscos", price=2000, main_stock=150, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                    Product(name="BL/vital", price=2500, main_stock=100, shop1_stock=0, shop2_stock=0, shop3_stock=0),
                ]
                db.session.bulk_save_objects(sample_products)
                db.session.commit()'''

code = code.replace(old_seed_block, new_seed_block)

with open(init_path, "w") as f:
    f.write(code)

print("Updated product seeding logic!")
