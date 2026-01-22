# Common Issues

## Viobot DHCP Network Configuration

DHCP is generally not recommended. In fixed deployments, it is better to keep the device IP static so you do not need to search for the device IP every time.

If your use case requires DHCP to assign the device IP, it is possible.

SSH into the device and run:

```bash
sudo cp /etc/netplan/01-netcfg.yaml /etc/netplan/01-netcfg.yaml.backup # backup
sudo vim /etc/netplan/01-netcfg.yaml
```

Set `dhcp4` to `yes`, comment out the following lines (mind the indentation), then save and exit.

![](image/image_f-ZSti1D88_y117bGxyF-.png)

## Time Synchronization with Other Controllers

For network time synchronization, you can use NTP: configure one device as an NTP server and the other as a client.

## RTK Time Synchronization

If you have a Viobot2 version with GNSS, connecting the GNSS antenna and using RTK means time synchronization is already available (GNSS + RTK share satellite time). If you only use an external RTK module, you need to connect the RTK PPS signal to the Viobot2 mainboard.

## System Time Abnormalities

1. For network time synchronization you can use `systemd-timesyncd`. By default, when network is available, Viobot2 will sync network time automatically.
2. If the system time keeps jumping back and forth when both RTK and GNSS are connected, you can try stopping network time sync and only use GPS time:

```bash
sudo systemctl stop systemd-timesyncd
```

## If UI Operation Is Not Convenient

The fastest way to use Viobot2 is via the client UI. Basic visual odometry can also be controlled via the SDK (HTTP protocol) or ROS communication. Some HM Inside mapping features still require UI.

## Mapping Progress Bar Jumps to 100% Immediately

In most cases, the mapping directory is incorrect: the path does not exist or the required mapping data is missing. Check that the mapping path matches the BoW save path and that the BoW files are valid. If everything looks correct, try updating to the latest firmware and retry.

## How to Check Whether Relocalization Succeeds

After relocalization is triggered, `/baton/stereo3/odom_relo` will be published. See **HM Mapping & Relocalization** -> **How to Tell Whether Relocalization Is Triggered** for details.

