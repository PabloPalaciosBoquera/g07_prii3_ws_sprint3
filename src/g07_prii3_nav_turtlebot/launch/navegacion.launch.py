# Simulación + Nav2 con el mapa guardado del F1L3 (AMCL) + RViz.
# Lo usan predefined_navigation.launch.py y autonomous_navigation.launch.py.
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    paquete = get_package_share_directory('g07_prii3_nav_turtlebot')
    nav2 = get_package_share_directory('nav2_bringup')
    parametros = os.path.join(
        get_package_share_directory('turtlebot3_navigation2'), 'param', 'waffle.yaml')
    mapa = os.path.join(paquete, 'maps', 'f1l3.yaml')

    return LaunchDescription([
        DeclareLaunchArgument('aruco', default_value='5'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(paquete, 'launch', 'simulacion.launch.py')),
            launch_arguments={'aruco': LaunchConfiguration('aruco')}.items()),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2, 'launch', 'bringup_launch.py')),
            launch_arguments={'map': mapa,
                              'use_sim_time': 'True',
                              'params_file': parametros}.items()),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(nav2, 'rviz', 'nav2_default_view.rviz')],
            parameters=[{'use_sim_time': True}]),
    ])
