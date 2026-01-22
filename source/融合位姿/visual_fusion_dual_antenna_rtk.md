# Visual + Dual-Antenna RTK Fusion

<font color='#FF0000'>Note: this feature requires version V2510xx or later.</font>

Dual-antenna RTK provides positioning from two antennas, which means it can provide both position and heading.

Viobot2 runs in VIO mode by default. When dual-antenna RTK data is not provided, the fused pose output is the VIO pose. After dual-antenna RTK data is provided and successfully initialized, the fused pose output becomes the vision+RTK fused pose, which is accurate like RTK and can continue to output even in weak-signal or no-signal conditions.

High-level steps:

0. Hardware preparation
1. Build/install dependencies (same as single-antenna RTK)
2. Build RTK driver (same as single-antenna RTK)
3. Connect RTK via serial
4. Calibrate RTK-to-left-camera extrinsics
5. Enable RTK fusion

## 1. Hardware Preparation

Currently, the only dual-antenna RTK supported by Viobot2 is **UM982** (WitMotion/Weite Intelligence).

You need to enable output:

- `$GGA` 10Hz
- `$RMC` 1Hz
- `#AGRICA` 10Hz

Configure output using the following commands (example uses COM1):

```
1. Configure serial baud rate (output via com1)
Config com1 460800
2. Set rover mode
MODE ROVER
3. Enable GGA/RMC output (default is no output after power-on)
GPGGA COM1 0.1
GPRMC COM1 1
4. Enable heading fixed solution
GPTHS 1
AGRICA COM1 0.1
5. Enable PPS
CONFIG PPS ENABLE GPS POSITIVE 500000 1000 0 0
6. Save permanently
SAVECONFIG
```

UM982 module:

![](image/um982-image.png)
<center style="font-size:14px;color:#C0C0C0;">UM982 module</center>

The data flow is basically the same as the single-antenna version. The only difference is that the topic message includes an additional `AGRICA` sentence:

![](./image/image_rtk_arrow_pic.png)

## 2. Driver & Extrinsic Calibration

In Viobot-UI, enable RTK and select the **dual-antenna** version, reboot the device, then start the RTK driver:

```bash
roslaunch hm_rtk hm_rtk.launch
```

Make sure you can see both `/rtk_nmea` and `/baton/rtk_sixdof` outputs.

This uses the open-source `HM_RTK_driver`. Hardware connection and general usage are the same as the single-antenna RTK method; the main difference is the calibration part.

### 2.1 Verify Fixed Solution

Check `/baton/rtk_sixdof` and determine fixed solution based on the comments below:

```shell
---
header:
  stamp:
    sec: 1757985729
    nanosec: 401312000
  frame_id: rtk
child_frame_id: ''
pose:
  pose:
    position:
      x: -2345251.8804
      y: 5394243.9843
      z: 2458010.9024
    orientation:
      x: 0.05099666757356264
      y: -0.00417499227936327
      z: -0.9953600365410679
      w: -0.08148807883870496
  covariance:
  - 0.00020449000000000002
  - 4.0e-08     # position fixed status: non-4 means not fixed (encoded as state * e-8 on an off-diagonal element)
  - 4.0e-08     # heading fixed status: non-4 means not fixed
  - 0.0
  - 3.4000000000000003e-07
  - 0.0
  - 0.0
  - 0.00052441
```

### 2.2 Calibrate RTK-to-Left-Camera Extrinsics

After confirming data is correct, open `hm_rtk.launch` and set the initial Y value and initial calibration values:

![rtk_cali_Y](image/rtk_cali_Y.png)

`calib_rtk_slam.launch`:

```xml
<launch>
    <node name="rtk_slam_calibrator" pkg="hm_rtk" type="calib_rtk_slam_node" output="screen">
        <param name="ex_rtk_slam_x" value="0.03"/>   <!-- frame: left camera as origin, XYZ-right/down/up, i.e. T_camL<-RTK -->
        <param name="ex_rtk_slam_y" value="-0.01"/>  <!-- required; height direction is degenerate and not optimized -->
        <param name="ex_rtk_slam_z" value="-0.24"/>
        <param name="ex_rtk_slam_yaw" value="30.0"/> <!-- unit: deg. yaw from SLAM frame to RTK frame. CCW positive, CW negative -->
        <param name="package_path" value="$(find hm_rtk)"/>
    </node>
</launch>
```

![](image/2025-10-28-15-32-39-image.png)

Restart the RTK driver:

```bash
roslaunch hm_rtk hm_rtk.launch
```

Start stereo3, then run the calibration launch:

```bash
roslaunch hm_rtk calib_rtk_slam.launch
```

After both stereo3 and calibration are running, move the Viobot2 + RTK antenna assembly quickly in random directions. Avoid standing still or moving in a straight line. A figure-8 motion is recommended. The algorithm uses the latest 10 seconds of data for calibration. After calibration finishes, press `Ctrl+C` to stop; the calibration results will be printed in the terminal.

![rtk_result](image/rtk_result.png)

## 3. RTK Fusion

Write the calibration results back into `HM_RTK.launch`. For ROS2, edit the corresponding parameters in `install/hm_rtk/share/hm_rtk/launch/hm_rtk_ros2.launch.py`.

```xml
<arg name="ex_rtk_slam_x" default="-0.026357"/>
<arg name="ex_rtk_slam_y" default="-0.05"/>
<arg name="ex_rtk_slam_z" default="-0.283098"/>
```

Restart the RTK driver, start stereo3, and move the device. After RTK reaches fixed solution, you will get fused results.

RTK-related topics:

```bash
/baton/stereo3/fusion_odom  # fused odometry in SLAM local frame
/baton/stereo3/fusion_path  # fused path in SLAM local frame
/baton/stereo3/rtk_path     # RTK path in SLAM local frame
```

> Note: currently, you can check whether fusion is active by verifying that `/baton/stereo3/rtk_path` is published and comparing whether `/baton/stereo3/fusion_odom` differs from `/baton/stereo3/odometry`.

## 4. About Time Synchronization

Current PPS time sync options:

1. With GNSS antenna connected and RTK mode enabled, the device can use PPS time synchronization via the onboard GNSS module.
2. If you modify Viobot hardware, you may need to solder out PPS and GND wires.

Both methods synchronize system time, and topic timestamps are based on the synchronized time.

## 5. Accuracy Test Report

| Path length | ATE RMSE |
| --- | --- |
| 1353.41 m | 0.0325 |

![alt text](image/image_ape_fusion_rtk.png)

