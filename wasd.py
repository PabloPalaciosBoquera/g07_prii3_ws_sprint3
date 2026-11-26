import sys, termios, tty
import rclpy
from geometry_msgs.msg import Twist

# tecla: (velocidad lineal m/s, velocidad de giro rad/s)
TECLAS = {'w': (0.15, 0.0), 's': (-0.15, 0.0), 'a': (0.0, 0.8), 'd': (0.0, -0.8), ' ': (0.0, 0.0)}

rclpy.init()
nodo = rclpy.create_node('teleop_wasd')
pub = nodo.create_publisher(Twist, '/cmd_vel', 10)
config = termios.tcgetattr(sys.stdin)
print('W/S avanzar/retroceder, A/D girar, espacio parar, Q salir')
try:
    tty.setraw(sys.stdin.fileno())
    while True:
        tecla = sys.stdin.read(1).lower()
        if tecla == 'q':
            break
        if tecla in TECLAS:
            msg = Twist()
            msg.linear.x, msg.angular.z = TECLAS[tecla]
            pub.publish(msg)
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, config)
    pub.publish(Twist())
    rclpy.shutdown()
