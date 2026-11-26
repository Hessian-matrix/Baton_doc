ROS 多机通信
======================================

本栏目说明 VIObot2 与开发主机、机器人主控之间的 ROS1 和 ROS2 多机通信配置。配置前应确保设备处于同一网络且能够互相 ``ping`` 通。

核心内容
----------------

- ROS1 主从机：统一 ``ROS_MASTER_URI`` 并正确设置各主机地址。
- ROS1 多 Master：在多个 ROS Master 之间同步所需话题。
- ROS2 多机通信：通过相同的 Domain ID 和网络配置发现节点。

推荐入口
----------------

- :doc:`配置 ROS1 主从机 <ros1-master-client>`
- :doc:`配置 ROS2 多机通信 <ros2-multi-host>`

.. toctree::
   :hidden:
   :maxdepth: 2

   ros1-master-client
   ros1-multi-master
   ros2-multi-host
