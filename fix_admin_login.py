import os

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

# Update auto-seed to include 'admin' as well
old_seed = '''        if not User.query.filter_by(username='owner').first():
            db.session.add(User(username='owner', password_hash=generate_password_hash('owner123'), role='owner'))'''

new_seed = '''        if not User.query.filter_by(username='owner').first():
            db.session.add(User(username='owner', password_hash=generate_password_hash('owner123'), role='owner'))
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', password_hash=generate_password_hash('admin123'), role='owner'))'''

if old_seed in code:
    code = code.replace(old_seed, new_seed)
    with open(init_path, "w") as f:
        f.write(code)
    print("Added admin user seeding!")

