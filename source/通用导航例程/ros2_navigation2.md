# ROS2 Navigation2 Demo

Demo code repo: (not provided in the original document)

> Note: this tutorial uses a wheeled robot as an example. Real applications usually require additional integration and development. Currently, mapping does not yet support building an occupancy grid map.

This project publishes the essential TF transforms required by Nav2.

First run the Viobot odometry algorithm. This node reads the algorithm pose output and publishes TF transforms `map -> odom -> base_link` based on the extrinsics between the device and the robot.

The map under the `map` directory is an empty map, which can be used for Nav2 when no prior map is available.

## Usage

### 1) Build

```bash
colcon build
```

### 2) Run the node

```bash
source install/setup.bash
ros2 run TF_Pub TF_node
```

### 3) Launch Nav2

```bash
ros2 launch nav2_bringup bringup_launch.py  map:=/home/ubuntu22/tf_ws/src/map.yaml
```

Update the map path based on your actual path.

### 4) Start navigation

```bash
rviz2
```

Set a Nav2 Goal in the map. You should see a planned trajectory.

### 5) Run your base controller

Run your own base controller node to execute `/cmd_vel`.

## Notes

The code requires extrinsics between the device and the robot, which must be updated according to your setup.

Based on testing, using values from mechanical drawings may also work.

