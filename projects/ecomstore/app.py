"""EcomStore - E-commerce Platform | Vulnerabilities: SQLi, XSS, RCE, CSRF, Auth Bypass"""
from flask import Flask, request, jsonify, render_template_string, session
import sqlite3, os, subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecom-secret'
DB = '/tmp/ecom.db'

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INT, name TEXT, price REAL, description TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INT, username TEXT, password TEXT, is_admin INT)')
    conn.execute('CREATE TABLE IF NOT EXISTS orders (id INT, user_id INT, product_id INT, quantity INT)')
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 1)")
    conn.execute("INSERT OR IGNORE INTO products VALUES (1, 'Laptop', 999.99, '<b>Premium laptop</b>')")
    conn.commit()
    conn.close()

init_db()

# VULN: SQLi - CVE-2025-64459 (Django SQLi), CVE-2010-1327 (TornadoStore SQLi)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # VULN: SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    conn = sqlite3.connect(DB)
    result = conn.execute(query).fetchone()
    conn.close()
    if result:
        session['user_id'] = result[0]
        session['is_admin'] = result[3]
        return jsonify({"login": "success", "user": username})
    return jsonify({"error": "Invalid credentials"}), 401

# VULN: XSS - CVE-2021-42053, CVE-2016-6186
@app.route('/products')
def products():
    search = request.args.get('search', '')
    conn = sqlite3.connect(DB)
    # VULN: SQLi + XSS
    query = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
    results = conn.execute(query).fetchall()
    conn.close()
    html = '<h1>Products</h1>'
    for p in results:
        # VULN: XSS - no escaping
        html += f'<div><h3>{p[1]}</h3><p>{p[3]}</p><p>Price: ${p[2]}</p></div>'
    return render_template_string(html)

# VULN: CSRF - CVE-2025-28062 (ERPNext CSRF)
@app.route('/order', methods=['POST'])
def place_order():
    # VULN: No CSRF protection
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)
    user_id = session.get('user_id', 0)
    conn = sqlite3.connect(DB)
    conn.execute(f"INSERT INTO orders VALUES (NULL, {user_id}, {product_id}, {quantity})")
    conn.commit()
    conn.close()
    return jsonify({"order": "placed"})

# VULN: RCE - CVE-2024-42845
@app.route('/admin/execute', methods=['POST'])
def admin_exec():
    # VULN: Weak admin check
    if session.get('is_admin'):
        code = request.json.get('code')
        # VULN: exec RCE
        exec(code)
        return jsonify({"executed": True})
    return jsonify({"error": "Forbidden"}), 403

# VULN: Path traversal in invoice download
@app.route('/invoice')
def invoice():
    file_path = request.args.get('path', '/tmp/invoice.pdf')
    # VULN: Path traversal
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except:
        return "Not found", 404

@app.route('/')
def index():
    return {"app": "EcomStore", "port": 5005, "endpoints": ["/login", "/products?search=", "/order", "/admin/execute", "/invoice?path="]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
