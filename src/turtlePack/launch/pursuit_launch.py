"""Lab 5 - Part 3: the pursuit, from one command (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

Starts: the simulator, and your tunable_writer REMAPPED onto the spawned
runner turtle (looping forever). Note what the remapping buys you: the
SAME writer node drives a completely different turtle - zero code edits.

Before launching, spawn the runner once (services, Lab 4!):

  ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, name: 'runner'}"

Then:

  ros2 launch my_first_pkg pursuit_launch.py

Goes in:  ~/ros2_ws/src/my_first_pkg/launch/pursuit_launch.py
(data_files for launch/ is already set up from Lab 4.)
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        Node(
            package='turtlesim',
            executable='turtlesim_node',
        ),

        # The RUNNER: your writer, remapped from turtle1 to the spawned
        # 'runner' turtle, looping forever with lazy gains.
        Node(
            package='turtlePack',
            executable='tunable_writer',
            name='runner_driver',
            parameters=[{'loop': True, 'k_lin': 1.2, 'k_ang': 6.0}],
            remappings=[
                ('/turtle1/cmd_vel', '/runner/cmd_vel'),
                ('/turtle1/pose',    '/runner/pose'),
                ('/turtle1/set_pen', '/runner/set_pen'),  # services remap too!
            ],
        ),

        # TODO: add YOUR chaser node here (package my_first_pkg,
        #   executable 'chaser'). Give it name='chaser'.
        #   It hunts turtle1's own topics, so it needs no remapping.

    ])
