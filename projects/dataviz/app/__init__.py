"""DataViz - Deliberately Vulnerable Data Analytics Platform

Vulnerabilities: Deserialization, RCE, CSV Injection, Info Disclosure, SSRF
"""

from flask import Flask


def create_app(config=None):
    """Factory pattern for app creation"""
    app = Flask(__name__)
    
    # Load config
    if config:
        app.config.from_object(config)
    else:
        from config import Config
        app.config.from_object(Config)
    
    # Initialize database
    from .models.database import init_db
    with app.app_context():
        init_db()
    
    # Register blueprints
    from .views.data import data_bp
    from .views.analysis import analysis_bp
    from .views.export import export_bp
    
    app.register_blueprint(data_bp, url_prefix='/data')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    app.register_blueprint(export_bp, url_prefix='/export')
    
    @app.route('/')
    def index():
        return {
            "app": "DataViz",
            "status": "running",
            "endpoints": [
                "/data/upload",
                "/data/load",
                "/analysis/eval",
                "/analysis/execute",
                "/export/csv",
                "/export/model"
            ]
        }
    
    return app
