#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String, Bool


class RoverStatusPublisher(Node):
    """
    Publishes rover battery level, mode, and emergency stop status.
    """

    def __init__(self):
        super().__init__('rover_status_publisher')

        self.battery_pub = self.create_publisher(Float32, 'battery_level', 10)
        self.mode_pub = self.create_publisher(String, 'rover_mode', 10)
        self.estop_pub = self.create_publisher(Bool, 'emergency_stop', 10)

        self.timer = self.create_timer(1.0, self.publish_status)

        self.battery = 100.0

    def publish_status(self):
 """
    Publishes the rover's battery level, mode, and emergency stop status.
    """

        battery_msg = Float32()
        battery_msg.data = self.battery

        mode_msg = String()
        mode_msg.data = "AUTONOMOUS"

        estop_msg = Bool()
        estop_msg.data = False

        self.battery_pub.publish(battery_msg)
        self.mode_pub.publish(mode_msg)
        self.estop_pub.publish(estop_msg)

        self.get_logger().info(
            f"Battery={self.battery:.1f}% Mode={mode_msg.data} Emergency={estop_msg.data}"
        )

        self.battery -= 0.5
        if self.battery < 0:
            self.battery = 100.0


def main(args=None):
"""
    Initializes and runs the rover status publisher node.
    """
    rclpy.init(args=args)
    node = RoverStatusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
