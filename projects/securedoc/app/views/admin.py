"""
Admin panel views
Administrative functionality with vulnerabilities
"""

from flask import Blueprint, request, redirect, url_for
from app.services.auth import AuthService
from app.services.export import ExportService
from app.services.file_service import FileService
from app.models.document import Document
from app.utils.network import fetch_url, proxy_request

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_panel():
    """Admin panel home"""
    if not AuthService.is_admin():
        return "Forbidden: Admin access required", 403
    
    return '''
    <html><body>
        <h1>Admin Panel</h1>
        <ul>
            <li><a href="/admin/export">Export Documents</a></li>
            <li><a href="/admin/fetch_url">Fetch External URL</a></li>
            <li><a href="/admin/generate_report">Generate Report</a></li>
            <li><a href="/admin/evaluate">Evaluate Expression</a></li>
            <li><a href="/admin/write_file">Write File</a></li>
        </ul>
        <p><a href="/docs">Back to Documents</a></p>
    </body></html>
    '''

@admin_bp.route('/export')
def export():
    """
    Export documents
    VULNERABILITY: RCE via ExportService
    """
    doc_id = request.args.get('id', '1')
    format_type = request.args.get('format', 'txt')
    options = request.args.get('options', '')
    
    document = Document.find_by_id(int(doc_id))
    
    if document:
        # Calls vulnerable export method with command injection
        filename = ExportService.export_to_format(
            document.to_dict(), 
            format_type, 
            options
        )
        return f"Exported to: {filename}"
    
    return "Document not found", 404

@admin_bp.route('/generate_report')
def generate_report():
    """
    Generate report
    VULNERABILITY: Command injection via doc_ids
    """
    doc_ids = request.args.get('ids', '1,2,3')
    
    # Calls vulnerable method with command injection
    result = ExportService.generate_report(doc_ids)
    
    return f"<html><body><h2>Report</h2><pre>{result}</pre></body></html>"

@admin_bp.route('/evaluate')
def evaluate():
    """
    Evaluate expression
    VULNERABILITY: RCE via eval()
    """
    expr = request.args.get('expr', '1+1')
    
    # Calls vulnerable eval method
    result = ExportService.evaluate_expression(expr)
    
    return f"<html><body><h2>Result: {result}</h2></body></html>"

@admin_bp.route('/fetch_url')
def fetch_external_url():
    """
    Fetch content from URL
    VULNERABILITY: SSRF
    """
    url = request.args.get('url', '')
    
    if url:
        # Calls vulnerable fetch_url function
        content = fetch_url(url)
        
        if content:
            return f"<html><body><h2>Content from {url}</h2><pre>{content[:1000]}</pre></body></html>"
        return "Failed to fetch URL", 500
    
    return '''
    <html><body>
        <h2>Fetch External URL</h2>
        <form method="get">
            <input type="text" name="url" placeholder="http://example.com" size="50">
            <button type="submit">Fetch</button>
        </form>
    </body></html>
    '''

@admin_bp.route('/proxy')
def proxy():
    """
    Proxy HTTP request
    VULNERABILITY: SSRF
    """
    url = request.args.get('url', '')
    
    if url:
        # Calls vulnerable proxy_request function
        result = proxy_request(url)
        
        return f"<html><body><pre>{result}</pre></body></html>"
    
    return "No URL provided", 400

@admin_bp.route('/write_file', methods=['GET', 'POST'])
def write_file():
    """
    Write file to filesystem
    VULNERABILITY: AFO
    """
    if request.method == 'POST':
        path = request.form.get('path', '')
        content = request.form.get('content', '')
        
        file_service = FileService('data/uploads')
        
        # Calls vulnerable write_to_path method
        success = file_service.write_to_path(path, content)
        
        if success:
            return f"File written to: {path}"
        return "Failed to write file", 500
    
    return '''
    <html><body>
        <h2>Write File</h2>
        <form method="post">
            <input type="text" name="path" placeholder="/path/to/file" size="50"><br>
            <textarea name="content" placeholder="Content" rows="10" cols="50"></textarea><br>
            <button type="submit">Write File</button>
        </form>
    </body></html>
    '''

@admin_bp.route('/execute_template', methods=['POST'])
def execute_template():
    """
    Execute custom template
    VULNERABILITY: RCE via exec()
    """
    template_code = request.form.get('code', '')
    context = {'title': 'Report', 'data': [1, 2, 3]}
    
    # Calls vulnerable exec method
    result = ExportService.execute_template(template_code, context)
    
    return f"<html><body><h2>Template Result</h2><pre>{result}</pre></body></html>"

@admin_bp.route('/deserialize', methods=['POST'])
def deserialize():
    """
    Deserialize settings
    VULNERABILITY: Unsafe deserialization with pickle
    """
    data = request.form.get('data', '')
    
    # Calls vulnerable pickle.loads
    settings = ExportService.deserialize_settings(data)
    
    return f"<html><body><pre>{settings}</pre></body></html>"
