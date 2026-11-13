import os

print("--- login.html ---")
if os.path.exists("app/templates/login.html"):
    with open("app/templates/login.html", "r") as f:
        print(f.read())
else:
    print("login.html not found!")

print("\n--- app/__init__.py snippet ---")
if os.path.exists("app/__init__.py"):
    with open("app/__init__.py", "r") as f:
        content = f.read()
        for line in content.splitlines():
            if "login" in line or "User" in line or "generate_password_hash" in line:
                print(line)

