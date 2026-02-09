"""AdminPanel - System Admin Dashboard | Vulnerabilities: RCE, Path Traversal, Multiple, Other (Docker, Account Takeover, Mercurial)"""
from flask import Flask, request, jsonify
import os, subprocess, pickle, socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin-secret'

# VULN: RCE cluster - CVE-2024-42845, CVE-2025-1550, CVE-2023-0297
@app.route('/system/exec', methods=['POST'])
def system_exec():
    cmd = request.json.get('command')
    # VULN: Command injection
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({"stdout": result.stdout, "stderr": result.stderr})

@app.route('/system/eval', methods=['POST'])
def system_eval():
    expr = request.json.get('expression')
    # VULN: eval RCE
    result = eval(expr)
    return jsonify({"result": str(result)})

@app.route('/system/python', methods=['POST'])
def python_exec():
    code = request.json.get('code')
    # VULN: exec RCE
    exec(code)
    return jsonify({"executed": True})

# VULN: Deserialization - CVE-2022-34668
@app.route('/config/load', methods=['POST'])
def load_config():
    data = request.json.get('data')
    # VULN: Unsafe pickle
    import base64
    config = pickle.loads(base64.b64decode(data))
    return jsonify({"config": str(config)})

# VULN: Path traversal - CVE-2024-40422
@app.route('/logs/view')
def view_logs():
    logfile = request.args.get('file', '/var/log/syslog')
    # VULN: Arbitrary file read
    try:
        with open(logfile, 'r') as f:
            return jsonify({"log": f.read()})
    except:
        return "Cannot read", 404

# VULN: Docker escape - CVE (DC/OS Marathon Docker), CVE (Docker Daemon)
@app.route('/docker/exec', methods=['POST'])
def docker_exec():
    container = request.json.get('container')
    cmd = request.json.get('cmd')
    # VULN: Arbitrary docker exec
    result = os.popen(f"docker exec {container} {cmd}").read()
    return jsonify({"output": result})

# VULN: Account Takeover - CVE-2019-19844 (Django), CVE-2023-0777 (modoboa)
@app.route('/users/reset', methods=['POST'])
def reset_password():
    username = request.json.get('username')
    new_password = request.json.get('password')
    # VULN: No verification, allows account takeover
    return jsonify({"reset": True, "user": username, "new_password": new_password})

# VULN: Mercurial hg-ssh - CVE (Mercurial RCE)
@app.route('/git/clone', methods=['POST'])
def git_clone():
    repo = request.json.get('repo')
    # VULN: Command injection in git/hg commands
    result = os.popen(f"hg clone {repo} /tmp/repo").read()
    return jsonify({"cloned": result})

# VULN: Multiple vulnerabilities - CVE-2016-4806/4807/4808 (Web2py)
@app.route('/web2py/debug')
def web2py_debug():
    # VULN: Exposes multiple attack vectors
    return jsonify({
        "database_uri": "sqlite:///admin.db",
        "secret": app.config['SECRET_KEY'],
        "routes": [str(rule) for rule in app.url_map.iter_rules()],
        "env": dict(os.environ)
    })

# VULN: Remote source code read - CVE-2022-30286 (PyScript)
@app.route('/source')
def source_code():
    module = request.args.get('module', 'app')
    # VULN: Reads Python source files
    try:
        filepath = module.replace('.', '/') + '.py'
        with open(filepath, 'r') as f:
            return jsonify({"source": f.read()})
    except:
        return "Not found", 404

@app.route('/')
def index():
    return {"app": "AdminPanel", "port": 5007, "endpoints": ["/system/exec", "/system/eval", "/system/python", "/config/load", "/logs/view?file=", "/docker/exec", "/users/reset", "/git/clone", "/web2py/debug", "/source?module="]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
