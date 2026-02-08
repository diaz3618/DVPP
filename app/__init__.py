"""
Application Package
A deliberately vulnerable document management system
"""

from flask import Flask, redirect, url_for
from app.views import auth_bp, docs_bp, admin_bp, api_bp
import sqlite3
import os

def create_app(config_class):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    init_database(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(docs_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    # Root route
    @app.route('/')
    def index():
        return '''
        <html><body>
            <h1>Document Management System</h1>
            <p><strong>WARNING:</strong> This is a deliberately vulnerable application!</p>
            <ul>
                <li><a href="/auth/login">Login</a></li>
                <li><a href="/docs">My Documents</a></li>
                <li><a href="/admin">Admin Panel</a></li>
            </ul>
            <hr>
            <h3>Test Credentials:</h3>
            <p>Admin: admin / admin123</p>
            <p>User: user / password123</p>
        </body></html>
        '''
    
    return app

def init_database(app):
    """Initialize SQLite database with sample data"""
    db_path = app.config['DATABASE']
    
    # Check if database exists
    if os.path.exists(db_path):
        return
    
    print(f"Initializing database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            bio TEXT,
            website TEXT
        )
    ''')
    
    # Create documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            filename TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    ''')
    
    # Insert sample users
    cursor.execute(
        "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
        ('admin', 'admin123', 'admin@securedoc.local', 'admin')
    )
    
    cursor.execute(
        "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
        ('user', 'password123', 'user@securedoc.local', 'user')
    )
    
    cursor.execute(
        "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
        ('alice', 'alice123', 'alice@securedoc.local', 'user')
    )
    
    # Insert sample documents
    cursor.execute(
        "INSERT INTO documents (title, content, owner_id, filename, created_at) VALUES (?, ?, ?, ?, ?)",
        ('Welcome Document', 'Welcome!', 1, 'welcome.txt', '2026-01-01T00:00:00')
    )
    
    cursor.execute(
        "INSERT INTO documents (title, content, owner_id, filename, created_at) VALUES (?, ?, ?, ?, ?)",
        ('Secret Admin Document', 'This is a secret admin document. Contains sensitive information.', 1, 'secret.txt', '2026-01-02T00:00:00')
    )
    
    cursor.execute(
        "INSERT INTO documents (title, content, owner_id, filename, created_at) VALUES (?, ?, ?, ?, ?)",
        ('User Document', 'This is a regular user document.', 2, 'user_doc.txt', '2026-01-03T00:00:00')
    )
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")
