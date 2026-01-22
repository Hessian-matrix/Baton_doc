# SDK Communication Protocol

Viobot2 integrates an HTTP server. You can use HTTP to read/write parameters and fetch stream data. You can also use ROS (master/slave) communication to control the device and obtain data/status.

## HTTP API Specification

**Default port:** 8000

### (1) Network Parameters

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/System/network` |
| METHOD | GET / PUT |
| Response BODY | `{  <br />"ipaddr":"192.168.1.100",  <br />"submask":"255.255.255.0",  <br />"gateway":"192.168.1.1", <br /> "macaddr":"FF:FF:FF:FF:FF:FF", <br /> "commandPort":8000, <br /> "heartbeatPort":6789,<br />"udpPort":10000<br />}` |

Response BODY fields:

| Field | Description |
| --- | --- |
| ipaddr | IP address |
| submask | Subnet mask |
| gateway | Gateway |
| macaddr | MAC address |
| commandPort | Command port |
| heartbeatPort | Heartbeat port |
| udpPort | UDP port |

### (2) Camera Intrinsics / Extrinsics

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/System/param` |
| METHOD | GET |

Response body fields (float):

| Field | Description |
| --- | --- |
| alpha fx fy cx cy xi | Camera model/distortion parameters (double sphere) |
| cam_extrinsi | Right-to-left transform |
| CL2I_extrinsic | Left-camera to IMU transform |

### (3) Smart Parameters

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Config/smart` |
| METHOD | GET / PUT |
| Response BODY | `{  <br />  "gray_image_enable": 0,<br />  "imu_enable": 0,<br />  "tof_enable": 0,<br />  "tof_deep_image_enable": 0,<br />  "tof_amp_image_enable": 0<br />  "light": 0<br />}` |

Response BODY fields:

| Field | Description |
| --- | --- |
| gray_image_enable | Grayscale image stream: 3 / 2 / 1 / 0 |
| imu_enable | IMU enable: 1 / 0 |
| tof_enable | TOF enable: 1 / 0 |
| tof_deep_image_enable | TOF depth image enable: 1 / 0 |
| tof_amp_image_enable | TOF amplitude image enable: 1 / 0 |
| light | Fill light enable: 1 / 0 |

Notes for `gray_image_enable`:

- 0: disable grayscale stream
- 1: enable left grayscale stream (mono)
- 2: enable right grayscale stream
- 3: enable stereo grayscale stream

### (4) Relocalization

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Smart/relocation` |
| METHOD | PUT |
| BODY | `[0,0,0,0,0,0,0,0,0,0,0,0]` |

BODY definition: a 3x4 pose transform matrix flattened into 12 floats; every 4 values represent one row.

### (5) VIO Algorithm Control

Note: the URL uses `"algo_tyep_num"` (typo kept as-is).

#### 1) Enable

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Algorithm/enable/"algo_tyep_num"` |
| METHOD | PUT |
| BODY | none |
| algo_tyep_num | `4: stereo3` |

#### 2) Disable

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Algorithm/disable/"algo_tyep_num"` |
| METHOD | PUT |
| BODY | none |
| algo_tyep_num | `4: stereo3` |

#### 3) Reboot

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Algorithm/reboot/"algo_tyep_num"` |
| METHOD | PUT |
| BODY | none |
| algo_tyep_num | `4: stereo3` |

#### 4) Reset

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Algorithm/reset/"algo_tyep_num"` |
| METHOD | PUT |
| BODY | none |
| algo_tyep_num | `4: stereo3` |

### (6) Add Loop Keyframe

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Smart/addKeyFrame` |
| METHOD | PUT |
| BODY | none |

### (7) Save Loop Keyframes

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Smart/saveKeyFrame` |
| METHOD | PUT |
| BODY | none |

### (8) Get Data Stream

| Item | Value |
| --- | --- |
| URL | `http://<ip>:<port>/Stream?Channel=<chan>` |
| METHOD | GET |
| BODY | none |
| chan | Stream channel ID:<br />Channel 1: IMU + stereo1 pose + stereo2 pose + velocity + fill-light status + TOF status + system status<br />Channel 2: left visible grayscale image<br />Channel 3: depth image + amplitude image<br />Channel 4: algorithm point cloud output<br />Channel 5: TOF point cloud<br />Channel 6: right visible grayscale image<br />Channel 7: globally consistent point cloud<br />Channel 8: RDF point cloud + pose |

Note: for mono versions, visible image uses channel 2 (left), and pose uses stereo1 pose.

Data packet format:

- Packet = header + payload
- Header = `0x33cccc33` + frame type (uint) + timestamp (uint) + sequence (uint) + width (uint) + height (uint) + length (uint)

After the server receives a stream request, it starts sending continuous packets.

When the server receives `Bye`, it stops streaming and disconnects.

| Frame Type ID | Frame Type |
| :--: | --- |
| 1 | IMU |
| 2 | Left grayscale image |
| 10 | Right grayscale image |
| 3 | Depth image |
| 4 | Amplitude image |
| 9 | TOF point cloud |
| 16 | TOF realtime status |
| 17 | Fill light realtime status |
| 7 | stereo2 point cloud |
| 15 | RDF point cloud |
| 14 | RDF pose |
| 11 | Globally consistent pose |
| 12 | Globally consistent point cloud |
| 13 | Device velocity |
| 5 | Algorithm pose |
| 6 | Loop-corrected pose |
| 8 | System status |
