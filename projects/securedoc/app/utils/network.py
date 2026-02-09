"""
Network utilities with SSRF vulnerabilities
"""

import requests
from typing import Optional, Dict
from urllib.parse import urlparse

def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """
    Fetch content from URL
    VULNERABILITY: Server-Side Request Forgery (SSRF)
    """
    # Vulnerable: No URL validation, can access internal resources
    try:
        response = requests.get(url, timeout=timeout)
        return response.text
    except Exception as e:
        return None

def proxy_request(url: str, method: str = 'GET', data: Dict = None) -> Dict:
    """
    Proxy HTTP request
    VULNERABILITY: SSRF - Can make requests to internal services
    """
    # Vulnerable: No whitelist, no internal IP blocking
    try:
        if method.upper() == 'POST':
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, params=data, timeout=10)
        
        return {
            'status': response.status_code,
            'headers': dict(response.headers),
            'content': response.text
        }
    except Exception as e:
        return {'error': str(e)}

def check_url_status(url: str) -> Dict:
    """
    Check if URL is accessible
    VULNERABILITY: SSRF for port scanning and service discovery
    """
    # Vulnerable: Can be used to scan internal network
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return {
            'accessible': True,
            'status_code': response.status_code,
            'final_url': response.url
        }
    except requests.exceptions.ConnectionError:
        return {'accessible': False, 'error': 'Connection failed'}
    except Exception as e:
        return {'accessible': False, 'error': str(e)}

def download_file(url: str, save_path: str) -> bool:
    """
    Download file from URL
    VULNERABILITY: SSRF + Arbitrary File Write
    """
    # Vulnerable: Can download from internal URLs and write to any path
    try:
        response = requests.get(url, timeout=30)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception:
        return False

def fetch_image(image_url: str) -> bytes:
    """
    Fetch image from URL
    VULNERABILITY: SSRF - Can access internal resources
    """
    # Vulnerable: No validation of URL or content type
    try:
        response = requests.get(image_url, timeout=10)
        return response.content
    except Exception:
        return b''

def validate_webhook_url(url: str) -> bool:
    """
    Validate webhook URL
    VULNERABILITY: Weak validation, SSRF possible
    """
    # Vulnerable: Weak checks that can be bypassed
    parsed = urlparse(url)
    
    # Weak blacklist
    blocked = ['localhost', '127.0.0.1']
    
    # Case-sensitive check (can be bypassed with case variation)
    if parsed.hostname in blocked:
        return False
    
    # Missing checks for:
    # - 0.0.0.0
    # - 169.254.169.254 (cloud metadata)
    # - Private IP ranges (10.x, 172.16-31.x, 192.168.x)
    # - DNS rebinding
    
    return True

def fetch_json_data(api_url: str, headers: Dict = None) -> Dict:
    """
    Fetch JSON data from API
    VULNERABILITY: SSRF with custom headers
    """
    # Vulnerable: User controls URL and headers
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def make_api_call(endpoint: str, api_key: str = None) -> str:
    """
    Make API call with optional authentication
    VULNERABILITY: SSRF + Potential credential exposure
    """
    # Vulnerable: Can access internal APIs
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        return response.text
    except Exception as e:
        return str(e)
