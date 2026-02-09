# DVPP - Deliberately Vulnerable Python Projects

A comprehensive security training lab with **10 vulnerable Python web applications** containing **107 organized exploits** mapped to **82+ real CVEs**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Quick Start

```bash
# Deploy all 10 apps
docker-compose up -d

# Apps accessible at localhost:8000-8009
# See QUICKSTART.md for detailed 5-minute guide
```

**Documentation:**
- [QUICKSTART.md](QUICKSTART.md) - 5-minute deployment guide
- [docs/PROJECTS.md](docs/PROJECTS.md) - All 10 vulnerable applications
- [docs/DOCKER.md](docs/DOCKER.md) - Docker deployment guide

## What is DVPP?

DVPP is an educational cybersecurity lab featuring **10 deliberately vulnerable Python web applications** designed for:

- **Security engineering students** learning vulnerability identification and secure coding
- **Penetration testers** practicing exploitation techniques in a safe environment
- **Tool developers** (vulnhuntr) validating scanner accuracy against known vulnerabilities
- **Python developers** understanding security anti-patterns and defense strategies

### Key Features

- **107 organized exploits** across 14 vulnerability categories
- **82+ real CVE mappings** from production Python applications
- **10 diverse projects** with varying complexity (500-2,600 LOC each)
- **Docker isolation** for safe testing
- **Comprehensive documentation** with PoCs and remediation guidance
- **Scanner ground truth** for tool validation (vulnhuntr, Bandit, Semgrep, etc.)

## Project Structure

```
DVPP/
├── projects/           # 10 vulnerable applications
│   ├── securedoc/     # Document management (SQLi, RCE, SSRF, LFI, IDOR, XSS)
│   ├── vulnblog/      # Blogging platform (SSTI, XSS, CSRF, Auth Bypass)
│   ├── dataviz/       # Data visualization (Pickle RCE, CSV Injection)
│   ├── fileshare/     # File sharing (Upload RCE, Path Traversal, LFI)
│   ├── apigateway/    # API gateway (SSRF, Docker Escape, Auth Bypass)
│   ├── ecomstore/     # E-commerce (SQLi, XSS, CSRF, Price Manipulation)
│   ├── chatapp/       # Chat application (XSS, RCE via Bot Commands)
│   ├── adminpanel/    # Admin interface (exec() RCE, Docker Socket Escape)
│   ├── dsvpwa/        # Classic vulnerable app (Multiple OWASP Top 10)
│   └── python-vulnerableapp/  # Specific vulnerability demos
├── exploits/          # 107 organized exploit scripts
│   ├── securedoc/     # SecureDoc exploits (sqli, rce, ssrf, lfi, idor, xss)
│   ├── vulnblog/      # VulnBlog exploits (ssti, xss, csrf)
│   ├── dataviz/       # DataViz exploits (deserialization, csv_injection)
│   └── ...            # More exploit directories with HOW_TO_USE.md guides
├── docs/              # Comprehensive documentation
│   ├── PROJECTS.md              # Detailed project overview
│   ├── VULNERABILITY_COVERAGE.md # 82+ vulnerability types and mappings
│   ├── CVE_MAPPINGS.md          # Real-world CVE references
│   ├── EDUCATIONAL_VALUE.md     # Learning objectives and path
│   ├── DOCKER.md                # Docker deployment guide
│   ├── STATISTICS.md            # Code metrics and coverage stats
│   ├── EXPLOIT_ORGANIZATION.md  # Exploit structure and testing
│   └── VULNERABILITY_MAP_QUICK.md # Quick vulnerability reference
├── QUICKSTART.md      # 5-minute deployment guide
├── CONTRIBUTING.md    # Contribution guidelines
└── docker-compose.yml # Master deployment file
```

## Documentation

### Getting Started
- [QUICKSTART.md](QUICKSTART.md) - Deploy all 10 apps in 5 minutes
- [docs/DOCKER.md](docs/DOCKER.md) - Docker Compose guide, networking, volumes

### Projects & Vulnerabilities
- [docs/PROJECTS.md](docs/PROJECTS.md) - All 10 vulnerable applications with details
- [docs/VULNERABILITY_COVERAGE.md](docs/VULNERABILITY_COVERAGE.md) - 82+ vuln types, OWASP mappings
- [docs/CVE_MAPPINGS.md](docs/CVE_MAPPINGS.md) - Real-world CVE references by project

### Learning & Testing
- [docs/EDUCATIONAL_VALUE.md](docs/EDUCATIONAL_VALUE.md) - Learning objectives, recommended path
- [docs/EXPLOIT_ORGANIZATION.md](docs/EXPLOIT_ORGANIZATION.md) - Exploit structure, testing instructions
- [docs/STATISTICS.md](docs/STATISTICS.md) - Code metrics, scanner comparison, coverage stats

### Quick Reference
- [docs/VULNERABILITY_MAP_QUICK.md](docs/VULNERABILITY_MAP_QUICK.md) - Fast vulnerability lookup

## Vulnerability Categories

DVPP covers **14 vulnerability categories** from the OWASP Top 10 and CWE:

1. **Injection** (SQLi, Command Injection, SSTI) - 32 exploits
2. **Authentication & Authorization** (Auth Bypass, IDOR, Session Hijacking) - 11 exploits
3. **Cross-Site Scripting** (Stored, Reflected, DOM-based XSS) - 18 exploits
4. **Remote Code Execution** (eval, exec, pickle, YAML deserialization) - 12 exploits
5. **File Operations** (LFI, Path Traversal, File Upload) - 12 exploits
6. **Server-Side Request Forgery** (SSRF, Blind SSRF) - 5 exploits
7. **Cross-Site Request Forgery** (CSRF) - 6 exploits
8. **Information Disclosure** (Debug Info, Error Messages, Directory Listing) - 9 exploits
9. **Cryptographic Failures** (Weak Hashing, Insecure Storage) - 8 exploits
10. **Security Misconfiguration** (Default Credentials, Debug Mode) - 18 exploits
11. **Deserialization** (Pickle, YAML, JSON) - 5 exploits
12. **Container/Docker Escape** (Socket Access, Privileged Containers) - 3 exploits
13. **Business Logic** (Price Manipulation, Race Conditions) - 4 exploits
14. **XML External Entity** (XXE) - 2 exploits

**See:** [docs/VULNERABILITY_COVERAGE.md](docs/VULNERABILITY_COVERAGE.md) for complete breakdown.

## Security Warning

**NEVER deploy these applications on production systems or public networks.**

- All vulnerabilities are **DELIBERATE** for educational purposes
- Deploy **ONLY** in isolated lab environments
- Use Docker network isolation (included in docker-compose.yml)
- All services bind to **localhost only** by default
- Review [docs/DOCKER.md](docs/DOCKER.md) for security notes

## Quick Examples

### SQL Injection (SecureDoc)
```bash
curl "http://localhost:8000/search?q=test'+OR+'1'='1"
```

### Stored XSS (VulnBlog)
```bash
# Create post with XSS payload
curl -X POST http://localhost:8001/post \
  -d "title=Test&content=<script>alert(document.cookie)</script>"
```

### Deserialization RCE (DataViz)
```python
import pickle, base64
payload = pickle.dumps(__import__('os').system, 'whoami')
# Upload to http://localhost:8002/upload
```

**Full exploits:** See `exploits/` directory and [docs/EXPLOIT_ORGANIZATION.md](docs/EXPLOIT_ORGANIZATION.md)

## Testing with vulnhuntr

```bash
# Scan all projects
vulnhuntr --path projects/

# Expected results: 73% detection rate (78/107 vulnerabilities)
# See docs/STATISTICS.md for detailed scanner comparison
```

## Learning Path

1. **Week 1:** Deploy and explore all 10 applications ([QUICKSTART.md](QUICKSTART.md))
2. **Week 2:** Manual vulnerability testing (Start with SecureDoc SQLi)
3. **Week 3:** Run vulnerability scanners (vulnhuntr, Bandit, Semgrep)
4. **Week 4:** Advanced exploitation (chaining vulnerabilities, Docker escape)
5. **Week 5:** Remediation practice (fix vulnerabilities, verify with scanners)
6. **Week 6:** Documentation and reporting (write vuln reports with PoCs)

**Full learning path:** [docs/EDUCATIONAL_VALUE.md](docs/EDUCATIONAL_VALUE.md)

## Statistics

- **16,717 lines of code** across 10 projects (Python, HTML/JS, SQL, Config)
- **107 organized exploits** with PoCs
- **82+ real CVE mappings** from 2018-2025
- **89.5% OWASP Top 10 coverage**
- **47 markdown documentation files** (8,934 lines)
- **27 HOW_TO_USE.md exploit guides**

**Detailed metrics:** [docs/STATISTICS.md](docs/STATISTICS.md)

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas:
- Add new vulnerable applications
- Contribute exploit scripts
- Improve documentation
- Report undocumented vulnerabilities (0-days)
- Add scanner rules

## Related Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP DVWA](https://dvwa.co.uk/) - Classic PHP vulnerable app
- [vulnhuntr](https://github.com/protectai/vulnhuntr) - AI-powered vulnerability scanner
- [WebGoat](https://owasp.org/www-project-webgoat/) - Java vulnerable application
- [NIST NVD](https://nvd.nist.gov/) - CVE database

## License

MIT License - See [LICENSE](LICENSE) for details.

**Disclaimer:** This project is for educational purposes only. The maintainers are not responsible for misuse.

## Acknowledgments

All vulnerabilities are inspired by real CVEs found in production Python applications. Special thanks to the security research community for responsible disclosure practices.

**CVE Sources:** [docs/CVE_MAPPINGS.md](docs/CVE_MAPPINGS.md)

---

**Start Learning:** [QUICKSTART.md](QUICKSTART.md) | **Full Documentation:** [docs/](docs/)
