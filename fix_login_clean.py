path = "app/__init__.py"
with open(path, "r") as f:
    code = f.read()

# Replace or insert clean login route implementation
old_login_block = """@app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['role'] = user.role
                if user.role == 'owner':
                    return redirect(url_for('owner_dashboard'))
                else:
                    return redirect(url_for('pos'))

            return render_template('login.html', error="Invalid username or password")
        return render_template('login.html')"""

new_login_block = """@app.route('/login', methods=['GET', 'POST'])
def login():
    if requ    if requ    if requ    if reqer    if requ    if requt('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        pwd_field = getattr(user, 'password_hash', None) or getattr(user, 'password', None)
                                                       wd_f                                             '] = use                                                       wd_f    r.ro                                                       wd_f           d'))
            else:
                return redi                return redi             der_                return redi           use                return redi                return redi      """
                :" in code:
    # Let's do a robust replacement of the login function definition onward
    import re
    code = re.sub(r'@app\.route\(\'\/login\'    code = re.sub(r'@app\.route\(\'\/login\'', new_login_block, code, flags=re.DOTALL)
    with open(path, "w") as f    with  f.w    with open(path, "w") as f    with  f.w    with open(path, "w") arect indentat    with open(pathrint("⚠️ Could not find login route.")
