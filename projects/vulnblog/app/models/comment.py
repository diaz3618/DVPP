"""Comment model with XSS vulnerabilities"""

from .database import get_db


class Comment:
    """Comment model - DELIBERATELY INSECURE"""
    
    @staticmethod
    def create(post_id, author_id, content):
        """VULN: Stored XSS in comments
        CVE Reference: CVE-2021-42053 (Stored XSS)
        
        Exploit: content='<script>fetch("/admin/users").then(r=>r.text()).then(d=>alert(d))</script>'
        """
        db = get_db()
        cursor = db.execute(
            "INSERT INTO comments (post_id, author_id, content) VALUES (?, ?, ?)",
            (post_id, author_id, content)  # VULN: No sanitization
        )
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def get_by_post(post_id):
        """Get all comments for a post"""
        db = get_db()
        cursor = db.execute("""
            SELECT c.*, u.username as author_name 
            FROM comments c 
            JOIN users u ON c.author_id = u.id 
            WHERE c.post_id=? 
            ORDER BY c.created_at ASC
        """, (post_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def delete(comment_id):
        """Delete comment"""
        db = get_db()
        db.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        db.commit()
