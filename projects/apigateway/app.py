"""APIGateway - REST API Gateway | Vulnerabilities: SSRF, RCE, Auth Bypass, Info Disclosure, Docker Escape"""
from flask import Flask, request, jsonify, Response
import urllib.request, subprocess, os, json, socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'api-secret'

# VULN: SSRF - CVE-2022-31188 (CVAT), CVE-2022-36551 (Label Studio)
@app.route('/proxy', methods=['POST'])
def proxy():
    url = request.json.get('url')
    # VULN: SSRF - no URL validation
    try:
        response = urllib.request.urlopen(url, timeout=10)
        return Response(response.read(), mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)})

# VULN: RCE - CVE-2023-27524 (Apache Superset), CVE-2025-0655 (D-Tale)
@app.route('/exec', methods=['POST'])
def execute_command():
    cmd = request.json.get('command')
    # VULN: Command injection
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({"stdout": result.stdout, "stderr": result.stderr})

# VULN: Docker escape - CVE (DC/OS Marathon), CVE (Docker Daemon unprotected)
@app.route('/docker/run', methods=['POST'])
def docker_run():
    image = request.json.get('image')
    command = request.json.get('command', 'echo hello')
    # VULN: Arbitrary docker command execution
    cmd = f"docker run --rm {image} {command}"
    result = os.popen(cmd).read()
    return jsonify({"result": result})

# VULN: Docker socket exposure
@app.route('/docker/socket', methods=['POST'])
def docker_socket():
    data = request.json.get('data')
    # VULN: Direct socket access (Docker daemon)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('/var/run/docker.sock')
    sock.send(data.encode())
    response = sock.recv(4096)
    sock.close()
    return jsonify({"response": response.decode()})

# VULN: Auth Bypass - CVE-2023-27524 (Apache Superset auth bypass)
@app.route('/admin', methods=['GET'])
def admin_panel():
    # VULN: No auth check if X-Admin header present
    if request.headers.get('X-Admin'):
        return jsonify({"admin": True, "secret_data": "FLAG{admin_bypass}"})
    return jsonify({"error": "Forbidden"}), 403

# VULN: Info Disclosure - CVE-2017-14955, CVE-2024-22513
@app.route('/status')
def status():
    # VULN: Exposes internal info
    return jsonify({
        "env": dict(os.environ),
        "config": app.config,
        "endpoints": [rule.rule for rule in app.url_map.iter_rules()]
    })

# VULN: JWT bypass
@app.route('/auth', methods=['POST'])
def auth():
    token = request.json.get('token', '')
    # VULN: Weak JWT validation (accepts "none" algorithm)
    if token == 'none' or 'admin' in token:
        return jsonify({"authenticated": True, "role": "admin"})
    return jsonify({"authenticated": False})

@app.route('/')
def index():
    return {"app": "APIGateway", "port": 5004, "endpoints": ["/proxy", "/exec", "/docker/run", "/docker/socket", "/admin", "/status", "/auth"]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
