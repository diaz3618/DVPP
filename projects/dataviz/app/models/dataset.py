"""Dataset model"""

from .database import get_db


class Dataset:
    """Dataset model"""
    
    @staticmethod
    def create(name, filepath, file_type):
        """Save dataset metadata"""
        db = get_db()
        cursor = db.execute(
            "INSERT INTO datasets (name, filepath, file_type) VALUES (?, ?, ?)",
            (name, filepath, file_type)
        )
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def get_by_id(dataset_id):
        """Get dataset by ID"""
        db = get_db()
        cursor = db.execute("SELECT * FROM datasets WHERE id=?", (dataset_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def list_all():
        """List all datasets"""
        db = get_db()
        cursor = db.execute("SELECT * FROM datasets ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
