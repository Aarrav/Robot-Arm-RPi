import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class TrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('trajectory_publisher')

        self.publisher_ = self.create_publisher(
            Float32MultiArray,
            '/joint_trajectory_command',
            10
        )

        # Send command after short delay
        self.timer = self.create_timer(2.0, self.send_command)

    def send_command(self):
        msg = Float32MultiArray()

        start_pos = 0.0          # radians
        end_pos = 1.745          # ~100 degrees
        duration = 3.0           # seconds

        msg.data = [start_pos, end_pos, duration]

        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent trajectory: {msg.data}')

        # Stop after one publish
        self.timer.cancel()


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
