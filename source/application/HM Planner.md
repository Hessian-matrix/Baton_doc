# HM Planner
## 全覆盖路径规划
Viobot2搭载了全覆盖的弓形路径规划算法，基于纯视觉里程计和重定位实现，在模拟割草应用的场景中能实现全覆盖草地作业的效果。
![](image/image_planner_result.png)
<center style="font-size:14px;color:#C0C0C0;">图1</center> 

## 详细流程
Viobot-UI连接Viobot2，在loop页设置好地图路径，点击开启回环/重定位，开启算法后绕割草区域一周，点击保存bow。

![](image/image_setting_planner.png)
<center style="font-size:14px;color:#C0C0C0;">loop页设置地图保存路径</center> 
类似于图1这样开启stereo3算法在草地边缘运行走一圈形成一个封闭的路径，然后保存地图：

![](image/image_planner_save_bow.png)
<center style="font-size:14px;color:#C0C0C0;">点击保存bow保存地图</center> 

然后停止stereo3算法，在设置->loop->勾选加载地图

![](image/image_planner_load_map.png)
<center style="font-size:14px;color:#C0C0C0;">加载地图</center> 

然后重新启动stereo3（注：如果已经圈好了规划的范围且已经勾选了加载地图的话不需要重新启动stereo3，直接开启即可），然后在命令行运行规划器：
~~~
rosrun hm_planner planner_coverage_v1
~~~

然后在Viobot-UI上就可看到全覆盖的规划路径了，规划算法会发布/cmd_vel控制底盘指令，接收该话题控制车辆即可实现全覆盖割草。

