## 1. 查看所有的网络连接

显示所有活动的TCP和UDP连接以及监听端口

```sh
netstat -ano
```

下面是命令输出中各个部分的含义：

- **Proto** (Protocol): 显示协议类型（如 TCP 或 UDP）。
- **Local Address** (本地地址): 显示本地计算机上的 IP 地址和端口号。
- **Foreign Address** (远程地址): 显示远程计算机的 IP 地址和端口号。
- **State** (状态): 显示连接的状态（例如，LISTENING、ESTABLISHED、TIME_WAIT 等）。
- **PID or Process ID** (进程ID): 显示与该连接或监听端口相关联的进程的标识符。

### 1.1 输出示例解释

假设你运行了 `netstat -ano` 并得到了以下输出：

```
Active Connections
 Proto   Local Address          Foreign Address        State           PID
 ------  -------------------    -------------------    -------         ----
 TCP     192.168.1.100:80      192.168.1.50:53678     ESTABLISHED     4128
 TCP     192.168.1.100:443     192.168.1.50:53680     LISTENING       1234
 TCP     192.168.1.100:443     192.168.1.50:53681     TIME_WAIT       -
 UDP     192.168.1.100:1234    *:*                   UNKNOWN         5678
```

- **TCP 192.168.1.100:80 192.168.1.50:53678 ESTABLISHED 4128**:
  - 表示有一个TCP连接处于建立状态（ESTABLISHED），本地端口是80，远程IP地址是192.168.1.50，远程端口是53678，与之关联的进程ID是4128。
- **TCP 192.168.1.100:443 \*:\* LISTENING 1234**:
  - 表示一个TCP监听端口443（通常为HTTPS服务），等待连接请求，与之关联的进程ID是1234。
- **TCP 192.168.1.100:443 192.168.1.50:53681 TIME_WAIT -**:
  - 表示一个TCP**连接已经关闭但还没有释放，处于TIME_WAIT状态**，与之没有关联的进程ID。
- **UDP 192.168.1.100:1234 \*:\* UNKNOWN 5678**:
  - 表示一个UDP端口1234处于未知状态，与之关联的进程ID是5678。

如果你需要进一步的信息，比如找出某个PID对应的程序名称，你可以使用任务管理器查看，或者使用其他命令行工具如 `tasklist /svc` 或 `wmic process where "pid=X"`（X 是 `netstat -ano` 中显示的 PID） 来确定使用该端口的应用程序。

## 2. findstr - 过滤

使用findstr进行过滤（类似Linux的grep）。

过滤出包含8081的所有行：

```sh
netstat -ano | findstr "8081"
或者进一步过滤
netstat -ano | findstr "LISTENING" | findstr "8081"
```

### 2.1 统计端口上的连接数

假设你想要统计端口8088处于 `TIME_WAIT` 状态的连接数，可以使用以下命令：

```bat
netstat -ano | findstr "8088" | find "TIME_WAIT" | find /c /v ""
```



## 3. tasklist - 查找相关程序

```sh
tasklist | findstr "8081"
```

如果你想查看PID为4128的进程信息，可以使用如下命令：

```sh
tasklist /FI "PID eq 4128"
```

## 4. wmic 查找进程文件所在位置

如果你想获取PID为4128的进程的详细信息，可以使用如下命令：

```bat
wmic process where "ProcessId='4128'" get Caption,ProcessId,ExecutablePath
```

## 5. taskkill - 杀死进程

```sh
taskkill /pid 8081  -t  -f
```

- -f 用来强制终止进程，使用需谨慎

