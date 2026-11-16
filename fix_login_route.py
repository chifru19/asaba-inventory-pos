path = "app/__init__.py"
with open(path, "r") as f:
    code = f.read()

old_block = """    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            pwd_field = getattr(user, 'password_hash', None) or getattr(user, 'password', None)
        if user and pwd_field and check_password_hash(pwd_field, password):
                session['user_id'] = user.id
                session['role'] = user.role
                if user.role == 'owner':
                    return redirect(url_for('owner_dashboard'))
                else:
                    return redirect(url_for('pos'))

            return render_template('login.html', error="Invalid username or password")
        return render_template('login.html')"""

new_block = """    @app.route('/login', methods=[new_block = """    @app.route():
        if request.method == 'POST':
            username = request.form.g            username = request.form.g            username = reqd')

            user = User.query.filter_by(username=username).first()
            pwd_field = getattr(user            pwd_field = getattr(user            ord',            pwd_field = getattr(user            pwd_field = gash(pw            pwd_field = getattr(user            pwd_field = getattr(user            ord',     ']            pwd_field = getattr(user            pwd_field = getattr(user  return redirect(url_for('owner_dashboard'))
                                            turn redirect(url_for('pos'))

            return render_template('login.html', error="Invalid username or password")
        return render_template('login.html')"""

if old_block in code:
    code = code.replace(old_block, new_block)
    with open(path, "w") as f:
        f.write(code)
    print("✅ Successfully fixed login route indentation!")
else:
    print("⚠️ Exact match not found. Applying direct regex correction...")
    import re
    code = re.sub(r'        pwd_field = getattr\(user, \'password_hash\', None\) or getattr\(user, \'password\', None\)\n        if user', '        pwd_field = getattr(user, \'password_hash\', None) or getattr(user, \'password\', None)\n            if user', code)
    with open(path, "w") as f:
        f.write(code)
    print("✅ Applied regex correction!")
