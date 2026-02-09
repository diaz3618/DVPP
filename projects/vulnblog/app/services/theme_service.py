"""Theme management service"""

from ..models.database import get_db


class ThemeService:
    """Theme management - DELIBERATELY INSECURE"""
    
    @staticmethod
    def get_active_theme():
        """Get currently active theme"""
        db = get_db()
        cursor = db.execute("SELECT * FROM themes WHERE active=1")
        theme = cursor.fetchone()
        return dict(theme) if theme else None
    
    @staticmethod
    def set_theme(theme_id):
        """VULN: No CSRF protection, no auth check"""
        db = get_db()
        # Deactivate all themes
        db.execute("UPDATE themes SET active=0")
        # Activate selected theme
        db.execute("UPDATE themes SET active=1 WHERE id=?", (theme_id,))
        db.commit()
    
    @staticmethod
    def create_custom_theme(name, template):
        """VULN: Allows user-controlled SSTI templates
        
        Exploit: template='{{ config.items() }}' or RCE payloads
        """
        db = get_db()
        cursor = db.execute(
            "INSERT INTO themes (name, template, active) VALUES (?, ?, 0)",
            (name, template)  # VULN: No validation
        )
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def list_all():
        """List all themes"""
        db = get_db()
        cursor = db.execute("SELECT * FROM themes")
        return [dict(row) for row in cursor.fetchall()]
