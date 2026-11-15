from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    print("--- Checking Existing Users ---")
    users = User.query.all()
    for u in users:
        print(f"Found username: {u.username}")

    # Ensure all common username variations exist with password123
    target_usernames = ["owner", "admin", "shop1", "worker_shop1", "shop2", "worker_shop2", "shop3", "worker_shop3"]
    pwd_hash = generate_password_hash("password123")

    for uname in target_usernames:
        user = User.query.filter_by(username=uname).first()
        if not user:
            user = User(username=uname, password=pwd_hash) if hasattr(User, "password") else User(username=uname, password_hash=pwd_hash)
            db.session.add(user)
            print(f"Created missing user: {uname}")
        else:
            if hasattr(user, "password"):
                user.password = pwd_hash
            else:
                user.password_hash = pwd_hash
            print(f"Updated password for: {uname}")

    db.session.commit()
    print("\n✅ All user accounts successfully synced and ready with password: password123")
