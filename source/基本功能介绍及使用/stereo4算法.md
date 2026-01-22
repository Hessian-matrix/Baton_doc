# Stereo4算法

stereo4算法的特点
stereo4算法是黑森矩阵最新开发的一套基于滤波的slam算法，其特点是开销更低，精度和steroe3的大致相当，适合在开销吃紧的场景使用。stereo4的算法平均开销相比stereo3的降低了约30%。

## 功能
stereo4算法目前已有融合RTK、建图与重定位这两大功能
## VIO
## sfm建图重定位
## 融合rtk
## 高频位姿
待更新

## 话题

stereo4目前的话题
```
/baton/stereo4/feature_img
/baton/stereo4/feature_img/compressed
/baton/stereo4/feature_img/compressedDepth
/baton/stereo4/feature_img/theora
/baton/stereo4/fusion_odom
/baton/stereo4/fusion_path
/baton/stereo4/map_odom
/baton/stereo4/map_path
/baton/stereo4/odom_path
/baton/stereo4/odom_relo
/baton/stereo4/odometry
/baton/stereo4/rtk_odom
/baton/stereo4/rtk_path
/baton/stereo4/lla_odom
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

