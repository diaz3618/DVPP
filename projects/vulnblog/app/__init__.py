"""VulnBlog - Deliberately Vulnerable Blogging Platform

Vulnerabilities: XSS, CSRF, SSTI, RCE, Auth Bypass
"""

from flask import Flask
from .models.database import init_db


def create_app(config=None):
    """Factory pattern for app creation"""
    app = Flask(__name__, template_folder='templates')
    
    # Load config
    if config:
        app.config.from_object(config)
    else:
        from config import Config
        app.config.from_object(Config)
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register blueprints
    from .views.auth import auth_bp
    from .views.blog import blog_bp
    from .views.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app
