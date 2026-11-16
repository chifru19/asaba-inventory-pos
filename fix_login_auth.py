path = "app/__init__.py"
with open(path, "r") as f:
    code = f.read()

old_check = "if user and check_password_hash(user.password_hash, password):"
new_check = """pwd_field = getattr(user, 'password_hash', None) or getattr(user, 'password', None)
        if user and pwd_field and check_password_hash(pwd_field, password):"""

if old_check in code:
    code = code.replace(old_check, new_check)
    with open(path, "w") as f:
        f.write(code)
    print("✅ Successfully patched login authentication in app/__init__.py!")
else:
    print("⚠️ Exact login check block not found. Trying fallback replacement...")
    code = code.replace("check_password_hash(user.password_hash, password)", "check_password_hash(getattr(user, 'password_hash', None) or getattr(user, 'password', None), password)")
    with open(path, "w") as f:
        f.write(code)
    print("✅ Applied fallback patch!")
