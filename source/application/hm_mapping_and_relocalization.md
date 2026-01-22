# HM Mapping & Relocalization (SFM)

This document demonstrates how to use Viobot2 to:

- Run **SFM reconstruction** (mapping)
- Use the built map for **global relocalization**

> - Robobaton + HM Inside currently supports 3D autonomous navigation/localization/perception for various robots in most indoor/outdoor scenes up to ~500 m².
> - HM Localization + combined navigation, together with HM Perception, enables medium/low-speed free exploration.

**Important notes:**

> - <font color='#FF0000'>For Viobot2 system versions **202511xx and later**, mapping requires the latest client UI. If your UI pages differ, update to the latest version from the official website before following this section.</font>
> - <font color='#FF0000'>Not supported: scenes with extremely poor visual features/lighting (e.g. snowfields, tunnels), very strict industrial accuracy requirements, or high-altitude flight above 30m.</font>
> - <font color='#FF0000'>SFM reconstruction may fail in low-texture areas or white-wall corridors.</font>
> - <font color='#FF0000'>Relocalization accuracy may decrease in flat/open scenes with few nearby features. The system can still rely on GNSS/RTK and visual localization.</font>

## Prerequisites

Before use, update Viobot2 firmware and Viobot-UI to the latest versions to avoid missing features. Official download page: [Hessian Matrix - Download Center](https://www.hessian-matrix.com/%e4%b8%8b%e8%bd%bd%e4%b8%ad%e5%bf%83/)

## High-level Steps

1. Configure Viobot2 in Viobot-UI.
2. Start **stereo3** and scan the environment.
3. Save the map.
4. Start mapping (SFM reconstruction).
5. Enable relocalization.
6. Check results.

Details below.

## Viobot Settings and Data Collection

Connect Viobot2 with Viobot-UI, click **Settings**, and go to the **Loop** tab. Mainly configure the following:

### 1) Configure map save path in UI

After connecting:

1. Open `Settings` and `Loop`.
2. Check `Enable loop/relocalization` to configure the relocalization file path. This is a path on Viobot2 used to store mapping-related files collected during stereo3 runtime.
3. Uncheck `Enable loop/relocalization`, then check `Record mapping info`.
4. Click **OK**, then close the tab.

### 2) Start stereo3 to record mapping info

Start stereo3. The algorithm will automatically store mapping-required files into the configured path. Move Viobot2 around the area you want to map (typically one loop), then stop stereo3. The files will be saved automatically.

![alt text](image/set_sfm_config_image.png)

> Note: if your UI differs, follow the section "UI mapping before v1031", or upgrade both Viobot2 software and UI to the latest versions.

After configuration, click **OK**, then start stereo3 and move the device for data collection. Avoid very fast viewpoint changes, otherwise the reconstruction quality may be poor.

### Alternative: without UI (edit config)

If you do not use the UI to collect data / run relocalization:

1. **Record data**: set `record_flag: true`, then start stereo3. The program will collect mapping data automatically. After stopping stereo3, `record_flag` will be set back to `false` automatically to avoid recording on the next run.
2. **Enable relocalization**: set `relocalization: true`. When stereo3 starts, it reads this config and enables relocalization.
3. **Mapping output path**: edit `/root/Baton/install/share/baton/config/sys.yaml`, set `pose_graph_save_path` and remember it; mapping results will be saved there.

```yaml
print_queue: false
use_imu: 2
gnss_select: 2
load_previous_pose_graph: false
add_keyframe_mode: 0
pose_graph_save_path: /home/user/pose_graph   # save pose_graph output here
gnss_T_imu:
  data:
    - 0
    - 0
    - 0
relocalization: false   # set true after mapping to enable relocalization
mask_path: /root/Baton/install/share/baton/config/s3_fisheye_mask.png # set stereo mask if view is occluded
only_sfm_data: true
record_flag: true    # set true to record mapping data, then start stereo3
zupt_acc_var: -1
zupt_gyr_var: -1
zupt_average_parallax: 0
```

After scanning the area, click **Stop** for stereo3 and wait a few seconds to ensure data is fully saved, then proceed to offline mapping.

## Offline Mapping (SFM Reconstruction)

After you have finished data collection and basic configuration, double-check the configs above. Then click **Start mapping** in the UI to see a progress bar. Mapping time increases with scene size.

After the progress finishes, you can find reconstruction results under the `HM_SFM` directory in the output path, and you can also use the UI **View map** to inspect results.

> Tips: you can also run mapping without the UI. SSH into Viobot2 and run the `mapping` node. Make sure the configured path and the saved BoW folder contain data:
>
> ```shell
> # ROS1:
> rosrun baton mapping
> ```
>
> ROS2 command is not available yet:
>
> <!--
> # ROS2:
> ros2 run baton mapping
> -->

![](image/image_mapping.png)

> Note: mapping requires high compute. It is normal for Viobot2 CPU usage to reach 100% during mapping. After mapping finishes, CPU usage will return to normal. Ensure stable power supply during this process.

> If the progress bar finishes instantly, check whether the BoW save path is correct and whether the BoW vocabulary/map files exist in that path. Normally mapping takes more than one minute.

Example directory structure after mapping (using `tree`):

```shell
root@PR-VIO: cd /home/my_relocation
root@PR-VIO:/home/my_relocation# tree
|-- xxx.jpg
|-- ...
`-- images  # folder
    |-- ...
`-- result  # folder
    |-- database.db
    `-- sparse
        `-- 0
            |-- cameras.bin
            |-- images.bin
            `-- points3D.bin
```

UI view example. After mapping completes, do not clear the trajectory. You can judge reconstruction quality by combining the SLAM trajectory, reconstruction path, keyframe camera poses, and point count:

![alt text](image/image_watch_sfm_map.png)

At this point, mapping is complete. Next, use the map for relocalization.

## RTK-Fused Mapping (Optional)

> Note: this section is only for cases where you want to fuse **SFM mapping** with **RTK** positioning to obtain a more accurate map. In most cases, visual-only SFM mapping is sufficient for mapping quality and relocalization.
>
> This feature is not fully released yet and is still under stability testing.

**Workflow:**

1. Follow the manual section [Fusion Pose / Visual Fusion RTK](../融合位姿/visual_fusion_single_antenna_rtk.md) to set up RTK driver and GNSS/RTK config.
2. After GNSS configs and `/rtk_nmea` topic are ready, verify that `/baton/rtk` is being published.
3. Start the latest UI (example: `roboBaton V20251031`), then: Settings -> Loop -> enable loop/relocalization -> set relocalization file path -> disable loop/relocalization -> enable record mapping info.
4. Start stereo3 and move around the mapping area to collect data, then stop the algorithm.
5. Click **Start mapping** in the UI.

In step 2, make sure RTK has a fixed solution. You can check `/baton/rtk`:

```shell
header:
  stamp:
    sec: 1759141703
    nanosec: 305476864
  frame_id: rtk
status:
  status: 2     # 2 means fixed solution; other values are not fixed
  service: 0
latitude: 22.81607205183333
longitude: 113.49725767266666
altitude: -1.7479999999999998
position_covariance:
- 0.054450000000000005
- 0.0
- 0.0
- 0.0
- 0.054450000000000005
- 0.0
- 0.0
- 0.0
- 0.054450000000000005
position_covariance_type: 48
```

The detailed UI steps in step 3:

![alt text](image/set_sfm_config_image.png)

After enabling it and running stereo3, the program will start a node named `extract_sfm` to collect mapping data. Note: after stopping stereo3, **Record mapping info** will be unchecked automatically in the Loop config page.

After data collection, many files will be saved under the configured path. One of them is `ecef_coordinates.txt`. Ensure it is not empty; otherwise RTK mapping will still be visual-only mapping.

After mapping completes, relocalization usage is the same as below.

## Run Relocalization

To run relocalization with the built map:

1. In the UI `Settings -> Loop`, check **Enable loop/relocalization** and **Load map**, save, then run stereo3.
2. Without UI: edit `/root/Baton/install/share/baton/config/sys.yaml` and set `relocalization: true`, then start stereo3 manually. (The `sys.yaml` path differs slightly between ROS1 and ROS2; you can search under `~/baton`.)

![](image/image_start_relocation.png)

After that, Viobot-UI will show a fused trajectory. You can try running the device through the same place multiple times and observe the trajectory changes. Example (indoor repeated runs): with relocalization, long-term odometry becomes more accurate:

![](image/image_hmsfm_result.png)

### How to Tell Whether Relocalization Is Triggered

After relocalization is triggered, a topic `/baton/stereo3/odom_relo` (type `geometry_msgs/PoseStamped`) will be published. You can judge whether relocalization succeeded by checking whether this topic is published. This topic provides the relocalized pose in the mapping coordinate frame.

> Note: the fused trajectory is published to `/baton/stereo3/fusion_odom`. This topic fuses GNSS/RTK/relocalization as pose output: it fuses whatever sources are available.

----------------------------------------------

###### Appendix (Optional)

> This appendix is not required for mapping/relocalization. The visualized map is sparse and mainly suitable for relocalization; it may not look intuitive. If you want to visualize the map built by Viobot2, you can use the steps below.

Viobot-UI supports a simple view of the path traveled when saving the map, which gives a rough idea of the reconstructed area. Example: driving a small vehicle outdoors:

![alt text](image/image_watch_map_pose.png)

To visualize the reconstruction result, you can use COLMAP on Windows ([download COLMAP x64](https://github.com/colmap/colmap/releases/download/3.11.1/colmap-x64-windows-nocuda.zip)). Example visualization:

![](image/image_sfm_result.png)

Steps to open the result in COLMAP:

First, download the reconstruction result from Viobot2:

```shell
# 1) zip the result on Viobot2
cd /home/my_relocation
zip -vr HM_SFM.zip HM_SFM

# 2) transfer to PC and unzip
# transfer HM_SFM.zip via Xshell/MobaXterm, then unzip on the PC
```

After extracting `colmap-x64`, double click `COLMAP.bat`:

![](image/image_colmap.png)

This opens a command window and a UI. Then follow the steps below to open the reconstructed folder:

![](image/image_open_sfm.png)

After selecting the folder, a dialog may pop up. Choose based on the prompt (usually select Yes to make it easier to inspect constraints between keyframes):

![](image/image_open_result2.png)

If you selected Yes, then select the `.db` file and the `images` folder, click Save, and the result will be loaded:

![](image/image_open_result3.png)

You can double click the camera icon of a keyframe to view details such as number of points, pose relationships, and linked keyframes:

![](image/image_view_kf.png)

