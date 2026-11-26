#!/bin/bash
# Lanza las demos del Sprint 3 en simulación
pkill -9 -f "gz sim"; pkill -9 -f rviz2; pkill -9 -f component_container
export ROS_DOMAIN_ID=77
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
cd ~/g07_prii3_ws
source install/setup.bash
case "$1" in
  3.2) ros2 launch g07_prii3_nav_turtlebot slam.launch.py ;;
  3.3) ros2 launch g07_prii3_nav_turtlebot predefined_navigation.launch.py ;;
  3.4) ros2 launch g07_prii3_nav_turtlebot autonomous_navigation.launch.py aruco:=${2:-17} ;;
  *) echo "Uso: demo 3.2 | demo 3.3 | demo 3.4 [5|6|17]" ;;
esac
