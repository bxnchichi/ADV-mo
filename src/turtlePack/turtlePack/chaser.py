"""Lab 5 - Part 3: the chaser - pursue a moving target (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

Your go-to-goal controller, third time - but now the goal MOVES. The
chaser (turtle1) subscribes to its own pose AND the runner's pose, and
drives toward wherever the runner is right now. It also publishes your
OWN message type, my_interfaces/msg/ChaseStatus, so anyone can watch
the hunt:

    ros2 topic echo /chase_status

Complete TODOs 1-3. Gains are parameters - tune them mid-chase:

    ros2 param set /chaser k_lin 2.5

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/chaser.py
Entry point:       'chaser = my_first_pkg.chaser:main'
Needs:             <depend>my_interfaces</depend> in package.xml
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from my_interfaces.msg import ChaseStatus   # <- YOUR message type!

GOAL_TOL_DEFAULT = 0.5


def normalize_angle(a):
    while a > math.pi:
        a -= 2.0 * math.pi
    while a <= -math.pi:
        a += 2.0 * math.pi
    return a


class Chaser(Node):

    def __init__(self):
        super().__init__('chaser')

        # TODO 1: declare the parameters:
        #   'k_lin' -> 1.8, 'k_ang' -> 8.0, 'catch_dist' -> 0.5

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.status_pub = self.create_publisher(ChaseStatus, '/chase_status', 10)

        self.sub_me = self.create_subscription(
            Pose, '/turtle1/pose', self.my_pose_cb, 10)
        self.sub_target = self.create_subscription(
            Pose, '/runner/pose', self.target_pose_cb, 10)

        self.me = None
        self.target = None
        self.caught = False
        self.timer = self.create_timer(0.05, self.control_loop)

    def my_pose_cb(self, msg):
        self.me = msg

    def target_pose_cb(self, msg):
        self.target = msg

    def control_loop(self):
        # Two poses needed before we can chase anything.
        if self.me is None or self.target is None:
            return

        # TODO 2: read the current parameter values (inside the loop,
        #   like in tunable_writer): k_lin, k_ang, catch_dist.
        k_lin = 1.8         # <-- replace
        k_ang = 8.0         # <-- replace
        catch_dist = 0.5    # <-- replace

        dx = self.target.x - self.me.x
        dy = self.target.y - self.me.y
        dist = math.hypot(dx, dy)

        if dist < catch_dist:
            self.caught = True

        msg = Twist()
        if not self.caught:
            heading_error = normalize_angle(
                math.atan2(dy, dx) - self.me.theta)
            msg.angular.z = k_ang * heading_error
            msg.linear.x = k_lin * dist if abs(heading_error) < 0.5 else 0.0
        self.pub.publish(msg)   # zero Twist once caught -> chaser stops

        # TODO 3: fill and publish the ChaseStatus message.
        #   status = ChaseStatus()
        #   status.distance = ... (float(dist))
        #   status.caught   = ...
        #   self.status_pub.publish(status)

        if self.caught:
            self.get_logger().info('GOTCHA! Runner caught.', once=True)


def main(args=None):
    rclpy.init(args=args)
    node = Chaser()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


# CLASS CONTEST: everyone starts with the same runner. Tune k_lin /
# k_ang for the fastest catch - but too aggressive and the chaser
# orbits the runner instead of catching it. Report your best time.
#
# THINK ABOUT IT: the chaser aims at where the runner IS. A smarter
# chaser aims where the runner WILL BE. What extra information from
# Pose would you use? (Hint: linear_velocity, theta.)
