"""Configuration for DataViz - DELIBERATELY INSECURE"""

import os


class Config:
    """Vulnerable configuration"""
    
    # VULN: Hardcoded secret key
    SECRET_KEY = 'dataviz-secret-789'
    
    # VULN: Debug mode enabled
    DEBUG = True
    
    # Database
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'dataviz.db')
    
    # Upload folder
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'data', 'uploads')
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
    
    #VULN: Allows pickle files
    ALLOWED_EXTENSIONS = {'csv', 'json', 'pkl', 'pickle', 'txt', 'py'}
    
    # VULN: Info disclosure
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    
    # VULN: No security headers
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SAMESITE = None
