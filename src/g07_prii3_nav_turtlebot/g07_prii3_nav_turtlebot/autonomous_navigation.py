import math

import cv2
import rclpy
from cv_bridge import CvBridge
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from sensor_msgs.msg import Image


# Poses en el frame "map": (x, y, ángulo en radianes).
# El origen del mapa es el punto donde arranca el robot en el pasillo.
POSE_INICIAL = (0.0, 0.0, 0.0)     # pasillo
POSE_PUERTA = (3.2, 1.0, 1.57)     # delante de la puerta, mirando al ArUco

# Pose final dentro del laboratorio según el id del ArUco de la puerta
DESTINOS = {
    5: (3.5, 7.1, 1.57),
    6: (-2.0, 6.5, 3.14),
    17: (0.5, 14.1, 3.14),
}


def crear_pose(navegador, x, y, angulo):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navegador.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(angulo / 2)
    pose.pose.orientation.w = math.cos(angulo / 2)
    return pose


def ir_a(navegador, pose):
    navegador.goToPose(crear_pose(navegador, *pose))
    while not navegador.isTaskComplete():
        pass
    return navegador.getResult() == TaskResult.SUCCEEDED


def main():
    rclpy.init()
    navegador = BasicNavigator(node_name='autonomous_navigation')

    # Diccionario de ArUco de Eurobot 2027
    diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    bridge = CvBridge()
    aruco = {'id': None}

    def imagen_callback(msg):
        imagen = bridge.imgmsg_to_cv2(msg, 'bgr8')
        # OpenCV 4.7 o más nuevo usa ArucoDetector; el 4.6 de Ubuntu 24.04, detectMarkers
        if hasattr(cv2.aruco, 'ArucoDetector'):
            _, ids, _ = cv2.aruco.ArucoDetector(diccionario).detectMarkers(imagen)
        else:
            # Umbral más alto: en Gazebo el borde blanco del ArUco sale gris
            parametros = cv2.aruco.DetectorParameters_create()
            parametros.adaptiveThreshConstant = 20
            _, ids, _ = cv2.aruco.detectMarkers(imagen, diccionario, parameters=parametros)
        if ids is not None:
            for i in ids.flatten():
                if int(i) in DESTINOS:
                    aruco['id'] = int(i)

    # 1. Pose inicial en el pasillo
    navegador.setInitialPose(crear_pose(navegador, *POSE_INICIAL))
    navegador.waitUntilNav2Active()

    # 2. Ir a la puerta del laboratorio
    navegador.info('Yendo a la puerta del laboratorio')
    if not ir_a(navegador, POSE_PUERTA):
        navegador.error('No se ha podido llegar a la puerta')
        rclpy.shutdown()
        return

    # 3. Leer el ArUco de la puerta con la cámara
    navegador.info('En la puerta. Buscando el ArUco...')
    navegador.create_subscription(Image, '/camera/image_raw', imagen_callback, 10)
    while aruco['id'] is None:
        rclpy.spin_once(navegador, timeout_sec=0.1)
    navegador.info(f'ArUco {aruco["id"]} detectado')

    # 4. Ir a la pose que corresponde a ese ArUco
    if ir_a(navegador, DESTINOS[aruco['id']]):
        navegador.info(f'Destino del ArUco {aruco["id"]} alcanzado')
    else:
        navegador.error('No se ha podido llegar al destino')

    navegador.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
