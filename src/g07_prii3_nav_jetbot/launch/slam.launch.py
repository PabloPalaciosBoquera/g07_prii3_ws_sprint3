# PBI 3.2: SLAM y navegación guiada desde RViz con el JetBot real.
# Antes, en el robot (por SSH): ros2 launch jetbot_pro_ros2 jetbot.py
# Para guardar el mapa al terminar:
#   ros2 run nav2_map_server map_saver_cli -f src/g07_prii3_nav_jetbot/maps/f1l3_real
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    paquete = get_package_share_directory('g07_prii3_nav_jetbot')
    nav2 = get_package_share_directory('nav2_bringup')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2, 'launch', 'bringup_launch.py')),
            launch_arguments={'slam': 'True',
                              'params_file': os.path.join(paquete, 'config', 'nav2_jetbot.yaml')
                              }.items()),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(nav2, 'rviz', 'nav2_default_view.rviz')]),
    ])
