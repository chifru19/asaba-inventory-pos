import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    pwd_hash = generate_password_hash("password123")
    
    users_config = {
        "owner": {"role": "owner", "store_id": "main"},
        "admin": {"role": "owner", "store_id": "main"},
        "shop1": {"role": "worker", "store_id": "shop1"},
        "worker_shop1": {"role": "worker", "store_id": "shop1"},
        "shop2": {"role": "worker", "store_id": "shop2"},
        "worker_shop2": {"role": "worker", "store_id": "shop2"},
        "shop3": {"role": "worker", "store_id": "shop3"},
        "worker_shop3": {"role": "worker", "store_id": "shop3"},
    }

    for uname, cfg in users_config.items():
        user = User.query.filter_by(username=uname).first()
        if not user:
            user = User(username=uname)
            db.session.add(user)
            print(f"Created user: {uname}")
        else:
            print(f"Updating user: {uname}")

        user.password_hash = pwd_hash
        if hasattr(user, "role"):
            user.role = cfg["role"]
        if hasattr(user, "store_id"):
            user.store_id = cfg["store_id"]

    db.session.commit()
    print("✅ All shop accounts successfully seeded!")

