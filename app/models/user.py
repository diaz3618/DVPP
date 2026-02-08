"""
User model with SQL injection vulnerabilities
"""

import sqlite3
from typing import Optional, Dict

class User:
    """User model with vulnerable SQL queries"""
    
    def __init__(self, id: int, username: str, email: str, role: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.password = password
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        conn = sqlite3.connect('securedoc.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """
        Find user by username
        VULNERABILITY: SQL Injection via string concatenation
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: Direct string concatenation
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['id'], row['username'], row['email'], 
                      row['role'], row['password'])
        return None
    
    @classmethod
    def find_by_id(cls, user_id: int) -> Optional['User']:
        """
        Find user by ID
        VULNERABILITY: SQL Injection via string formatting
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: String formatting
        query = "SELECT * FROM users WHERE id = {}".format(user_id)
        cursor.execute(query)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['id'], row['username'], row['email'], 
                      row['role'], row['password'])
        return None
    
    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional['User']:
        """
        Authenticate user
        VULNERABILITY: SQL Injection in login
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: Concatenated SQL with both username and password
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['id'], row['username'], row['email'], 
                      row['role'], row['password'])
        return None
    
    @classmethod
    def search_users(cls, search_term: str) -> list:
        """
        Search users by username or email
        VULNERABILITY: SQL Injection in search
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: User input in LIKE clause
        query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
        cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(row['id'], row['username'], row['email'], 
                   row['role'], row['password']) for row in rows]
    
    @classmethod
    def update_profile(cls, user_id: int, data: Dict[str, str]):
        """
        Update user profile
        VULNERABILITY: SQL Injection in UPDATE
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: Dynamic query construction
        updates = []
        for key, value in data.items():
            updates.append(f"{key} = '{value}'")
        
        update_clause = ', '.join(updates)
        query = f"UPDATE users SET {update_clause} WHERE id = {user_id}"
        
        cursor.execute(query)
        conn.commit()
        conn.close()
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
