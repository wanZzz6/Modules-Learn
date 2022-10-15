## 查看所有的网络连接

```sh
netstat -ano
```

协议、本地地址、外部地址、状态、PID

## findstr - 过滤

使用findstr进行过滤（类似Linux的grep），过滤出包含8081的所有行：

```sh
netstat -ano | findstr "LISTENING"| findstr "8081"
```

## tasklist - 查找相关程序

```sh
tasklist | findstr "8081"
```

## taskkill - 杀死进程

```sh
taskkill /pid 8081  -t  -f
```

- -f 用来强制执行

