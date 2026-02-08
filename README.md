# Damn Vulnerable Python Project

⚠️ **WARNING**: This application contains INTENTIONAL security vulnerabilities for educational purposes.

**DO NOT DEPLOY THIS APPLICATION IN ANY PRODUCTION ENVIRONMENT**

## Purpose

This is a deliberately vulnerable document management system created as a testing target for the [vulnhuntr](https://github.com/diaz3618/vulnhuntr). It demonstrates realistic code structure with multiple types of security vulnerabilities distributed across different layers of the application.

## Vulnerability Classes

### 1. SQL Injection (SQLI)
**Locations:**
- [app/models/user.py](app/models/user.py): `find_by_username()`, `find_by_id()`, `authenticate()`, `search_users()`, `update_profile()`
- [app/models/document.py](app/models/document.py): `find_by_id()`, `search()`, `delete()`, `update()`
- [app/views/auth.py](app/views/auth.py): `/auth/login`, `/auth/search`
- [app/views/documents.py](app/views/documents.py): `/docs/search`

**Description:** String concatenation and formatting used in SQL queries instead of parameterized queries.

**Example:**
```python
# In user.py
query = f"SELECT * FROM users WHERE username = '{username}'"
```

**Exploit:** `/auth/login` with `username=admin'--` or `/auth/search?q=a' OR '1'='1`

### 2. Insecure Direct Object Reference (IDOR)
**Locations:**
- [app/models/document.py](app/models/document.py): `find_by_id()`, `delete()`, `update()`
- [app/views/documents.py](app/views/documents.py): `/docs/view/<id>`, `/docs/edit/<id>`, `/docs/delete/<id>`
- [app/views/api.py](app/views/api.py): `/api/users/<id>`, `/api/documents/<id>`

**Description:** No authorization checks to verify if the current user has permission to access/modify resources.

**Example:**
```python
# In document.py - no ownership check
def find_by_id(cls, doc_id: int):
    query = f"SELECT * FROM documents WHERE id = {doc_id}"
```

**Exploit:** Access `/docs/view/1` to view any document regardless of ownership

### 3. Local File Inclusion (LFI)
**Locations:**
- [app/services/file_service.py](app/services/file_service.py): `read_file()`, `read_file_absolute()`, `get_file_path()`
- [app/views/documents.py](app/views/documents.py): `/docs/download/<path>`, `/docs/read_file`
- [app/views/api.py](app/views/api.py): `/api/file/read`

**Description:** User input controls file paths without proper validation, allowing directory traversal.

**Example:**
```python
# In file_service.py
def read_file(self, filename: str):
    file_path = os.path.join(self.upload_folder, filename)
    with open(file_path, 'r') as f:
        return f.read()
```

**Exploit:** `/docs/read_file?file=../../etc/passwd` or `/docs/download/../../etc/passwd`

### 4. Arbitrary File Overwrite (AFO)
**Locations:**
- [app/services/file_service.py](app/services/file_service.py): `write_file()`, `write_to_path()`, `save_upload()`
- [app/views/admin.py](app/views/admin.py): `/admin/write_file`
- [app/utils/network.py](app/utils/network.py): `download_file()`

**Description:** User controls file paths in write operations without validation.

**Example:**
```python
# In file_service.py
def write_to_path(self, path: str, content: str):
    with open(path, 'w') as f:
        f.write(content)
```

**Exploit:** `/admin/write_file` with `path=/tmp/malicious.sh`

### 5. Remote Code Execution (RCE)
**Locations:**
- [app/services/export.py](app/services/export.py): `export_to_format()`, `evaluate_expression()`, `execute_template()`, `deserialize_settings()`
- [app/views/admin.py](app/views/admin.py): `/admin/export`, `/admin/evaluate`, `/admin/execute_template`, `/admin/deserialize`

**Description:** Dangerous functions (`eval()`, `exec()`, `subprocess`, `pickle.loads()`) used with user input.

**Example:**
```python
# In export.py
def evaluate_expression(expression: str):
    return eval(expression)  # Dangerous!
```

**Exploit:** `/admin/evaluate?expr=__import__('os').system('whoami')`

### 6. Cross-Site Scripting (XSS)
**Locations:**
- [app/utils/helpers.py](app/utils/helpers.py): `format_output()`, `render_content()`, `render_search_results()`, `create_html_element()`
- [app/views/auth.py](app/views/auth.py): `/auth/login`, `/auth/profile`, `/auth/search`
- [app/views/documents.py](app/views/documents.py): `/docs/view/<id>`, `/docs/search`

**Description:** User input rendered in HTML without proper escaping.

**Example:**
```python
# In auth.py
return f"<p>Welcome, {user_name}!</p>"  # No escaping
```

**Exploit:** `/auth/profile?message=<script>alert('XSS')</script>`

### 7. Server-Side Request Forgery (SSRF)
**Locations:**
- [app/utils/network.py](app/utils/network.py): `fetch_url()`, `proxy_request()`, `fetch_image()`, `make_api_call()`
- [app/views/admin.py](app/views/admin.py): `/admin/fetch_url`, `/admin/proxy`
- [app/views/api.py](app/views/api.py): `/api/webhook`, `/api/proxy`

**Description:** Application makes HTTP requests to user-specified URLs without validation.

**Example:**
```python
# In network.py
def fetch_url(url: str):
    return requests.get(url).text  # No validation!
```

**Exploit:** `/admin/fetch_url?url=http://169.254.169.254/latest/meta-data/` (AWS metadata)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

The application will start on `http://0.0.0.0:5000`

## Test Credentials

- **Admin**: username: `admin`, password: `admin123`
- **User**: username: `user`, password: `password123`
- **User**: username: `alice`, password: `alice123`

## Testing with vulnhuntr

From the vulnhuntr directory:

```bash
vulnhuntr -r /path/to/DVPP
```

## Expected Findings

The vulnhuntr scanner should identify all 7 vulnerability classes:

- ✓ **SQLI** (SQL Injection) - 10+ instances across models
- ✓ **IDOR** (Insecure Direct Object Reference) - 5+ instances in document access
- ✓ **LFI** (Local File Inclusion) - 5+ instances in file operations
- ✓ **AFO** (Arbitrary File Overwrite) - 4+ instances in file writes
- ✓ **RCE** (Remote Code Execution) - 6+ instances via eval/exec/subprocess/pickle
- ✓ **XSS** (Cross-Site Scripting) - 10+ instances in output rendering
- ✓ **SSRF** (Server-Side Request Forgery) - 8+ instances in network operations

## Vulnerability Flow Examples

### Example 1: SQLI in Authentication
```
User Input → /auth/login → AuthService.login() → User.authenticate() → SQL Injection
```

### Example 2: IDOR in Document Access
```
User Input → /docs/view/2 → Document.find_by_id() → No ownership check → IDOR
```

### Example 3: RCE via Expression Evaluation
```
User Input → /admin/evaluate?expr=... → ExportService.evaluate_expression() → eval() → RCE
```

### Example 4: SSRF in URL Fetch
```
User Input → /admin/fetch_url?url=... → fetch_url() → requests.get() → SSRF
```

### Example 5: LFI in File Read
```
User Input → /docs/read_file?file=../../etc/passwd → FileService.read_file() → open() → LFI
```

## Design Principles

This application follows common patterns seen in real vulnerable applications:

1. **Layered Architecture**: Vulnerabilities span multiple layers (models, services, utils, views)
2. **Complex Call Chains**: Vulnerabilities require tracing through multiple function calls
3. **Realistic Code**: Uses common frameworks (Flask) and patterns (blueprints, services)
4. **Multiple Entry Points**: Same vulnerabilities accessible through different routes
5. **Bypass Attempts**: Some functions include weak validation that can be bypassed

## Notes

- Uses SQLite for simplicity (no external database required)
- All file operations use relative paths within the project
- Debug mode is enabled for detailed error messages
- Secret keys and credentials are hardcoded in [config.py](config.py)
- No authentication required for many vulnerable endpoints (realistic in legacy apps)

## Disclaimer

**FOR EDUCATIONAL USE ONLY**

This application is intentionally insecure and demonstrates vulnerabilities that should NEVER be present in production code. It is designed specifically for:

- Security research and education
- Testing vulnerability scanners
- Training security professionals
- Demonstrating secure coding practices (by counterexample)

Use only in isolated, controlled environments. Do not expose to the internet or use with real data.
Damn Vulnerable Python Project
