"""
Export service with RCE vulnerabilities
"""

import subprocess
import pickle
import os
from typing import Any, Dict

class ExportService:
    """Handle document export with vulnerabilities"""
    
    @staticmethod
    def export_to_format(document: Dict, format_type: str, options: str = '') -> str:
        """
        Export document to various formats
        VULNERABILITY: Remote Code Execution via subprocess
        """
        filename = f"export_{document['id']}.{format_type}"
        
        # Vulnerable: User input directly in shell command
        cmd = f"echo '{document['content']}' > /tmp/{filename} {options}"
        
        try:
            # Vulnerable: shell=True with unsanitized input
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return filename
        except Exception as e:
            return None
    
    @staticmethod
    def generate_report(doc_ids: str) -> str:
        """
        Generate report for multiple documents
        VULNERABILITY: Command injection via doc_ids parameter
        """
        # Vulnerable: User input in shell command
        cmd = f"python -c \"print('Generating report for: {doc_ids}')\""
        
        try:
            result = subprocess.check_output(cmd, shell=True, text=True)
            return result
        except Exception as e:
            return str(e)
    
    @staticmethod
    def evaluate_expression(expression: str) -> Any:
        """
        Evaluate mathematical expression for report calculations
        VULNERABILITY: RCE via eval()
        """
        # Vulnerable: eval() on user input
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return str(e)
    
    @staticmethod
    def execute_template(template_code: str, context: Dict) -> str:
        """
        Execute template code for custom exports
        VULNERABILITY: RCE via exec()
        """
        # Vulnerable: exec() on user input
        try:
            local_vars = {'context': context, 'result': ''}
            exec(template_code, {}, local_vars)
            return local_vars.get('result', '')
        except Exception as e:
            return str(e)
    
    @staticmethod
    def deserialize_settings(data: str) -> Dict:
        """
        Deserialize export settings
        VULNERABILITY: Unsafe deserialization with pickle
        """
        # Vulnerable: pickle.loads on user data
        try:
            settings = pickle.loads(bytes.fromhex(data))
            return settings
        except Exception as e:
            return {}
    
    @staticmethod
    def run_export_script(script_name: str, args: str) -> str:
        """
        Run export script
        VULNERABILITY: Command injection
        """
        # Vulnerable: Unsanitized arguments to script
        cmd = f"./scripts/{script_name} {args}"
        
        try:
            result = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
            return result
        except Exception as e:
            return str(e)
