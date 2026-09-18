"""Lab 4 - Part 2: pen control with a service client (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

Your Lab 3 calligraphy had one flaw: the turtle draws a line BETWEEN
letters. The fix is the /turtle1/set_pen SERVICE. This file is your
Lab 3 waypoint controller, complete - your job is the service parts:
complete TODOs 1-3 so the pen lifts on "travel" segments.

Each waypoint now has a third value:  (x, y, pen_down)
  pen_down = True   draw while driving to this point
  pen_down = False  travel with the pen up (no line)

Remember:  ros2 run turtlesim turtlesim_node   first.

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/pen_writer.py
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

# ---------------------------------------------------------------------------
# Sample: "L I" - two letters with a pen-up travel move between them.
# HOMEWORK: replace with YOUR 3 initials (yes, the same ones - now with
# clean gaps between the letters).
# WAYPOINTS = [
#     (2.0, 9.0, False),   # travel to the start of "L" (pen up)
#     (2.0, 5.0, True),    # draw the vertical stroke
#     (4.0, 5.0, True),    # draw the horizontal stroke
#     (5.5, 9.0, False),   # travel to the start of "I" (pen up)
#     (5.5, 5.0, True),    # draw the "I"
# ]
# ---------------------------------------------------------------------------


start_x = 4.5
start_y = 2

WAYPOINTS = [
    # B
    (start_x, start_y, False),
    (start_x, start_y + 1, True),
    (start_x - 1.25, start_y + 1, True),
    (start_x - 0.25, start_y + 1, False),
    (start_x - 0.25, start_y + 2, True),
    (start_x - 1.25, start_y + 2, True),
    (start_x - 1.25, start_y, True),
    (start_x, start_y, True),

    # E
    (start_x + 0.5, start_y, False),
    (start_x + 0.5, start_y + 2, True),
    (start_x + 1.5, start_y + 2, True),
    (start_x + 0.5, start_y + 2, False),
    (start_x + 0.5, start_y + 1, False),
    (start_x + 1.5, start_y + 1, True),
    (start_x + 0.5, start_y + 1, False),
    (start_x + 0.5, start_y, False),
    (start_x + 1.5, start_y, True),

    # N
    (start_x + 2, start_y, False),
    (start_x + 2, start_y + 2, True),
    (start_x + 3, start_y, True),
    (start_x + 3, start_y + 2, True), 

]

K_LIN = 1.5
K_ANG = 6.0
GOAL_TOL = 0.15


def normalize_angle(a):
    while a > math.pi:
        a -= 2.0 * math.pi
    while a <= -math.pi:
        a += 2.0 * math.pi
    return a


class PenWriter(Node):

    def __init__(self):
        super().__init__('pen_writer')

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose',
                                            self.pose_callback, 10 )

        # TODO 1: create the service client.
        #   Signature: self.create_client(srv_type, service_name)
        #   Type: SetPen (imported above), name: '/turtle1/set_pen'
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen') # <-- replace this

        # Good practice: don't start until the service exists.
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for /turtle1/set_pen ...')

        self.pose = None
        self.target_idx = 0
        self.pen_is_down = None   # unknown until we set it once

        self.timer = self.create_timer(0.05, self.control_loop)
        self.start_time = self.get_clock().now()


    def pose_callback(self, msg):
        self.pose = msg

    def set_pen(self, down):
        """Ask turtlesim to lower (down=True) or lift (down=False) the pen."""
        req = SetPen.Request()
        req.r, req.g, req.b = 255, 255, 255
        req.width = 3
        # TODO 2: fill in req.off and send the request.
        #   req.off = 1 lifts the pen, 0 lowers it  (note: int, not bool)
        #   Send it with:  self.pen_client.call_async(req)
        #   (call_async returns immediately - we don't block the control loop
        #    waiting for the answer; the pen changes within a few ms.)
        req.off = 0 if down else 1
        self.pen_client.call_async(req)

        self.pen_is_down = down
        self.get_logger().info(f'pen {"down" if down else "up"}')

    # def teleport(self, x, y):
    #     self.get_logger().info

    def control_loop(self):
        if self.pose is None:
            return
        if self.target_idx >= len(WAYPOINTS):
            self.pub.publish(Twist())
            return

        gx, gy, pen_down = WAYPOINTS[self.target_idx]

        # TODO 3: if this segment's pen state differs from the current one,
        #   call self.set_pen(pen_down) BEFORE driving on.
        #   (Compare with self.pen_is_down.)
        self.set_pen(pen_down)

        dx, dy = gx - self.pose.x, gy - self.pose.y
        dist = math.sqrt(dx * dx + dy * dy)
        heading_error = normalize_angle(math.atan2(dy, dx) - self.pose.theta)

        msg = Twist()
        msg.angular.z = K_ANG * heading_error
        msg.linear.x = K_LIN * dist if abs(heading_error) < 0.5 else 0.0
        self.pub.publish(msg)

        if dist < GOAL_TOL:
            t = self.get_clock().now() - self.start_time
            self.get_logger().info(f'reached waypoint {self.target_idx} at {t}')
            self.target_idx += 1


def main(args=None):
    rclpy.init(args=args)
    node = PenWriter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


# BONUS: for long travel moves, driving with the pen up is slow. Teleport
# instead: the /turtle1/teleport_absolute service (turtlesim/srv/
# TeleportAbsolute) jumps straight to (x, y, theta). Lift the pen, teleport,
# lower the pen. Careful: teleporting with the pen DOWN draws a line!
