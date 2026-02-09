"""Information disclosure utilities

VULNERABILITIES:
- Verbose error messages
- Stack trace exposure
- Configuration leaks
"""

import traceback
import sys
import os


class InfoService:
    """Information disclosure - DELIBERATELY INSECURE"""
    
    @staticmethod
    def get_system_info():
        """VULN: Info Disclosure - exposes system details
        CVE Reference: CVE-2017-14955 (Check_MK info disclosure), CVE-2024-22513 (JWT info disclosure)
        """
        return {
            "python_version": sys.version,
            "platform": sys.platform,
            "executable": sys.executable,
            "path": sys.path,
            "modules": list(sys.modules.keys()),
            "env": dict(os.environ),  # VULN: Exposes environment variables
            "cwd": os.getcwd()
        }
    
    @staticmethod
    def get_detailed_error(exception):
        """VULN: Verbose error messages with stack traces
        CVE Reference: CVE-2014-0242 (mod_wsgi info disclosure)
        """
        return {
            "error_type": type(exception).__name__,
            "error_message": str(exception),
            "traceback": traceback.format_exc(),  # VULN: Full stack trace
            "locals": str(sys.exc_info()),  # VULN: Local variables
        }
    
    @staticmethod
    def debug_info():
        """VULN: Debug endpoint exposing internals"""
        from flask import current_app
        return {
            "config": {k: str(v) for k, v in current_app.config.items()},  # VULN: Config leak
            "secret_key": current_app.config.get('SECRET_KEY'),  # VULN: Secret exposed
            "debug": current_app.debug,
            "env": current_app.env
        }
