
import serial
import time

ser = serial.Serial('/dev/serial0', 9600, timeout=1)

def send_command(command):
    ser.write((command+'\n').encode("utf-8"))
    time.sleep(0.5)

try:
    while True:
        cmd = input("Enter command (or 'exit' to quit): ")
        if cmd.lower() == 'exit':
            break
        send_command(cmd)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
