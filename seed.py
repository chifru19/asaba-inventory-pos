from app import create_app
from app.extensions import db
from app.models import Product

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    all_items = [
        {"name": "Balea Deo Mn Fresh & Exdry", "sku": "BAL-001", "purchase_price": 850.0, "selling_price": 10000.0, "initial_stock": 1200, "stock_quantity": 1000, "min_threshold": 10},
        {"name": "Balea Deo Mn Inv & Sens", "sku": "BAL-002", "purchase_price": 850.0, "selling_price": 10000.0, "initial_stock": 1200, "stock_quantity": 1000, "min_threshold": 10},
        {"name": "Balea SPRAY 4 Wm 48H", "sku": "BAL-003", "purchase_price": 850.0, "selling_price": 9000.0, "initial_stock": 1200, "stock_quantity": 1000, "min_threshold": 10},
        {"name": "Balea DEO ROLLON Mn", "sku": "BAL-004", "purchase_price": 600.0, "selling_price": 7000.0, "initial_stock": 1000, "stock_quantity": 800, "min_threshold": 10},
        {"name": "Balea DEO ROLLON WN", "sku": "BAL-005", "purchase_price": 600.0, "selling_price": 7000.0, "initial_stock": 1000, "stock_quantity": 800, "min_threshold": 10},
        {"name": "Balea Bodylotion", "sku": "BAL-006", "purchase_price": 950.0, "selling_price": 13000.0, "initial_stock": 1800, "stock_quantity": 1500, "min_threshold": 15},
        {"name": "Balea Bodymilk", "sku": "BAL-007", "purchase_price": 950.0, "selling_price": 13000.0, "initial_stock": 1800, "stock_quantity": 1500, "min_threshold": 15},
        {"name": "Balea Bcream-Sheabut", "sku": "BAL-008", "purchase_price": 1750.0, "selling_price": 4080000.0, "initial_stock": 3000, "stock_quantity": 2500, "min_threshold": 20},
        {"name": "Balea Dgel H&M 750ml", "sku": "BAL-009", "purchase_price": 1250.0, "selling_price": 4590000.0, "initial_stock": 1800, "stock_quantity": 1500, "min_threshold": 15},
        {"name": "Balea Denkmit Duftspray", "sku": "BAL-010", "purchase_price": 950.0, "selling_price": 612000.0, "initial_stock": 1200, "stock_quantity": 1000, "min_threshold": 10},
        {"name": "Balea Enthaarungs creme", "sku": "BAL-011", "purchase_price": 1150.0, "selling_price": 1854000.0, "initial_stock": 1800, "stock_quantity": 1500, "min_threshold": 15},
        {"name": "Rossmann Facelle Classic", "sku": "CIEN-101", "purchase_price": 990.0, "selling_price": 585000.0, "initial_stock": 1800, "stock_quantity": 1500, "min_threshold": 15},
        {"name": "Cien Spray 4Men", "sku": "CIEN-102", "purchase_price": 750.0, "selling_price": 1460000.0, "initial_stock": 1200, "stock_quantity": 1000, "min_threshold": 10},
        {"name": "Cien Spray 4Wm", "sku": "CIEN-103", "purchase_price": 850.0, "selling_price": 9000.0, "initial_stock": 1200, "stock_quantity": 1000, "min_threshold": 10},
        {"name": "LD-Dentalux-Complex 3", "sku": "CIEN-104", "purchase_price": 550.0, "selling_price": 3360000.0, "initial_stock": 1000, "stock_quantity": 800, "min_threshold": 10},
        {"name": "Cien Dusgel 1L", "sku": "CIEN-105", "purchase_price": 1590.0, "selling_price": 18000.0, "initial_stock": 2500, "stock_quantity": 2000, "min_threshold": 20},
        {"name": "Cien Blotion Q10", "sku": "CIEN-106", "purchase_price": 1750.0, "selling_price": 630000.0, "initial_stock": 3000, "stock_quantity": 2500, "min_threshold": 25},
        {"name": "Cien Schauma Shampo", "sku": "CIEN-107", "purchase_price": 950.0, "selling_price": 140400.0, "initial_stock": 1500, "stock_quantity": 1300, "min_threshold": 15},
        {"name": "Toilet roll-10/3lag", "sku": "HH-001", "purchase_price": 3590.0, "selling_price": 60000.0, "initial_stock": 6500, "stock_quantity": 6000, "min_threshold": 50},
        {"name": "Doussy 3L", "sku": "HH-002", "purchase_price": 3690.0, "selling_price": 1120000.0, "initial_stock": 5500, "stock_quantity": 5000, "min_threshold": 50},
        {"name": "Kuschelweich 1L", "sku": "HH-003", "purchase_price": 1950.0, "selling_price": 1488000.0, "initial_stock": 2500, "stock_quantity": 2000, "min_threshold": 20},
        {"name": "Dash powder -100", "sku": "HH-004", "purchase_price": 8490.0, "selling_price": 3900000.0, "initial_stock": 14000, "stock_quantity": 13000, "min_threshold": 100}
    ]

    for item in all_items:
        db.session.add(Product(**item))

    db.session.commit()
    print("Database re-created and seeded with initial and current stock!")
