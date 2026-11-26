import math

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


# Poses en el frame "map": (x, y, ángulo en radianes).
# El origen del mapa es el punto donde arranca el robot en el pasillo.
POSE_INICIAL = (0.0, 0.0, 0.0)   # pasillo
POSE_FINAL = (1.0, 6.0, 1.57)    # dentro del laboratorio


def crear_pose(navegador, x, y, angulo):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navegador.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(angulo / 2)
    pose.pose.orientation.w = math.cos(angulo / 2)
    return pose


def main():
    rclpy.init()
    navegador = BasicNavigator(node_name='predefined_navigation')

    # Le decimos a AMCL dónde está el robot y esperamos a que Nav2 esté listo
    navegador.setInitialPose(crear_pose(navegador, *POSE_INICIAL))
    navegador.waitUntilNav2Active()

    navegador.info('Yendo al punto final del laboratorio')
    navegador.goToPose(crear_pose(navegador, *POSE_FINAL))
    while not navegador.isTaskComplete():
        pass

    if navegador.getResult() == TaskResult.SUCCEEDED:
        navegador.info('Punto final alcanzado')
    else:
        navegador.error('No se ha podido llegar al punto final')

    navegador.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
