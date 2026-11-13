import os

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

health_route = '''
    @app.route('/health')
    def health_check():
        return {"status": "healthy"}, 200
'''

if "/health" not in code:
    if "@app.route('/')" in code:
        code = code.replace("@app.route('/')", health_route + "\n    @app.route('/')")
        with open(init_path, "w") as f:
            f.write(code)
        print("Successfully added /health route to app/__init__.py!")
    else:
        print("Error: Could not find @app.route('/') in app/__init__.py")
else:
    print("/health route already exists.")
