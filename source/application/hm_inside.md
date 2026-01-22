# Introduction

This commercial release of **HM Inside** makes the commercial deployment of pure-vision SLAM/VIO more feasible. We will also work with partners to support more SoC platforms. The combination of sensors and compute on the robot edge will push many medium/low-speed robot forms (wheeled, legged, UAVs) from 2D to 3D, and from narrow indoor environments to larger spaces.

HM Inside includes four major modules:

![](image/image_hm_inside_maindamster.png)

- `HM Localization`: estimates the current camera pose using images + IMU, i.e. VIO (Visual-Inertial Odometry).
- `HM Planner`:
  - `Point-to-point navigation`: given a goal B, automatically generates a path from start A to goal B and publishes velocity control commands.
  - `Coverage navigation`: given a closed region, automatically generates a full-coverage path in the region and publishes velocity control commands.
- `HM Mapping`: builds a prior map from many photos, which can help HM Localization improve accuracy and stability.
- `HM Perception`:
  - `Stereo depth`: produces a depth map (per-pixel distance), useful for navigation/obstacle avoidance.
  - `Semantic segmentation`: produces per-pixel semantic labels (object categories).

![](image/image_hm_preception.png)
<center style="font-size:14px;color:#C0C0C0;">Top: stereo disparity and colored point cloud; Bottom: semantic segmentation results (left: original, right: grass segmented).</center>

## Scope

Currently, the working scope and boundary of Robobaton + HMInside are:

1) 3D autonomous navigation/localization/perception for various robots in most indoor/outdoor scenes up to ~500 m².

2) HM Localization + combined navigation, together with HM Perception, to support medium/low-speed free exploration.

Not supported:

1) Scenarios with extremely poor visual features/lighting (e.g., snowfields, tunnels), very strict industrial accuracy requirements, or high-altitude flight (e.g., above 30m).

2) Current SFM reconstruction may fail in low-texture areas or white-wall corridors.

3) Relocalization accuracy may decrease in flat/open scenes with few nearby features. The system can still rely on GNSS/RTK and visual localization.

4) Relocalization is not yet coupled with GNSS/RTK information. Adaptation is planned.

> Note: HM Inside can generate significant heat. For long-duration operation, please ensure adequate cooling or wait for a future cooling module release.

