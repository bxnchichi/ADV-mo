"""Lab 3 - Part 3: your first subscriber node (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

Complete the three TODOs. Use talker.py as your reference - a subscriber
looks almost the same, but it reacts to messages instead of creating them.

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/listener.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):

    def __init__(self):
        # TODO 1: call the parent constructor and name this node 'listener'.

        # TODO 2: create a subscription to the 'chatter' topic.
        #   Signature: self.create_subscription(msg_type, topic_name, callback, queue_size)
        #   Use String, 'chatter', self.chatter_callback, and 10.
        #   Store the result in self.subscription.
        pass  # delete this line when you are done

    def chatter_callback(self, msg):
        # TODO 3: log the received text using self.get_logger().info(...)
        #   The text of the message is in msg.data
        pass  # delete this line when you are done


def main(args=None):
    rclpy.init(args=args)
    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
