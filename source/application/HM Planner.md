# HM Planner
## 全覆盖路径规划

### 简介

Viobot2内置了全覆盖的弓形路径规划算法，基于纯视觉里程计和重定位实现，在一些需要全覆盖的应用场景如家庭扫地机、割草机能直接使用。

![](image/image_planner_result.png)
<center style="font-size:14px;color:#C0C0C0;">图1</center> 

### 详细流程

Viobot-UI连接Viobot2，在loop页设置好地图路径，点击开启回环/重定位，开启算法后绕割草区域一周，点击保存bow。

![](image/image_setting_planner.png)
<center style="font-size:14px;color:#C0C0C0;">loop页设置地图保存路径</center> 
类似于图1这样开启stereo3算法在需要全覆盖的作业范围的边缘运行走一圈形成一个封闭的路径，然后保存地图：

![](image/image_planner_save_bow.png)
<center style="font-size:14px;color:#C0C0C0;">点击保存bow保存地图</center> 

然后停止stereo3算法，在设置->loop->勾选加载地图

![](image/image_planner_load_map.png)
<center style="font-size:14px;color:#C0C0C0;">加载地图</center> 

然后重新启动stereo3（注：如果已经圈好了规划的范围且已经勾选了加载地图的话不需要重新启动stereo3，直接开启即可），然后在命令行运行规划器(安装不同版本ROS的Viobot按ROS版本选择以下命令)：
ROS1:
~~~
rosrun hm_planner planner_coverage_v1
~~~

ROS2:

~~~
ros2 run hm_planner planner_coverage_v1
~~~
然后在rviz上就可以通过订阅/baton/planner/global_path话题看到全覆盖的规划路径了，规划算法会发布/cmd_vel控制底盘指令，接收该话题控制车辆即可实现全覆盖作业任务

### 规划器的参数配置

ROS1版本的配置文件路径在`/root/Baton/install/share/hm_planner/config/config.yaml`,ROS2版本配置文件路径：`/root/Baton/install/hm_planner/share/hm_planner/config/config.yaml`,其中的配置内容主要是常见的规划器配置和坐标系的相关配置：

~~~ yaml
lineSpacing：覆盖间隔
max_linear_speed：最大线速度
max_angular_speed：最大角速度

t_camera_vehicle_x：车辆中心到相机外参的x分量
t_camera_vehicle_y：车辆中心到相机外参的y分量
t_camera_vehicle_z：车辆中心到相机外参的z分量
~~~

坐标系请参考下图：

![](image/image_tf_frame.png)
