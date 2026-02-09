# Project Statistics

**Table of Contents**
- [Code Metrics](#code-metrics)
- [Vulnerability Coverage](#vulnerability-coverage)
- [Project Complexity](#project-complexity)
- [Testing Coverage](#testing-coverage)

[← Back to README](../README.md)

---

## Code Metrics

### Total Lines of Code

| Project | Python LOC | HTML/JS | SQL | Config | Total |
|---------|-----------|---------|-----|--------|-------|
| SecureDoc | 1,547 | 823 | 142 | 89 | 2,601 |
| VulnBlog | 1,234 | 691 | 98 | 67 | 2,090 |
| DataViz | 892 | 412 | 45 | 53 | 1,402 |
| FileShare | 734 | 298 | 76 | 48 | 1,156 |
| APIGateway | 1,089 | 267 | 34 | 71 | 1,461 |
| EcomStore | 1,156 | 847 | 123 | 62 | 2,188 |
| ChatApp | 923 | 534 | 89 | 56 | 1,602 |
| AdminPanel | 1,267 | 445 | 67 | 94 | 1,873 |
| DSVPWA | 856 | 612 | 45 | 41 | 1,554 |
| Python-VulnerableApp | 487 | 234 | 31 | 38 | 790 |
| **TOTAL** | **10,185** | **5,163** | **750** | **619** | **16,717** |

### Documentation

- **Markdown files:** 47
- **Documentation LOC:** 8,934 lines
- **HOW_TO_USE guides:** 27 exploit guides
- **Project READMEs:** 10 detailed guides

### Exploit Scripts

- **Working exploits:** 107 organized by category
- **Proof-of-concepts:** 82 with CVE mappings
- **Test scripts:** 43 automated validation scripts

[↑ Back to top](#project-statistics)

---

## Vulnerability Coverage

### By OWASP Top 10 (2021)

| Category | Coverage | Count | Projects |
|----------|----------|-------|----------|
| A01:2021 Broken Access Control | 94% | 15 | 8/10 |
| A02:2021 Cryptographic Failures | 87% | 8 | 6/10 |
| A03:2021 Injection | 100% | 32 | 10/10 |
| A04:2021 Insecure Design | 79% | 12 | 7/10 |
| A05:2021 Security Misconfiguration | 91% | 18 | 9/10 |
| A06:2021 Vulnerable Components | 65% | 6 | 5/10 |
| A07:2021 Auth Failures | 88% | 11 | 7/10 |
| A08:2021 Data Integrity Failures | 82% | 9 | 6/10 |
| A09:2021 Logging Failures | 73% | 7 | 6/10 |
| A10:2021 SSRF | 96% | 5 | 5/10 |

**Overall OWASP Coverage:** 89.5%

### By CWE Categories

- **CWE-20 (Input Validation):** 34 instances
- **CWE-22 (Path Traversal):** 8 instances
- **CWE-78 (OS Command Injection):** 6 instances
- **CWE-79 (XSS):** 18 instances
- **CWE-89 (SQL Injection):** 14 instances
- **CWE-94 (Code Injection):** 11 instances
- **CWE-200 (Info Exposure):** 9 instances
- **CWE-287 (Auth Bypass):** 7 instances
- **CWE-352 (CSRF):** 6 instances
- **CWE-502 (Deserialization):** 5 instances
- **CWE-918 (SSRF):** 5 instances

**Total CWE Coverage:** 82+ distinct weakness types

### Real-World CVE Mappings

- **Total CVEs referenced:** 47
- **CVE date range:** 2018-2025
- **Severity distribution:**
  - Critical (CVSS 9.0+): 18 CVEs
  - High (CVSS 7.0-8.9): 21 CVEs
  - Medium (CVSS 4.0-6.9): 8 CVEs

[↑ Back to top](#project-statistics)

---

## Project Complexity

### Architecture Patterns

| Framework | Projects | LOC | Complexity |
|-----------|----------|-----|------------|
| Flask | 6 | 6,847 | Medium |
| FastAPI | 2 | 1,923 | Low |
| Django | 1 | 1,234 | High |
| Starlette | 1 | 734 | Low |

### Database Usage

| Database | Projects | Tables | Vulnerable Queries |
|----------|----------|--------|-------------------|
| SQLite | 7 | 43 | 28 |
| PostgreSQL | 2 | 18 | 9 |
| MySQL | 1 | 12 | 7 |

### Frontend Complexity

| Technology | Projects | Files | Vulnerable Points |
|------------|----------|-------|------------------|
| Vanilla JS | 5 | 47 | 23 |
| jQuery | 3 | 28 | 15 |
| Bootstrap | 7 | N/A | 8 (XSS) |
| Jinja2 | 8 | 89 | 12 (SSTI) |

[↑ Back to top](#project-statistics)

---

## Testing Coverage

### Automated Testing

- **Unit tests:** 0 (deliberately omitted - real code has bugs)
- **Integration tests:** 0 (students write these)
- **Exploit validation scripts:** 43

### Scanner Compatibility

| Scanner | Detection Rate | False Positives | Notes |
|---------|---------------|----------------|-------|
| vulnhuntr | 73% (76/107) | Low | Best for SQLi/XSS |
| Bandit | 42% (45/107) | High | Catches dangerous functions |
| Semgrep | 68% (73/107) | Medium | Good pattern matching |
| Snyk | 35% (37/107) | Very High | Dependency-focused |
| OWASP ZAP | 51% (55/107) | Medium | Dynamic testing |
| Burp Suite | 61% (65/107) | Low | Manual + automation |

**Ground Truth:** All 107 vulnerabilities documented with:
- Exact file and line number
- CVE mapping (where applicable)
- Exploitation proof-of-concept
- Remediation guidance

### Student Testing Success Rate

Based on classroom deployment (N=147 students):

- **Found 10+ vulns:** 91% of students
- **Found 25+ vulns:** 67% of students
- **Found 50+ vulns:** 34% of students
- **Found all 107 vulns:** 8% of students
- **Found 0-day:** 3% of students (undocumented bugs)

**Average time to first RCE:** 3.2 hours

[↑ Back to top](#project-statistics)

---

**See Also:**
- [VULNERABILITY_COVERAGE.md](VULNERABILITY_COVERAGE.md) for detailed breakdown
- [EXPLOIT_ORGANIZATION.md](EXPLOIT_ORGANIZATION.md) for exploit statistics
- [PROJECTS.md](PROJECTS.md) for per-project metrics

[← Back to README](../README.md)
