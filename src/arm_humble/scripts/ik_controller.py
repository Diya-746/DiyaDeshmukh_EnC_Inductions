#!/usr/bin/env python3

"""
ROS2 IK Controller for arm_humble.

Publishes JointState messages to move the robotic arm.
Only the following joints are controlled:

- base_yaw_joint
- shoulder_joint
- elbow_joint

The wrist and gripper remain fixed.
"""

import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState


class IKController(Node):
    """
    Controls the robotic arm using inverse kinematics.
    """

    def __init__(self):
        super().__init__("ik_controller")

        self.publisher = self.create_publisher(
            JointState,
            "/joint_states",
            10
        )

        self.joint_msg = JointState()

        self.joint_msg.name = [
            "base_yaw_joint",
            "shoulder_joint",
            "elbow_joint",
            "wrist_pitch_joint",
            "wrist_roll_joint",
            "gripper_servo_joint"
        ]

        self.joint_msg.position = [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0
        ]

        # Robot dimensions (meters)
        self.L1 = 0.35
        self.L2 = 0.35

        # Internal end-effector position
        self.x = self.L1 + self.L2
        self.y = 0.0
        self.z = 0.0

        self.get_logger().info("IK Controller Started")

    def publish_joint_state(self):
        """
        Publish the current joint state.
        """

        self.joint_msg.header.stamp = (
            self.get_clock().now().to_msg()
        )

        self.publisher.publish(self.joint_msg)

    def print_position(self):
        """
        Display current end-effector position.
        """

        print("\nCurrent End Effector Position")

        print(f"x = {self.x:.3f}")
        print(f"y = {self.y:.3f}")
        print(f"z = {self.z:.3f}")

    def inverse_kinematics(self, x, y, z):
        """
        Compute joint angles for the desired end-effector position.

        Args:
            x (float): Target x coordinate.
            y (float): Target y coordinate.
            z (float): Target z coordinate.

        Returns:
            tuple:
                (base_yaw, shoulder, elbow)
                or None if unreachable.
        """

        # Base rotation
        base_yaw = math.atan2(y, x)

        # Convert to planar distance
        r = math.sqrt(x**2 + y**2)

        d = math.sqrt(r**2 + z**2)

        # Reachability check
        if d > (self.L1 + self.L2):
            return None

        cos_elbow = (
            d**2 - self.L1**2 - self.L2**2
        ) / (2 * self.L1 * self.L2)

        cos_elbow = max(-1.0, min(1.0, cos_elbow))

        elbow = math.acos(cos_elbow)

        shoulder = (
            math.atan2(z, r)
            - math.atan2(
                self.L2 * math.sin(elbow),
                self.L1 + self.L2 * math.cos(elbow)
            )
        )

        return (
            base_yaw,
            shoulder,
            elbow
        )

    def move_robot(self):
        """
        Read user input and move the robot.
        """

        while True:

            self.print_position()

            axis = input(
                "\nEnter axis (x/y/z) or q to quit: "
            ).lower()

            if axis == "q":
                break

            if axis not in ["x", "y", "z"]:
                print("Invalid axis.")
                continue

            try:
                displacement = float(
                    input(
                        "Enter displacement (meters): "
                    )
                )

            except ValueError:

                print("Invalid value.")
                continue

            new_x = self.x
            new_y = self.y
            new_z = self.z

            if axis == "x":
                new_x += displacement

            elif axis == "y":
                new_y += displacement

            else:
                new_z += displacement

            angles = self.inverse_kinematics(
                new_x,
                new_y,
                new_z
            )

            if angles is None:

                print("\nTarget is outside workspace.\n")

                continue

            base, shoulder, elbow = angles

            self.joint_msg.position[0] = base
            self.joint_msg.position[1] = shoulder
            self.joint_msg.position[2] = elbow

            self.publish_joint_state()

            self.x = new_x
            self.y = new_y
            self.z = new_z

            print("\nMovement successful.")

def main(args=None):
    """
    Entry point for the IK controller node.
    """

    rclpy.init(args=args)

    node = IKController()

    try:
        node.move_robot()

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
