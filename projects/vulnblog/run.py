"""
Entry point for VulnBlog
"""

from app import create_app
from config import Config

if __name__ == '__main__':
    app = create_app(Config)
    print("=" * 60)
    print("VulnBlog - Vulnerable Blogging Platform")
    print("WARNING: Intentionally vulnerable application!")
    print("Running on http://0.0.0.0:5001")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5001, debug=True)
