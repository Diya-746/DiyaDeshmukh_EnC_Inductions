import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import Command

from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = get_package_share_directory("arm_humble")

    xacro_file = os.path.join(
        pkg_share,
        "urdf",
        "my_custom_arm.urdf.xacro"
    )

    rviz_config_file = os.path.join(
        pkg_share,
        "rviz",
        "view_arm.rviz"
    )

    robot_description = Command(["xacro ", xacro_file])

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description
            }
        ]
    )


    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        rviz_node
    ])
