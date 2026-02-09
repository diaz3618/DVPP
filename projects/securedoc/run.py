"""
Entry point
Run with: python run.py
"""

from app import create_app
from config import Config

if __name__ == '__main__':
    app = create_app(Config)
    print("=" * 60)
    print("Super safe and secure Document Management System")
    print("WARNING: This is a deliberately vulnerable application!")
    print("Running on http://0.0.0.0:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
