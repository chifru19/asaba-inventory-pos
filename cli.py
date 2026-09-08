import click
from app import app
from extensions import db
from models import Product, Sale, SaleItem

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
        
        item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=qty,
            price_at_sale=product.selling_price
        )
        db.session.add(item)
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
