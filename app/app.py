from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        url = request.form.get('url')
        port = request.form.get('port')
        nslookup_check = request.form.get('nslookup')
        curl_check = request.form.get('curl')
        telnet_check = request.form.get('telnet')
        ping_check = request.form.get('ping')

        # Perform selected tests
        if nslookup_check:
            try:
                result += f"Nslookup result for {url}:\n"
                result += subprocess.check_output(['nslookup', url], stderr=subprocess.STDOUT).decode('utf-8')
            except subprocess.CalledProcessError as e:
                result += f"Nslookup failed: {e.output.decode('utf-8')}\n"

        if curl_check:
            try:
                result += f"\nCurl result for {url}:\n"
                result += subprocess.check_output(['curl', '-I', url], stderr=subprocess.STDOUT).decode('utf-8')
            except subprocess.CalledProcessError as e:
                result += f"Curl failed: {e.output.decode('utf-8')}\n"

        if telnet_check:
            try:
                result += f"\nTelnet result for {url}:{port}:\n"
                result += subprocess.check_output(['nc', '-zv', url, port], stderr=subprocess.STDOUT).decode('utf-8')
            except subprocess.CalledProcessError as e:
                result += f"Telnet failed: {e.output.decode('utf-8')}\n"

        if ping_check:
            try:
                result += subprocess.check_output(['ping', '-c', '4', url], stderr=subprocess.STDOUT).decode('utf-8')
            except subprocess.CalledProcessError as e:
                result += f"Ping failed: {e.output.decode('utf-8')}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
