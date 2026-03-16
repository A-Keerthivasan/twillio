from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import subprocess
import sys
import os

app = Flask(__name__)
CORS(app)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AquaAssistant - Send Alert</title>

<style>
html, body {
margin: 0;
padding: 0;
height: 100%;
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
color: #e0f7fa;
overflow: hidden;
}

body {
background: url('https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGpqNWV0MjVod3dwcWZkajI5dHNrdGpub2czc2Qzc3Jhdm00ZWcxYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VI2UC13hwWin1MIfmi/giphy.gif') no-repeat center center fixed;
background-size: cover;
}

.overlay {
position: fixed;
top: 0; left: 0; right: 0; bottom: 0;
background-color: rgba(0, 0, 30, 0.6);
z-index: 0;
}

.card {
position: fixed;
top: 50%;
left: 50%;
transform: translate(-50%, -50%);
background: rgba(0, 40, 60, 0.75);
padding: 40px;
max-width: 400px;
border-radius: 16px;
text-align: center;
z-index: 1;
}

select, button {
margin: 8px;
padding: 10px;
border-radius: 8px;
font-size: 1.1rem;
cursor: pointer;
}

#status {
margin-top: 20px;
color: #81d4fa;
font-weight: bold;
}
</style>

<script>
function sendAlert() {

const recipient = document.getElementById('recipient').value;
const statusElement = document.getElementById('status');

statusElement.textContent = "Sending alert...";

fetch('/send-alert', {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({recipient})
})

.then(response => response.json())

.then(data => {

if(data.message){
statusElement.textContent = data.message;
statusElement.style.color = "#00e676";
}

else if(data.error){
statusElement.textContent = "Error: " + data.error;
statusElement.style.color = "#ff5252";
}

})

.catch(error => {
statusElement.textContent = "Error: " + error;
statusElement.style.color = "#ff5252";
});

}
</script>

</head>

<body>

<div class="overlay"></div>

<div class="card">

<h2>AquaAssistant Alert System</h2>

<label>Select Recipient:</label>

<br><br>

<select id="recipient">
<option value="Public">Public</option>
<option value="DWLR Service Manager">DWLR Service Manager</option>
<option value="Corporation">Corporation</option>
<option value="Farmer">Farmer</option>
</select>

<br>

<button onclick="sendAlert()">Send Alert</button>

<div id="status"></div>

</div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/send-alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        recipient = data.get('recipient', 'Public')

        python_cmd = 'python3' if sys.platform != 'win32' else 'python'

        result = subprocess.run(
            [python_cmd, 'main.py', recipient],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return jsonify({"message": f"Alert sent to {recipient}!"})
        else:
            return jsonify({"error": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
