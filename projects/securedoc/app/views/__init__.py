"""
Views package - Flask blueprints for routing
Each module represents a feature area of the application
"""

from app.views.auth import auth_bp
from app.views.documents import docs_bp
from app.views.admin import admin_bp
from app.views.api import api_bp

__all__ = ['auth_bp', 'docs_bp', 'admin_bp', 'api_bp']
