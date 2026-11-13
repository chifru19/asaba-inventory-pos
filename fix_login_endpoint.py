import os

init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

new_login = '''    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.get_json() or {}
            username = data.get('username') or request.form.get('username')
            password = data.get('password') or request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['role'] = user.role
                redirect_url = url_for('owner_dashboard') if user.role == 'owner' else url_for('pos')
                if request.is_json or request.headers.get('Content-Type') == 'application/json':
                    return jsonify({"success": True, "redirect": redirect_url})
                return redirect(redirect_url)
            
            if request.is_json or request.headers.get('Content-Type') == 'application/json':
                return jsonify({"success": False, "message": "Invalid username or password"}), 400
            return render_template('login.html', error="Invalid username or password")
        return render_template('login.html')'''

import re
code = re.sub(r'@app\.route\(\'/login\'[\s\S]*?def login\(\):[\s\S]*?(?=\n\s*@app\.route|\Z)', new_login + "\n\n", code)

with open(init_path, "w") as f:
    f.write(code)

print("Successfully updated login route!")
