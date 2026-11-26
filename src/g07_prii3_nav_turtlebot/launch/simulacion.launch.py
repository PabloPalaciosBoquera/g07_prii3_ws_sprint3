# Abre Gazebo con el mundo F1L3, el TurtleBot3 Waffle en el pasillo
# y el ArUco elegido (5, 6 o 17) en la puerta del laboratorio.
# Lo usan los demás launch del paquete.
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

# El Waffle es el TurtleBot3 que lleva cámara
os.environ['TURTLEBOT3_MODEL'] = 'waffle'


def generate_launch_description():
    paquete = get_package_share_directory('g07_prii3_nav_turtlebot')
    tb3_launch = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    gz_launch = os.path.join(get_package_share_directory('ros_gz_sim'), 'launch')
    mundo = os.path.join(paquete, 'worlds', 'f1l3.sdf')
    modelos = os.path.join(paquete, 'models')

    return LaunchDescription([
        DeclareLaunchArgument('aruco', default_value='5'),

        AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', modelos),

        # Gazebo (servidor y ventana)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(gz_launch, 'gz_sim.launch.py')),
            launch_arguments={'gz_args': ['-r -s -v2 ', mundo],
                              'on_exit_shutdown': 'true'}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(gz_launch, 'gz_sim.launch.py')),
            launch_arguments={'gz_args': '-g -v2 ',
                              'on_exit_shutdown': 'true'}.items()),

        # TurtleBot3 en el pasillo (mismo sitio que en el mundo del profesor)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3_launch, 'robot_state_publisher.launch.py')),
            launch_arguments={'use_sim_time': 'true'}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3_launch, 'spawn_turtlebot3.launch.py')),
            launch_arguments={'x_pose': '-2.0', 'y_pose': '-5.6'}.items()),

        # ArUco en la pared de la puerta del laboratorio, mirando al pasillo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-name', 'aruco',
                       '-file', [modelos, '/g07_aruco_', LaunchConfiguration('aruco'), '/model.sdf'],
                       '-x', '1.21', '-y', '-3.27', '-z', '0.12', '-Y', '-1.5708'],
            output='screen'),
    ])
