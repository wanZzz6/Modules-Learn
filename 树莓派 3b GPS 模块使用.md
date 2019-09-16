[toc]

---

[淘宝连接](https://wiki.52pi.com/index.php/USB-Port-GPS_Module_SKU:EZ-0048#How_to_use_it)

[USB-Port-GPS Module SKU:EZ-0048](https://wiki.52pi.com/index.php/USB-Port-GPS_Module_SKU:EZ-0048)

[接线方式（USB 版）](https://blog.csdn.net/qq_32384313/article/details/77744542)

[接线方式（串口版）](https://blog.csdn.net/qq_32384313/article/details/77745386)

![接线方式](https://images0.cnblogs.com/blog/485996/201411/082008090659506.png)

**引脚说明**

| 名称 | 说明                                                                 |
| ---- | -------------------------------------------------------------------- |
| VCC  | 电源（3.3V~5.0V）                                                    |
| GND  | 地                                                                   |
| TXD  | 模块串口发送脚（TTL 电平，不能直接接 RS232 电平!），可接单片机的 RXD |
| RXD  | 模块串口接收脚（TTL 电平，不能直接接 RS232 电平!），可接单片机的 TXD |
| PPS  | 时钟脉冲输出脚，接任意 GPIO 引脚                                     |

其中，PPS 引脚同时连接到了模块自带了的状态指示灯。PPS 指示灯（即 PPS 引脚），在默认条件下（没经过程序设置），有 2 个状态：
1， 常亮，表示模块已开始工作，但还未实现定位。
2， 闪烁（100ms 灭，900ms 亮），表示模块已经定位成功。
**注意：** 不建议使用 GPIO 引脚连接 GPS 模块，需要修改系统默认串口设置，最好需要一根 USB-to-TTL 线连接

## 测试

> cat /dev/ttyUSB2

## 一、console 测试

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

   > sudo cgps [-s ] 5]

# 二、GPIO 连接需要额外修改配置（关闭蓝牙对硬件串口的使用）

参考教程：

- https://blog.csdn.net/berryfish/article/details/60147631

- https://blog.csdn.net/Veritaz/article/details/89815205

- https://blog.csdn.net/qq_32384313/article/details/77745907

## 原因

**树莓派 3**上用户目前无法正常是使用 GPIO 中的 UART 串口(GPIO14&GPIO15),也就是说用户无论是想用串口来调试树莓派，还是想用 GPIO 中的串口来连接 GPS,蓝牙，XBEE 等等串口外设目前都是有问题的。

原因是树莓派 CPU 内部有两个串口，一个是**硬件串口**(官方称为 PL011 UART)，一个是**迷你串口**(官方成为 mini-uart)。在树莓派 2B/B+这些老版树莓派上，官方设计时都是将“**硬件串口**”分配给 GPIO 的 UART(GPIO14&GPIO15)，因此可以独立调整串口的速率和模式。而树莓派 3 的设计上，官方在设计时将硬件串口分配给了新增的蓝牙模块上，而将一个没有时钟源，必须由内核提供时钟参考源的“**迷你串口**”分配给了 GPIO 的串口，这样以来由于内核的频率本身是变化的，就会导致“**迷你串口**”的速率**不稳定**，这样就出现了无法正常使用的情况。

目前解决方法就是，关闭蓝牙对**硬件串口**的使用，将硬件串口重新恢复给 GPIO 的串口使用，也就意味着树莓派 3 的**板载蓝牙和串口，两者是无法兼得的。**

## 具体步骤

### 1. 关闭板载蓝牙功能

首先，打开你的 Terminal，输入一下语句：

> sudo systemctl disable hciuart

然后，编辑文档/lib/systemd/system/hciuart.service，命令如下：

> sudo nano /lib/systemd/system/hciuart.service

将文档中所有的 "ttyAMA0"改成"ttyS0"，**总共要修改两处**，修改好以后保存退出。

### 2.恢复串口使用并禁用控制台

首先，编辑文档 /boot/config.txt，命令如下:

> sudo nano /boot/config.txt

在文档的末尾，添加语句：

> dtoverlay=pi3-miniuart-bt

#### 注意

该语句中的"pi3-miniuart-bt"是在文件夹 /boot/overlays 中可以找到的。如果没有，你可以下载一个"pi3-miniuart-bt-overlay"文件并将其拷贝至/boot/overlays 文件夹中，并且将上面的语句更改为： dtoverlay=pi3-miniuart-bt-overlay  即可，具体可以参考该作者：http://ukonline2000.com/?p=880

接着，我们编辑文档 /boot/cmdline.txt，命令如下：

> sudo nano /boot/cmdline.txt

然后还需要删一个东西，把

> dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait

删除一部分最终变成

> dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait

这里我们要注意：该替换内容是针对于设置通用串口的，这个内容实际上是关闭了 serial console，因为只有这样方可使串口变为通用，即可以使树莓派连接外部设备。如果你是想用串口连接、登录以及控制树莓派，则需要 enable seiral console，具体方法可以[参考博客](http://www.briandorey.com/post/Raspberry-Pi-3-UART-Boot-Overlay-Part-Two)

最后，我们依次执行以下命令完成所有配置并重启：

    sudo apt-get update

    sudo apt-get upgrade

    sudo reboot

完成以上步骤后，我们现在可以通过`ttyAMA0`与外部设备进行连接了。

# 三、指令解析

## NMEA-0183 协议简介

NMEA-0183 协议采用 ASCII 码来传递 GPS 定位信息，我们称之为帧。

帧格式形如：\$aaccc,ddd,ddd,„,ddd\*hh(CR)(LF)

1. “\$”：帧命令起始位
2. aaccc：地址域，前两位为识别符（aa），后三位为语句名（ccc）
3. ddd„ddd：数据
4. “\*”：校验和前缀（也可以作为语句数据结束的标志）
5. hh：校验和（check sum），\$与\*之间所有字符 ASCII 码的校验和（各字节做异或运算，得到校验和后，再转换 16 进制格式的 ASCII 字符）
6. (CR)(LF)：帧结束，回车和换行符

![demo](https://images0.cnblogs.com/blog/485996/201411/082016074569921.png)

- 每行开头 2 字母

  - GN：全球导航卫星系统（GNSS-global navigationsatellite system）
  - BD：北斗导航卫星系统（COMPASS）

- 后续 3 个字母

  - GGA：GPS 定位信息时间、位置、定位数据
  - GLL：大地坐标信息，经纬度、UTC 时间和定位状态

  - GSA：当前卫星信息，接收机模式和卫星工作数据,包括位置和水平/竖直稀释精度等。稀释精度（Dilution of Precision）是个地理定位术语.一个接收器可以在同一时间得到许多颗卫星定位信息，但在精密定位上，只要四颗卫星讯号即已足够了

  - GSV：可见卫星信息，包括卫星 ID，海拔，仰角，方位角，信噪比（SNR）等

  - RMC：推荐定位信息，日期，时间，位置，方向，速度数据。是最常用的一个消息

  - VTG：地面速度信息方位角与对地速度

  - MSS：信噪比(SNR),信号强度，频率，比特率

  - ZDA：时间（UTC）和日期数据

  UTC 时间即协调世界时，相当于本初子午线(0 度经线)上的时间，北京时间比 UTC 早 8 个小时

## 指令讲解

### 1. \$GPGGA

（GPS 定位信息，Global Positioning System Fix Data）

\$GPGGA 语句的基本格式如下（其中 M 指单位 M，hh 指校验和，CR 和 LF 代表回车换行，下同）：

\$GPGGA,(1),(2),(3),(4),(5),(6),(7),(8),(9),M,(10),M,(11),(12)\*hh(CR)(LF)

(1) UTC 时间，格式为 hhmmss.ss；要换算成北京时间只需要加上 8 小时即可.
(2 )纬度，格式为 ddmm.mmmmm（**度分格式**）；
(3) 纬度半球，N 或 S（北纬或南纬）；
(4) 经度，格式为 dddmm.mmmmm（**度分格式**）；
(5) 经度半球，E 或 W（东经或西经）；
(6) GPS 状态，0=未定位，1=非差分定位，2=差分定位；
(7) 正在使用的用于定位的卫星数量（00~12）
(8) HDOP 水平精确度因子（0.5~99.9）
(9) 海拔高度（-9999.9 到 9999.9 米）+ 单位
(10) 大地水准面高度（-9999.9 到 9999.9 米） + 单位
(11) 差分时间（从最近一次接收到差分信号开始的秒数，非差分定位，此项为空）
(12) 差分参考基站标号（0000 到 1023，首位 0 也将传送，非差分定位，此项为空)

**举例如下：**

\$GPGGA,023543.00,2308.28715,N,11322.09875,E,1,06,1.49,41.6,M,-5.3,M,,\*7D

GGA 和 RMC 都会返回时间，GGA 的第一个参数<1>就是 UTC 时间，即协调世界时，格式为 hhmmss，**要换算成北京时间只需要加上 8 小时**即可；RMC 的<9>为 UTC 日期，格式为 ddmmyy（日月年）。下面列一条 RMC 返回的数据：

> \$GPRMC,125315.00,A,3853.70120,N,12133.61898,E,1.710,,081114,,,A\*7E

我们可以数一下，<1>对应的是 125315.00 也就是 UTC 时间 12:53:15，换算成北京时间就是 20:53:15；参数<9>为 081114，根据 dd/mm/yy 来算就是 14 年 11 月 08 日~

### 2. \$GPGSA（当前卫星信息）

\$GPGSA 语句的基本格式如下：

\$GPGSA,(1),(2),(3),(3),(3),(3),(3),(3),(3),(3),(3),(3),(3),(3),(4),(5),(6)\*hh(CR)(LF)

(1) 模式，M = 手动，A = 自动。
(2) 定位类型，1=未定位，2=2D 定位，3=3D 定位。
(3) 正在用于定位的卫星号（01~32）
(4) PDOP 综合位置精度因子（0.5-99.9）
(5) HDOP 水平精度因子 1（0.5-99.9）
(6) VDOP 垂直精度因子（0.5-99.9）
举例如下：
\$GPGSA,A,3,26,02,05,29,15,21,,,,,,,2.45,1.49,1.94\*0E
注 1：精度因子值越小，则准确度越高。

### 3. \$GPGSV

（可见卫星数，GPS Satellites in View）

\$GPGSV 语句的基本格式如下：
\$GPGSV, (1),(2),(3),(4),(5),(6),(7),...,(4),(5),(6),(7)\*hh(CR)(LF)

(1) GSV 语句总数。
(2) 本句 GSV 的编号。
(3) 可见卫星的总数（00~12，前面的 0 也将被传输）。
(4) 卫星编号（01~32，前面的 0 也将被传输）。
(5) 卫星仰角（00~90 度，前面的 0 也将被传输）。
(6) 卫星方位角（000~359 度，前面的 0 也将被传输）
(7) 信噪比（00~99dB，没有跟踪到卫星时为空）。
注：每条 GSV 语句最多包括四颗卫星的信息，其他卫星的信息将在下一条$GPGSV语句中输出。
举例如下：
\$GPGSV,3,1,12,02,39,117,25,04,02,127,,05,40,036,24,08,10,052,*7E
\$GPGSV,3,2,12,09,35,133,,10,01,073,,15,72,240,22,18,05,274,*7B
\$GPGSV,3,3,12,21,10,316,31,24,16,176,,26,65,035,42,29,46,277,18\*7A

### 4. \$GPRMC

（推荐定位信息，Recommended Minimum Specific GPS/Transit Data）
\$GPRMC 语句的基本格式如下：
\$GPRMC,(1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)\*hh(CR)(LF)

(1) UTC 时间，hhmmss（时分秒）
(2) 定位状态，A=有效定位，V=无效定位
(3) 纬度 ddmm.mmmmm（度分）
(4) 纬度半球 N（北半球）或 S（南半球）
(5) 经度 dddmm.mmmmm（度分）
(6) 经度半球 E（东经）或 W（西经）
(7) 地面速率（000.0~999.9 节）
(8) 地面航向（000.0~359.9 度，以真北方为参考基准）
(9) UTC 日期，ddmmyy（日月年）
(10)磁偏角（000.0~180.0 度，前导位数不足则补 0）
(11) 磁偏角方向，E（东）或 W（西）
(12) 模式指示（A=自主定位，D=差分，E=估算，N=数据无效）
举例如下：
\$GPRMC,023543.00,A,2308.28715,N,11322.09875,E,0.195,,240213,,,A\*78

### 5，\$GPVTG（地面速度信息，Track Made Good and Ground Speed）

\$GPVTG 语句的基本格式如下：
\$GPVTG,(1),T,(2),M,(3),N,(4),K,(5)\*hh(CR)(LF)

(1) 以真北为参考基准的地面航向（000~359 度，前面的 0 也将被传输）
(2) 以磁北为参考基准的地面航向(000~359 度，前面的 0 也将被传输)
(3) 地面速率(000.0~999.9 节，前面的 0 也将被传输)
(4) 地面速率(0000.0~1851.8 公里/小时，前面的 0 也将被传输)
(5) 模式指示（A=自主定位，D=差分，E=估算，N=数据无效）
举例如下：
\$GPVTG,,T,,M,0.195,N,0.361,K,A\*2A

### 6. \$GPGLL（定位地理信息，Geographic Position）

\$GPGLL 语句的基本格式如下：
\$GPGLL,(1),(2),(3),(4),(5),(6),(7)\*hh(CR)(LF)

(1) 纬度 ddmm.mmmmm（度分）
(2) 纬度半球 N（北半球）或 S（南半球）
(3) 经度 dddmm.mmmmm（度分）
(4) 经度半球 E（东经）或 W（西经）
(5) UTC 时间：hhmmss（时分秒）
(6) 定位状态，A=有效定位，V=无效定位
(7) 模式指示（A=自主定位，D=差分，E=估算，N=数据无效）
举例如下：
\$GPGLL,2308.28715,N,11322.09875,E,023543.00,A,A\*6A

### 7. \$GPZDA（当前时间信息）

\$GPZDA 语句的基本格式如下：
\$GPZDA,(1),(2),(3),(4),(5),(6)\*hh(CR)(LF)

(1) UTC 时间：hhmmss（时分秒）
(2) 日
(3) 月
(4) 年
(5) 本地区域小时（NEO-6M 未用到，为 00）
(6) 本地区域分钟（NEO-6M 未用到，为 00）
举例如下：
\$GPZDA,082710.00,16,09,2002,00,00\*64

### 8. 校验

NMEA-0183 协议命令帧部分就介绍到这里，接下来我们看看 NMEA-0183 协议的校验，通过前面的介绍，我们知道每一帧最后都有一个 hh 的校验和，该校验和是通过计算$与*之间所有字符ASCII码的异或运算得到，将得到的结果以ASCII字符表示就是该校验（hh）。
例如语句：$GPZDA,082710.00,16,09,2002,00,00\*64，校验和（红色部分参与计算）计算方法为：
0X47xor 0X50xor 0X5Axor 0X44xor 0X41xor 0X2Cxor 0X30xor 0X38xor 0X32xor 0X37xor 0X31xor 0X30xor 0X2Exor 0X30xor 0X30xor 0X2Cxor 0X31xor 0X36xor 0X2Cxor 0X30xor 0X39xor 0X2Cxor 0X32xor 0X30xor 0X30xor 0X32xor 0X2Cxor 0X30xor 0X30xor 0X2Cxor 0X30xor 0X30
得到的结果就是 0X64，用 ASCII 表示就是 64。
NMEA-0183 协议我们就介绍到这里，了解了该协议，我们就可以编写单片机代码，解析 NMEA-0183 数据，从而得到 GPS 定位的各种信息了。

## 经纬度计算

同样的，GGA 和 RMC 都会返回经纬度；GGA 的<2>\~<5>和 RMC 的<3>\~<6>含义及格式相同，下面还是以 RMC 来做示范（看看上一点的 RMC 数据）。找到 RMC 参数<3>\~<6>，分别是
<3> |3853.70120 |纬度（ddmm.mmmm）|
---|---|---|
<4> |N| 纬度半球（N 北半球、S 南半球）
<5> |12133.61898| 经度（dddmm.mmmm）
<6> |E| 经度半球（E 东经、W 西经）

纬度和经度都是“度分”格式，dd 代表度，m 代表分，那么显而易见：

纬度信息：3853.70120，就是 38 度和 53.70120 分。

分换算成度只需要除以 60，也就是 53.70120 / 60 = 0.89502，那么 3853.70120 的含义就是 38.89502°

---

# 三、使用 python 解析 GPS 数据

## pynmea2 输出实时经纬度信息

```python
import serial
import pynmea2


def parseGPS(string):
   if string.find('GGA') > 0:  ## 推荐定位 RMC（时间信息更完整）
       msg = pynmea2.parse(string)
       print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" %
             (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir,
              msg.altitude, msg.altitude_units))


serialPort = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5)

# a = serialPort.read(300).decode()
# print(a)

serialPort.flushInput()

while True:
   string = serialPort.readline().decode()
   parseGPS(string)
```

## gps 模块使用 (先开启 GPSD 服务， cgps -s)

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

## 输出 TPV-时间位置速度信息

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

## 输出卫星信息

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
