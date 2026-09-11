"""Lab 3 - Part 4: a new message type - geometry_msgs/Twist (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

This node is talker.py with a different message type and topic - that is
the whole point. Complete the three TODOs and the turtle drives in a
circle, open-loop (publish and hope: no feedback yet - that comes next).

Remember to start the simulator first:  ros2 run turtlesim turtlesim_node

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/turtle_circle.py
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist   # <-- new message type (was: String)


class TurtleCircle(Node):

    def __init__(self):
        super().__init__('turtle_circle')

        # TODO 1: create a publisher of Twist messages.
        #   Which topic does the turtle listen on? You found it in Lab 2
        #   with 'ros2 topic list -t'. Queue size 10.
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)  # <-- replace this

        # Publish 10 times per second - a steady stream, like teleop does.
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        # TODO 2: set a forward speed and a turning speed.
        #   msg.linear.x  = forward speed (m/s)
        #   msg.angular.z = turning speed (rad/s)
        #   Use the circle values you found in Lab 2, Checkpoint 4.
        msg.linear.x = 2.0  # forward speed
        msg.angular.z = 6.28  # turning speed


        # TODO 3: publish the message.
        self.publisher_.publish(msg)
        pass  # delete this line when you are done


def main(args=None):
    rclpy.init(args=args)
    node = TurtleCircle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


# B ONUS (if you finish early): make the turtle drive a figure-eight.
# Hint: count timer ticks (self.tick += 1) and flip the sign of
# msg.angular.z every few seconds, e.g. when (self.tick // 50) % 2 changes.
 