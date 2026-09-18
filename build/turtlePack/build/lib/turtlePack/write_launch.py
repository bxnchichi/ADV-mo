"""Lab 4 - Part 5: one command to rule them all (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

You have been juggling 3+ terminals for two weeks. A LAUNCH FILE starts
a whole set of nodes with one command:

    ros2 launch my_first_pkg write_launch.py

SETUP (this file does NOT go with your Python nodes):
  1. Put this file in:   ~/ros2_ws/src/my_first_pkg/launch/write_launch.py
     (create the 'launch' folder next to setup.py)
  2. Tell setup.py to install it - add the launch folder to data_files:

        import os
        from glob import glob
        ...
        data_files=[
            ...existing entries...,
            (os.path.join('share', package_name, 'launch'),
             glob(os.path.join('launch', '*launch.py'))),
        ],

  3. colcon build, source, launch.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # The simulator.
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
        ),

        # TODO 1: add a second Node entry that starts YOUR pen_writer
        #   (package 'my_first_pkg', executable 'pen_writer').

        # TODO 2 (after TODO 1 works): can you also start your
        #   adder_server here? How many nodes does 'ros2 node list'
        #   show after one launch command?
    ])
