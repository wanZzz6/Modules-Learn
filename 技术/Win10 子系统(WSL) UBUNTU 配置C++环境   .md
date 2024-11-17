> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 https://www.cnblogs.com/jasonxiaoqinde/p/10763185.html

1.`sudo apt-get install build-essential`

2.`sudo apt install gcc-8`

3.`sudo apt install g++-8`

```
cd /usr/bin
ln -s gcc-4.8 gcc
ln -s g++-4.8 g++
ln -s gcc-4.8 cc
ln -s g++-4.8 c++
```

可能需要 root 权限。可以 sudo su root 获取 root 权限。

一次安装基础包：

```
apt install python automake libtool flex texinfo libcppunit-dev make libncurses5-dev zlib1g-dev binutils-dev libssl-dev -y
```

### 为什么要在 windows 下编译 Linux 项目？

我们是做后台开发的，虽然我们的 svr 都泡在 tlinux 上，但是大部分同学写代码 / 看代码还都是在 windows 下，使用类似于 Clion、visual studio、source insight 等编辑器（可以方便的跳转），只有真正需要编译的时候才去编译机上进行编译。这样就有一个问题：当带有有编译错误时，需要在 windows 上改一下再通过 rz 或者 ftp 工具传过去再进行编译，效率不高。如果可以在 windows 上编译，就只用在编译完成进行一次 svn 提交即可，需要运行的时候再去编译机编译运行。而且编译完成后对于那些存在于 tar 包里面代码也可以做到跳转，写代码看代码也比较方便。

当然还有一个原因是组内有使用 mac 的同学做了在 mac 下的编译，心想 windows 不能没人管啊，于是就研究了下在 windows 下的编译。

### 什么是 WSL？

Windows Subsystem for Linux（简称 WSL）是一个为在 Windows 10 上能够原生运行 Linux 二进制可执行文件（ELF 格式）的兼容层。它是由微软与 Canonical 公司合作开发，目标是使纯正的 Ubuntu 14.04 "Trusty Tahr" 映像能下载和解压到用户的本地计算机，并且映像内的工具和实用工具能在此子系统上原生运行。发展到现在不止支持 Ubuntu，还有 OpenSuse、SUSE Linux Enterprise Svr、Debian、Kali 等操作系统。

### 如何开启 WSL?

本文以 Ubuntu 为例，展示如何在 WIN10 下开启 WSL。本文所说的都是在开发网下面进行的操作，所以需要申请临时访问外网权限。

1， 在服务里面将 WIN10 的自动更新服务打开，并把 win10 更新到最新版本。可以在 [https://www.microsoft.com/zh-cn/software-download/windows10](https://www.microsoft.com/zh-cn/software-download/windows10) 下载最新的升级器进行快速升级。

2，打开开发者模式：开始菜单 =>windows 设置 => 更新和安全 => 针对开发人员 => 开发人员模式

3，安装 WSL 组件：控制面板 =>程序和功能 =>启用或关闭 windows 功能 =>在 “适用于 Linux 的 Windows 子系统” 前面打钩，确定后重启系统

4，去应用商店下载 Ubuntu：开始菜单 => 打开 windows store=> 搜索 linux=> 在 windows 运行 linux？是的 => 获取这些应用 => 选择 ubuntu 进行下载，下载完成后自动安装。注意：由于我们公司网络策略，这块如果有相关问题要等好久，我就是因为不明网络原因重装了一次 win10 才解决，后面下载也经常遇到各种问题，比如速度慢、弹出错误等，不行就重启，杀后台进程，多试几次应该都可以的。

这些都完成后，你的开始菜单里面应该有了 ubuntu 的图标，点击进去进行安装即可，第一次会要求输入用户名和密码。

后续开启 ubuntu 子系统可以在 cmd 里面输入 bash 或者 ubuntu 即可，也可以选择开始菜单里面的 ubuntu 图标。开启后就是个标准的 linux 程序了，可以看到系统的 C D E 等盘都被挂载到了 / mnt 下面。

### 如何编译代码?

apt update

1，设置源和代理，修改系统配置

*   WSL 默认带的包很少，编译需要的东西很多都要自己安装。ubuntu 下面安装使用 apt 工具，需要设置相关源，这个网上找下相关教程即可，不再赘述。

2，下载安装相关的组件：

不同的项目需要的编译工具，以我们项目为例：

*   我们需要 gcc4.8，所以：

```
sudp apt install gcc-4.8

sudp apt install g++-4.8
```

再做一下软链接：

```
cd /usr/bin
ln -s gcc-4.8 gcc
ln -s g++-4.8 g++
ln -s gcc-4.8 cc
ln -s g++-4.8 c++
```

可能需要 root 权限。可以 sudo su root 获取 root 权限。

一次安装基础包：

```
apt install python automake libtool flex texinfo libcppunit-dev make libncurses5-dev zlib1g-dev binutils-dev libssl-dev -y
```

*   cmake 需要升级到 3.9 以上，去 https://cmake.org/download / 下载 3.9 版本，解压后 ./bootstrap && make && make install
*   uuid 项目需要 automake1.13 版本，protobuf 需要 1.14 版本的 automake，apt 上 install 的 automake 是 1.15 版本的，所以还需要去 [http://ftp.gnu.org/gnu/automake/](http://ftp.gnu.org/gnu/automake/) 下载对应的版本，./configure && make && make install
*   mysync 需要 bison 使用 2.7 版本，3.0 以上的版本 mysql-5-1-16 会报错，去 [http://ftp.gnu.org/gnu/bison/](http://ftp.gnu.org/gnu/bison/) 下载 2.7 版本安装包，然后./configure，make， make install 即可。有可能会报找不到 bison 的错误，使用命令：find . -type f | xargs touch -t `date +%Y%m%d%H%M`
*   你可以像在 linux 下面编译你的代码了。哦不，本来就是在 linux 下面，哈哈。

其他一些 tips

*   clion 最新的编译器才支持 WSL，需要去官网下载最新的。
*   clion 的 WSL 是通过 ssh 连接到 ubuntu 的，同理你也可以自己用 ssh 工具（比如 putty、secureCRT 等）连接到 ubuntu，这里给一个 ubuntu 下面开启 sshd 的方法，参考：[https://hbaaron.github.io/blog_2017/%E5%9C%A8wsl%E4%B8%8B%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8sshd%E5%85%A8%E6%94%BB%E7%95%A5/](https://hbaaron.github.io/blog_2017/%E5%9C%A8wsl%E4%B8%8B%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8sshd%E5%85%A8%E6%94%BB%E7%95%A5/)
*   代码可以通过 svn checkout 到 D E 盘等，编译的时候如果需要用到 / 目录之类的，可以通过软链接实现

# VS Code 插件

1. 首先确保安装了1.35或者以上版本的 VS Code，然后在拓展界面搜索`Remote - WSL`安装即可。

2. 接下来打开你的项目所在文件夹，然后这个文件夹下<kbd>Ctrl</kbd> + <kbd>~</kbd> 打开终端，输入`WSL`，然后输入 `code .`，这时会自动的打开一个 VS Code
3. 之前安装的 VS Code 插件此时需要在WSL下重新安装一遍，在拓展页面会显示安装 on WSL，点击即可，ctrl + \ 可以在调出WSL。如果你是 Python 开发者，`windows + shift + p`然后输入`Python: Select Interpreter`可以选择WSL下的 python 解释器。


参考：[在 Windows 上将 Python 用于 Web 开发](https://docs.microsoft.com/zh-cn/windows/python/web-frameworks)
