# PBI 3.2: SLAM y navegación guiada desde RViz (simulación).
# Se construye el mapa a la vez que se navega con la herramienta "Nav2 Goal" de RViz.
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    paquete = get_package_share_directory('g07_prii3_nav_turtlebot')
    nav2 = get_package_share_directory('nav2_bringup')
    parametros = os.path.join(
        get_package_share_directory('turtlebot3_navigation2'), 'param', 'waffle.yaml')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(paquete, 'launch', 'simulacion.launch.py'))),

        # Nav2 con SLAM (slam_toolbox) en lugar de mapa + AMCL
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2, 'launch', 'bringup_launch.py')),
            launch_arguments={'slam': 'True',
                              'use_sim_time': 'True',
                              'params_file': parametros}.items()),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(nav2, 'rviz', 'nav2_default_view.rviz')],
            parameters=[{'use_sim_time': True}]),
    ])
