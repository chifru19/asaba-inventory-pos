from flask import Flask
from app.extensions import db
from app.models import User, Product

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asaba-pos-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        
        # Create default owner if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='owner', store_id='global')
            admin.set_password('admin123')
            db.session.add(admin)

        # Full inventory list extracted from documentation (Prices in CFA)
        inventory_items = [
            {'name': 'BL-Deo Mn Fresh&Exdry', 'price': 1000.0, 'stock': 15},
            {'name': 'Bl-deo Mn Inv& Sens', 'price': 1000.0, 'stock': 12},
            {'name': 'BL-SPRAY 4 Wm 48H', 'price': 1000.0, 'stock': 15},
            {'name': 'SPRAYS men F&EF', 'price': 1000.0, 'stock': 10},
            {'name': 'BL-spray Wm', 'price': 1000.0, 'stock': 10},
            {'name': 'BL-spray Mn', 'price': 1000.0, 'stock': 10},
            {'name': 'DEO ROLLON mn', 'price': 800.0, 'stock': 72},
            {'name': 'DEO ROLLON WN', 'price': 800.0, 'stock': 120},
            {'name': 'BL-Bodylotion', 'price': 1500.0, 'stock': 168},
            {'name': 'BL-Bodymilk', 'price': 1500.0, 'stock': 165},
            {'name': 'BL Body coscos', 'price': 2000.0, 'stock': 10},
            {'name': 'BL/vital', 'price': 2500.0, 'stock': 10},
            {'name': 'BL/urea/Q10', 'price': 2500.0, 'stock': 70},
            {'name': 'BL-Bcream-Sheabut', 'price': 2500.0, 'stock': 204},
            {'name': 'Bl-Bcream-vanille/SheaB', 'price': 2500.0, 'stock': 96},
            {'name': 'BL-Dgel H&M 750ml', 'price': 2000.0, 'stock': 306},
            {'name': 'BL men Dusgel 300ml', 'price': 1000.0, 'stock': 86},
            {'name': 'BL Savon H&M', 'price': 1000.0, 'stock': 36},
            {'name': 'BL-Tpaste Dontodent', 'price': 700.0, 'stock': 28},
            {'name': 'Rossmann facelle clasic', 'price': 1000.0, 'stock': 390},
            {'name': 'Cien Spray 4Men', 'price': 1000.0, 'stock': 73},
            {'name': 'LD-Dentalux-Complex 3', 'price': 800.0, 'stock': 175},
            {'name': 'Cien Dgel 300ml 3x colour', 'price': 1000.0, 'stock': 20},
            {'name': 'Cein Schauma Shampo', 'price': 1300.0, 'stock': 9},
            {'name': 'Doussy 3L', 'price': 2500.0, 'stock': 56},
            {'name': 'Kuschelweich 1L', 'price': 2000.0, 'stock': 62},
            {'name': 'W5 Glas reinigen', 'price': 1000.0, 'stock': 50},
            {'name': 'W5 Dischwasser', 'price': 1000.0, 'stock': 30},
            {'name': 'Hot chocolate', 'price': 5000.0, 'stock': 20},
            {'name': 'Chocolate', 'price': 3000.0, 'stock': 25},
            {'name': 'Dash powder-100', 'price': 15000.0, 'stock': 300},
            {'name': 'Cornflakes 500g', 'price': 2500.0, 'stock': 120},
            {'name': 'LACUNA Blotion', 'price': 2000.0, 'stock': 300},
            {'name': 'Biocura Spray M', 'price': 1500.0, 'stock': 600},
            {'name': 'Tbrush aldi', 'price': 1000.0, 'stock': 1200}
        ]

        # Populate workers and inventory for Shop 1, Shop 2, and Shop 3
        shops = ['shop1', 'shop2', 'shop3']
        for shop in shops:
            worker_username = f'worker_{shop}'
            if not User.query.filter_by(username=worker_username).first():
                worker = User(username=worker_username, role='worker', store_id=shop)
                worker.set_password('password123')
                db.session.add(worker)
            
            # Populate products if none exist for this shop
            if not Product.query.filter_by(store_id=shop).first():
                for item in inventory_items:
                    p = Product(
                        name=f"{item['name']} ({shop.upper()})", 
                        price=item['price'], 
                        stock=item['stock'], 
                        store_id=shop
                    )
                    db.session.add(p)

        db.session.commit()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    
    @app.route('/api/allocate_stock', methods=['POST'])
    def allocate_stock():
        if session.get('role') != 'owner':
            return jsonify({"error": "Unauthorized"}), 401
        data = request.json
        product_id = data.get('product_id')
        shop = data.get('shop') # 'shop1', 'shop2', 'shop3'
        qty = int(data.get('qty', 0))
        return jsonify({"success": True, "message": f"Successfully allocated {qty} to {shop}"})

    return app

