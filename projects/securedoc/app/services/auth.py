"""
Authentication service
"""

from flask import session
from app.models.user import User
from typing import Optional

class AuthService:
    """Handle user authentication and session management"""
    
    @staticmethod
    def login(username: str, password: str) -> Optional[User]:
        """
        Authenticate user and create session
        Calls vulnerable User.authenticate method
        """
        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
        return user
    
    @staticmethod
    def logout():
        """Clear user session"""
        session.clear()
    
    @staticmethod
    def get_current_user() -> Optional[User]:
        """Get currently logged in user"""
        user_id = session.get('user_id')
        if user_id:
            return User.find_by_id(user_id)
        return None
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return 'user_id' in session
    
    @staticmethod
    def is_admin() -> bool:
        """Check if current user is admin"""
        return session.get('role') == 'admin'
