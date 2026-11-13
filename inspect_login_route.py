with open("app/__init__.py", "r") as f:
    lines = f.readlines()

in_login = False
for line in lines:
    if "def login():" in line:
        in_login = True
    if in_login:
        print(line, end="")
        if "return" in line and "render_template" in line and not line.strip().startswith("if") and not line.strip().startswith("elif") and not line.strip().startswith("else"):
            # check if we exited login function or if it's the end
            pass
    if in_login and line.strip().startswith("@app.route"):
        if "def login" not in line:
            break
