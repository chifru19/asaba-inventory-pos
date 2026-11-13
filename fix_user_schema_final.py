import os

# 1. Update app/models.py to ensure the User model has the correct columns
models_path = "app/models.py"
with open(models_path, "r") as f:
    models_code = f.read()

# Make sure User model has password_hash and role, dropping obsolete/conflicting columns if needed
clean_user_model = '''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='worker')'''

# Replace User model definition
import re
models_code = re.sub(r'class User\(db\.Model\):[\s\S]*?(?=\n\nclass|\Z)', clean_user_model, models_code)

with open(models_path, "w") as f:
    f.write(models_code)
print("Updated app/models.py!")

# 2. Update app/__init__.py seeding logic to use password_hash properly
init_path = "app/__init__.py"
with open(init_path, "r") as f:
    init_code = f.read()

old_seed = '''        if not User.query.filter_by(username='owner').first():
            owner = User(username='owner', password=generate_password_hash('owner123'), role='owner')
            db.session.add(owner)
        if not User.query.filter_by(username='worker_shop1').first():
            worker = User(username='worker_shop1', password=generate_password_hash('worker123'), role='worker')
            db.session.add(worker)'''

new_seed = '''        if not User.query.filter_by(username='owner').first():
            owner = User(username='owner', password_hash=generate_password_hash('owner123'), role='owner')
            db.session.add(owner)
        if not User.query.filter_by(username='worker_shop1').first():
            worker = User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker')
            db.session.add(worker)'''

if old_seed in init_code:
    init_code = init_code.replace(old_seed, new_seed)
    with open(init_path, "w") as f:
        f.write(init_code)
    print("Updated app/__init__.py seed block!")

