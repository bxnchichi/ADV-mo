from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turtlePack'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
        glob(os.path.join('launch', '*launch.py'))),        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bxnchxchi',
    maintainer_email='benchi2507@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = turtlePack.talker:main',
            'listener = turtlePack.listener:main',
            'turtle_circle = turtlePack.turtle_circle:main',
            'turtle_writer = turtlePack.turtle_writer:main',
            'pen_writer = turtlePack.pen_writer:main',
            'pen_writer_teleport = turtlePack.pen_writer_teleport:main',
            'adder_server = turtlePack.adder_server:main', 
            'tunable_writer = turtlePack.tunable_writer:main',
            'chaser = turtlePack.chaser:main',
        ],
    },
)
