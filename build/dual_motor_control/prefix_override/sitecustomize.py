import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/robotarm/Robot-Arm-RPi/install/dual_motor_control'
