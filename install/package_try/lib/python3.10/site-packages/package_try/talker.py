"""Lab 3 - Part 2: your first publisher node.

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

This file is COMPLETE - we will walk through it together in class.
Read every line and make sure you can explain what it does.

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/talker.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    """A node that publishes a String message on /chatter twice per second."""

    def __init__(self):
        # Every node needs a name - this is what 'ros2 node list' shows.
        super().__init__('talker')

        # Publisher: message type, topic name, queue size.
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # Timer: call self.timer_callback every 0.5 seconds.
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello from Python! count = {self.count}'
        self.publisher_.publish(msg)
        # get_logger() prints with a timestamp - always prefer it over print().
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)          # start ROS communication
    node = Talker()                # create our node
    try:
        rclpy.spin(node)           # keep it alive, run callbacks
    except KeyboardInterrupt:
        pass                       # Ctrl+C is the normal way to stop
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
