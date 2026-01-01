from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h2>Robot Arm Jog UI</h2>
    <button onclick="send('j1_plus')">J1 +</button>
    <button onclick="send('j1_minus')">J1 -</button>
    <br><br>
    <button onclick="send('j2_plus')">J2 +</button>
    <button onclick="send('j2_minus')">J2 -</button>

    <script>
    function send(cmd) {
        fetch('/jog', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: cmd})
        });
    }
    </script>
    """

@app.route('/jog', methods=['POST'])
def jog():
    data = request.get_json()
    cmd = data['command']
    print(f"Jog command received: {cmd}")
    return jsonify(status="ok")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
