"""User model with authentication vulnerabilities

VULNERABILITIES:
- Auth Bypass: No password hashing, plain comparison
- SQLi: String concatenation in queries
"""

import sqlite3
from .database import get_db


class User:
    """User model - DELIBERATELY INSECURE"""
    
    @staticmethod
    def authenticate(username, password):
        """VULN: SQL Injection via string concatenation
        CVE Reference: Similar to CVE-2025-64459 (Django SQLi)
        
        Exploit: username=' OR '1'='1'--
        """
        db = get_db()
        # VULN: SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor = db.execute(query)
        user = cursor.fetchone()
        return dict(user) if user else None
    
    @staticmethod
    def find_by_username(username):
        """VULN: SQL Injection in user lookup
        
        Exploit: username=' UNION SELECT 1,2,3,4,5,6--
        """
        db = get_db()
        # VULN: SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}'"
        cursor = db.execute(query)
        user = cursor.fetchone()
        return dict(user) if user else None
    
    @staticmethod
    def create_user(username, password, email, bio=""):
        """VULN: No password hashing, XSS in bio
        CVE Reference: Similar to CVE-2016-6186 (Django XSS)
        """
        db = get_db()
        try:
            # VULN: Plain text password storage
            cursor = db.execute(
                "INSERT INTO users (username, password, email, bio) VALUES (?, ?, ?, ?)",
                (username, password, email, bio)  # VULN: bio not sanitized - XSS
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    @staticmethod
    def update_profile(user_id, bio):
        """VULN: Stored XSS via profile bio
        CVE Reference: CVE-2021-42053 (django-unicorn XSS)
        
        Exploit: bio='<script>alert(document.cookie)</script>'
        """
        db = get_db()
        # VULN: No sanitization - Stored XSS
        db.execute("UPDATE users SET bio=? WHERE id=?", (bio, user_id))
        db.commit()
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        db = get_db()
        cursor = db.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    @staticmethod
    def list_all():
        """List all users"""
        db = get_db()
        cursor = db.execute("SELECT id, username, email, is_admin, bio FROM users")
        return [dict(row) for row in cursor.fetchall()]
