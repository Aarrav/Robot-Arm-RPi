from flask import Flask, request, jsonify
import serial
import threading
import queue
import time

# ---------- Serial Setup ----------
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
print("Using /dev/ttyAMA0 for serial communication.")
time.sleep(2)

cmd_queue = queue.Queue()

def serial_worker():
    while True:
        cmd = cmd_queue.get()
        if cmd is None:
            break
        
        # Priority Check: If it's a STOP command, we might want to flush the queue?
        # For now, we just send it immediately.
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
                margin-bottom: 20px;
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
                border: none;
                border-radius: 8px;
                color: white;
                padding: 20px 30px;
                font-size: 1.5rem;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.1s, background-color 0.2s;
                min-width: 80px;
                touch-action: manipulation;
                -webkit-tap-highlight-color: transparent;
            }
            .btn-minus { background-color: #d32f2f; }
            .btn-plus { background-color: #388e3c; }
            
            /* STOP BUTTON STYLES */
            .btn-stop {
                background-color: #b71c1c; /* Darker Red */
                width: 100%;
                max-width: 200px;
                padding: 25px;
                margin-bottom: 30px;
                font-size: 2rem;
                letter-spacing: 2px;
                border: 2px solid #ff5252;
                box-shadow: 0 0 15px rgba(255, 82, 82, 0.4);
            }
            
            button:active {
                transform: scale(0.95);
                opacity: 0.8;
            }
            @media (hover: hover) {
                .btn-minus:hover { background-color: #b71c1c; }
                .btn-plus:hover { background-color: #2e7d32; }
                .btn-stop:hover { background-color: #ff1744; box-shadow: 0 0 25px rgba(255, 23, 68, 0.6); }
            }
        </style>
    </head>
    <body>

        <h2>🤖 Robot Arm UI</h2>

        <button class="btn-stop" onclick="send('STOP')">STOP</button>

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
    
    # Optional: Clear queue if STOP is pressed so it executes immediately?
    # For now, we just add it to the queue.
    if cmd == "STOP":
        # Strategy: You might want to empty the queue here so previous movements are cancelled
        with cmd_queue.mutex:
            cmd_queue.queue.clear()
            
    cmd_queue.put(cmd)
    return jsonify(status="ok")

# ---------- Main ----------
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        cmd_queue.put(None)
        if ser.is_open:
            ser.close()