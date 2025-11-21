# HM建图与重定位

此文档用于演示如何用viobot2实现sfm重建功能（建图）,以及用建好的地图做全局重定位。

> - 目前Robobaton + HM inside支持在500平方米内不分室内外的大部分场景中的各类机器人三维自主导航定位与感知；
> - HM Localization + 组合导航，结合HM Perception实现中低速自由探索；

**注意：**
> - <font color='#eb0b0bff'>目前viobot2系统版本为202511xx及之后的版本建图需要最新版本的上位机UI配合使用,请参考本章《SFM重定位新版本UI使用》，11月之前的算法版本不受影响</font>
> - <font color='#FF0000'>不支持：如雪原、隧道等视觉特征/光照太差的场景、精度要求极高的严肃工业场景海拔30米向上飞行场景。</font>
> - <font color='#FF0000'>目前SFM重建在无纹理区域、走廊白墙场景容易失败。</font>
> - <font color='#FF0000'>目前重定位在平坦、开阔、近处特征少的场景重定位精度会降低，系统仍然可以依靠GNSS、RTK以及视觉定位正常工作。</font>
> - <font color='#FF0000'>重定位并未与GNSS、RTK的信息做耦合，之后有计划做适配，请用户敬请期待。</font>



## 前置准备

建议使用前先在官网下载最新的viobot2固件、viobot-ui上位机，避免有些功能无法使用，附上官网更新固件的下载页面[黑森矩阵-下载中心 ](https://www.hessian-matrix.com/%e4%b8%8b%e8%bd%bd%e4%b8%ad%e5%bf%83/)

## sfm重建、sfm重定位的粗略步骤：

1. 通过viobot上位机配置viobot；

2. 启动stereo3算法，扫描场地环境；

3. 保存地图；

4. 开始建图；

5. 开启重定位；

6. 查看结果；

详细步骤如下：

## viobot设置与采集数据

viobot-ui连接viobot2，点击设置，找到loop一栏：
- 勾选“开启回环/重定位”，重定位文件夹可以保持默认路径；
- **“加载地图”不要勾选**，否则无法采集数据；
- mask路径就是当viobot镜头画面中有固定物体的遮挡时设置区域屏蔽作用的，如安装到小车上可以通过设置mask屏蔽画面中的车体部分对算法的影响，如没有画面遮挡保持为空即可；

以上设置完成后点击确定，之后再启动stereo3算法，开始移动viobot2去采集数据，注意过程中画面视角不要变化过快避免之后的重建的结果不理想。

如果不通过UI配置采集数据的方法：
按照以下配置`/root/Baton/install/share/baton/config/sys.yaml`,修改`pose_graph_save_path`的路径并记录下来，之后的建图的结果将保存到这里；
~~~ yaml
print_queue: false
use_imu: 2
dt_threshold: 6
gnss_select: 2
load_previous_pose_graph: false
add_keyframe_mode: 1        #需要开启建图数据记录此项为1
pose_graph_save_path: /home/user/pose_graph/    #保存pose_graph的路径
gnss_T_imu:
  data:
    - 0
    - 0
    - 0
relocalization: false   #建图完后有了地图此项为true就是开启了重定位
mask_path: ""
only_sfm_data: true
~~~


![](image/image_viobot_setting.png)

需要建图的区域扫描完后点击保存BOW，等待几秒即可保存完整数据,之后进入下一步离线建图。

![](image/image_save_bow.png)

> Tips: 也可通过ros的话题控制保存bow：
~~~ shell
# ros1: 
rostopic pub -1 /baton/loop/keyframe_action/goal loop_action/KeyFrameHandleActionGoal  "goal: {function: 2}" #function=2即保存bow


# ros2
ros2: ros2 action send_goal /baton/loop/keyframe_action loop_action/KeyFrameHandle "{function: 2}"  #function=2即保存bow
~~~

## 离线建图

前面已经完成了建图的数据采集、基础配置项，建图前建议按照上一节检查一下基础配置项，之后点击“开始建图”之后出现建图的进度条，整个建图的用时视建图的环境大小而增大，进图条结束之后可以在输出路径下的HM_SFM目录下找到重建的结果了：
前面已经完成了建图的数据采集、基础配置项，建图前建议按照上一节检查一下基础配置项，之后点击“开始建图”之后出现建图的进度条，整个建图的用时视建图的环境大小而增大，进图条结束之后可以在输出路径下的HM_SFM目录下找到重建的结果了：

> Tips:此处运行建图也可不通过UI进行建图，ssh登录viobot2通过运行mapping节点进行建图，注意之前配置的路径以及保存的bow文件夹是否存在内容：
~~~ shell
# ros1:
rosrun baton mapping
~~~

<!-- #ros2的指令目前还没有 ros2:
ros2 run baton mapping -->

![](image/image_mapping.png)

> 注意：整个建图过程中对算力需求很高，viobot2的cpu在这段时间会出现cpu占用跑满的情况，是正常的现象，等建图完成之后cpu占用就会恢复正常，在此过程中注意保持viobot2供电的稳定性。

> 建图时如果出现进度条一点就跑完的需要检查一下前面保存bow的路径是否正确，以及路径下是否有bow保存的词袋文件这些，正常情况下建图是一分钟以上的。

下图是用tree来查看建图完成的目录结构

```shell
root@PR-VIO: cd /home/my_relocation
root@PR-VIO:/home/my_relocation# tree
|-- xxx.jpg
|-- ...
`-- images  # 文件夹
    |-- ...
`-- result  # 文件夹
    |-- database.db
    `-- sparse
        `-- 0
            |-- cameras.bin
            |-- images.bin
            `-- points3D.bin
```
至此，使用viobot建图的步骤都已完成，下面开始使用建图的结果来跑重定位。
## 运行重定位
接下来就是用前面已经建好的图运行重定位功能，首选还是在UI上的设置 loop一栏勾选加载地图选项再保存，然后运行stereo3算法。
![](image/image_start_relocation.png)

之后在Viobot-UI上位机上会输出一条融合后的轨迹，可以尝试让设备多次运行到同一个地方查看轨迹的变化。以下是在室内重复多次运行的一个结果，可以看到有重定位的加入后长时间工作里程计更准确：
![](image/image_hmsfm_result.png)

### 判断重定位是否触发

触发重定位之后会发布一个`geometry_msgs/PoseStamped`类型的`/baton/stereo3/odom_relo`话题,需要根据是否接接收到此话题判断重定位是否成功，此话题发布的是建图坐标系下的重定位位姿。


> 注意：融合后的轨迹是在slam坐标系下的，而非地图坐标系，后续会拓展增加融合后地图坐标系和重定位触发信号。

## SFM重定位新版本UI使用
> 本节适用202511xx及之后的算法版本使用教程,上位机UI的版本需要20251031版本，最新ui下载页面[黑森矩阵下载中心](https://www.hessian-matrix.com/%e4%b8%8b%e8%bd%bd%e4%b8%ad%e5%bf%83/)


1. 建图使用
   
  1.1 上位机配置保存建图路径：
  连接上位机后，打开`设置`页面，点开`loop`选项卡，勾选`开启回环/重定位`，可以配置重定位文件路径，这个路径是在viobot2里面的路径，用于存放开启算法后保存下来的建图所需要文件，然后将开启 `回环/重定位`勾选去掉，再勾选`记录建图信息`，点击下面的确定，然后关闭选项卡。

    ![alt text](image/set_sfm_config_image.png)
  1.2 开启算法记录建图信息:
  开启stereo3算法，算法会自动将建图所需信息文件存放到所配置的路径下。开着算法带着viobot2循着需要建图的环境跑一圈，然后停止算法，文件就自动保存好了。

2. 建图：点击`开始建图`按钮，等待上位机的进图条跳转到满格，然后关闭建图弹窗。
  
3. 开启重定位：点开设置，`loop`选项卡，勾选`开启回环/重定位`和`加载地图`两个勾，确认下面的`重定位文件路径`正确，点击确定，关闭弹窗。

点击启动`stereo3`算法，算法在已经建好图的环境下运行就会自己触发重定位，将当前的位姿拉回到地图坐标系下了。
![alt text](image/open_new_relocation_image.png)


----------------------------------------------

###### 附加部分*(非必须步骤)

> 注意：这以下的内容非建图-重定位的必须步骤，并且可视化出来的地图是稀疏的，只是适合用来做重定位的，可视化的结果并不直观，如果有可视化Vibot2建好的地图的需要的可以用此附加部分去显示出来。

Viobot-ui上支持简单的查看看保存地图时已经走过的路径，可以看到重建的区域大概是什么样的,这里用一个小车在户外跑一圈的场景做演示。
![alt text](image/image_watch_map_pose.png)


  如果想要可视化建图出来的结果需要借助到Windows下的colmap软件（[点击下载colmap x64](https://github.com/colmap/colmap/releases/download/3.11.1/colmap-x64-windows-nocuda.zip)），这里用室外的一个重建完的地图做可视化的演示，效果如下：
![](image/image_sfm_result.png)


下面来按步骤用colmap打开建图结果，首先从viobot2上下载重建完的结果：

```shell
# 1) 在viobot2上压缩建图结果文件
cd /home/my_relocation
zip -vr HM_SFM.zip HM_SFM
# 2)传输到电脑、解压
# 将HM_SFM.zip通过xhell、mobaxterm等软件传输到电脑上
# 电脑上解压HM_SFM.zip
```

下载colmap-x64之后解压会得到一下的文件，双击COLMAP.bat运行
![](image/image_colmap.png)


同时弹出一个命令行和ui界面,然后按照下面的步骤打开viobot2重建完成的文件夹即可让colmap显示重建好地图：

![](image/image_open_sfm.png)

打开文件夹之后有一个对话框，根据下图中的说明按需选择即可，一般可以选择yes，方便查看关键帧之间的约束。
![](image/image_open_result2.png)


上一步选择了yes之后再选择.db文件和images文件夹，之后点save就完成了打开重建结果：

![](image/image_open_result3.png)

可以双击关键帧的相机图标可以查看每一帧的详细信息包括提取的点数、位姿关系、以及关联的关键帧等

![](image/image_view_kf.png)


