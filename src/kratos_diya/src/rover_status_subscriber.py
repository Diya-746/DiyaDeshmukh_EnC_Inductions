#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String, Bool


class RoverStatusSubscriber(Node):
    """
    Subscribes to rover status topics and prints received values.
    """

    def __init__(self):
        super().__init__('rover_status_subscriber')

        self.create_subscription(
            Float32,
            'battery_level',
            self.battery_callback,
            10
        )

        self.create_subscription(
            String,
            'rover_mode',
            self.mode_callback,
            10
        )

        self.create_subscription(
            Bool,
            'emergency_stop',
            self.estop_callback,
            10
        )

    def battery_callback(self, msg):
"""
    Processes incoming battery level messages.
    """
        self.get_logger().info(f"Battery Level: {msg.data:.1f}%")

    def mode_callback(self, msg):
 """
    Processes incoming rover mode messages.
    """
        self.get_logger().info(f"Mode: {msg.data}")

    def estop_callback(self, msg):
 """
    Processes incoming emergency stop messages.
    """
        self.get_logger().info(f"Emergency Stop: {msg.data}")


def main(args=None):
 """
    Initializes and runs the rover status subscriber node.
    """
    rclpy.init(args=args)

    node = RoverStatusSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
