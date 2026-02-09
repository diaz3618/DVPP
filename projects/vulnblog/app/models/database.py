"""Database initialization and connection"""

import sqlite3
import os
from flask import g, current_app


def get_db():
    """Get database connection"""
    if 'db' not in g:
        db_path = os.path.join(current_app.config['DATABASE_PATH'])
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize database schema"""
    db_path = current_app.config['DATABASE_PATH']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            is_admin INTEGER DEFAULT 0,
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            published INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    # Themes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            template TEXT NOT NULL,
            active INTEGER DEFAULT 0
        )
    ''')
    
    # Insert default users (VULN: weak passwords)
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email, is_admin, bio)
        VALUES ('admin', 'admin123', 'admin@vulnblog.local', 1, 'Administrator account'),
               ('blogger', 'password', 'blogger@vulnblog.local', 0, 'Regular blogger'),
               ('user', 'user', 'user@vulnblog.local', 0, 'Regular user')
    ''')
    
    # Insert default theme (VULN: SSTI-vulnerable template)
    cursor.execute('''
        INSERT OR IGNORE INTO themes (name, template, active)
        VALUES ('default', '<h1>{{ title }}</h1><div>{{ content }}</div>', 1),
               ('custom', '{{ custom_template }}', 0)
    ''')
    
    db.commit()
    db.close()
