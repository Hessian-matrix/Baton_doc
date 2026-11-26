硬件接口使用
======================================

本栏目说明 VIObot2 的外部接口、存储和网络连接方法。接线前请先核对接口电平、供电要求与线序，避免损坏设备或外设。

接口能力
----------------

- UART、I2C 和 CAN 外设通信。
- TF 卡挂载与数据存储。
- 有线网卡、Wi-Fi 和 ADB 调试连接。

推荐入口
----------------

- :doc:`查看设备接口总览 <interfaces>`
- :doc:`配置串口通信 <serial>`
- :doc:`配置网络连接 <network-wifi>`

.. warning::

   格式化 TF 卡会清除卡内数据，请在操作前完成备份。

.. toctree::
   :hidden:
   :maxdepth: 2

   interfaces
   network-wifi
   sd-card
   serial
   i2c
   can
   adb
