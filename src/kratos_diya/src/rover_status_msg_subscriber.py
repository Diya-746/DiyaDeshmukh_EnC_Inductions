#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from kratos_diya_msgs.msg import RoverStatus


class RoverStatusMsgSubscriber(Node):
    """
    Subscribes to the custom RoverStatus message and prints the received data.
    """

    def __init__(self):
        super().__init__('rover_status_msg_subscriber')

        self.subscription = self.create_subscription(
            RoverStatus,
            'rover_status',
            self.status_callback,
            10
        )

    def status_callback(self, msg):
        """
        Processes incoming RoverStatus messages.
        """
        self.get_logger().info(
            f"Battery Level: {msg.battery_level:.1f}% | "
            f"Mode: {msg.rover_mode} | "
            f"Emergency Stop: {msg.emergency_stop}"
        )


def main(args=None):
    """
    Initializes and runs the rover status message subscriber node.
    """
    rclpy.init(args=args)

    node = RoverStatusMsgSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
