# SDK数据定义

设备上电会开启一个服务器，通过http协议进行参数读写及流数据获取，也可以通过ros主从机通信来控制以及获取数据和设备状态。

<!-- ## 1.设置和操作

### （1）设置设备ip

​	设置后重启生效

### （2）tof开关 ON/OFF

​	通过通信协议中的smart参数设置

&#x20;   默认：OFF

### （3）补光灯开关 ON/OFF

​	通过通信协议中的smart参数设置

&#x20;   默认：OFF

### （4）raw\_data输出设置

​	通过通信协议中的smart参数设置

&#x20;    图像：0/1/2/3 (注：0：无图像通过流数据输出；1：左目；2：右目；3：双目图像通过流数据输出)

&#x20;    imu：ON/OFF

&#x20;    tof深度图：ON/OFF

&#x20;    tof幅度图：ON/OFF

&#x20;    默认：OFF

ROS控制需要发送下面的话题，话题数据是自定义的，详情参考配套demo中的msg

```
Type: system_ctrl::viobot_ctrl
Topic: /system_ctrl
```

### （5）VIO算法

&#x20;  启停：ON/OFF

&#x20;  重启：restart

&#x20;  重置：reset

&#x20;  重定位: relocation

ROS控制需要发送下面的话题，话题数据是自定义的，详情参考配套demo中的msg

```
Type: system_ctrl::algo_ctrl
Topic: /stereo1_ctrl    /stereo2_ctrl    /mono_ctrl
``` -->

## 1.SDK数据输出

### （1）传感器原始数据
<!-- todo -->
注：需设置raw_data输出

#### 1）imu

```c
typedef struct {
  double acc_x,acc_y,acc_z,groy_x,groy_y,groy_z;
  uint32_t time_stamp;
}imu;
```

#### 2）图像数据

```c
uint16_t width,height;
uint32_t time_stamp;
char data[width * height];
```


### （2）算法数据

​	   注：启动算法后才会输出

##### 		1）位姿

​			7个float数据——位置x,y,z+四元数x,y,z,w。通过流获取，详见3.（5）获取数据流

##### 		2）速度

​			3个double数据——x,y,z。通过流获取，详见3.（5）获取数据流


### （3）相机内外参数据

```c
//内参结构体
typedef struct{
    float left_cam_fx;      // 焦距长度x (像素)
    float left_cam_fy;      // 焦距长度y (像素)
    float left_cam_cx;      // 光心投影坐标x(像素)
    float left_cam_cy;      // 光心投影坐标y(像素)
    float left_cam_xi;      //double sphere畸变系数xi
    float left_cam_alpha;   //double sphere畸变系数alpha
    float right_cam_fx;
    float right_cam_fy;
    float right_cam_cx;
    float right_cam_cy;
    float right_cam_xi;
    float right_cam_alpha;
    float cam_extrinsic_px;         //右目到左目的位姿变换（平移+四元数旋转）
    float cam_extrinsic_py;
    float cam_extrinsic_pz;
    float cam_extrinsic_qx;
    float cam_extrinsic_qy;
    float cam_extrinsic_qz;
    float cam_extrinsic_qw;
    float CL2I_extrinsic_px;        //左目到imu的位姿变换（平移+四元数旋转）
    float CL2I_extrinsic_py;
    float CL2I_extrinsic_pz;
    float CL2I_extrinsic_qx;
    float CL2I_extrinsic_qy;
    float CL2I_extrinsic_qz;
    float CL2I_extrinsic_qw;
} LensPara;
```

<!-- #### 	2）IMU内参 无响应

```c
//内参结构体
typedef struct{
    float acc_n;          // 加速度计噪声
    float acc_w;          // 加速度计随机游走
    float gyr_n;          // 陀螺仪噪声
    float gyr_w;          // 陀螺仪随机游走
} ImuParam;
``` -->




<!-- ### （4）系统算法状态

```c
typedef enum{
    ready = 0,
    stereo1_initializing,
    stereo1_running,
    stereo2_initializing,
    stereo2_running,
    mono_initializing,
    mono_running,
}system_status;
```

单个字节，上电连接后默认为ready，给设备发送了启动指后会进入初始化状态（initializing），初始化完成进入运行状态（running）

注：默认可以通过ros获取数据 -->

<!-- ### ROS话题：

#### (1)raw_data

i.图像数据

```c
Type: sensor_msgs/msg/Image
Topic: /image_left     /image_right
```

ii.imu数据

```c
Type: sensor_msgs::Imu
Topic:  /imu
```

iii.tof点云数据(需开启tof)

```c
Type: sensor_msgs::PointCloud2
Topic: /tof_cloud
(x,y,z)
```

iiii.tof幅度图和深度图(需开启tof)

```c
Type: sensor_msgs::Image
Topic: /amp_image  /depth_image
```

iiiii.系统状态

```
#此项为自定义的ros msg,可以在SDK例程里面找到
Type: system_ctrl::viobot_ctrl
Topic: /sys_status
```

iiiiii.算法状态

```
#此项为自定义的ros msg,可以在SDK例程里面找到，具体状态见（4）系统算法状态
Type: system_ctrl::algo_staus
Topic: /algo_status
```

iiiiii.相机参数

```
Type: sensor_msgs::CameraInfo
Topic： /camera_left_info  /camera_right_info
```

#### (2)算法输出

i.stereo2

​	pose + twist:

```bash
Type: nav_msgs::Odometry
Topic: 
	/pr_loop/odometry_rect
	/pr_loop/odometry_adjusted #全局一致
```

​	pointcloud:

```bash
Type: sensor_msgs::PointCloud2
Topic: 
	/pr_loop/points #原生点云(融合的)
	/pr_loop/points_rdf  #RDF点云(融合的)
	/pr_loop/points_adjusted #这个是全局一致性
```

ii.stereo1

​	pose:

```
Type: nav_msgs::Odometry
Topic:  /pr_loop/odometry_rect
```

iii.mono1

​	pose:

```
Type: nav_msgs::Odometry
Topic: /mono1_loop/loop_pose
```

#### (3)参数数据

双目内参：

```
Type:sensor_msgs::CameraInfo
Topic: /camera_left_info  /camera_right_info
```

### ROS2话题：

此部分对应ROS2版本

#### (1)raw_data

i.图像数据

```c
Type: sensor_msgs::msg::Image
Topic: /image_left     /image_right
```

ii.imu数据

```c
Type: sensor_msgs::msg::Imu
Topic:  /imu
```

iii.tof点云数据(需开启tof)

```c
Type: sensor_msgs::msg::PointCloud2
Topic: /tof_cloud
(x,y,z)
```

iiii.tof幅度图和深度图(需开启tof)

```c
Type: sensor_msgs::msg::Image
Topic: /amp_image  /depth_image
```

iiiii.系统状态

```
#此项为自定义的ros msg,可以在SDK例程里面找到
Type: system_ctrl::msg::ViobotCtrl
Topic: /sys_status
```

iiiiii.算法状态

```
#此项为自定义的ros msg,可以在SDK例程里面找到，具体状态见（4）系统算法状态
Type: system_ctrl::msg::AlgoStatus
Topic: /algo_status
```

iiiiii.相机参数

```
Type: sensor_msgs::msg::CameraInfo
Topic： /camera_left_info  /camera_right_info
```

#### (2)算法输出

i.stereo2

​	pose + twist:

```bash
Type: nav_msgs::msg::Odometry
Topic: 
    /pr_loop/odometry
    /pr_loop/odometry_adjusted #全局一致
```

​	pointcloud:

```bash
Type: sensor_msgs::msg::PointCloud2
Topic: 
	/pr_loop/points #原生点云(融合的)
	/pr_loop/points_rdf  #RDF点云(融合的)
	/pr_loop/points_adjusted #这个是全局一致性
```

ii.stereo1

​	pose:

```
Type: nav_msgs::msg::Odometry
Topic:  /pr_loop/odometry_rect
```

iii.mono1

​	pose:

```
Type: nav_msgs::msg::Odometry
Topic: /mono1_loop/loop_pose
```

#### (3)参数数据

双目内参：

```
Type:sensor_pub::msg::ImageInfo
Topic: /camera_left_info  /camera_right_info
``` -->

## 3.通信协议

【***\*协议说明\****】HTTP协议主要用于参数读写及流数据获取，默认端口8000

【***\*接口说明\****】

### （1）网络参数

| ***\*URL\****    | http://< ip >:< port >/System/network                        |
| ---------------- | ------------------------------------------------------------ |
| ***\*METHOD\**** | GET/PUT                                                      |
| ***\*BODY\****   | {  <br />"ipaddr":"192.168.1.100",  <br />"submask":"192.168.0.1.0",  <br />"gateway":"192.168.1.1", <br /> "macaddr":"FF:FF:FF:FF:FF:FF", <br /> "commandPort":8000, <br /> "heartbeatPort":6789,<br />"udpPort":10000<br />} |

BODY参数定义：

| ipaddr        | IP地址   |
| ------------- | -------- |
| submask       | 子网掩码 |
| gateway       | 网关地址 |
| macaddr       | MAC地址  |
| commandPort   | 指令端口 |
| heartbeatPort | 心跳端口 |
| udpPort       | UDP端口  |

 示例：
 ~~~ json
GET: http://192.168.3.10:8000/System/network
retrun:
{
    "ipaddr": "192.168.3.10",
    "submask": "255.255.255.0",
    "gateway": "192.168.3.1",
    "macaddr": "FF:FF:FF:FF:FF:FF",
    "commandPort": 8000,
    "heartbeatPort": 6789,
    "udpPort": 10000
}
 ~~~

### （2）相机内外参

| ***\*URL\****                                                | http://< ip >:< port >/System/param        |
| :----------------------------------------------------------- | ------------------------------------------------------------ |
| ***\*METHOD\****                                             | GET                                                          |



BODY参数定义：（float）

| alpha fx fy cx cy xi     | double spere 相机模型畸变参数|
| ------------------------ | ---------------------------- |
|cam_extrinsi              |右目到左目的坐标变换           |
| CL2I_extrinsic           | 左目到imu的坐标变换          |

示例
~~~
GET: http://192.168.3.10:8000/System/param
return:
{
    "left_cam.fx": 161.841393477148586,
    "left_cam.fy": 161.730837115321521,
    "left_cam.cx": 320.211856996505389,
    "left_cam.cy": 237.303872164579872,
    "left_cam.xi": -0.279593379748090,
    "left_cam.alpha": 0.563464940393459,
    "right_cam.fx": 165.576971762865526,
    "right_cam.fy": 165.447644216261438,
    "right_cam.cx": 320.046219470526012,
    "right_cam.cy": 241.989924464922581,
    "right_cam.xi": -0.258659860632949,
    "right_cam.alpha": 0.569348129203276,
    "cam_extrinsic.px": 0.057603404270098,
    "cam_extrinsic.py": 0.000982731176737,
    "cam_extrinsic.pz": 0.000121991681132,
    "cam_extrinsic.qx": -0.000426461815132,
    "cam_extrinsic.qy": 0.001524022245945,
    "cam_extrinsic.qz": 0.001893525715907,
    "cam_extrinsic.qw": 0.999996955018803,
    "CL2I_extrinsic.px": 0.031381137669086,
    "CL2I_extrinsic.py": 0.003780222497880,
    "CL2I_extrinsic.pz": -0.000907357316464,
    "CL2I_extrinsic.qx": -0.005790754170666,
    "CL2I_extrinsic.qy": 0.999981432980785,
    "CL2I_extrinsic.qz": -0.001751826831367,
    "CL2I_extrinsic.qw": 0.000724035690780
}
~~~
 

<!-- ### （3）IMU内参 

| ***\*URL\****    | http://< ip >:< port >/Config/imuInter                       |
| ---------------- | ------------------------------------------------------------ |
| ***\*METHOD\**** | GET                                                          |
| ***\*BODY\****   | { <br />   "acc_n":0, <br />   "acc_w":0,<br />   "gyr_n":0, <br />   "gyr_w":0<br />} |

BODY参数定义：（float）

| acc_n | 加速度计噪声     |
| ----- | ---------------- |
| acc_w | 加速度计随机游走 |
| gyr_n | 陀螺仪噪声       |
| gyr_w | 陀螺仪随机游走   | -->

 

### （3）smart参数

| ***\*URL\****    | http://< ip >:< port >/Config/smart                          |
| ---------------- | ------------------------------------------------------------ |
| ***\*METHOD\**** | GET/PUT                                                      |
| ***\*BODY\****   | {  <br />  "gray_image_enable": 0,<br />  "imu_enable": 0,<br />  "tof_enable": 0,<br />  "tof_deep_image_enable": 0,<br />  "tof_amp_image_enable": 0<br />  "light": 0<br />} |
|                  |                                                              |

BODY参数定义：

| gray_image_enable     | 灰度图启用：3 / 2 / 1 / 0 |
| --------------------- | ------------------------- |
| imu_enable            | Imu启用：1/0              |
| tof_enable            | Tof启用：1/0              |
| tof_deep_image_enable | Tof深度图启用：1/0        |
| tof_amp_image_enable  | Tof幅度图启用：1/0        |
| light                 | 补光灯开关：1/0           |

 注：灰度图启用：

​	0：不启用流获取灰度图

​	1：启用流获取左目灰度图（单目）

​	2：启用流获取右目灰度图

​	3：启用流获取双目灰度图



<!-- ### （4）重定位

| ***\*URL\****    | http://< ip >:< port >/Smart/relocation |
| ---------------- | --------------------------------------- |
| ***\*METHOD\**** | PUT                                     |
| ***\*BODY\****   | [0,0,0,0,0,0,0,0,0,0,0,0]               |

BODY参数定义：一个3行4列的位姿变换矩阵，由12个浮点数组成的数组，每4个值表示矩阵的一行 -->

###  （4）Vio算法控制

#### 1）Vio算法启用

| ***\*URL\****    | http://< ip >:< port >/Algorithm/enable/"algo_tyep_num"    |
| ---------------- | ---------------------------------------------------------- |
| ***\*METHOD\**** | PUT                                                        |
| ***\*BODY\****   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3                            |

#### 2）Vio算法禁用

| ***\*URL\****    | http://< ip >:< port >/Algorithm/disable/"algo_tyep_num"   |
| ---------------- | ---------------------------------------------------------- |
| ***\*METHOD\**** | PUT                                                        |
| ***\*BODY\****   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3                            |

#### 3）Vio算法重启

| ***\*URL\****    | http://< ip >:< port >/Algorithm/reboot/"algo_tyep_num"    |
| ---------------- | ---------------------------------------------------------- |
| ***\*METHOD\**** | PUT                                                        |
| ***\*BODY\****   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3                            |

#### 4）Vio算法重置

| ***\*URL\****    | http://< ip >:< port >/Algorithm/reset/"algo_tyep_num"     |
| ---------------- | ---------------------------------------------------------- |
| ***\*METHOD\**** | PUT                                                        |
| ***\*BODY\****   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3                            |



<!-- ###  （7）回环添加关键帧

| ***\*URL\****    | http://< ip >:< port >/Smart/addKeyFrame |
| ---------------- | ---------------------------------------- |
| ***\*METHOD\**** | PUT                                      |
| ***\*BODY\****   | 无                                       | -->

 

<!-- ###  （8）回环保存关键帧

| ***\*URL\****    | http://< ip >:< port >/Smart/saveKeyFrame |
| ---------------- | ----------------------------------------- |
| ***\*METHOD\**** | PUT                                       |
| ***\*BODY\****   | 无                                        | -->

 

<!-- ### （9）cam2imu参数

| ***\*URL\****    | http://< ip >:< port >/Config/cam2imu |
| ---------------- | ------------------------------------- |
| ***\*METHOD\**** | GET                                   |
| ***\*BODY\****   | [0,0,0,0, 0,0,0,0, 0,0,0,0]           |

BODY参数定义：一个3行4列的变换矩阵，由12个浮点数组成的数组，每4个值表示矩阵的一行 -->

<!-- ### （10）tof2cam参数

| ***\*URL\****    | http://< ip >:< port >/Config/tof2cam |
| ---------------- | ------------------------------------- |
| ***\*METHOD\**** | GET                                   |
| ***\*BODY\****   | [0,0,0,0, 0,0,0,0, 0,0,0,0]           |

BODY参数定义：一个3行4列的变换矩阵，由12个浮点数组成的数组，每4个值表示矩阵的一行 -->

### （5）获取数据流

| ***\*URL\****    | http://< ip >:< port >/Stream?Channel=< chan >               |
| ---------------- | ------------------------------------------------------------ |
|                  | chan:数据流通道号<br />   通道1：imu + stereo3位姿  + 速度   + 系统状态<br />   通道2：左目可见光灰度图<br />   通道3：深度图 + 幅度图<br />   通道4：算法输出点云 <br />   通道5：tof点云  <br />   通道6：右目可见光灰度图<br />   通道7：全局一致点云<br />   通道8：RDF点云+位姿<br /> |
| ***\*METHOD\**** | GET                                                          |
| ***\*BODY\****   | 无                                                           |
| 注：             | 单目版本可见光图为通道2：左目可见光，位姿为stereo1位姿       |

数据包=帧头+帧数据；

帧头=0x33cccc33+帧类型（uint）+时间戳（uint）+序列号（uint）+宽（uint）+高（uint）+长度（uint）；

服务端收到数据流请求后开始发送连续数据包。

当服务端收到Bye，则停止发送数据流，并断开连接。

| 帧类型编号 |      帧类型      |
| :--------: | :--------------: |
|     1      |       IMU        |
|     2      | 左目可见光灰度图 |
|     10     | 右目可见光灰度图 |
|     3      |      深度图      |
|     4      |      幅度图      |
|     9      |     tof点云      |
|     16     |   TOF实时状态    |
|     17     |  补光灯实时状态  |
|     7      | stereo2算法点云  |
|     15     |     RDF点云      |
|     14     |     RDF位姿      |
|     11     |   全局一致位姿   |
|     12     |   全局一致点云   |
|     13     |     设备速度     |
|            |                  |
|     5      |     算法位姿     |
|     6      |     回环位姿     |
|     8      |     系统状态     |
