# 飞控配置

## 配置前提

本组合产品支持 ArduPilot/ArduCopter 和 PX4。开始前应通过 Mission Planner 或 QGroundControl 导出完整参数，并记录飞控型号、固件版本和 Lite 实际连接的 UART。

用户必须先完成：

- 机架、IMU、罗盘、遥控器、飞行模式和失效保护等基础初始化。
- Lite 与飞控的 TX/RX 交叉连接和可靠共地。
- 将飞控对应 UART 配置为 MAVLink2、921600 bps。
- 确认该 UART 未被其他外设占用，并保持飞控未解锁。

Lite 设备名与飞控端口编号没有对应关系。必须按飞控接线图确认实际 UART，再选择对应的 `SERIALn_*` 或 `MAV_x_*` 参数。

## Web 飞控配置模板

Web 的“飞控配置”支持 ArduPilot/ArduCopter EKF3 接入。模板不负责飞控基础初始化，也不能在串口尚未连通时修正串口协议和波特率。

页面提供：

| Web 项 | 用途 |
| --- | --- |
| EKF3 来源模板 | 选择视觉使用 SRC2 或 SRC3，以及使用视觉航向或罗盘航向 |
| EKF 来源切换 RC 通道 | 指定三段开关使用的遥控器通道 |
| 安全模式 RC 通道 | 指定视觉异常时的人工安全控制通道 |

操作顺序：

1. 选择模板和两个不同的 RC 通道。
2. 点击“探测当前配置”，检查当前值、目标值、待修改项和综合判定。
3. 确认飞控未解锁，点击“备份并应用配置”。
4. 下载修改前和修改后的参数备份。
5. 按页面提示重启飞控，并点击顶部“重启 Bridge”。
6. 再次“探测当前配置”，确认所有接入项目通过。

选择 RC 通道前，应在 Mission Planner 中确认对应通道未承担飞行模式、返航、急停等关键功能。

## ArduPilot / ArduCopter

### MAVLink 串口与 GPS

以下以 `SERIAL1` 为例。使用其他 UART 时，应整体替换为对应的 `SERIALn_PROTOCOL` 和 `SERIALn_BAUD`。

| 参数 | 基线值 | 说明 |
| --- | ---: | --- |
| `SERIAL1_PROTOCOL` | `2` | 使用 MAVLink2 |
| `SERIAL1_BAUD` | `921` | 表示 921600 bps |
| `GPS1_TYPE` | `14` | GPS1 使用 MAVLink GPS |
| `GPS2_TYPE` | `0` | 仅在没有第二个 GPS 时禁用 GPS2 |
| `GPS_PRIMARY` | `0` | 单 GPS 配置优先 GPS1 |
| `GPS_AUTO_SWITCH` | `0` | 单 GPS 调试时固定主 GPS |

旧版固件可能显示 `GPS_TYPE` 和 `GPS_TYPE2`。参数 `14` 应在当前 Mission Planner 中显示为 MAVLink/MAV；若枚举含义不同，应先核对固件版本。

> 飞控 UART 必须配置为 MAVLink2，不能配置为直连 GPS 或 UBX。

### EKF3 与视觉定位

| 参数 | 基线值 | 说明 |
| --- | ---: | --- |
| `EK3_ENABLE` | `1` | 启用 EKF3 |
| `AHRS_EKF_TYPE` | `3` | AHRS 使用 EKF3 |
| `EK2_ENABLE` | `0`（参数存在时） | 使用 EKF3 基线 |
| `VISO_TYPE` | `1` | 使用 MAVLink 视觉里程计 |
| `EK3_SRC_OPTIONS` | `0` | 使用来源组切换基线 |
| `VISO_DELAY_MS` | `10`（初始值） | 最终按飞控日志标定 |
| `VISO_QUAL_MIN` | `0` | 拒绝无效视觉质量 |

`VISO_ORIENT` 必须与实际相机安装和飞控固件约定一致。它与 Web 的“相机安装方向”（`camera_orientation`）不是同一参数，不能直接复制数值。

### EKF 来源组参考

以下基线将 SRC1 用于 GPS、SRC3 用于视觉：

| 来源字段 | SRC1：GPS | SRC2：未用 | SRC3：视觉 |
| --- | ---: | ---: | ---: |
| `POSXY` | `3` | `0` | `6` |
| `POSZ` | `1` | `1` | `1` |
| `VELXY` | `3` | `0` | `6` |
| `VELZ` | `3` | `0` | `6` |
| `YAW` | `1` | `1` | `6` 或 `1` |

- `SRC3_YAW=6` 使用视觉航向。
- `SRC3_YAW=1` 使用罗盘航向，应选择 Web 中对应的“罗盘航向”模板。

若要把视觉放在 SRC2，应直接选择 Web 中相应模板，不要只修改单个 `EK3_SRCx_*` 参数。

### 遥控器来源切换

选择一个空闲三段通道作为“EKF 来源切换 RC 通道”。应用模板后，对应 `RCx_OPTION` 为 `90`。

| 开关位置 | 典型 PWM | 基线来源 |
| --- | ---: | --- |
| 低挡 | 1000 | SRC1，GPS |
| 中挡 | 1500 | SRC2 |
| 高挡 | 2000 | SRC3，视觉 |

实际来源取决于所选模板。必须在 Mission Planner 遥控器页面确认三个挡位均能稳定识别。来源切换开关不得与 Stabilize、AltHold、Loiter 等飞行模式开关复用。

### 写入后核对

1. 重启飞控并重新读取完整参数。
2. 在 Web 的“飞控配置”中再次“探测当前配置”。
3. 在未解锁状态下验证 GPS、视觉和 RC 来源切换。
4. 只有地面方向检查和 EKF 健康状态均通过后，才进入飞行验证。

不得通过关闭关键解锁检查、伪造定位状态或放宽质量门限来绕过未完成的验证。

## PX4

PX4 当前不使用 Web 的 ArduPilot 模板，应在 QGroundControl 中手动配置。

### MAVLink 串口

| 参数族 | 配置要求 | 说明 |
| --- | --- | --- |
| `MAV_x_CONFIG` | 选择 Lite 实际连接的 TELEM/UART | `x` 为所用 MAVLink 实例 |
| `MAV_x_MODE` | 选择适合外部计算机的模式 | 枚举名称随版本变化 |
| `SER_TELn_BAUD` | `921600` | `n` 对应实际 TELEM 端口 |
| MAVLink 版本 | MAVLink2 | 必须与 Lite 设置一致 |

### EKF2 外部视觉与 GNSS

| PX4 参数 | 配置要求 |
| --- | --- |
| `EKF2_EV_CTRL` | 启用任务需要的外部视觉位置、速度和可选航向融合 |
| `EKF2_EV_DELAY` | 根据 ULog 标定视觉延迟 |
| `EKF2_EV_POS_X/Y/Z` | 填写视觉传感器相对机体的实测安装偏移 |
| `EKF2_GPS_CTRL` | 启用任务需要的 GNSS 位置、速度和高度融合 |
| `EKF2_GPS_POS_X/Y/Z` | 按 PX4 机体系填写 D20 天线位置 |
| `EKF2_HGT_REF` | 根据任务明确选择高度基准 |

旧版 PX4 可能使用 `EKF2_AID_MASK`。具体参数名和枚举以当前 QGroundControl 显示为准。

完成配置后，应在 QGroundControl 中确认 GPS、External Vision、local position、速度和航向持续更新，并通过 ULog 检查估计器实际采用情况和创新量。完成地面动作与低高度分级验证后，才可逐步扩大飞行范围。
