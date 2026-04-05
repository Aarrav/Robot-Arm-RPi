import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class MotorCommander(Node):
    def __init__(self):
        super().__init__('motor_commander')
        self.pub = self.create_publisher(Float32MultiArray, '/move_base', 10)

    def send_command(self, final, duration):
        msg = Float32MultiArray()
        msg.data = [final, duration]
        self.pub.publish(msg)
        self.get_logger().info(f'Sent: {final}° over {duration}s')

def main(args=None):
    rclpy.init(args=args)
    node = MotorCommander()

    print('=== Base Motor Control ===')
    while True:
        try:
            final    = float(input('Final absolute position   (degrees): '))
            duration = float(input('Duration         (seconds): '))
            node.send_command(final, duration)
            print()
        except KeyboardInterrupt:
            print('\nExiting.')
            break
        except ValueError:
            print('Invalid input, please enter numbers only.')

    node.destroy_node()
    rclpy.shutdown()