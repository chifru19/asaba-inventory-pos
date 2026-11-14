with open("app/__init__.py", "r") as f:
    code = f.read()

print("=== ALLOCATE STOCK ROUTE ===")
start = code.find("def allocate_stock")
if start != -1:
    print(code[start:start+1000])

print("\n=== OWNER DASHBOARD TEMPLATE CHECK ===")
if os.path.exists("app/templates/owner_dashboard.html"):
    with open("app/templates/owner_dashboard.html", "r") as tf:
        t_content = tf.read()
        print("Owner dashboard length:", len(t_content))
        if "sales" in t_content.lower():
            print("Found sales in owner dashboard template")
        else:
            print("Sales summary missing from owner dashboard template!")
