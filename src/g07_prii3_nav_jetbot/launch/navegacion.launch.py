# Nav2 con el mapa real del F1L3 (AMCL) + RViz para el JetBot.
# Lo usan predefined_navigation.launch.py y autonomous_navigation.launch.py.
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
            launch_arguments={'map': os.path.join(paquete, 'maps', 'f1l3.yaml'),
                              'params_file': os.path.join(paquete, 'config', 'nav2_jetbot.yaml')
                              }.items()),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(nav2, 'rviz', 'nav2_default_view.rviz')]),
    ])
