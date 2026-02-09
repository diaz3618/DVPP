"""Network utilities with SSRF vulnerabilities

VULNERABILITIES:
- Server-Side Request Forgery (SSRF)
- No URL validation
"""

import urllib.request
import urllib.parse
import json


class NetworkService:
    """Network operations - DELIBERATELY INSECURE"""
    
    @staticmethod
    def fetch_remote_data(url):
        """VULN: SSRF - fetches arbitrary URLs
        CVE Reference: CVE-2022-31188 (CVAT SSRF), CVE-2022-36551 (Label Studio SSRF)
        
        Exploit: url='http://169.254.169.254/latest/meta-data/iam/security-credentials/'
        Also: url='file:///etc/passwd' or url='http://localhost:6379/' (Redis)
        """
        try:
            # VULN: No URL validation - SSRF
            response = urllib.request.urlopen(url, timeout=10)
            content = response.read().decode('utf-8')
            return {"success": True, "content": content, "url": url}
        except Exception as e:
            # VULN: Info disclosure via error messages
            return {"success": False, "error": str(e), "url": url}
    
    @staticmethod
    def load_remote_dataset(url, format='json'):
        """VULN: SSRF + Deserialization
        CVE Reference: CVE-2022-31188 (CVAT SSRF)
        
        Exploit: url='http://internal-server/admin.pkl'
        """
        try:
            # VULN: SSRF
            response = urllib.request.urlopen(url, timeout=10)
            content = response.read()
            
            if format == 'json':
                return json.loads(content)
            elif format == 'pickle':
                # VULN: Combines SSRF + Deserialization
                import pickle
                return pickle.loads(content)  # VULN: Unsafe deserialization
            else:
                return content.decode('utf-8')
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def proxy_request(target_url, method='GET', data=None):
        """VULN: Open proxy functionality - SSRF
        
        Exploit: target_url='http://169.254.169.254/latest/user-data'
        """
        try:
            if method == 'POST' and data:
                data_bytes = urllib.parse.urlencode(data).encode('utf-8')
                req = urllib.request.Request(target_url, data=data_bytes, method='POST')
            else:
                req = urllib.request.Request(target_url, method=method)
            
            # VULN: Acts as open proxy - SSRF
            response = urllib.request.urlopen(req, timeout=10)
            return {
                "status": response.status,
                "headers": dict(response.headers),
                "body": response.read().decode('utf-8')
            }
        except Exception as e:
            return {"error": str(e)}
