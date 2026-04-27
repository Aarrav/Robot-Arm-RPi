import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class DualMotorCommander(Node):
    def __init__(self):
        super().__init__('dual_motor_commander')

        # One topic per joint
        self.base_pub = self.create_publisher(
            Float32MultiArray, '/base/move', 10)
        self.shoulder_pub = self.create_publisher(
            Float32MultiArray, '/shoulder/move', 10)

        self.get_logger().info('Dual Motor Commander ready.')

    def send_command(self, base_final, shoulder_final, duration):
        # Base command: [final_pos, duration]
        base_msg = Float32MultiArray()
        base_msg.data = [float(base_final), float(duration)]
        self.base_pub.publish(base_msg)

        # Shoulder command: [final_pos, duration]
        shoulder_msg = Float32MultiArray()
        shoulder_msg.data = [float(shoulder_final), float(duration)]
        self.shoulder_pub.publish(shoulder_msg)

        self.get_logger().info(
            f'Sent — Base: {base_final}°  Shoulder: {shoulder_final}°  Duration: {duration}s'
        )

def main(args=None):
    rclpy.init(args=args)
    node = DualMotorCommander()

    print('=== Dual Motor Control ===')
    while True:
        try:
            base_final     = float(input('Base final position     (degrees): '))
            shoulder_final = float(input('Shoulder final position (degrees): '))
            duration       = float(input('Duration                (seconds): '))
            print()
            node.send_command(base_final, shoulder_final, duration)
            print()
        except KeyboardInterrupt:
            print('\nExiting.')
            break
        except ValueError:
            print('Invalid input — numbers only.\n')

    node.destroy_node()
    rclpy.shutdown()