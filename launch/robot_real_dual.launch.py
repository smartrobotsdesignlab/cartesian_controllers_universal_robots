# -----------------------------------------------------------------------------
# \file    robot.launch.py
#
# \author  Stefan Scherzinger <scherzin@fzi.de>
# \date    2023/05/30
#
# -----------------------------------------------------------------------------

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    this_pkg = FindPackageShare("cartesian_controllers_universal_robots")

    # Declare arguments
    arg_alice_ip = DeclareLaunchArgument(
        "alice_robot_ip", default_value="192.168.15.6", description="The robot's IP address"
    )

    arg_bob_ip = DeclareLaunchArgument(
        "bob_robot_ip", default_value="192.168.15.4", description="The robot's IP address"
    )
    ur_type = DeclareLaunchArgument(
        "ur_type",
        description="Type/series of used UR robot.",
        choices=["ur3", "ur3e", "ur5", "ur5e", "ur10", "ur10e", "ur16e"]
    )
    declared_args = [arg_alice_ip, arg_bob_ip, ur_type]

    # Robot description
    description_file = PathJoinSubstitution([this_pkg, "urdf", "setup_real_dual.urdf.xacro"])
    alice_ip = LaunchConfiguration("alice_robot_ip")
    tf_prefix = LaunchConfiguration("tf_prefix")
    robot_description_content = Command(
        [
            FindExecutable(name="xacro"),
            " ",
            description_file,
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    # Robot control
    robot_controllers = PathJoinSubstitution([this_pkg, "config", "controller_manager_real_dual.yaml"])
    control_node = Node(
        package="ur_robot_driver",
        executable="ur_ros2_control_node",
        output="screen",
        #prefix="screen -d -m gdb -command=/home/scherzin/.ros/my_debug_log --ex run --args",
        remappings=[
            ('alice_motion_control_handle/target_frame', 'alice_target_frame'),
            ('bob_motion_control_handle/target_frame', 'bob_target_frame'),
            ('alice_cartesian_compliance_controller/target_frame', 'alice_target_frame'),
            ('bob_cartesian_compliance_controller/target_frame', 'bob_target_frame'),
            ('alice_cartesian_force_controller/target_frame', 'alice_target_frame'),
            ('bob_cartesian_force_controller/target_frame', 'bob_target_frame'),
            ('alice_cartesian_force_controller/ft_sensor_wrench', 'alice_ft_sensor_wrench'),
            ('bob_cartesian_force_controller/ft_sensor_wrench', 'bob_ft_sensor_wrench'),
            ('alice_cartesian_compliance_controller/ft_sensor_wrench', 'alice_ft_sensor_wrench'),
            ('bob_cartesian_compliance_controller/ft_sensor_wrench', 'bob_ft_sensor_wrench'),
            ('alice_force_torque_sensor_broadcaster/wrench', 'alice_ft_sensor_wrench'),
            ('bob_force_torque_sensor_broadcaster/wrench', 'bob_ft_sensor_wrench'),
            ],
        parameters=[robot_description, robot_controllers],
    )

    def controller_spawner(name, *args):
        return Node(
            package="controller_manager",
            executable="spawner",
            output="screen",
            arguments=[name] + [a for a in args],
        )

    # Active controllers
    active_list = [
            "joint_state_broadcaster",
            "alice_force_torque_sensor_broadcaster",
            "bob_force_torque_sensor_broadcaster",
            # "alice_scaled_joint_trajectory_controller",
            # "bob_scaled_joint_trajectory_controller",
            "alice_cartesian_motion_controller",
            "bob_cartesian_motion_controller",
            # "alice_motion_control_handle",
            # "bob_motion_control_handle",
            "bob_hand_controller",
            "alice_hand_controller"
            ]
    active_spawners = [controller_spawner(controller) for controller in active_list]

    # Inactive controllers
    inactive_list = [
            "alice_cartesian_compliance_controller",
            "bob_cartesian_compliance_controller",
            "alice_cartesian_force_controller",
            "bob_cartesian_force_controller",
            # "alice_cartesian_motion_controller",
            # "bob_cartesian_motion_controller"
            ]
    inactive_spawners = [controller_spawner(controller, "--inactive") for controller in inactive_list]


    # TF tree
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
        
    )

    # Visualization
    rviz_config = PathJoinSubstitution([this_pkg, "etc", "setup.rviz"])
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config]
    )

    # Nodes to start
    nodes = [rviz, control_node, robot_state_publisher] + active_spawners + inactive_spawners

    return LaunchDescription(declared_args + nodes)