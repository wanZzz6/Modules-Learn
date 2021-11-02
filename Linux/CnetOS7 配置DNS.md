在CentOS 7下有几种方式：

### 1. nmcli

显示当前网络连接

```sh
# nmcli connection show

NAME UUID                                 TYPE           DEVICE
eno1 5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03 802-3-ethernet eno1
```

修改当前网络连接对应的DNS服务器，这里的网络连接可以用名称或者UUID来标识

```sh
nmcli con mod eno1 ipv4.dns "114.114.114.114 8.8.8.8"
```

将dns配置生效

```sh
nmcli con up eno1
```

### 2. 手工修改 /etc/resolv.conf

*   修改 /etc/NetworkManager/NetworkManager.conf 文件，在 main 部分添加 “dns=none” 选项：

```
[main]
plugins=ifcfg-rh
dns=none
```

*   NetworkManager 重新装载上面修改的配置

```sh
systemctl restart NetworkManager.service
```

*   手工修改 /etc/resolv.conf

```
nameserver 114.114.114.114
nameserver 8.8.8.8
```

