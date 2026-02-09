"""
Document model with IDOR and SQL injection vulnerabilities
"""

import sqlite3
from typing import Optional, List
from datetime import datetime

class Document:
    """Document model with vulnerable data access"""
    
    def __init__(self, id: int, title: str, content: str, owner_id: int, 
                 filename: str, created_at: str):
        self.id = id
        self.title = title
        self.content = content
        self.owner_id = owner_id
        self.filename = filename
        self.created_at = created_at
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        conn = sqlite3.connect('securedoc.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    @classmethod
    def create(cls, title: str, content: str, owner_id: int, filename: str) -> 'Document':
        """Create a new document"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        created_at = datetime.now().isoformat()
        
        cursor.execute(
            "INSERT INTO documents (title, content, owner_id, filename, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, content, owner_id, filename, created_at)
        )
        
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return cls(doc_id, title, content, owner_id, filename, created_at)
    
    @classmethod
    def find_by_id(cls, doc_id: int) -> Optional['Document']:
        """
        Find document by ID
        VULNERABILITY: IDOR - No authorization check
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: No check if user has permission to access this document
        query = f"SELECT * FROM documents WHERE id = {doc_id}"
        cursor.execute(query)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['id'], row['title'], row['content'], 
                      row['owner_id'], row['filename'], row['created_at'])
        return None
    
    @classmethod
    def get_by_owner(cls, owner_id: int) -> List['Document']:
        """Get all documents for a user"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM documents WHERE owner_id = ?", (owner_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(row['id'], row['title'], row['content'], 
                   row['owner_id'], row['filename'], row['created_at']) 
                for row in rows]
    
    @classmethod
    def search(cls, query: str) -> List['Document']:
        """
        Search documents
        VULNERABILITY: SQL Injection in search
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: Unparameterized query
        sql = f"SELECT * FROM documents WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(row['id'], row['title'], row['content'], 
                   row['owner_id'], row['filename'], row['created_at']) 
                for row in rows]
    
    @classmethod
    def delete(cls, doc_id: int):
        """
        Delete document
        VULNERABILITY: IDOR - No authorization check
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: Anyone can delete any document if they know the ID
        query = f"DELETE FROM documents WHERE id = {doc_id}"
        cursor.execute(query)
        
        conn.commit()
        conn.close()
    
    @classmethod
    def update(cls, doc_id: int, title: str, content: str):
        """
        Update document
        VULNERABILITY: IDOR - No authorization check
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Vulnerable: No ownership verification
        query = f"UPDATE documents SET title = '{title}', content = '{content}' WHERE id = {doc_id}"
        cursor.execute(query)
        
        conn.commit()
        conn.close()
    
    def to_dict(self):
        """Convert document to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'owner_id': self.owner_id,
            'filename': self.filename,
            'created_at': self.created_at
        }
