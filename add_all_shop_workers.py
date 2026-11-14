with open("app/__init__.py", "r") as f:
    code = f.read()

# Target the user creation block and expand it to include worker_shop2 and worker_shop3
old_block = '''            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))'''

new_block = '''            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='worker_shop2').first():
                db.session.add(User(username='worker_shop2', password_hash=generate_password_hash('worker123'), role='worker'))
            if not User.query.filter_by(username='worker_shop3').first():
                db.session.add(User(username='worker_shop3', password_hash=generate_password_hash('worker123'), role='worker'))'''

if old_block in code:
    code = code.replace(old_block, new_block)
    with open("app/__init__.py", "w") as f:
        f.write(code)
    print("Successfully added worker_shop2 and worker_shop3 seeding!")
else:
    print("Could not find target seeding block.")
