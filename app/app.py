from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Connectivity Test App!"

@app.route('/test', methods=['POST'])
def test_connectivity():
    url = request.form.get('url')
    port = request.form.get('port')
    nslookup_result = None
    curl_result = None
    telnet_result = None
    ping_result = None

    # Perform NSLookup
    if request.form.get('nslookup'):
        try:
            nslookup_result = subprocess.check_output(['nslookup', url], stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            nslookup_result = f"NSLookup failed: {e.output.decode('utf-8')}"

    # Perform Curl
    if request.form.get('curl'):
        try:
            curl_result = subprocess.check_output(['curl', '-I', f'{url}:{port}'], stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            curl_result = f"Curl failed: {e.output.decode('utf-8')}"

    # Perform Telnet
    if request.form.get('telnet'):
        try:
            telnet_result = subprocess.check_output(['nc', '-zv', url, port], stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            telnet_result = f"Telnet failed: {e.output.decode('utf-8')}"

    # Perform Ping
    if request.form.get('ping'):
        try:
            ping_result = subprocess.check_output(['ping', '-c', '4', url], stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            ping_result = f"Ping failed: {e.output.decode('utf-8')}"

    return jsonify({
        'nslookup': nslookup_result,
        'curl': curl_result,
        'telnet': telnet_result,
        'ping': ping_result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
