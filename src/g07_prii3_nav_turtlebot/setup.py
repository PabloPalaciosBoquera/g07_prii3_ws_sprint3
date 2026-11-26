import os
from glob import glob

from setuptools import setup

package_name = 'g07_prii3_nav_turtlebot'

# Copia los modelos de los ArUco conservando sus carpetas
modelos = []
for carpeta in glob('models/**/', recursive=True):
    ficheros = [f for f in glob(carpeta + '*') if os.path.isfile(f)]
    if ficheros:
        modelos.append((os.path.join('share', package_name, carpeta), ficheros))

setup(
    name=package_name,
    version='0.3.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/worlds', glob('worlds/*')),
        ('share/' + package_name + '/maps', glob('maps/*')),
    ] + modelos,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grupo 07',
    maintainer_email='g07@upv.es',
    description='Sprint 3: navegación del TurtleBot3 simulado en el F1L3',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'predefined_navigation = g07_prii3_nav_turtlebot.predefined_navigation:main',
            'autonomous_navigation = g07_prii3_nav_turtlebot.autonomous_navigation:main',
        ],
    },
)
