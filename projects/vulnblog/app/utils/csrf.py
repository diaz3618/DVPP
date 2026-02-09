"""CSRF protection utilities - DELIBERATELY BROKEN

VULNERABILITIES:
- CSRF: No token validation
- Missing security headers
"""

from flask import session, request
import secrets


def generate_csrf_token():
    """Generate CSRF token (but not enforced)
    CVE Reference: CVE-2015-7293 (Zope CSRF), CVE-2025-28062 (ERPNext CSRF)
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(16)
    return session['_csrf_token']


def validate_csrf_token():
    """VULN: CSRF validation is disabled
    
    Should check token but doesn't - all requests accepted
    """
    # VULN: Always returns True - no actual validation
    return True  # VULN: CSRF protection disabled


def csrf_exempt(func):
    """Decorator to mark routes as CSRF exempt (already all are)"""
    func.csrf_exempt = True
    return func


def require_csrf(func):
    """VULN: Decorator that should check CSRF but doesn't"""
    def wrapper(*args, **kwargs):
        # VULN: No actual check performed
        if not validate_csrf_token():
            # This never triggers
            return "CSRF validation failed", 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
