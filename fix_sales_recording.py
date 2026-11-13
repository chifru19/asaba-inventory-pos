import os

# 1. Update app/models.py to ensure Sale model exists
models_path = "app/models.py"
if os.path.exists(models_path):
    with open(models_path, "r") as f:
        models_code = f.read()
    
    if "class Sale" not in models_code:
        sale_model = '''
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    shop = db.Column(db.String(50), default='shop1')
    items_json = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
'''
        models_code += "\n" + sale_model
        with open(models_path, "w") as f:
            f.write(models_code)
        print("Added Sale model to app/models.py!")

# 2. Update app/__init__.py with sales API routes and context
init_path = "app/__init__.py"
with open(init_path, "r") as f:
    init_code = f.read()

# Add Sale import if needed
if "Sale" not in init_code:
    init_code = init_code.replace("from app.models import Product, User", "from app.models import Product, User, Sale")

# Add sales API routes if not present
sales_routes = '''
    @app.route('/api/sales', methods=['GET', 'POST'])
    def handle_sales():
        from datetime import datetime, date
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
            
        if request.method == 'POST':
            data = request.json or {}
            items = data.get('items', [])
            total = float(data.get('total', 0))
            shop = data.get('shop', 'shop1')
            
            import json
            sale = Sale(
                user_id=session.get('user_id'),
                shop=shop,
                items_json=json.dumps(items),
                total=total
            )
            
            # Deduct stock
            for item in items:
                p_id = item.get('id')
                qty = item.get('qty', 1)
                product = Product.query.get(p_id)
                if product:
                    shop_attr = f"{shop}_stock"
                    current_stk = getattr(product, shop_attr, getattr(product, 'stock', 0))
                    setattr(product, shop_attr, max(0, current_stk - qty))
            
            db.session.add(sale)
            db.session.commit()
            return jsonify({"success": True, "message": "Sale completed and recorded successfully!"})
            
        # GET today's sales
        today_start = datetime.combine(date.today(), datetime.min.time())
        sales = Sale.query.filter(Sale.timestamp >= today_start).order_by(Sale.timestamp.desc()).all()
        
        sales_list = []
        for s in sales:
            sales_list.append({
                "id": s.id,
                "total": s.total,
                "shop": s.shop,
                "timestamp": s.timestamp.strftime("%H:%M:%S") if s.timestamp else "",
                "items": json.loads(s.items_json) if s.items_json else []
            })
        return jsonify(sales_list)
'''

if "/api/sales" not in init_code:
    init_code = init_code.replace("return app", sales_routes + "\n    return app")
    with open(init_path, "w") as f:
        f.write(init_code)
    print("Added /api/sales routes to app/__init__.py!")

# 3. Update pos() route to pass today's sales initially
init_code = init_code.replace(
    "products = Product.query.all()\n        return render_template('pos.html', products=products)",
    "products = Product.query.all()\n        from datetime import datetime, date\n        today_start = datetime.combine(date.today(), datetime.min.time())\n        sales = Sale.query.filter(Sale.timestamp >= today_start).order_by(Sale.timestamp.desc()).all()\n        return render_template('pos.html', products=products, sales=sales)"
)
with open(init_path, "w") as f:
    f.write(init_code)

# 4. Update app/templates/pos.html to send POST /api/sales and render sales dynamically
pos_path = "app/templates/pos.html"
if os.path.exists(pos_path):
    with open(pos_path, "r") as f:
        pos_html = f.read()
    
    # Replace completeSale function
    old_complete_sale = '''    function completeSale() {
        if (cart.length === 0) {
            alert("Cart is empty!");
            return;
        }
        alert("Sale completed successfully!");
        cart = [];
        updateCart();
    }'''

    new_complete_sale = '''    function completeSale() {
        if (cart.length === 0) {
            alert("Cart is empty!");
            return;
        }
        let total = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
        fetch('/api/sales', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ items: cart, total: total, shop: 'shop1' })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Sale completed successfully!");
                cart = [];
                updateCart();
                location.reload();
            } else {
                alert("Error recording sale: " + (data.error || "Unknown error"));
            }
        })
        .catch(err => {
            alert("Connection error while completing sale.");
            console.error(err);
        });
    }'''

    if old_complete_sale in pos_html:
        pos_html = pos_html.replace(old_complete_sale, new_complete_sale)
    
    # Update Sold Today section to render sales
    sold_today_old = '''                    <h4 class="text-sm font-black text-stone-800 uppercase tracking-wider mb-3">Sold Today</h4>
                    <p class="text-xs text-stone-400 italic">No sales recorded yet today.</p>'''

    sold_today_new = '''                    <h4 class="text-sm font-black text-stone-800 uppercase tracking-wider mb-3">Sold Today</h4>
                    {% if sales %}
                        <div class="space-y-3 max-h-60 overflow-y-auto">
                        {% for s in sales %}
                            <div class="bg-stone-50 p-3 rounded-xl border border-stone-200 text-xs">
                                <div class="flex justify-between font-bold text-stone-800 mb-1">
                                    <span>Sale #{{ s.id }}</span>
                                    <span class="text-teal-900">CFA {{ "{:,.0f}".format(s.total) }}</span>
                                </div>
                                <p class="text-[10px] text-stone-500">{{ s.timestamp }}</p>
                            </div>
                        {% endfor %}
                        </div>
                    {% else %}
                        <p class="text-xs text-stone-400 italic">No sales recorded yet today.</p>
                    {% endif %}'''

    if sold_today_old in pos_html:
        pos_html = pos_html.replace(sold_today_old, sold_today_new)
        with open(pos_path, "w") as f:
            f.write(pos_html)
        print("Successfully updated pos.html with dynamic sales submission and rendering!")

print("Sales recording fix applied successfully!")
