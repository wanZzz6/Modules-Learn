> Mac 系统请切换到root用户下使用

- `-vv`, `-vvv`  : 打印详细信息
- `udp\tcp`：例如：`udp port 5060 or udp portrange 10500-11652  `
- tcp、ip、icmp、arp、rarp 和 tcp、udp、icmp这些选项等都要放到第一个参数的位置，用来过滤数据报的类型
- `-i eth1` : 只抓经过网卡eth1的包，取`-i any` 可捕获所有网卡数据包
- `-t` : 不显示时间戳
- `-s 0` : 抓取数据包时默认抓取长度为68字节。加上`-s 0` 后可以抓到完整的数据包
- `-c 100` : 只抓取100个数据包
- `dst port ! 22` : 不抓取目标端口是22的数据包
- `src net 192.168.1.0/24` : 数据包的源网络地址为192.168.1.0/24
- `portrange` : 指定端口范围，一般前面需要配合其他参数，如 `udp portrange 10000-10100`
- `-w ./target.cap` : 保存成cap文件，方便用wireshark分析
- `host` 指定 ip 收到和发出的所有分组   `tcpdump host 192.168.131.128`  



**示例**：

- 直接启动tcpdump将监视第一个网络接口上所有流过的数据包。

  ```sh
  tcpdump
  ```

- 截获所有192.168.131.128主机收到的和发出的所有的分组

  ```sh
  tcpdump host 192.168.131.128
  ```

- 截获主机192.168.131.130和主机192.168.131.128的通信

  ```sh
  tcpdump host 192.168.131.130 and 192.168.131.128
  tcpdump -n -i eth1 host 192.168.131.130 and host 192.168.131.128
  ```
  




```sh
tcpdump tcp -i eth1 -t -s 0 -c 100 and dst port ! 22 and src net 192.168.1.0/24 -w ./target.cap
```

```sh
tcpdump -i eth0 udp port 5060 or tcp port 5060 or udp portrange 30000-30400  or tcp portrange 30000-30400

tcpdump -i eth0 port 5060 or portrange 30000-30100

tcpdump -i eno3 udp port 20080 or tcp port 20080

tcpdump -i eno4 host 59.206.39.116
nmcli connection show
```

