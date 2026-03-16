from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import sys
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        recipient = data.get('recipient', 'Public')

        python_cmd = 'python3' if sys.platform != 'win32' else 'python'

        result = subprocess.run([python_cmd, 'main.py', recipient], capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({"message": f"Alert sent to {recipient}!"})
        else:
            return jsonify({"error": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
