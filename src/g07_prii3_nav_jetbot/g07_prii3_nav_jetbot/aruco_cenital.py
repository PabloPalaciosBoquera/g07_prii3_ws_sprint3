import cv2
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ArucoCenital(Node):

    def __init__(self):
        super().__init__('aruco_cenital')
        self.publicador = self.create_publisher(String, '/aruco_cenital', 10)

        # Cámara cenital conectada por USB
        self.camara = cv2.VideoCapture(0)

        # Diccionario de Eurobot 2027
        self.diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)

        self.create_timer(0.1, self.detectar)

    def detectar(self):
        ok, imagen = self.camara.read()
        if not ok:
            self.get_logger().warn('No se puede leer la cámara')
            return

        # OpenCV 4.7 o más nuevo usa ArucoDetector; el 4.6 de Ubuntu 24.04, detectMarkers
        if hasattr(cv2.aruco, 'ArucoDetector'):
            esquinas, ids, _ = cv2.aruco.ArucoDetector(self.diccionario).detectMarkers(imagen)
        else:
            esquinas, ids, _ = cv2.aruco.detectMarkers(imagen, self.diccionario)

        # Texto con el id y el centro (en píxeles) de cada ArUco detectado
        texto = ''
        if ids is not None:
            for i in range(len(ids)):
                centro = esquinas[i][0].mean(axis=0)
                texto += f'id: {ids[i][0]}, x: {int(centro[0])}, y: {int(centro[1])}\n'

        msg = String()
        msg.data = texto
        self.publicador.publish(msg)

        # Ventana para ver lo que detecta durante la demostración
        cv2.aruco.drawDetectedMarkers(imagen, esquinas, ids)
        cv2.imshow('Camara cenital', imagen)
        cv2.waitKey(1)


def main():
    rclpy.init()
    nodo = ArucoCenital()
    rclpy.spin(nodo)
    nodo.camara.release()
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
