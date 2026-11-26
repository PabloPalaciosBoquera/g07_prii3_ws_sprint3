from glob import glob

from setuptools import setup

package_name = 'g07_prii3_nav_jetbot'

setup(
    name=package_name,
    version='0.3.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*')),
        ('share/' + package_name + '/maps', glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Grupo 07',
    maintainer_email='g07@upv.es',
    description='Sprint 3: ArUco con cámara cenital y navegación del JetBot real en el F1L3',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'aruco_cenital = g07_prii3_nav_jetbot.aruco_cenital:main',
            'predefined_navigation = g07_prii3_nav_jetbot.predefined_navigation:main',
            'autonomous_navigation = g07_prii3_nav_jetbot.autonomous_navigation:main',
        ],
    },
)
