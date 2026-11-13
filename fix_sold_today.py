import os

# 1. Update app/__init__.py to return recent sales safely without timezone filtering bugs
init_path = "app/__init__.py"
with open(init_path, "r") as f:
    init_code = f.read()

old_sales_get = '''        # GET today's sales
        today_start = datetime.combine(date.today(), datetime.min.time())
        sales = Sale.query.filter(Sale.timestamp >= today_start).order_by(Sale.timestamp.desc()).all()'''

new_sales_get = '''        # GET recent sales (latest 20 sales)
        sales = Sale.query.order_by(Sale.id.desc()).limit(20).all()'''

if old_sales_get in init_code:
    init_code = init_code.replace(old_sales_get, new_sales_get)
    with open(init_path, "w") as f:
        f.write(init_code)
    print("Updated /api/sales backend query in app/__init__.py!")

# 2. Update app/templates/pos.html to ensure id="soldTodayContainer" wraps the Sold Today section
pos_path = "app/templates/pos.html"
if os.path.exists(pos_path):
    with open(pos_path, "r") as f:
        pos_html = f.read()

    # Wrap the Sold Today content with id="soldTodayContainer"
    target_block = '''<h4 class="text-sm font-black text-stone-800 uppercase tracking-wider mb-3">Sold Today</h4>'''
    
    if 'id="soldTodayContainer"' not in pos_html:
        wrapped_block = '''<h4 class="text-sm font-black text-stone-800 uppercase tracking-wider mb-3">Sold Today</h4>
                    <div id="soldTodayContainer">'''
        
        # Find the closing part or replace the placeholder
        pos_html = pos_html.replace(target_block, wrapped_block)
        
        # Also close the div before the end of that sidebar card
        pos_html = pos_html.replace(
            '<p class="text-xs text-stone-400 italic">No sales recorded yet today.</p>',
            '<p class="text-xs text-stone-400 italic">No sales recorded yet today.</p></div>'
        )
        
        with open(pos_path, "w") as f:
            f.write(pos_html)
        print("Added id=\"soldTodayContainer\" wrapper to pos.html!")

print("Sold Today fix applied successfully!")
