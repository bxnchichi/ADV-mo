"""Lab 5 - Part 1: parameters - stop hard-coding your gains (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

This is your pen-aware waypoint writer from Lab 4, with the magic numbers
promoted to PARAMETERS. Complete TODOs 1-2, then tune the running node
from another terminal - no rebuild:

    ros2 param list /tunable_writer
    ros2 param set  /tunable_writer k_ang 20.0     # mid-drawing!
    ros2 param set  /tunable_writer loop true      # drive forever

The 'loop' parameter matters for Part 3: a looping writer is the RUNNER
that your chaser will hunt (launch file remaps it onto the spawned
turtle).

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/tunable_writer.py
Entry point:       'tunable_writer = my_first_pkg.tunable_writer:main'
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

# Waypoints: (x, y, pen_down). Swap in your own initials if you like.
WAYPOINTS = [
    (2.0, 9.0, False),
    (2.0, 5.0, True),
    (4.0, 5.0, True),
    (5.5, 9.0, False),
    (5.5, 5.0, True),
    (8.0, 8.0, False),
    (8.0, 5.0, True),
]

GOAL_TOL = 0.15


def normalize_angle(a):
    while a > math.pi:
        a -= 2.0 * math.pi
    while a <= -math.pi:
        a += 2.0 * math.pi
    return a


class TunableWriter(Node):

    def __init__(self):
        super().__init__('tunable_writer')

        # TODO 1: declare the parameters with their default values.
        #   Signature: self.declare_parameter(name, default)
        #   Declare: 'k_lin' -> 1.5, 'k_ang' -> 6.0, 'loop' -> False
        #   (An undeclared parameter cannot be set or read - ROS 2 is
        #    strict about this, unlike ROS 1.)

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose',
                                            self.pose_callback, 10)

        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for set_pen ...')

        self.pose = None
        self.target_idx = 0
        self.pen_is_down = None
        self.timer = self.create_timer(0.05, self.control_loop)

    def pose_callback(self, msg):
        self.pose = msg

    def set_pen(self, down):
        req = SetPen.Request()
        req.r = req.g = req.b = 255
        req.width = 3
        req.off = 0 if down else 1
        self.pen_client.call_async(req)
        self.pen_is_down = down

    def control_loop(self):
        if self.pose is None:
            return

        # TODO 2: read the CURRENT parameter values - inside the loop, so
        # a 'ros2 param set' takes effect immediately.
        #   value = self.get_parameter('name').value
        k_lin = 1.5    # <-- replace with the parameter value
        k_ang = 6.0    # <-- replace with the parameter value
        loop = False   # <-- replace with the parameter value

        if self.target_idx >= len(WAYPOINTS):
            if loop:
                self.target_idx = 0     # start over - endless runner
            else:
                self.pub.publish(Twist())
                return

        gx, gy, pen_down = WAYPOINTS[self.target_idx]
        if pen_down != self.pen_is_down:
            self.set_pen(pen_down)

        dx, dy = gx - self.pose.x, gy - self.pose.y
        dist = math.hypot(dx, dy)
        heading_error = normalize_angle(math.atan2(dy, dx) - self.pose.theta)

        msg = Twist()
        msg.angular.z = k_ang * heading_error
        msg.linear.x = k_lin * dist if abs(heading_error) < 0.5 else 0.0
        self.pub.publish(msg)

        if dist < GOAL_TOL:
            self.target_idx += 1


def main(args=None):
    rclpy.init(args=args)
    node = TunableWriter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


# EXPERIMENT (Part 1): while it draws, try
#   ros2 param set /tunable_writer k_ang 25.0     -> wobbly handwriting
#   ros2 param set /tunable_writer k_ang 2.0      -> lazy, rounded corners
# Watch the same waypoints produce different handwriting. THAT is why
# gains are configuration, not code.
