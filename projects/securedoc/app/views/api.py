"""
API endpoints
RESTful API with vulnerabilities
"""

from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.document import Document
from app.services.file_service import FileService
from app.utils.network import fetch_url

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/users/<int:user_id>')
def get_user(user_id):
    """
    Get user by ID
    VULNERABILITY: IDOR - No access control
    """
    # Calls vulnerable find_by_id with SQL injection potential
    user = User.find_by_id(user_id)
    
    if user:
        return jsonify(user.to_dict())
    
    return jsonify({'error': 'User not found'}), 404

@api_bp.route('/documents/<int:doc_id>')
def get_document(doc_id):
    """
    Get document by ID
    VULNERABILITY: IDOR - No authorization check
    """
    document = Document.find_by_id(doc_id)
    
    if document:
        return jsonify(document.to_dict())
    
    return jsonify({'error': 'Document not found'}), 404

@api_bp.route('/search')
def search():
    """
    Search API
    VULNERABILITY: SQL injection
    """
    query = request.args.get('q', '')
    type = request.args.get('type', 'documents')
    
    if type == 'users':
        results = User.search_users(query)
        return jsonify([u.to_dict() for u in results])
    else:
        results = Document.search(query)
        return jsonify([d.to_dict() for d in results])

@api_bp.route('/file/read')
def read_file_api():
    """
    Read file via API
    VULNERABILITY: LFI
    """
    filename = request.args.get('file', '')
    path = request.args.get('path', '')
    
    file_service = FileService('data/uploads')
    
    if path:
        # Vulnerable: Read arbitrary path
        content = file_service.read_file_absolute(path)
    else:
        # Vulnerable: Path traversal in filename
        content = file_service.read_file(filename)
    
    if content:
        return jsonify({'content': content})
    
    return jsonify({'error': 'File not found'}), 404

@api_bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Trigger webhook
    VULNERABILITY: SSRF
    """
    url = request.json.get('url', '')
    data = request.json.get('data', {})
    
    # Calls vulnerable fetch_url
    result = fetch_url(url)
    
    return jsonify({'status': 'sent', 'response': result})

@api_bp.route('/proxy')
def api_proxy():
    """
    API proxy
    VULNERABILITY: SSRF
    """
    target_url = request.args.get('url', '')
    
    if target_url:
        content = fetch_url(target_url)
        return jsonify({'content': content})
    
    return jsonify({'error': 'No URL provided'}), 400
