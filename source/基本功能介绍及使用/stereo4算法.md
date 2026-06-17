# Stereo4算法

## 功能特点

stereo4算法是黑森矩阵最新开发的一套更轻量双目鱼眼视觉slam算法，其特点是开销更低，精度和steroe3的大致相当，在25hz图像输入时stereo4的算法平均开销相比stereo3的降低了约30%~50%，对于算力受限时可以使用。stereo4同样支持重定位+rtk的耦合，但是stereo4暂时没有在线回环的功能。

## VIO
使用的25hz双目图像+200hz imu输出，输出的odometry为25hz。
## sfm建图重定位
同样支持跑vio采集建图数据用来SFM建图，stereo3建图的数据可用于stereo4算法启动时的重定位地图数据，反之也可。
## 融合rtk
支持接入10hz RTK定位消息，stereo4配置了RTK模式后可输出融合rtk的里程计，可将低频的RTK数据耦合成高频的定位输出，支持在RTK信号受限的场景中持续定位
## 高频位姿
支持imu插值的高频里程计，输出频率可到200hz。

## 话题

stereo4目前的话题
```
/baton/stereo4/feature_img
/baton/stereo4/feature_img/compressed
/baton/stereo4/feature_img/compressedDepth
/baton/stereo4/feature_img/theora
/baton/stereo4/fusion_odom    #融合后的odometry，在SLAM局部坐标系下
/baton/stereo4/fusion_path    #融合后的历史轨迹，在SLAM局部坐标系下
/baton/stereo4/map_odom
/baton/stereo4/map_path
/baton/stereo4/odom_path
/baton/stereo4/odom_relo
/baton/stereo4/odometry
/baton/stereo4/rtk_odom
/baton/stereo4/rtk_path     #RTK历史轨迹，在SLAM局部坐标系下
/baton/stereo4/lla_odom     #融合后的odometry，XYZ是经纬高（单位:度、米），朝向是在东北天坐标系下
/baton/stereo4_ctrl

```

## 话题控制

下面是使用话题控制算法的用法，发布`system_ctrl/algo_ctrl`类型的/baton/stereo4_ctrl话题可控制stereo4算法的启动（algo_enable: true）、停止（algo_enable: false）、重启（algo_reboot: true）、重置（algo_reset: true"）。
ros1:
```
rostopic pub /baton/stereo4_ctrl system_ctrl/algo_ctrl "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
algo_enable: true
algo_reboot: false
algo_reset: false"
```

ros2:
```
ros2 topic pub --once /baton/stereo4_ctrl system_ctrl/msg/AlgoCtrl "{
    header: {stamp: {sec: 0, nanosec: 0}, frame_id: ''},
    algo_enable: true, 
    algo_reboot: false,
    algo_reset: false}"
```

## http控制

调用方式直接是 HTTP PUT，不需要 body，把127.0.0.1换成自己设备的ip即可。
启动算法：`PUT http://127.0.0.1:8000/Algorithm/enable/5`
停止算法：`PUT http://127.0.0.1:8000/Algorithm/disable/5`
重启算法：`PUT http://127.0.0.1:8000/Algorithm/reboot/5`
重置算法：`PUT http://127.0.0.1:8000/Algorithm/reset/5`