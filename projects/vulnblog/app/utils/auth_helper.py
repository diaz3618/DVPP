"""Authentication helpers - DELIBERATELY INSECURE

VULNERABILITIES:
- Session fixation
- Weak session management
- No session timeout
"""

from flask import session, request
from functools import wraps


def login_user(user):
    """VULN: Session fixation - doesn't regenerate session ID
    CVE Reference: CVE-2013-4200 (Plone session hijacking)
    
    Should call session.regenerate() but doesn't
    """
    # VULN: Session fixation vulnerability
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['is_admin'] = user.get('is_admin', 0)
    # VULN: No session regeneration
    # VULN: No session timeout set


def logout_user():
    """Clear session"""
    session.clear()


def get_current_user():
    """Get current logged-in user"""
    if 'user_id' in session:
        return {
            'id': session['user_id'],
            'username': session['username'],
            'is_admin': session.get('is_admin', 0)
        }
    return None


def login_required(func):
    """VULN: Weak authentication check"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # VULN: Easily bypassable - just check session
        if 'user_id' not in session:
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """VULN: Admin check via session value (can be manipulated)
    CVE Reference: CVE-2022-37109 (Auth bypass), CVE-2022-31125 (Auth control)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # VULN: Relies on client-side session data
        if not session.get('is_admin'):
            # VULN: Can bypass by setting session['is_admin'] = 1
            return "Forbidden", 403
        return func(*args, **kwargs)
    return wrapper
