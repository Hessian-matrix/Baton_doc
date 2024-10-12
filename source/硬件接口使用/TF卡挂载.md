# Viobot的TF卡挂载

将TF卡插到Viobot的卡槽里面，注意TF卡的存储速度。

### 1.查看TF卡

```bash
lsblk
```

![](image/image_d4ZNuIQK0s.png)

可以看到新增了一个119.4G的存储块，也就是刚插进去的TF卡，名字是`mmcblk1`

Viobot系统不支NTFS格式的TF卡，需要存储大文件的化我们可以把TF卡格式化为EXT4格式，注意如果使用的内存卡不是空的，格式化之前，请自行备份保存好自己的文件。

### 2.格式化TF卡

```bash
sudo mkfs.ext4 /dev/mmcblk1 
```

![](image/image_EIZAScmWIk.png)

### 3.挂载

```bash
sudo mkdir /mnt/tfcard
sudo mount /dev/mmcblk1 /mnt/tfcard
```

查看挂载

```bash
df -h
```

![](image/image_iaJXUroOwO.png)

可以看到/dev/mmcblk1已经被正确挂载到了/mnt/tfcard

### 4.卸载

```bash
sudo umount /dev/mmcblk1
```

### 5.开机自动挂载

挂载TF卡是一次性的，如果设备重启就需要重新挂载，如果需要开机挂载TF卡的话可以把先确保已经创建好了/mnt目录下的挂载文件夹，再把`mount /dev/mmcblk1 /mnt/tfcard`写到`"/etc/user_setup/performance.sh"`文件下的最后一行里面保存退出，重启即可。

![](image/image_rTjitNJof3.png)
