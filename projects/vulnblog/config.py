"""
VulnBlog - A Deliberately Vulnerable Blog Platform
WARNING: Contains intentional security vulnerabilities
FOR EDUCATIONAL PURPOSES ONLY
"""

import os
from datetime import datetime

class Config:
    """Application configuration with security issues"""
    SECRET_KEY = 'blog-secret-key-456'  # Hardcoded
    DEBUG = True
    
    # Database
    DATABASE = 'vulnblog.db'
    
    # File uploads
    UPLOAD_FOLDER = 'data/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html'}
    
    # Session
    SESSION_COOKIE_HTTPONLY = False  # Vulnerable to XSS exploitation
    SESSION_COOKIE_SAMESITE = None  # Vulnerable to CSRF
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # Admin
    ADMIN_USER = 'admin'
    ADMIN_PASS = 'Password123!'  # Weak password
    
    # CSRF (intentionally weak)
    WTF_CSRF_ENABLED = False  # CSRF protection disabled
