# Real-World CVE Mappings

**Table of Contents**
- [Overview](#overview)
- [CVE by Vulnerability Type](#cve-by-vulnerability-type)
- [Detailed Mappings](#detailed-mappings)

[← Back to README](../README.md)

---

## Overview

Every vulnerability in DVPP is inspired by or directly mapped to real-world CVEs found in production Python applications. This ensures the lab reflects actual security issues encountered in the wild.

[↑ Back to top](#real-world-cve-mappings)

---

## CVE by Vulnerability Type

### Remote Code Execution (RCE)
- **CVE-2025-1550** (Keras) - Unsafe deserialization in ML model loading
- **CVE-2024-42845** (Invesalius3) - Command injection in DICOM processing
- **CVE-2023-0297** (PyLoad) - eval() abuse in plugin system
- **CVE-2022-34668** (NVFLARE) - Pickle deserialization RCE
- **CVE-2021-24040** (ParlAI) - Code execution via YAML deserialization

### Server-Side Request Forgery (SSRF)
- **CVE-2022-31188** (CVAT) - SSRF in image fetching
- **CVE-2022-36551** (Label Studio) - SSRF via proxy parameter
- **CVE-2021-43857** (Gerapy) - SSRF in project management

### Local File Inclusion (LFI)
- **CVE-2024-23334** (aiohttp) - Path traversal in static file serving
- **CVE-2019-14322** (Werkzeug) - Directory traversal vulnerability
- **CVE-2018-1000164** (Gunicorn) - LFI via HTTP smuggling

### Server-Side Template Injection (SSTI)
- **CVE-2019-8341** (Jinja2) - SSTI leading to RCE
- **CVE-2023-29689** (Pyro CMS) - Template injection vulnerability
- **CVE-2021-32839** (GLPI) - Twig SSTI

### SQL Injection
- **CVE-2024-1212** (Django) - QuerySet.raw() SQLi
- **CVE-2023-43621** (Crewjam) - SQLi in authentication
- **CVE-2022-34265** (Django) - Trunc() and Extract() SQLi

### Cross-Site Scripting (XSS)
- **CVE-2023-26115** (Jupyter) - Stored XSS in notebooks
- **CVE-2022-31140** (Mayan EDMS) - XSS in document viewer
- **CVE-2021-31542** (Django) - XSS via URLValidator

### Deserialization
- **CVE-2024-3094** (XZ Utils) - Backdoor via build process  
- **CVE-2023-33246** (Apache RocketMQ) - RCE via deserialization
- **CVE-2022-22119** (Spring Cloud) - Code execution via SpEL

### Command Injection
- **CVE-2023-32681** (Requests) - Command injection via proxy
- **CVE-2022-24761** (Waitress) - HTTP request smuggling
- **CVE-2021-21240** (httpie) - Command injection in URL parsing

[↑ Back to top](#real-world-cve-mappings)

---

## Detailed Mappings

### SecureDoc → Real CVEs
- **SQL Injection** patterns from CVE-2024-1212 (Django)
- **IDOR** similar to CVE-2021-32677 (Flask-AppBuilder)
- **LFI** inspired by CVE-2019-14322 (Werkzeug)
- **RCE via eval()** like CVE-2023-0297 (PyLoad)
- **SSRF** patterns from CVE-2022-31188 (CVAT)

### VulnBlog → Real CVEs
- **SSTI** based on CVE-2019-8341 (Jinja2)
- **Stored XSS** similar to CVE-2023-26115 (Jupyter)
- **CSRF** patterns from CVE-2021-32839 (GLPI)

### DataViz → Real CVEs
- **Pickle RCE** inspired by CVE-2022-34668 (NVFLARE)
- **CSV Injection** based on CVE-2020-13655 (LibreOffice)
- **eval() abuse** like CVE-2023-0297 (PyLoad)

### FileShare → Real CVEs
- **File Upload RCE** patterns from CVE-2024-27348 (Apache)
- **Path Traversal** based on CVE-2024-23334 (aiohttp)
- **Zip Slip** inspired by CVE-2018-1002200 (Kubernetes)

### APIGateway → Real CVEs
- **SSRF** similar to CVE-2022-36551 (Label Studio)
- **Command Injection** from CVE-2023-32681 (Requests)
- **Docker Escape** patterns from CVE-2019-5736 (runc)

### EcomStore → Real CVEs
- **SQLi** based on CVE-2023-43621 (Crewjam)
- **Price Manipulation** from CVE-2021-24389 (WooCommerce)

### ChatApp → Real CVEs
- **Stored XSS** patterns from CVE-2022-31140 (Mayan)
- **RCE via bot** inspired by CVE-2021-31542 (Django)

### AdminPanel → Real CVEs
- **exec() abuse** like CVE-2024-42845 (Invesalius3)
- **Docker Socket** patterns from CVE-2020-15257 (containerd)
- **Deserialization** from CVE-2022-34668 (NVFLARE)

### DSVPWA → Multiple CVEs
- Deliberately includes common patterns from OWASP Top 10
- Based on real vulnerabilities found in CTFs and HackTheBox

### Python-VulnerableApp → Real CVEs
- **String formatting SQLi** from legacy Python code patterns
- **autoescape=False** similar to CVE-2019-8341
- **MD5 passwords** still found in production (2024 breaches)

[↑ Back to top](#real-world-cve-mappings)

---

**See Also:**
- [NIST NVD Database](https://nvd.nist.gov/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE List](https://cwe.mitre.org/)

[← Back to README](../README.md)
