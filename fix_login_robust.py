import os

# 1. Update app/__init__.py to handle standard form POST requests cleanly
init_path = "app/__init__.py"
with open(init_path, "r") as f:
    code = f.read()

robust_login = '''    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Ensure default accounts always exist
        try:
            if not User.query.filter_by(username='owner').first():
                db.session.add(User(username='owner', password_hash=generate_password_hash('owner123'), role='owner'))
            if not User.query.filter_by(username='worker_shop1').first():
                db.session.add(User(username='worker_shop1', password_hash=generate_password_hash('worker123'), role='worker'))
            db.session.commit()
        except Exception:
            db.session.rollback()

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
        return render_template('login.html')'''

import re
code = re.sub(r'@app\.route\(\'/login\'[\s\S]*?def login\(\):[\s\S]*?(?=\n\s*@app\.route|\Z)', robust_login + "\n\n", code)

with open(init_path, "w") as f:
    f.write(code)

# 2. Update app/templates/login.html to use standard form submission
login_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Asaba POS</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-stone-100 min-h-screen flex items-center justify-center font-sans">
    <div class="bg-white p-8 rounded-2xl shadow-xl border border-stone-200 max-w-md w-full space-y-6">
        <div class="text-center">
            <h2 class="text-2xl font-black text-stone-800 uppercase tracking-wider">Asaba POS Login</h2>
            <p class="text-xs text-stone-500 mt-1">Sign in to manage inventory & sales</p>
        </div>

        {% if error %}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-xs font-bold text-center">
            {{ error }}
        </div>
        {% endif %}

        <form method="POST" action="/login" class="space-y-4">
            <div>
                <label class="block text-xs font-bold text-stone-700 uppercase tracking-wider mb-2">Username</label>
                <input type="text" name="username" required class="w-full px-4 py-3 bg-stone-50 border border-stone-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-800">
            </div>
            <div>
                <label class="block text-xs font-bold text-stone-700 uppercase tracking-wider mb-2">Password</label>
                <input type="password" name="password" required class="w-full px-4 py-3 bg-stone-50 border border-stone-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-800">
            </div>
            <button type="submit" class="w-full bg-teal-900 text-white py-3 rounded-xl font-black uppercase text-xs tracking-widest hover:bg-teal-950 transition shadow-md">
                Login
            </button>
        </form>
    </div>
</body>
</html>
'''

with open("app/templates/login.html", "w") as f:
    f.write(login_html)

print("Successfully updated login route and template to robust form submission!")
