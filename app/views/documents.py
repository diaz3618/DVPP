"""
Document management views
Handles document CRUD operations
"""

from flask import Blueprint, request, redirect, url_for, send_file
from app.services.auth import AuthService
from app.services.file_service import FileService
from app.models.document import Document
from app.utils.helpers import render_content, format_output

docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

@docs_bp.route('/')
def list_documents():
    """List all documents for current user"""
    if not AuthService.is_authenticated():
        return redirect(url_for('auth.login'))
    
    user = AuthService.get_current_user()
    documents = Document.get_by_owner(user.id)
    
    docs_html = '<ul>'
    for doc in documents:
        docs_html += f'<li><a href="/docs/view/{doc.id}">{doc.title}</a></li>'
    docs_html += '</ul>'
    
    return f"""
    <html><body>
        <h1>My Documents</h1>
        {docs_html}
        <p><a href="/docs/create">Create New Document</a></p>
        <p><a href="/auth/logout">Logout</a></p>
    </body></html>
    """

@docs_bp.route('/view/<int:doc_id>')
def view_document(doc_id):
    """
    View document by ID
    VULNERABILITY: IDOR - No authorization check
    """
    # Calls Document.find_by_id which doesn't verify ownership
    document = Document.find_by_id(doc_id)
    
    if not document:
        return "Document not found", 404
    
    # Vulnerable: XSS in content display
    return f"""
    <html><body>
        <h1>{document.title}</h1>
        <div class="content">{document.content}</div>
        <p>Owner ID: {document.owner_id}</p>
        <p><a href="/docs/edit/{document.id}">Edit</a> | 
           <a href="/docs/delete/{document.id}">Delete</a></p>
        <p><a href="/docs">Back to My Documents</a></p>
    </body></html>
    """

@docs_bp.route('/create', methods=['GET', 'POST'])
def create_document():
    """Create new document"""
    if not AuthService.is_authenticated():
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user = AuthService.get_current_user()
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        
        doc = Document.create(title, content, user.id, f"doc_{title}.txt")
        
        return redirect(url_for('docs.view_document', doc_id=doc.id))
    
    return '''
    <html><body>
        <h2>Create Document</h2>
        <form method="post">
            <input type="text" name="title" placeholder="Title" required><br>
            <textarea name="content" placeholder="Content" rows="10" cols="50"></textarea><br>
            <button type="submit">Create</button>
        </form>
    </body></html>
    '''

@docs_bp.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
def edit_document(doc_id):
    """
    Edit document
    VULNERABILITY: IDOR - No ownership check
    """
    # No check if current user owns this document
    document = Document.find_by_id(doc_id)
    
    if not document:
        return "Document not found", 404
    
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        
        # Vulnerable update - no ownership verification
        Document.update(doc_id, title, content)
        
        return redirect(url_for('docs.view_document', doc_id=doc_id))
    
    return f"""
    <html><body>
        <h2>Edit Document</h2>
        <form method="post">
            <input type="text" name="title" value="{document.title}" required><br>
            <textarea name="content" rows="10" cols="50">{document.content}</textarea><br>
            <button type="submit">Update</button>
        </form>
    </body></html>
    """

@docs_bp.route('/delete/<int:doc_id>')
def delete_document(doc_id):
    """
    Delete document
    VULNERABILITY: IDOR - No authorization check
    """
    # No check if current user owns this document
    Document.delete(doc_id)
    
    return redirect(url_for('docs.list_documents'))

@docs_bp.route('/search')
def search_documents():
    """
    Search documents
    VULNERABILITY: SQL injection via Document.search
    """
    query = request.args.get('q', '')
    
    if query:
        # Calls vulnerable search method
        documents = Document.search(query)
        
        results_html = '<ul>'
        for doc in documents:
            results_html += f'<li><a href="/docs/view/{doc.id}">{doc.title}</a></li>'
        results_html += '</ul>'
        
        # XSS vulnerability
        return f"""
        <html><body>
            <h2>Search Results for: {query}</h2>
            {results_html}
            <p><a href="/docs">Back</a></p>
        </body></html>
        """
    
    return '''
    <html><body>
        <h2>Search Documents</h2>
        <form method="get">
            <input type="text" name="q" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
    </body></html>
    '''

@docs_bp.route('/download/<path:filename>')
def download_file(filename):
    """
    Download file
    VULNERABILITY: LFI via path parameter
    """
    file_service = FileService('data/uploads')
    
    # Vulnerable: filename parameter from URL with path traversal
    file_path = file_service.get_file_path(filename)
    
    try:
        return send_file(file_path)
    except Exception as e:
        return f"Error: {str(e)}", 404

@docs_bp.route('/read_file')
def read_file():
    """
    Read file content
    VULNERABILITY: LFI
    """
    filename = request.args.get('file', '')
    
    file_service = FileService('data/uploads')
    
    # Calls vulnerable read_file method
    content = file_service.read_file(filename)
    
    if content:
        # XSS vulnerability: unescaped content
        return f"""
        <html><body>
            <h2>File: {filename}</h2>
            <pre>{content}</pre>
        </body></html>
        """
    
    return "File not found", 404

@docs_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload file
    VULNERABILITY: Path traversal in filename
    """
    if not AuthService.is_authenticated():
        return redirect(url_for('auth.login'))
    
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    file_service = FileService('data/uploads')
    
    # Calls vulnerable save_upload method
    filename = file_service.save_upload(file)
    
    return f"File uploaded: {filename}"
