"""
Authentication views
Handles login, logout, and user registration
"""

from flask import Blueprint, request, redirect, url_for, session, render_template_string
from app.services.auth import AuthService
from app.models.user import User
from app.utils.helpers import render_content

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login endpoint
    Calls vulnerable authentication methods
    """
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Calls User.authenticate which has SQL injection
        user = AuthService.login(username, password)
        
        if user:
            return redirect(url_for('docs.list_documents'))
        else:
            error_msg = request.args.get('error', 'Invalid credentials')
            # XSS vulnerability: error message not escaped
            return f"""
            <html><body>
                <h2>Login Failed</h2>
                <p>{error_msg}</p>
                <a href="/auth/login">Try again</a>
            </body></html>
            """
    
    # Simple login form
    return '''
    <html><body>
        <h2>Login</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </body></html>
    '''

@auth_bp.route('/logout')
def logout():
    """Logout endpoint"""
    AuthService.logout()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
def profile():
    """
    User profile page
    VULNERABILITY: XSS in profile display
    """
    if not AuthService.is_authenticated():
        return redirect(url_for('auth.login'))
    
    user = AuthService.get_current_user()
    
    # Get custom bio/message from query params
    message = request.args.get('message', '')
    
    # Vulnerable: Unescaped user data
    return f"""
    <html><body>
        <h1>Profile: {user.username}</h1>
        <p>Email: {user.email}</p>
        <p>Role: {user.role}</p>
        {f'<div class="message">{message}</div>' if message else ''}
        <a href="/auth/logout">Logout</a>
    </body></html>
    """

@auth_bp.route('/search')
def search_users():
    """
    Search for users
    VULNERABILITY: SQL injection via User.search_users
    """
    query = request.args.get('q', '')
    
    if query:
        # Calls vulnerable search method
        users = User.search_users(query)
        
        results_html = '<ul>'
        for user in users:
            results_html += f'<li>{user.username} - {user.email}</li>'
        results_html += '</ul>'
        
        # XSS vulnerability: query not escaped
        return f"""
        <html><body>
            <h2>Search Results for: {query}</h2>
            {results_html}
        </body></html>
        """
    
    return '''
    <html><body>
        <h2>Search Users</h2>
        <form method="get">
            <input type="text" name="q" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
    </body></html>
    '''

@auth_bp.route('/update_profile', methods=['POST'])
def update_profile():
    """
    Update user profile
    VULNERABILITY: SQL injection via User.update_profile
    """
    if not AuthService.is_authenticated():
        return redirect(url_for('auth.login'))
    
    user = AuthService.get_current_user()
    
    # Get all form data
    update_data = request.form.to_dict()
    
    # Calls vulnerable update method with user-controlled keys and values
    User.update_profile(user.id, update_data)
    
    return redirect(url_for('auth.profile'))
