# PBI 3.1: ids y coordenadas de los ArUco del tablero con la cámara cenital (USB).
# Para ver el topic en otra terminal: ros2 topic echo /aruco_cenital
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='g07_prii3_nav_jetbot',
            executable='aruco_cenital',
            output='screen'),
    ])
