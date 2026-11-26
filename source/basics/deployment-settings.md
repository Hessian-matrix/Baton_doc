# 工程应用上的相关配置


## mask屏蔽遮挡

将viobot2安装到各种设备上时在viobot2的画面中可能会有设备本身的侵入，从而对viobot2的算法造成干扰，这时候就需要配置镜头的mask来屏蔽这些干扰,需要使用Photoshop等软件根据镜头画面遮挡情况制作一张像下面的有黑白区域的图片，这里mask是留白区域即表示无遮挡的画面区域，黑色区域为屏蔽掉不处理的区域。如下就是一张 鱼眼相机的mask图像。


![alt text](image/gengral_mask.png)


制作好一张这种图像之后通过ssh将其上传到viobot2机器内部存储有两种方式配置mask生效，一种是UI上配置路径，还有是通过编辑配置文件的方式。先来第一种UI配置的方式：设置-》loop-》mask路径，填入正确的路径重启相机即可，第二种是编辑`/root/Baton/install/baton/share/baton/config/sys.yaml`文件里有个`mask_path`的配置项。


![alt text](image/1760929514231.png)

~~~yaml
print_queue: false
use_imu: 2
gnss_select: 1
load_previous_pose_graph: false
add_keyframe_mode: 1
pose_graph_save_path: /home/user/pose_graph/
gnss_T_imu:
  data:
    - 0
    - 0
    - 0
relocalization: false
mask_path: /root/Baton/install/share/baton/config/s3_fisheye_mask.png
~~~