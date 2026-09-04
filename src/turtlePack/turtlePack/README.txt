Lab 3 starter files — ROS 2 Humble (Python)
2103581 Robot Operating System and Applications / 2147427 Advanced Mobile Robots

WHAT'S HERE
  talker.py         complete publisher (we walk through it in class)
  listener.py       subscriber with 3 TODOs (you complete it)
  turtle_circle.py  same pattern, new message type (Twist) - 3 TODOs,
                    drives the turtle in an open-loop circle
  turtle_writer.py  closed-loop waypoint controller with 3 TODOs in class
                    + TODO 4 as homework: make the turtle write YOUR
                    3 initials (e.g. Surat Kwanmuang -> SKM)

WHERE THE FILES GO
  ~/ros2_ws/src/my_first_pkg/my_first_pkg/     <- next to __init__.py

SETUP (once) — after creating the package in the lab:
  cd ~/ros2_ws/src
  ros2 pkg create --build-type ament_python my_first_pkg --dependencies rclpy std_msgs geometry_msgs turtlesim
  # copy the three .py files into my_first_pkg/my_first_pkg/

REGISTER THE EXECUTABLES
  Edit ~/ros2_ws/src/my_first_pkg/setup.py and make entry_points look like this:

    entry_points={
        'console_scripts': [
            'talker = my_first_pkg.talker:main',
            'listener = my_first_pkg.listener:main',
            'turtle_circle = my_first_pkg.turtle_circle:main',
            'turtle_writer = my_first_pkg.turtle_writer:main',
        ],
    },

BUILD AND RUN (every time you change code)
  cd ~/ros2_ws
  colcon build
  source install/setup.bash        # in EVERY terminal you use
  ros2 run my_first_pkg talker

GOLDEN RULE
  If ros2 says "package not found" or "no executable found":
  did you build? did you source install/setup.bash in THIS terminal?
