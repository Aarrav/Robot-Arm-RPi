from flask import Flask, request, jsonify
import serial
import threading
import queue
import time

# ---------- Serial Setup ----------
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)

cmd_queue = queue.Queue()

def serial_worker():
    while True:
        cmd = cmd_queue.get()
        if cmd is None:
            break
        ser.write((cmd + '\n').encode('utf-8'))
        print(f"Sent to Teensy: {cmd}")
        time.sleep(0.05)

serial_thread = threading.Thread(target=serial_worker, daemon=True)
serial_thread.start()

# ---------- Flask Setup ----------
app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h2>Robot Arm Jog UI</h2>
    <button onclick="send('J1_PLUS')">J1 +</button>
    <button onclick="send('J1_MINUS')">J1 -</button>
    <br><br>
    <button onclick="send('J2_PLUS')">J2 +</button>
    <button onclick="send('J2_MINUS')">J2 -</button>

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
    cmd_queue.put(cmd)
    return jsonify(status="ok")

# ---------- Main ----------
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        cmd_queue.put(None)
        ser.close()
