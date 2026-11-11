# Asaba Inventory & POS System

A custom, lightweight multi-store Inventory and Point of Sale (POS) application built specifically for Ngia Ngu's shops. Designed to manage multiple stores, track real-time stock levels, record daily revenue, and automate low-stock reorder alerts.

## Features

* **Multi-Store Management**: Supports separate inventory catalogs and sales summaries across multiple shops (Shop 1, Shop 2, and Shop 3).
* **Owner Dashboard**: Live calculation of store-specific sales revenue, active product counts, and easy store switching.
* **Automated Reorder Alerts**: Instantly flags items that fall below their minimum stock threshold.
* **Inventory Catalog**: Manages product registration, prices in CFA, initial stock, and store assignment.
* **POS Checkout**: Seamlessly deducts stock quantities and logs transactions per sale.

## Tech Stack

* **Backend**: Python (Flask, Flask-SQLAlchemy, Flask-Migrate, Gunicorn)
* **Database**: SQLite
* **Frontend**: Bootstrap 5, Jinja2 Templates

## Local Demonstration Setup

To run the application locally for demonstrations using Gunicorn:

### 1. Clone and Navigate to the Repository
```bash
git clone [https://github.com/chifru19/asaba-inventory-pos.git](https://github.com/chifru19/asaba-inventory-pos.git)
cd asaba-inventory-pos
2. Activate the Virtual Environment
Bash
source venv/bin/activate
3. Seed the Database
Bash
rm -f instance/*.db
python seed.py
4. Run the Application with Gunicorn
Bash
gunicorn run:app --bind 0.0.0.0:8000
Once running, open your browser and navigate to:http://127.0.0.1:8000

Developer Profile
Lead Developer: Frank Fru

Website: frankfru.com

GitHub: github.com/chifru19

LinkedIn: LinkedIn Profile

Contact Email: chifru19@googlemail.com


### Follow-Up Commands

Run the following command in your terminal to update your repository with this clean file:

```bash
cat << 'EOF' > README.md
# Asaba Inventory & POS System

A custom, lightweight multi-store Inventory and Point of Sale (POS) application built specifically for Ngia Ngu's shops. Designed to manage multiple stores, track real-time stock levels, record daily revenue, and automate low-stock reorder alerts.

## Features

* **Multi-Store Management**: Supports separate inventory catalogs and sales summaries across multiple shops (Shop 1, Shop 2, and Shop 3).
* **Owner Dashboard**: Live calculation of store-specific sales revenue, active product counts, and easy store switching.
* **Automated Reorder Alerts**: Instantly flags items that fall below their minimum stock threshold.
* **Inventory Catalog**: Manages product registration, prices in CFA, initial stock, and store assignment.
* **POS Checkout**: Seamlessly deducts stock quantities and logs transactions per sale.

## Tech Stack

* **Backend**: Python (Flask, Flask-SQLAlchemy, Flask-Migrate, Gunicorn)
* **Database**: SQLite
* **Frontend**: Bootstrap 5, Jinja2 Templates

## Local Demonstration Setup

To run the application locally for demonstrations using Gunicorn:

### 1. Clone and Navigate to the Repository
```bash
git clone [https://github.com/chifru19/asaba-inventory-pos.git](https://github.com/chifru19/asaba-inventory-pos.git)
cd asaba-inventory-pos
2. Activate the Virtual Environment
Bash
source venv/bin/activate
3. Seed the Database
Bash
rm -f instance/*.db
python seed.py
4. Run the Application with Gunicorn
Bash
gunicorn run:app --bind 0.0.0.0:8000
Once running, open your browser and navigate to:http://127.0.0.1:8000

Developer Profile
Lead Developer: Frank Fru

Website: frankfru.com

GitHub: github.com/chifru19

LinkedIn: LinkedIn Profile

Contact Email: chifru19@googlemail.com
EOF
