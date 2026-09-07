from app import create_app
from app.models import db, Product

app = create_app()

with app.app_context():
    db.create_all()
    
    # Clear existing products to avoid duplication and cleanly load the full inventory sheet
    Product.query.delete()
    
    items = [
        # Balea Line
        Product(name="Balea Deo Men Fresh & Dry", sku="BL-MEN-FRESH", purchase_price=0.85, selling_price=1000.00, stock_quantity=15, min_threshold=5),
        Product(name="Balea Deo Sensitive", sku="BL-DEO-SENS", purchase_price=0.85, selling_price=1000.00, stock_quantity=12, min_threshold=4),
        Product(name="Balea Bodylotion Bloomy Kiss", sku="BL-LOTION-BLOOM", purchase_price=0.95, selling_price=1300.00, stock_quantity=16, min_threshold=5),
        Product(name="Balea Bodymilk Love Melon", sku="BL-MILK-MELON", purchase_price=0.95, selling_price=1300.00, stock_quantity=16, min_threshold=5),
        Product(name="Balea Bodycream Shea Butter", sku="BL-CREAM-SHEA", purchase_price=1.75, selling_price=4080.00, stock_quantity=204, min_threshold=20),
        Product(name="Balea Duschgel H&M 750ml", sku="BL-DGEL-750", purchase_price=1.25, selling_price=4590.00, stock_quantity=306, min_threshold=20),
        Product(name="Balea Men Duschgel 300ml", sku="BL-DGEL-MEN", purchase_price=0.55, selling_price=1000.00, stock_quantity=86, min_threshold=10),
        Product(name="Balea Handwash", sku="BL-HANDWASH", purchase_price=0.75, selling_price=1000.00, stock_quantity=12, min_threshold=4),
        Product(name="Balea Savon Sensitive", sku="BL-SAVON-SENS", purchase_price=0.55, selling_price=500.00, stock_quantity=28, min_threshold=5),
        Product(name="Balea Toothpaste Dontodent", sku="BL-TP-DONT", purchase_price=0.65, selling_price=800.00, stock_quantity=28, min_threshold=5),
        Product(name="Balea Enthaarungscreme", sku="BL-CREME-ENTH", purchase_price=1.15, selling_price=1500.00, stock_quantity=120, min_threshold=15),
        Product(name="Balea Denkmit Duftspray", sku="BL-DUFT-SPRAY", purchase_price=0.95, selling_price=1000.00, stock_quantity=612, min_threshold=30),

        # Cien Line
        Product(name="Cien Spray For Men", sku="CIEN-SP-MEN", purchase_price=0.75, selling_price=1460.00, stock_quantity=73, min_threshold=10),
        Product(name="Cien Dentalux Complex 3", sku="CIEN-DENT-3", purchase_price=0.55, selling_price=3360.00, stock_quantity=175, min_threshold=20),
        Product(name="Cien Duschgel 1L", sku="CIEN-DGEL-1L", purchase_price=1.59, selling_price=18000.00, stock_quantity=80, min_threshold=10),
        Product(name="Cien Bodylotion Q10", sku="CIEN-BL-Q10", purchase_price=1.75, selling_price=6300.00, stock_quantity=21, min_threshold=5),
        Product(name="Cien Schauma Shampoo", sku="CIEN-SCHAUMA", purchase_price=0.95, selling_price=1404.00, stock_quantity=12, min_threshold=4),
        Product(name="Cien Savon Soap", sku="CIEN-SAVON", purchase_price=1.09, selling_price=2880.00, stock_quantity=180, min_threshold=20),
        Product(name="Cien Duschgel 300ml Color", sku="CIEN-DGEL-COL", purchase_price=0.85, selling_price=3600.00, stock_quantity=18, min_threshold=5),
        Product(name="Cien Mouthwash 750ml", sku="CIEN-MOUTHW", purchase_price=1.25, selling_price=9000.00, stock_quantity=30, min_threshold=5),

        # Aldi & Other Supermarket Line
        Product(name="Biocura Spray Men", sku="BIOC-SP-M", purchase_price=0.75, selling_price=600.00, stock_quantity=12, min_threshold=4),
        Product(name="Doussy Softener 3L", sku="DOUS-3L", purchase_price=3.69, selling_price=1120.00, stock_quantity=564, min_threshold=30),
        Product(name="Kuschelweich Softener 1L", sku="KUSCH-1L", purchase_price=1.95, selling_price=1488.00, stock_quantity=100, min_threshold=15),
        Product(name="W5 Glas Reiniger", sku="W5-GLAS", purchase_price=0.85, selling_price=750.00, stock_quantity=50, min_threshold=10),
        Product(name="W5 Dishwasher Tablets", sku="W5-DISH", purchase_price=0.95, selling_price=540.00, stock_quantity=12, min_threshold=4),
        Product(name="Dash Powder 100", sku="DASH-100", purchase_price=8.49, selling_price=3900.00, stock_quantity=300, min_threshold=25),
        Product(name="Orlando Dog Food 10kg", sku="ORL-DOG-10", purchase_price=9.99, selling_price=15000.00, stock_quantity=60, min_threshold=10),
        Product(name="Softland Fresh 2L", sku="SOFT-2L", purchase_price=1.75, selling_price=240.00, stock_quantity=12, min_threshold=4),

        # Electronics, Appliances & Equipment
        Product(name="Irvering 3L H2O Boiler", sku="APPL-BOILER", purchase_price=6.50, selling_price=1620.00, stock_quantity=12, min_threshold=2),
        Product(name="Plastic Mixer 800W", sku="APPL-MIXER", purchase_price=11.50, selling_price=900.00, stock_quantity=6, min_threshold=2),
        Product(name="Glass Mixer 800W", sku="APPL-GLAS-MIX", purchase_price=13.50, selling_price=1080.00, stock_quantity=6, min_threshold=2),
        Product(name="Compressor Fridge", sku="FRIDGE-COMP", purchase_price=10.00, selling_price=2400.00, stock_quantity=200, min_threshold=10),
        Product(name="Short Fridge 1.5m", sku="FRIDGE-SHORT", purchase_price=35.00, selling_price=480000.00, stock_quantity=1, min_threshold=1),
        Product(name="Tabletop Fridge", sku="FRIDGE-TABLE", purchase_price=30.00, selling_price=550000.00, stock_quantity=1, min_threshold=1),
        Product(name="Gas Herd Beko 5-Head", sku="GAS-BEKO-5", purchase_price=300.00, selling_price=300000.00, stock_quantity=1, min_threshold=1),
        Product(name="PC Screens 20-22 Zoll", sku="TECH-SCR-20", purchase_price=5.00, selling_price=1001.00, stock_quantity=143, min_threshold=15),
        Product(name="PC Screens 24-26 Zoll VIP Red", sku="TECH-SCR-24", purchase_price=15.00, selling_price=610000.00, stock_quantity=6, min_threshold=2),
        Product(name="Airfryer", sku="APPL-AIRFRY", purchase_price=10.00, selling_price=75000.00, stock_quantity=5, min_threshold=1),
        Product(name="Washing Machine", sku="APPL-WASH", purchase_price=50.00, selling_price=100000.00, stock_quantity=1, min_threshold=1),
        Product(name="Billard Table", sku="EQUIP-BILLIARD", purchase_price=300.00, selling_price=1100000.00, stock_quantity=1, min_threshold=1),
        Product(name="Tyres 8*4 with Doubling", sku="VEH-TYRES-84", purchase_price=5.00, selling_price=5400000.00, stock_quantity=150, min_threshold=10),
        Product(name="Yaris Blue 2004", sku="VEH-YARIS-04", purchase_price=1450.00, selling_price=2700000.00, stock_quantity=1, min_threshold=1)
    ]
    
    db.session.add_all(items)
    db.session.commit()
    print("Asaba's complete inventory catalog successfully loaded!")

