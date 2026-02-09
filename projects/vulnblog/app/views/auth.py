"""Authentication views

VULNERABILITIES:
- SQLi in login
- No CSRF protection- Session fixation
"""

from flask import Blueprint, request, jsonify, render_template_string
from ..models.user import User
from ..utils.auth_helper import login_user, logout_user, get_current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """VULN: SQL Injection + No CSRF
    CVE Reference: CVE-2025-64459 (Django SQLi)
    
    Exploit: POST username=admin'-- &password=anything
    """
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULN: SQL Injection via User.authenticate
        user = User.authenticate(username, password)
        
        if user:
            # VULN: Session fixation
            login_user(user)
            return jsonify({"success": True, "message": "Logged in", "user": user['username']})
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    # Simple login form
    return render_template_string('''
        <html><body>
        <h2>VulnBlog Login</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
        <p>Default users: admin/admin123, blogger/password, user/user</p>
        </body></html>
    ''')


@auth_bp.route('/register', methods=['POST'])
def register():
    """VULN: XSS in bio, no CSRF protection
    CVE Reference: CVE-2021-42053 (XSS)
    
    Exploit: POST bio=<script>alert(1)</script>
    """
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    bio = request.form.get('bio', '')  # VULN: No sanitization
    
    # VULN: Stored XSS in bio
    user_id = User.create_user(username, password, email, bio)
    
    if user_id:
        return jsonify({"success": True, "message": "User created", "user_id": user_id})
    else:
        return jsonify({"success": False, "message": "Username already exists"}), 400


@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    """VULN: No CSRF protection on logout"""
    logout_user()
    return jsonify({"success": True, "message": "Logged out"})


@auth_bp.route('/profile', methods=['GET'])
def profile():
    """Display current user profile"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    full_user = User.get_by_id(user['id'])
    return jsonify(full_user)


@auth_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """VULN: Stored XSS + No CSRF
    CVE Reference: CVE-2021-42053 (Stored XSS)
    
    Exploit: POST bio=<img src=x onerror=alert(document.cookie)>
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    bio = request.form.get('bio', '')
    # VULN: Stored XSS via bio
    User.update_profile(user['id'], bio)
    
    return jsonify({"success": True, "message": "Profile updated"})
