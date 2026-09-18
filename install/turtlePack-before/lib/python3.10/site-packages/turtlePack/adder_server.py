"""Lab 4 - Part 3: write your OWN service server (YOUR TURN).

2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

So far you have only CALLED services that turtlesim provides. Now you
provide one yourself. This node offers an /add_two_ints service using the
standard example_interfaces/srv/AddTwoInts type:

    request:  int64 a, int64 b     response: int64 sum

Complete TODOs 1-2, build, run it, and call it from a second terminal:

    ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts \
        "{a: 7, b: 35}"

NOTE: add  <depend>example_interfaces</depend>  to package.xml.

Put this file in:  ~/ros2_ws/src/my_first_pkg/my_first_pkg/adder_server.py
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

# command
# ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 7, b: 35}" 

class AdderServer(Node):

    def __init__(self):
        super().__init__('adder_server')

        # TODO 1: create the service.
        #   Signature: self.create_service(srv_type, service_name, callback)
        #   Type: AddTwoInts, name: 'add_two_ints', callback: self.handle_add
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.handle_add)  # <-- replace this

        self.get_logger().info('adder_server ready - waiting for requests')

    def handle_add(self, request, response):
        """Called once per incoming request. Fill the response and RETURN it -
        forgetting the return statement is the classic bug here."""
        # TODO 2: compute response.sum from request.a and request.b,
        #   log a line showing the request, and return the response.
        a = request.a 
        b = request.b
        response.sum = a+b
        self.get_logger().info(f"{a} + {b} = {response.sum}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AdderServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


# THINK ABOUT IT: while your server node spins, run 'ros2 service list' in
# another terminal. Besides /add_two_ints you will see six /adder_server/...
# services you never wrote - every node gets parameter services for free.
