import os

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

seed_code = '''
    with app.app_context():
        db.create_all()
        from werkzeug.security import generate_password_hash
        # Create default owner if not exists
        if not User.query.filter_by(username='owner').first():
            owner = User(username='owner', password=generate_password_hash('owner123'), role='owner')
            db.session.add(owner)
        # Create default worker if not exists
        if not User.query.filter_by(username='worker_shop1').first():
            worker = User(username='worker_shop1', password=generate_password_hash('worker123'), role='worker')
            db.session.add(worker)
        db.session.commit()
'''

if "User.query.filter_by(username='owner')" not in code:
    code = code.replace("db.create_all()", seed_code)
    with open(init_path, "w") as f:
        f.write(code)
    print("Added automatic user seeding to app/__init__.py!")

