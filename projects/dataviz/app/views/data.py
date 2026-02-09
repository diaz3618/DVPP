"""Data upload and management views

VULNERABILITIES:
- Unsafe file upload
- Deserialization via pickle
"""

from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from ..models.dataset import Dataset
from ..services.pickle_service import PickleService

data_bp = Blueprint('data', __name__)


@data_bp.route('/upload', methods=['POST'])
def upload_file():
    """VULN: Allows uploading pickle files (deserialization RCE)
    CVE Reference: CVE-2022-34668 (NVFLARE), CVE-2021-24040 (ParlAI)
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    # VULN: Allows dangerous file extensions
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)
    
    # Save metadata
    file_type = filename.split('.')[-1] if '.' in filename else 'unknown'
    dataset_id = Dataset.create(filename, filepath, file_type)
    
    return jsonify({
        "success": True,
        "dataset_id": dataset_id,
        "filename": filename,
        "type": file_type
    })


@data_bp.route('/load/<int:dataset_id>', methods=['GET'])
def load_dataset(dataset_id):
    """VULN: Loads pickle files unsafely
    CVE Reference: CVE-2022-34668 (NVFLARE pickle)
    """
    dataset = Dataset.get_by_id(dataset_id)
    if not dataset:
        return jsonify({"error": "Dataset not found"}), 404
    
    filepath = dataset['filepath']
    file_type = dataset['file_type']
    
    try:
        if file_type in ['pkl', 'pickle']:
            # VULN: Unsafe deserialization
            data = PickleService.load_model(filepath)
            return jsonify({"success": True, "data": str(data)})
        elif file_type == 'csv':
            with open(filepath, 'r') as f:
                return jsonify({"success": True, "data": f.read()})
        else:
            with open(filepath, 'rb') as f:
                content = f.read()
                return jsonify({"success": True, "data": content.decode('utf-8', errors='ignore')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@data_bp.route('/load-remote', methods=['POST'])
def load_remote():
    """VULN: SSRF + Deserialization
    CVE Reference: CVE-2022-31188 (CVAT SSRF) + deserialization
    """
    from ..utils.network import NetworkService
    
    url = request.json.get('url')
    format = request.json.get('format', 'json')
    
    # VULN: SSRF + possible deserialization
    result = NetworkService.load_remote_dataset(url, format)
    return jsonify(result)


@data_bp.route('/list', methods=['GET'])
def list_datasets():
    """List all datasets"""
    datasets = Dataset.list_all()
    return jsonify(datasets)
