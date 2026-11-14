with open("app/__init__.py", "r") as f:
    code = f.read()

start = code.find("def allocate_stock")
if start != -1:
    print(code[start:start+1200])
