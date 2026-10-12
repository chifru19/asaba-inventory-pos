import click
from app import create_app
from app.extensions import db
from app.models import Product, Sale

app = create_app()

@click.group()
def cli():
    """Asaba Inventory & POS Command Line Interface"""
    pass

@cli.group()
def owner():
    """Owner-only secure commands: Add products & prices"""
    pass

@owner.command('add')
@click.option('--passcode', prompt=True, hide_input=True, help='Owner security passcode')
@click.option('--name', prompt='Product Name')
@click.option('--sku', prompt='Product SKU')
@click.option('--buy', type=float, prompt='Purchase Price')
@click.option('--sell', type=float, prompt='Selling Price')
@click.option('--stock', type=int, prompt='Initial Stock Quantity')
@click.option('--min-stock', type=int, default=3, prompt='Minimum Threshold')
def owner_add(passcode, name, sku, buy, sell, stock, min_stock):
    if passcode != 'asaba2026owner':
        click.echo('❌ Access Denied: Incorrect Owner Passcode.')
        return
    
    with app.app_context():
        product = Product(
            name=name, sku=sku, 
            purchase_price=buy, selling_price=sell, 
            stock_quantity=stock, min_threshold=min_stock
        )
        db.session.add(product)
        db.session.commit()
        click.echo(f'✅ Success: Product "{name}" (SKU: {sku}) added by Owner!')

@owner.command('seed-all')
@click.option('--passcode', prompt=True, hide_input=True, help='Owner security passcode')
def owner_seed_all(passcode):
    """Bulk seed all inventory items from the store catalog"""
    if passcode != 'asaba2026owner':
        click.echo('❌ Access Denied: Incorrect Owner Passcode.')
        return
        
    initial_items = [
        {"name": "Bl-deo Mn Fresh&Exdry", "sku": "BL-01", "buy": 667.0, "sell": 1000.0, "stock": 50},
        {"name": "Bl-deo Mn Inv& Sens", "sku": "BL-02", "buy": 667.0, "sell": 1000.0, "stock": 50},
        {"name": "BL-SPRAY 4 Wm 48H", "sku": "BL-03", "buy": 667.0, "sell": 9000.0, "stock": 30},
        {"name": "BL-SPRAY men F&EF", "sku": "BL-04", "buy": 667.0, "sell": 10000.0, "stock": 25},
        {"name": "DEO ROLLON mn", "sku": "BL-05", "buy": 72720.60, "sell": 800800.0, "stock": 43},
        {"name": "DEO ROLLON WN", "sku": "BL-06", "buy": 120120.0, "sell": 800800.0, "stock": 72},
        {"name": "10BL-Bodylotion", "sku": "BL-07", "buy": 168.0, "sell": 1500.0, "stock": 10},
        {"name": "10BL-Bodymilk", "sku": "BL-08", "buy": 165.0, "sell": 1500.0, "stock": 10},
        {"name": "Cien Spray 4Men", "sku": "CN-01", "buy": 731460.0, "sell": 1000.0, "stock": 1000},
        {"name": "LD-Dentalux-Complex 3", "sku": "LD-01", "buy": 175420.0, "sell": 800.0, "stock": 800},
    ]
    
    with app.app_context():
        added_count = 0
        for data in initial_items:
            existing = Product.query.filter_by(sku=data["sku"]).first()
            if not existing:
                product = Product(
                    name=data["name"],
                    sku=data["sku"],
                    purchase_price=data["buy"],
                    selling_price=data["sell"],
                    stock_quantity=data["stock"],
                    min_threshold=3
                )
                db.session.add(product)
                added_count += 1
        
        db.session.commit()
        click.echo(f'✅ Successfully seeded {added_count} new items into the inventory!')

@cli.group()
def sales():
    """Cashier actions: Record sales & automatically subtract stock"""
    pass

@sales.command('record')
@click.option('--sku', prompt='Product SKU', help='SKU of item sold')
@click.option('--qty', type=int, prompt='Quantity Sold', help='Quantity sold')
def sales_record(sku, qty):
    with app.app_context():
        product = Product.query.filter_by(sku=sku).first()
        if not product:
            click.echo(f'❌ Error: Product with SKU "{sku}" not found in inventory.')
            return
        
        if product.stock_quantity < qty:
            click.echo(f'❌ Error: Insufficient stock for {product.name}. Available: {product.stock_quantity}')
            return
        
        product.stock_quantity -= qty
        total = product.selling_price * qty
        sale = Sale(total_amount=total)
        db.session.add(sale)
        db.session.flush()
        
        db.session.commit()
        
        click.echo(f'✅ Sale Recorded: {qty}x {product.name} @ {product.selling_price:,.2f} = Total: {total:,.2f}')
        click.echo(f'📦 Updated Stock for {product.name}: {product.stock_quantity} remaining.')

@cli.command('inventory')
def list_inventory():
    """View current inventory catalog and stock levels"""
    with app.app_context():
        products = Product.query.all()
        click.echo("\n--- ASABA INVENTORY CATALOG ---")
        for p in products:
            click.echo(f"[{p.sku}] {p.name} | Price: {p.selling_price:,.2f} | Stock: {p.stock_quantity}")

if __name__ == '__main__':
    cli()