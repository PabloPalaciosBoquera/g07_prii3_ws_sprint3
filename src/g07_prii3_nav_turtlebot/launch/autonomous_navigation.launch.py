# PBI 3.4: navegación autónoma según el ArUco de la puerta (simulación).
# Uso: ros2 launch g07_prii3_nav_turtlebot autonomous_navigation.launch.py aruco:=6
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    paquete = get_package_share_directory('g07_prii3_nav_turtlebot')

    return LaunchDescription([
        DeclareLaunchArgument('aruco', default_value='5'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(paquete, 'launch', 'navegacion.launch.py')),
            launch_arguments={'aruco': LaunchConfiguration('aruco')}.items()),

        Node(
            package='g07_prii3_nav_turtlebot',
            executable='autonomous_navigation',
            parameters=[{'use_sim_time': True}],
            output='screen'),
    ])
