# PBI 3.3: navegación predefinida del pasillo al laboratorio (simulación).
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    paquete = get_package_share_directory('g07_prii3_nav_turtlebot')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(paquete, 'launch', 'navegacion.launch.py'))),

        Node(
            package='g07_prii3_nav_turtlebot',
            executable='predefined_navigation',
            parameters=[{'use_sim_time': True}],
            output='screen'),
    ])
