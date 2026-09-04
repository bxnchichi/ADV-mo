"""Lab 3 - Part 4: turtle calligraphy with a feedback loop (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

Goal: a node that SUBSCRIBES to the turtle's pose and PUBLISHES velocity
commands to steer it through a list of waypoints - your first closed-loop
controller. In class you make it trace the sample letter "L"; for homework
you replace the waypoints with the strokes of YOUR OWN 3 initials
(e.g. Surat Kwanmuang -> SKM).

Remember to start the simulator first:  ros2 run turtlesim turtlesim_node

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/turtle_writer.py
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

# ---------------------------------------------------------------------------
# Waypoints, as (x, y) in turtlesim's world (0..11 on both axes).
# The turtle visits them in order, drawing as it goes.
#
# Sample: the letter "L" (three corner points):
WAYPOINTS = [
    (2.0, 9.0),   # top of the vertical stroke
    (2.0, 5.0),   # bottom corner
    (4.0, 5.0),   # end of the horizontal stroke
]
# HOMEWORK (TODO 4): replace this list with the strokes of your own
# 3 initials. Sketch each letter on graph paper first and keep letters
# about 2 units wide with a gap between them.
# ---------------------------------------------------------------------------

# Controller gains and tolerances - tune these in Part 4!
K_LIN = 1.5      # forward speed gain
K_ANG = 6.0      # turning speed gain
GOAL_TOL = 0.15  # how close (in world units) counts as "reached"


def normalize_angle(a):
    """Wrap any angle into (-pi, pi]. ALWAYS run heading errors through
    this - otherwise an error of +350 degrees makes the turtle spin the
    long way around instead of turning -10 degrees."""
    while a > math.pi:
        a -= 2.0 * math.pi
    while a <= -math.pi:
        a += 2.0 * math.pi
    return a


class TurtleWriter(Node):

    def __init__(self):
        super().__init__('turtle_writer')

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # TODO 1: subscribe to the turtle's pose.
        #   Topic: '/turtle1/pose', message type: Pose (already imported),
        #   callback: self.pose_callback, queue size: 10.
        self.sub = None  # <-- replace this

        self.pose = None      # latest Pose message (None until one arrives)
        self.target_idx = 0   # which waypoint we are driving to

        # The control loop runs 20 times per second.
        self.timer = self.create_timer(0.05, self.control_loop)

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):
        # No pose received yet? Then we don't know where we are - do nothing.
        if self.pose is None:
            return

        # Finished all waypoints? Publish one zero-velocity command and stop.
        if self.target_idx >= len(WAYPOINTS):
            self.pub.publish(Twist())
            return

        gx, gy = WAYPOINTS[self.target_idx]

        # TODO 2: compute the error between us and the goal.
        #   dx, dy        : goal position minus our position
        #                   (our position: self.pose.x, self.pose.y)
        #   dist          : Euclidean distance, math.sqrt(dx**2 + dy**2)
        #   heading_error : normalize_angle(math.atan2(dy, dx) - self.pose.theta)
        dist = 0.0           # <-- replace this
        heading_error = 0.0  # <-- replace this

        # TODO 3: proportional control - turn toward the goal, drive when
        # roughly facing it.
        #   msg.angular.z = K_ANG * heading_error
        #   msg.linear.x  = K_LIN * dist   if abs(heading_error) < 0.5
        #                   else 0.0       (turn in place first)
        msg = Twist()
        # ... your two lines here ...
        self.pub.publish(msg)

        # Reached the waypoint? Move on to the next one.
        if dist < GOAL_TOL:
            self.get_logger().info(f'Reached waypoint {self.target_idx}: ({gx}, {gy})')
            self.target_idx += 1


def main(args=None):
    rclpy.init(args=args)
    node = TurtleWriter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


# BONUS (for the homework): the line the turtle draws BETWEEN two letters
# spoils the writing. Turtlesim has services to lift the pen and teleport:
#     /turtle1/set_pen            (turtlesim/srv/SetPen, off=1 lifts the pen)
#     /turtle1/teleport_absolute  (turtlesim/srv/TeleportAbsolute)
# Try them from the terminal with 'ros2 service call ...' while your node
# runs - or call them from Python after next week's class on services.
