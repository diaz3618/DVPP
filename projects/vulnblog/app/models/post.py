"""Blog post model

VULNERABILITIES:
- XSS: Unescaped content rendering
- SQLi: String concatenation
"""

from .database import get_db


class Post:
    """Post model - DELIBERATELY INSECURE"""
    
    @staticmethod
    def create(title, content, author_id):
        """VULN: Stored XSS in title and content
        CVE Reference: CVE-2021-42053 (django XSS)
        
        Exploit: title='<img src=x onerror=alert(1)>'
        """
        db = get_db()
        cursor = db.execute(
            "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
            (title, content, author_id)  # VULN: No sanitization
        )
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def find_by_id(post_id):
        """Get post by ID"""
        db = get_db()
        cursor = db.execute("""
            SELECT p.*, u.username as author_name 
            FROM posts p 
            JOIN users u ON p.author_id = u.id 
            WHERE p.id=?
        """, (post_id,))
        post = cursor.fetchone()
        return dict(post) if post else None
    
    @staticmethod
    def search(keyword):
        """VULN: SQL Injection via search
        
        Exploit: keyword=' OR 1=1--
        """
        db = get_db()
        # VULN: SQL Injection
        query = f"SELECT * FROM posts WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"
        cursor = db.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def list_all(limit=10):
        """List recent posts"""
        db = get_db()
        cursor = db.execute("""
            SELECT p.*, u.username as author_name 
            FROM posts p 
            JOIN users u ON p.author_id = u.id 
            ORDER BY p.created_at DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update(post_id, title, content):
        """VULN: Stored XSS in updates"""
        db = get_db()
        db.execute(
            "UPDATE posts SET title=?, content=? WHERE id=?",
            (title, content, post_id)  # VULN: No sanitization
        )
        db.commit()
    
    @staticmethod
    def delete(post_id):
        """Delete post"""
        db = get_db()
        db.execute("DELETE FROM posts WHERE id=?", (post_id,))
        db.commit()
