"""ChatApp - Real-time Chat Application | Vulnerabilities: XSS, RCE, Auth Bypass, Path Traversal, Info Disclosure"""
from flask import Flask, request, jsonify, render_template_string
import sqlite3, os, subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat-secret'
DB = '/tmp/chat.db'
UPLOADS = '/tmp/chat_uploads'
os.makedirs(UPLOADS, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INT, user TEXT, content TEXT, timestamp TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INT, username TEXT, password TEXT)')
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin')")
    conn.commit()
    conn.close()

init_db()

# VULN: XSS in messages - CVE-2023-38501 (copyparty XSS), CVE-2021-42053
@app.route('/send', methods=['POST'])
def send_message():
    user = request.json.get('user', 'anonymous')
    content = request.json.get('content')
    # VULN: Stored XSS - no sanitization
    conn = sqlite3.connect(DB)
    conn.execute(f"INSERT INTO messages VALUES (NULL, '{user}', '{content}', datetime('now'))")
    conn.commit()
    conn.close()
    return jsonify({"sent": True})

# VULN: XSS display
@app.route('/messages')
def get_messages():
    conn = sqlite3.connect(DB)
    messages = conn.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT 50').fetchall()
    conn.close()
    html = '<h1>Chat Messages</h1><ul>'
    for msg in messages:
        # VULN: XSS - unescaped content
        html += f'<li><strong>{msg[1]}</strong>: {msg[2]}</li>'
    html += '</ul>'
    return render_template_string(html)

# VULN: RCE via bot commands - CVE-2023-0297 (PyLoad)
@app.route('/bot', methods=['POST'])
def chatbot():
    command = request.json.get('command')
    # VULN: eval RCE
    if command.startswith('/eval'):
        expr = command[6:]
        result = eval(expr)  # VULN
        return jsonify({"bot_response": str(result)})
    # VULN: exec RCE
    elif command.startswith('/exec'):
        code = command[6:]
        exec(code)  # VULN
        return jsonify({"bot_response": "Executed"})
    # VULN: Command injection
    elif command.startswith('/run'):
        cmd = command[5:]
        result = os.popen(cmd).read()  # VULN
        return jsonify({"bot_response": result})
    return jsonify({"bot_response": "Unknown command"})

# VULN: Auth bypass - CVE-2022-31125
@app.route('/admin/read_log')
def read_log():
    # VULN: No auth + path traversal
    logfile = request.args.get('file', '/var/log/app.log')
    try:
        with open(logfile, 'r') as f:
            return jsonify({"log": f.read()})
    except:
        return jsonify({"error": "Cannot read file"})

# VULN: Info disclosure - CVE-2017-14955
@app.route('/debug')
def debug():
    return jsonify({
        "environment": dict(os.environ),
        "files": os.listdir(UPLOADS),
        "db_path": DB
    })

@app.route('/')
def index():
    return {"app": "ChatApp", "port": 5006, "endpoints": ["/send", "/messages", "/bot", "/admin/read_log?file=", "/debug"]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
