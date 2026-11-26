# Sprint 3 — Navegación autónoma en F1L3 · Grupo 07

Entrega del **Sprint 3 de Proyectos III — Robótica Inteligente**, con SLAM, navegación mediante Nav2 y detección de ArUco.

## Paquetes del Sprint 3

Dos paquetes en `src/`:

- `g07_prii3_nav_turtlebot`: simulación (TurtleBot3 Waffle en Gazebo Harmonic con el mundo F1L3).
- `g07_prii3_nav_jetbot`: robot real (JetBot) y cámara cenital.

Además, en la raíz del workspace:

- `demo.sh`: atajo de simulación que presupone `~/g07_prii3_ws` y cierra procesos previos de Gazebo, RViz y componentes ROS. Para una ejecución independiente de esa ruta, utiliza los comandos `ros2 launch` de esta guía.
- `wasd.py`: mueve el JetBot con las teclas W, A, S y D (útil para hacer el mapa).

Probado con Ubuntu 24.04 y ROS 2 Jazzy.

## 1. Descarga e instalación

```bash
git clone https://github.com/PabloPalaciosBoquera/g07_prii3_ws_sprint3.git
cd g07_prii3_ws_sprint3
```

Los bloques siguientes utilizan Bash. Si utilizas Zsh, ejecuta `bash` antes de cargar archivos `setup.bash`. Cada nueva terminal debe cargar ROS y el workspace.


```bash
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox \
  ros-jazzy-turtlebot3-gazebo ros-jazzy-turtlebot3-navigation2 ros-jazzy-ros-gz \
  ros-jazzy-cv-bridge ros-jazzy-nav2-simple-commander
source /opt/ros/jazzy/setup.bash
# Desde la raíz del workspace clonado:
colcon build --symlink-install
source install/setup.bash
```

En el laboratorio, para que la simulación no se mezcle con los datos de otros grupos, en cada terminal (con el JetBot se usa el dominio del robot; ver el apartado 7):

```bash
export ROS_DOMAIN_ID=77
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST   # solo en simulación
```

El mundo `f1l3_gazebo` del profesor es para Gazebo Classic, que no existe en Jazzy. Está adaptado a Gazebo Harmonic en `g07_prii3_nav_turtlebot/worlds/f1l3.sdf`, con las mismas paredes. Los ArUco 5, 6 y 17 están en `models/` y usan el diccionario `DICT_4X4_100`. Las texturas del zip del profesor eran de `DICT_5X5_100` y no se detectaban con el diccionario de Eurobot 2027.

## 2. PBI 3.1: ArUco con la cámara cenital

Con la cámara conectada por USB:

```bash
ros2 launch g07_prii3_nav_jetbot aruco_cenital.launch.py
```

En otra terminal:

```bash
ros2 topic echo /aruco_cenital
```

Cada línea es `id: 5, x: 320, y: 240`, con el centro del ArUco en píxeles. Si se mueve un ArUco, cambian sus coordenadas. Si se quita, desaparece su línea.

## 3. PBI 3.2: SLAM y navegación guiada con RViz

**Simulación**

```bash
ros2 launch g07_prii3_nav_turtlebot slam.launch.py
```

En RViz, con **Nav2 Goal**, se manda al robot a puntos cercanos de la zona ya vista; el mapa crece mientras se recorre el pasillo y el laboratorio. El paquete ya incluye el mapa `maps/f1l3.yaml` hecho así. Para guardar uno nuevo:

```bash
ros2 run nav2_map_server map_saver_cli -f src/g07_prii3_nav_turtlebot/maps/f1l3
colcon build --symlink-install
```

**JetBot**: primero, en el robot por SSH, `ros2 launch jetbot_pro_ros2 jetbot.py`. Después, en el PC:

```bash
ros2 launch g07_prii3_nav_jetbot slam.launch.py
```

El robot se guía con **Nav2 Goal** o con `python3 wasd.py`. No hace falta guardar este mapa: para navegar, el JetBot usa el mismo `maps/f1l3.yaml` que la simulación (apartado 6).

## 4. PBI 3.3: navegación predefinida

```bash
ros2 launch g07_prii3_nav_turtlebot predefined_navigation.launch.py
ros2 launch g07_prii3_nav_jetbot predefined_navigation.launch.py
```

El robot sale de `POSE_INICIAL`, en el pasillo, y va a `POSE_FINAL`, dentro del laboratorio.

## 5. PBI 3.4: navegación autónoma con ArUco

```bash
ros2 launch g07_prii3_nav_turtlebot autonomous_navigation.launch.py aruco:=5
ros2 launch g07_prii3_nav_jetbot autonomous_navigation.launch.py
```

Secuencia: pasillo → puerta (`POSE_PUERTA`) → lee el ArUco con la cámara → va al destino de ese ArUco (`DESTINOS`). En simulación, `aruco:=5`, `6` o `17` elige qué ArUco aparece en la puerta.

| ArUco | Destino en el mapa (x, y) |
|---|---|
| 5 | (3,5; 7,1) |
| 6 | (−2,0; 6,5) |
| 17 | (0,5; 14,1) |

## 6. Poses

Las poses están en el frame `map` y se escriben al principio de cada nodo como `(x, y, ángulo)`, en metros y radianes.

**Simulación.** El origen del mapa es el punto donde aparece el robot en Gazebo, así que `POSE_INICIAL = (0.0, 0.0, 0.0)`.

**JetBot.** El mundo F1L3 está a escala real, así que el JetBot usa el mismo mapa (`maps/f1l3.yaml`) y los mismos destinos que la simulación. La pose inicial es un punto del pasillo elegido por nosotros y marcado en el suelo: `POSE_INICIAL = (2.36, 0.21, -0.03)`. Se midió colocando el robot en la marca, ajustándolo en RViz con **2D Pose Estimate** y leyendo `/amcl_pose`. El robot siempre tiene que salir de esa marca y mirando hacia el mismo lado.

## 7. JetBot en el laboratorio

1. **En el robot** (`ssh jetbot@IP_DEL_ROBOT`), con su `ROS_DOMAIN_ID` (el nuestro es 199): `ros2 launch jetbot_pro_ros2 jetbot.py`. La cámara arranca con ese mismo launch (bloque `gscam_node` activado) y publica en `/camera/image_raw`.
2. **En el PC**, en cada terminal:

   ```bash
   export ROS_DOMAIN_ID=199
   unset ROS_AUTOMATIC_DISCOVERY_RANGE
   source /opt/ros/jazzy/setup.bash
   # Desde la raíz de este workspace:
   source install/setup.bash
   ```

3. Para hacer el mapa a mano: `python3 wasd.py`.

Cambios en `config/nav2_jetbot.yaml` respecto a los parámetros del TurtleBot3 Burger:

- `enable_stamped_cmd_vel: false`: el JetBot recibe `Twist`, no `TwistStamped`.
- `robot_base_frame: base_footprint`: es el frame base del JetBot.
- Monitor de colisiones con `source_timeout: 5.0` y `base_shift_correction: false`: el láser llega por wifi con más de 0,2 s de retraso y, con los valores originales, el monitor paraba el robot.

## 8. Detección de ArUco y versión de OpenCV

Ubuntu 24.04 trae OpenCV 4.6, que no tiene `ArucoDetector`. Los nodos usan `ArucoDetector` si existe (OpenCV 4.7 o posterior) y, si no, `cv2.aruco.detectMarkers` con `adaptiveThreshConstant = 20`. Sin ese ajuste, OpenCV 4.6 no detecta los ArUco de Gazebo, porque el borde blanco del marcador se ve gris.

## Documentación de sprints anteriores

- [Sprint 1 — Turtlesim y dibujo del 7](README_SPRINT1.md).

La documentación principal de esta entrega corresponde al Sprint 3.
