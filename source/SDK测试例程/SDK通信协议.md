# SDK通信协议

Viobot2内部集成了一个HTTP服务器，可以通过http协议进行参数读写及流数据获取，也可以通过ros主从机通信来控制以及获取数据和设备状态。


## HTTP接口协议规范

**协议说明** 默认端口8000


### （1）网络参数

| URL   | http://< ip >:< port >/System/network                        |
| ---------------- | ------------------------------------------------------------ |
| METHOD| GET/PUT                                                      |
| Response BODY   | {  <br />"ipaddr":"192.168.1.100",  <br />"submask":"192.168.0.1.0",  <br />"gateway":"192.168.1.1", <br /> "macaddr":"FF:FF:FF:FF:FF:FF", <br /> "commandPort":8000, <br /> "heartbeatPort":6789,<br />"udpPort":10000<br />} |

Response BODY参数定义：

| ipaddr        | IP地址   |
| ------------- | -------- |
| submask       | 子网掩码 |
| gateway       | 网关地址 |
| macaddr       | MAC地址  |
| commandPort   | 指令端口 |
| heartbeatPort | 心跳端口 |
| udpPort       | UDP端口  |

 
### （2）相机内外参

| URL                                              | http://< ip >:< port >/System/param        |
| :----------------------------------------------------------- | ------------------------------------------------------------ |
| METHOD                                           | GET                                                          |



Response Body参数定义：（float）

| alpha fx fy cx cy xi     | double spere 相机模型畸变参数|
| ------------------------ | ---------------------------- |
|cam_extrinsi              |右目到左目的坐标变换           |
| CL2I_extrinsic           | 左目到imu的坐标变换          |


 
<!-- 
### （3）smart参数

| URL    | http://< ip >:< port >/Config/smart                          |
| ---------------- | ------------------------------------------------------------ |
| METHOD | GET/PUT                                                      |
| Response BODY   | {  <br />  "gray_image_enable": 0,<br />  "imu_enable": 0,<br />  "tof_enable": 0,<br />  "tof_deep_image_enable": 0,<br />  "tof_amp_image_enable": 0<br />  "light": 0<br />} |
|                  |                                                              |

Response BODY参数定义：

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

​	3：启用流获取双目灰度图 -->



### （4）重定位

| URL    | http://< ip >:< port >/Smart/relocation |
| ---------------- | --------------------------------------- |
| METHOD | PUT                                     |
| BODY   | [0,0,0,0,0,0,0,0,0,0,0,0]               |

BODY参数定义：一个3行4列的位姿变换矩阵，由12个浮点数组成的数组，每4个值表示矩阵的一行

###  （5）Vio算法控制

#### 1）Vio算法启用

| URL    | http://< ip >:< port >/Algorithm/enable/"algo_type_num"    |
| ---------------- | ---------------------------------------------------------- |
| METHOD | PUT                                                        |
| BODY   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3<br /> |

#### 2）Vio算法禁用

| URL    | http://< ip >:< port >/Algorithm/disable/"algo_tyep_num"   |
| ---------------- | ---------------------------------------------------------- |
| METHOD | PUT                                                        |
| BODY   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3<br /> |

#### 3）Vio算法重启

| URL    | http://< ip >:< port >/Algorithm/reboot/"algo_tyep_num"    |
| ---------------- | ---------------------------------------------------------- |
| METHOD | PUT                                                        |
| BODY   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3<br /> |

#### 4）Vio算法重置

| URL    | http://< ip >:< port >/Algorithm/reset/"algo_tyep_num"     |
| ---------------- | ---------------------------------------------------------- |
| METHOD | PUT                                                        |
| BODY   | 无                                                         |
| 注：             | "algo_tyep_num":<br />4:stereo3<br /> |



###  （6）回环添加关键帧

| URL    | http://< ip >:< port >/Smart/addKeyFrame |
| ---------------- | ---------------------------------------- |
| METHOD | PUT                                      |
| BODY   | 无                                       |

 

###  （7）回环保存关键帧

| URL    | http://< ip >:< port >/Smart/saveKeyFrame |
| ---------------- | ----------------------------------------- |
| METHOD | PUT                                       |
| BODY   | 无                                        |


### （8）获取数据流

| URL    | http://< ip >:< port >/Stream?Channel=< chan >               |
| ---------------- | ------------------------------------------------------------ |
|                  | chan:数据流通道号<br />   通道1：imu + stereo1位姿 + stereo2位姿 + 速度  + 补光灯实时状态 + TOF实时状态 + 系统状态<br />   通道2：左目可见光灰度图<br />   通道3：深度图 + 幅度图<br />   通道4：算法输出点云 <br />   通道5：tof点云  <br />   通道6：右目可见光灰度图<br />   通道7：全局一致点云<br />   通道8：RDF点云+位姿<br /> |
| METHOD | GET                                                          |
| BODY   | 无                                                           |
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
