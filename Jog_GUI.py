from flask import Flask, request, jsonify
import serial
import threading
import queue
import time

# ---------- Serial Setup ----------
# Ensure your wiring matches /dev/serial0 (pins 14/15 on Pi)
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)

cmd_queue = queue.Queue()

def serial_worker():
    while True:
        cmd = cmd_queue.get()
        if cmd is None:
            break
        # Adding new line as per original logic
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
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Robot Control</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #1e1e1e;
                color: #e0e0e0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
            }
            h2 {
                margin-bottom: 30px;
                font-weight: 300;
                letter-spacing: 1px;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }
            .control-row {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                background: #2d2d2d;
                padding: 10px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            .label {
                width: 60px;
                text-align: center;
                font-weight: bold;
                font-size: 1.2rem;
                margin: 0 15px;
            }
            button {
                background-color: #3a3a3a;
                border: none;
                border-radius: 8px;
                color: white;
                padding: 20px 30px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 1.5rem;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.1s, background-color 0.2s;
                min-width: 80px;
                touch-action: manipulation; /* Improves response on touch screens */
                -webkit-tap-highlight-color: transparent;
            }
            /* Specific Colors for Plus/Minus */
            .btn-minus { background-color: #d32f2f; }
            .btn-plus { background-color: #388e3c; }
            
            /* Active State (Click effect) */
            button:active {
                transform: scale(0.95);
                opacity: 0.8;
            }
            
            /* Hover State (Desktop only) */
            @media (hover: hover) {
                .btn-minus:hover { background-color: #b71c1c; }
                .btn-plus:hover { background-color: #2e7d32; }
            }
        </style>
    </head>
    <body>

        <h2>🤖 Robot Arm UI</h2>

        <div class="control-row">
            <button class="btn-minus" onclick="send('J1_MINUS')">-</button>
            <div class="label">J1</div>
            <button class="btn-plus" onclick="send('J1_PLUS')">+</button>
        </div>

        <div class="control-row">
            <button class="btn-minus" onclick="send('J2_MINUS')">-</button>
            <div class="label">J2</div>
            <button class="btn-plus" onclick="send('J2_PLUS')">+</button>
        </div>

        <script>
            function send(cmd) {
                // Visual feedback in console
                console.log("Sending: " + cmd);
                
                fetch('/jog', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command: cmd})
                }).catch(err => console.error("Error:", err));
            }
        </script>
    </body>
    </html>
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
        # Host 0.0.0.0 allows access from other devices on the network
        app.run(host='0.0.0.0', port=5000)
    finally:
        cmd_queue.put(None)
        if ser.is_open:
            ser.close()