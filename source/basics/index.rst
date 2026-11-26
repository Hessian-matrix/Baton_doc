基本功能介绍及使用
======================================

本栏目集中说明 VIObot2 的算法、数据、系统配置和日常维护，是完成设备接入后进一步开发的主要参考。

内容概览
----------------

- **算法能力：** Stereo3 / Stereo4、回环检测、重定位和双目深度。
- **数据接口：** 图像、IMU、视觉里程计、点云、GNSS 与融合位姿。
- **工程配置：** 算法控制、NTP 时间同步和面向实际项目的参数配置。
- **运行维护：** 数据包录制、版本查看与系统更新。

推荐入口
----------------

- :doc:`认识核心功能 <core-features>`
- :doc:`了解输出数据 <data-reference>`
- :doc:`控制视觉算法 <algorithm-control>`
- :doc:`工程应用配置 <deployment-settings>`

.. toctree::
   :hidden:
   :maxdepth: 2

   core-features
   data-reference
   algorithm-control
   stereo4
   loop-closure
   relocalization
   stereo-depth
   gnss
   data-recording
   ntp
   deployment-settings
   updates
