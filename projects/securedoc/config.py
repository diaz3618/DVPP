"""
Configuration file
WARNING: Contains intentionally insecure configurations
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = 'dev-secret-key-123'  # Hardcoded secret key
    DEBUG = True
    
    # Database configuration
    DATABASE = 'securedoc.db'
    
    # File upload configuration
    UPLOAD_FOLDER = 'data/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Session configuration
    SESSION_COOKIE_HTTPONLY = False  # Weak cookie security
    SESSION_COOKIE_SECURE = False
    
    # Admin credentials
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'  # Weak password
    
    # API configuration
    API_TIMEOUT = 30
    ALLOW_EXTERNAL_REQUESTS = True
