# ROS2 Multi-Machine Communication

This page applies to **ROS2**. Viobot2 ships with **Ubuntu 22.04 + ROS2 Humble**. This page demonstrates ROS2-to-ROS2 communication only. If you need ROS1-to-ROS2 bridging, please refer to relevant ROS documentation.

## Network Connection

Connect the x86 PC and Viobot2 to the same LAN, make sure they are in the same subnet and can ping each other.

Example:

- x86 IP: `10.21.12.133`
- device IP: `10.21.12.182`

You can check IPs with `ifconfig`.

## Configure ROS2 Communication

For ROS2, multi-machine discovery typically depends on `ROS_DOMAIN_ID`.

On Viobot2, connect with the client UI and set `ROS_DOMAIN_ID` as shown (example value: `37`). You can also append to `/home/PRR/.bashrc`, e.g. `export ROS_DOMAIN_ID=37`.

Note:

- After changing settings on Viobot2, reboot the device for it to take effect.
- After editing `~/.bashrc` on the x86 PC, re-source it (or open a new terminal).

![](image/image_ros_domain.png)

After both sides are configured, run `ros2 topic list` on the x86 PC and you should see Viobot2 topics. You can also open `rqt` and subscribe to Viobot2 left image topic; if the image displays, ROS2 communication is working.

![](image/image_ros2success_connect.png)

## Control stereo3 via ROS2 Topics

### Environment Example

1) Viobot2 (ROS2 Humble), IP: `192.168.1.100`  
2) x86 PC (ROS2 Galactic), IP: `192.168.1.103`

Prerequisites:

- Build [ROS2_interfaces](https://github.com/Hessian-matrix/ROS2_interfaces.git) on the PC that will communicate with Viobot2.
- Set correct static IPs on both sides (same subnet) and ensure they can ping each other.

![alt text](image/ping_image.png)

Then source the built workspace, set the same `ROS_DOMAIN_ID` on both Viobot2 and the x86 PC, and verify you can see topics on the x86 PC:

1. Clone and build [ROS2_interfaces](https://github.com/Hessian-matrix/ROS2_interfaces.git).
2. On the x86 PC, add `export ROS_DOMAIN_ID=182` to `~/.bashrc`. On Viobot2, set `DOMAIN_ID` via UI, or edit `/home/PRR/.bashrc`:

   ![alt text](image/set_DOMAIN_ID_image.png)

3. `source [your_ros2_interfaces_path]/install/setup.bash`
4. Run `ros2 topic list`:

   ![alt text](image/ros2_topic_list_image.png)

### Start/Stop via Topic Publishing

Publish from the x86 PC:

Start stereo3:

```text
ros2 topic pub --once /baton/stereo3_ctrl system_ctrl/AlgoCtrl "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''}, algo_enable: true, algo_reboot: false, algo_reset: false}"
```

Stop stereo3:

```text
ros2 topic pub --once /baton/stereo3_ctrl system_ctrl/AlgoCtrl "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''}, algo_enable: false, algo_reboot: false, algo_reset: false}"
```

Reboot stereo3:

```text
ros2 topic pub --once /baton/stereo3_ctrl system_ctrl/AlgoCtrl "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''}, algo_enable: true, algo_reboot: true, algo_reset: false}"
```

Example (starting stereo3 from Ubuntu):

![](image/algo_ctrl_image.png)

