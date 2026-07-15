# Cartesian Controllers for Dual Universal Robots

This repository provides launch files, controller configurations, and robot
descriptions for running Cartesian controllers with a dual Universal Robots
manipulator setup.

The implementation in the `ros2-dual` branch is based on the `ros2` branch of
[`stefanscherzinger/cartesian_controllers_universal_robots`](https://github.com/stefanscherzinger/cartesian_controllers_universal_robots).

The original repository provides Cartesian controller configurations for a
single Universal Robots manipulator. This branch extends and modifies that
configuration for a dual-manipulator system.

The two manipulators are referred to as:

```text
alice
bob
```

## Requirements

This package requires a ROS 2 workspace containing the dependencies used by
the original upstream project, including:

- Universal Robots ROS 2 Driver
- `ros2_control`
- Cartesian controllers
- Xacro
- RViz 2

The exact package dependencies are listed in `package.xml`.

From the workspace root, install available ROS dependencies with:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

## Cloning

Clone the dual-manipulator branch into the `src` directory of a ROS 2
workspace:

```bash
cd ~/ros2_ws/src

git clone --branch ros2-dual \
  https://github.com/smartrobotsdesignlab/cartesian_controllers_universal_robots.git
```

## Building

Build and source the workspace:

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## Running the fake dual-manipulator setup

Launch the dual-manipulator system using fake hardware:

```bash
ros2 launch cartesian_controllers_universal_robots \
  robot_fake_dual.launch.py
```

## Running the real dual-manipulator setup

Launch the real dual-manipulator configuration with:

```bash
ros2 launch cartesian_controllers_universal_robots \
  robot_real_dual.launch.py
```

## Controller and frame naming

The dual-manipulator configuration uses prefixes to distinguish the two
robots.

Typical frame names include:

```text
alice_base_link
alice_tool0

bob_base_link
bob_tool0
```

Controller names are also separated for Alice and Bob. Refer to the YAML files
under `config/` for the exact controller names.

When publishing Cartesian targets, trajectories, or controller commands, make
sure that the target controller and frame names correspond to the correct
manipulator.

## Calibration

Use separate calibration data for each physical robot.

For example:

```text
config/alice_calibration.yaml
config/bob_calibration.yaml
```

Calibration parameters must correspond to the actual robot on which they are
used. Do not reuse calibration data generated for a different robot.

## Attribution

This project is derived from:

> Stefan Scherzinger, `cartesian_controllers_universal_robots`, `ros2` branch.

The original source code is distributed under the BSD 3-Clause License.

The original copyright notices, license conditions, and disclaimer are
retained. Modifications for the dual-manipulator configuration are maintained
by the Smart Robots Design Lab.

## License

This repository is distributed under the BSD 3-Clause License.

See the [`LICENSE`](LICENSE) file for the complete license text.
