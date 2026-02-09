"""FileShare - File Upload/Download Platform | Vulnerabilities: File Upload RCE, Path Traversal, LFI, XSS, Open Redirect"""
from flask import Flask, request, jsonify, send_file, redirect, render_template_string
import os, subprocess, zipfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fileshare-secret'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# VULN: File Upload RCE - CVE-2022-31161 (Roxy WI), CVE-2012-6081 (MoinMoin)
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = request.form.get('filename', file.filename)  # VULN: User-controlled filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # VULN: No sanitization
    file.save(filepath)
    # VULN: Executes uploaded Python files
    if filename.endswith('.py'):
        result = subprocess.run(['python3', filepath], capture_output=True, text=True)
        return jsonify({"uploaded": filename, "executed": True, "output": result.stdout})
    return jsonify({"uploaded": filename})

# VULN: Path Traversal - CVE-2024-40422 (Devika), CVE-2023-37474 (copyparty), CVE-2024-23334 (aiohttp)
@app.route('/download')
def download():
    path = request.args.get('path', '')  # VULN: No validation
    # VULN: Path traversal - can access any file
    try:
        return send_file(path)  # VULN: Direct file access
    except:
        return "File not found", 404

# VULN: LFI - CVE-2019-14322 (Werkzeug), CVE-2018-7490 (uWSGI), CVE-2014-4650 (Python CGI)
@app.route('/view')
def view_file():
    file = request.args.get('file', '')  # VULN: User input
    # VULN: Local file inclusion
    content = open(file, 'r').read()  # VULN: No path restriction
    return render_template_string(f"<pre>{content}</pre>")  # VULN: XSS

# VULN: Open Redirect - CVE-2021-21337 (PluggableAuthService)
@app.route('/redirect')
def redirect_to():
    url = request.args.get('url', '/')
    return redirect(url)  # VULN: Unvalidated redirect

# VULN: Zip Slip - AFO via extract
@app.route('/extract', methods=['POST'])
def extract_zip():
    file = request.files['file']
    zip_path = '/tmp/upload.zip'
    file.save(zip_path)
    # VULN: Zip slip vulnerability - arbitrary file write
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('/tmp/extracted')  # VULN: No path validation
    return jsonify({"extracted": True})

# VULN: RCE via file processing
@app.route('/process', methods=['POST'])
def process_file():
    filename = request.json.get('file')
    command = request.json.get('command', 'cat')  # VULN: User-controlled command
    # VULN: Command injection
    result = os.system(f"{command} {filename}")  # VULN: Shell injection
    return jsonify({"result": result})

@app.route('/')
def index():
    return {"app": "FileShare", "port": 5003, "endpoints": ["/upload", "/download?path=", "/view?file=", "/extract", "/process", "/redirect?url="]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
