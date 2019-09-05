[toc]

---

[淘宝连接](https://wiki.52pi.com/index.php/USB-Port-GPS_Module_SKU:EZ-0048#How_to_use_it)

[USB-Port-GPS Module SKU:EZ-0048](https://wiki.52pi.com/index.php/USB-Port-GPS_Module_SKU:EZ-0048)

[接线方式（USB 版）](https://blog.csdn.net/qq_32384313/article/details/77744542)

[接线方式（串口版）](https://blog.csdn.net/qq_32384313/article/details/77745386)

![](https://images0.cnblogs.com/blog/485996/201411/082008090659506.png)

**注意：** 不建议使用 GPIO 引脚连接 GPS 模块，容易出问题，最好需要一根 USB-to-TTL 线连接

## 测试

> cat /dev/ttyUSB2

## 用法

### 命令行方式

1. 安装 GPS 模块的包

   > sudo apt-get update && sudo apt-get -y install gpsd gpsd-clients python-gps

2. 启动 gps 服务并对其进行控制

   - 开机启动: sudo systemctl enable gpsd.socket
   - 启用服务: sudo systemctl start gpsd.socket
   - 重启服务: sudo systemctl restart gpsd.socket
   - 检查运行状态: sudo systemctl status gpsd.socket

3. 修改配置文件（可选）

   在 /dev/default/gpsd 中

   - 修改串口地址

     > DEVICES="/dev/ttyUSB2"

   - 重启服务

     > sudo systemctl restart gpsd.socket

4. 查看当前 GPS 信息

   > sudo sgps [-s ] 5]

### GPIO 连接需要额外修改配置（关闭蓝牙对硬件串口的使用）

参考：https://blog.csdn.net/Veritaz/article/details/89815205

参考：https://blog.csdn.net/qq_32384313/article/details/77745907

**树莓派 3**上用户目前无法正常是使用 GPIO 中的 UART 串口(GPIO14&GPIO15),也就是说用户无论是想用串口来调试树莓派，还是想用 GPIO 中的串口来连接 GPS,蓝牙，XBEE 等等串口外设目前都是有问题的。

原因是树莓派 CPU 内部有两个串口，一个是**硬件串口**(官方称为 PL011 UART)，一个是**迷你串口**(官方成为 mini-uart)。在树莓派 2B/B+这些老版树莓派上，官方设计时都是将“**硬件串口**”分配给 GPIO 的 UART(GPIO14&GPIO15)，因此可以独立调整串口的速率和模式。而树莓派 3 的设计上，官方在设计时将硬件串口分配给了新增的蓝牙模块上，而将一个没有时钟源，必须由内核提供时钟参考源的“**迷你串口**”分配给了 GPIO 的串口，这样以来由于内核的频率本身是变化的，就会导致“**迷你串口**”的速率不稳定，这样就出现了无法正常使用的情况。

目前解决方法就是，关闭蓝牙对**硬件串口**的使用，将硬件串口重新恢复给 GPIO 的串口使用，也就意味着树莓派 3 的**板载蓝牙和串口，两者是无法兼得的。**

#### 精简版解决方案

方案一：

    1.  设置里打开硬件串口，关闭串口控制台调试

    2.  sudo nano /boot/config.txt 加上 dtoverlay=pi3-miniuart-bt

方案二：

    1. 设置里打开硬件串口，关闭串口控制台调试
    2. sudo nano /boot/config.txt 加上 dtoverlay=pi3-disable-bt

#### 详细版

##### 先启用串口

    > ls -l /dev

看到的应该只有 serial1 -> ttyAMA0

然后在设置中启用串口，会发现 /dev 目录下变成了两个：
serial0 -> ttyS0 和 serial1 ->ttyAMA0
（ps. 设置中启用串口相当于在 /boot/config.txt 里面加上了一句 enable_uart=1
）
但是现在是不可使用的，因为树莓派上引出的 TX 和 RX 口(serial0)分配给了 ttyS0，我们想要的是 serial0 -> ttyAMA0

##### 禁用蓝牙

因为蓝牙也使用硬件串口，所以我们在 /boot/config.txt 里面加上

> dtoverlay=pi3-disable-bt

ttyAMA0 得以释放，这时候树莓派也自动交换了 ttyAMA0 和 ttyS0，把 serial0 分配给了 ttyAMA0 。

网上还有一种解决方案是 sudo nano /boot/config.txt 加上 dtoverlay=pi3-miniuart-bt 不再赘述

##### 禁用控制台

最后，硬件串口为原串口控制台使用，为避免冲突，在设置里禁用串口控制台
如果非要用 bash 来禁用：

```bash
sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service
```

然后还需要删一个东西，把

> dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait

删除一部分最终变成

> dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait

## 标识说明

![](https://images0.cnblogs.com/blog/485996/201411/082016074569921.png)

- 每行开头 2 字母

  - GN：全球导航卫星系统（GNSS-global navigationsatellite system）
  - BD：北斗导航卫星系统（COMPASS）

- 后续字母

  - GGA：GPS 定位信息时间、位置、定位数据
  - GLL：经纬度,UTC 时间和定位状态

  - GSA：当前卫星信息，接收机模式和卫星工作数据,包括位置和水平/竖直稀释精度等。稀释精度（Dilution of Precision）是个地理定位术语.一个接收器可以在同一时间得到许多颗卫星定位信息，但在精密定位上，只要四颗卫星讯号即已足够了

  - GSV：可见卫星信息，包括卫星 ID，海拔，仰角，方位角，信噪比（SNR）等

  - RMC：推荐定位信息，日期，时间，位置，方向，速度数据。是最常用的一个消息

  - VTG：地面速度信息方位角与对地速度

  - MSS：信噪比(SNR),信号强度，频率，比特率

  - ZDA：时间和日期数据

### GGA 和 RMC 的时间

来看一下 GGA 和 RMC 返回的格式：

> \$GPGGA,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,M,<10>,M,<11>,<12>\*hh<CR><LF>

> \$GPRMC,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,<10>,<11>,<12>\*hh<CR><LF>

GGA 和 RMC 都会返回时间，他们的第一个参数<1>就是 UTC 时间，即协调世界时，格式为 hhmmss，要换算成北京时间只需要加上 8 小时即可；RMC 的<9>为 UTC 日期，格式为 ddmmyy（日月年）。下面列一条 RMC 返回的数据：

> \$GPRMC,125315.00,A,3853.70120,N,12133.61898,E,1.710,,081114,,,A\*7E

我们可以数一下，<1>对应的是 125315.00 也就是 UTC 时间 12:53:15，换算成北京时间就是 20:53:15；参数<9>为 081114，根据 dd/mm/yy 来算就是 14 年 11 月 08 日~

### 经纬度计算

同样的，GGA 和 RMC 都会返回经纬度；GGA 的<2>\~<5>和 RMC 的<3>\~<6>含义及格式相同，下面还是以 RMC 来做示范（看看上一点的 RMC 数据）。找到 RMC 参数<3>\~<6>，分别是
<3> |3853.70120 |纬度（ddmm.mmmm）|
---|---|---|
<4> |N| 纬度半球（N 北半球、S 南半球）
<5> |12133.61898| 经度（dddmm.mmmm）
<6> |E| 经度半球（E 东经、W 西经）

纬度和经度都是“度分”格式，dd代表度，m代表分，那么显而易见：

纬度信息：3853.70120，就是38度和53.70120分。

分换算成度只需要除以60，也就是 53.70120 / 60 = 0.89502，那么3853.70120的含义就是38.89502° 

---

## 使用 python 解析 GPS 数据

### pynmea2 输出实时经纬度信息

```python
import serial
import pynmea2


def parseGPS(string):
    if string.find('GGA') > 0:
        msg = pynmea2.parse(string)
        print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" %
              (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir,
               msg.altitude, msg.altitude_units))


serialPort = serial.Serial(get_com_devices()[0], 9600, timeout=0.5)

# a = serialPort.read(300).decode()
# print(a)

serialPort.flushInput()

while True:
    string = serialPort.readline().decode()
    parseGPS(string)
```

### gps 模块使用 (先开启 GPSD 服务， cgps -s)

参考: https://gpsd.gitlab.io/gpsd/gpsd_json.html

```python
from gps import *
import time

session = gps(mode=WATCH_ENABLE)
try:
    while True:
        report = next(session)
        if report['class'] == 'VERSION':
            print('connect GPS successfully')
        if report['class'] == 'DEVICES':
            print('searching satellite ....')
        if report['class'] == 'WATCH':
            print('search satellite successfully')
        if report['class'] == 'TPV':
            print('Latitude:   ', report.lat)
            print('Longitude:  ', report.lon)
        if report['class'] == 'SKY':
            print('satellites NO.', len(report.satellites))
        time.sleep(3)
except StopIteration:
    print("GPSD has terminated")
```

### 输出 TPV-时间位置速度信息

```python
from gps import *
import time

gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
print('latitude\tlongitude\ttime utc\t\t\taltitude\tepv\tept\tspeed\tclimb')

try:
    while True:
        report = next(gpsd)
        if report['class'] == 'TPV':
            print(getattr(report, 'lat', 0.0), "\t", end=' ')
            print(getattr(report, 'lon', 0.0), "\t", end=' ')
            print(getattr(report, 'time', ''), "\t", end=' ')
            print(getattr(report, 'alt', 'nan'), "\t\t", end=' ')
            print(getattr(report, 'epv', 'nan'), "\t", end=' ')
            print(getattr(report, 'ept', 'nan'), "\t", end=' ')
            print(getattr(report, 'speed', 'nan'), "\t", end=' ')
            print(getattr(report, 'climb', 'nan'), "\t")
            time.sleep(1)
except (KeyboardInterrupt, SystemExit):  #when you press ctrl+c
    print("Done.\nExiting.")
```

### 输出卫星信息

```python
#! /usr/bin/python

from gps import *
import time
import os

gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

try:
    while True:
        report = gpsd.next()
        if report['class'] == 'SKY':
            os.system('clear')
            print (' Satellites (total of', len(gpsd.satellites), ' in view)')
            for i in gpsd.satellites:
                print ('t', i)

            print('\n\n')
            print(
                'PRN = PRN ID of the satellite. 1-63 are GNSS satellites, 64-96 are GLONASS satellites, 100-164 are SBAS satellites'
            )
            print('E = Elevation in degrees')
            print('As = Azimuth, degrees from true north')
            print('ss = Signal stength in dB')
            print('used = Used in current solution?')

        time.sleep(1)

except (KeyboardInterrupt, SystemExit):  #when you press ctrl+c
    print "Done.\nExiting."
```
