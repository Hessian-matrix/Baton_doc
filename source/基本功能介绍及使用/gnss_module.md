# GNSS Module

Before starting, download the latest client and update package from the [Hessian Matrix website](https://www.hessian-matrix.com/%e4%b8%8b%e8%bd%bd%e4%b8%ad%e5%bf%83/) and update the device.

## 1. Enable GNSS Data Reception

After connecting to the device, click **Settings** in the client and open the **GNSS** tab:

![](image/image_83znJpEQ-T.png)

If GNSS is already checked, GNSS reception is enabled. Typically you cannot acquire satellites indoors, so the number of observed satellites may be 0.

If GNSS is not checked, check it and click **OK**. To ensure the module works correctly, manually reboot the device to reload the driver.

## 2. Verify Module Status

Connect the GNSS antenna, and place it where satellites are visible. Avoid placing it close to metal objects or strong electromagnetic interference sources. The settings page will refresh the number of satellites, shown as **Observed satellites**. If it stays 0, the antenna or connection may be faulty; please check the connection.

![image-20250415145206850](image/image-20250415145206850.png)

Click **Show GNSS** to display more detailed satellite quality information:

- Left: line charts of visible / available / used satellites
- Middle: sky plot showing azimuth and elevation of available satellites
- Right: SNR bar chart for each available satellite (gray) and used satellite (blue)

![](image/image-gnss_quality_view.png)

Note: if the algorithm is not started, since satellites are not used for pose estimation, the number of available satellites can be -1 and SNR can be -1. To reduce interference, keep the antenna at least 20cm away from the mainboard. Outdoors, SNR should be > 35.

## 3. Configure Antenna Extrinsics

There is an extrinsics input on the settings page. Set it based on the measured distance between the antenna and the camera module (unit: meters).

Using the camera module forward direction as reference:

- +X: left of the camera module
- +Y: below the camera module
- +Z: behind the camera module

As shown:

![](image/image_1jdONHm-ux.png)

After entering the extrinsics, click **OK** to apply.

## 4. Algorithm Test

After setting the extrinsics, start the stereo3 algorithm; it will run in **GVIO** mode. The **available satellites** value will update in real time. When the number of available satellites is greater than 12, GNSS data quality is good and will be fused with VIO, improving accuracy and robustness.

![gnss](image/gnss.png)

During use, monitor visible/available satellites to ensure GVIO works well. If satellites are insufficient, GVIO will fall back to VIO mode; normal VIO usage is not affected.

## 5. GNSS Topic Output

After enabling GNSS correctly, you can find GNSS-related topics in the topic list. Message types differ slightly between ROS1 and ROS2; here we use ROS1 as an example. You can find the message definitions in [Hessian-matrix ROS_interfaces](https://github.com/Hessian-matrix/ROS_interfaces.git).

```
/baton/gnss/ephem       Type: gnss_comm/GnssEphemMsg
/baton/gnss/meas        Type: gnss_comm/GnssMeasMsg
```

## 6. GVIO Data Notes

GNSS does not output raw NMEA (lat/lon/alt directly). It outputs raw GNSS observations. The stereo3 algorithm tightly couples GNSS raw observations with VIO to obtain poses with smaller accumulated drift in the global frame.

If you need lat/lon/alt output, refer to the parsing and message publishing approach in [gnss_comm](https://github.com/HKUST-Aerial-Robotics/gnss_comm.git) and the published GNSS topic messages.

