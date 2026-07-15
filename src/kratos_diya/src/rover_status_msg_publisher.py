#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from kratos_diya_msgs.msg import RoverStatus


class RoverStatusMsgPublisher(Node):
    """
    Publishes rover status using a custom ROS2 message.
    """

    def __init__(self):
        super().__init__('rover_status_msg_publisher')

        self.status_pub = self.create_publisher(
            RoverStatus,
            'rover_status',
            10
        )

        self.battery = 100.0

        self.timer = self.create_timer(
            1.0,
            self.publish_status
        )

    def publish_status(self):
        """
        Publishes the rover status using a custom ROS2 message.
        """

        msg = RoverStatus()

        msg.battery_level = self.battery
        msg.rover_mode = "AUTONOMOUS"
        msg.emergency_stop = False

        self.status_pub.publish(msg)

        self.get_logger().info(
            f"Battery={msg.battery_level:.1f}% "
            f"Mode={msg.rover_mode} "
            f"Emergency={msg.emergency_stop}"
        )

        self.battery -= 0.5

        if self.battery < 0:
            self.battery = 100.0


def main(args=None):
    """
    Initializes and runs the rover status message publisher node.
    """
    rclpy.init(args=args)

    node = RoverStatusMsgPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
