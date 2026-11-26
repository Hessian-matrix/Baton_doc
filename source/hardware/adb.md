# 设备adb

adb软件下载[https://wwbnp.lanzoum.com/ie6QE3e7fv8j](https://wwbnp.lanzoum.com/ie6QE3e7fv8j)

先通过USB-type-c接口连接Viobot2设备，此接口仅为adb，不能使用otg.

打开cmd命令行

进到adb.exe路径下

```bash
adb.exe devices
```

软件会自动搜索设备，将搜索到的设备的唯一码打出来

如ed22c951f81d1e23

```bash
adb.exe -s ed22c951f81d1e23   shell
```

连接成功后会以root用户连接设备

修改ip

```bash
vim /etc/netplan/01-netcfg.yaml
```

![](image/image_Qrj8Bd6rz_.png)
