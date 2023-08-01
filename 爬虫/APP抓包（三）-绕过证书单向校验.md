# Xposed绕过安卓证书单向校验

## 一、概述

在使用Charlse等抓包软件时，安装好了软件根证书后，抓包时仍会看到部分https请求连接失败（显示红色），点击请求详情，如果看到类似未知证书、证书被拒绝等信息，且将这些https请求单独放行后能请求成功，就说明App启用了SSL Pinning(又叫做“SSL证书绑定”)的技术。

> 在Charles中单独放行http\https请求步骤：复制请求URL，点击菜单栏Proxy->SSL Proxying Settings，在*Exclude*一栏点击*Add*按钮，填写URL，端口一般是443，点击OK关闭即可。后续想继续抓取此URL可再次打开设置取消前面的勾选，或者删除该条目。

如果你作为一个App开发者，要想实现SSL Pinning，大致从以下三个方向着手，具体就不展开介绍了：

- 公钥校验
- 证书校验
- Host校验

，

SSL Pinning又分两种情况：

- 客户端存在校验服务端证书，服务器也不存在证书校验，单项校验
- 客户端存在证书校验，服务器也存在证书校验，双向校验。

本文内容主要是为了解决第一种情况，第二种情况较麻烦，后续再讲。

## 二、解决方案

### 2.1 Android系统+Xposed+JustTrustMe++

Xposed 框架是一款可以在不修改 APK 的情况下影响程序运行（修改系统）的框架服务，**依赖root权限**，基于它可以制作出许多功能强大的模块。

项目地址：[github.com](https://github.com/rovo89/Xposed)，但是该项目早已经停止维护。

有类似功能的替代框架也有很多：[VirtualXposed](https://github.com/android-hacker/VirtualXposed)、[LSPosed](https://github.com/LSPosed/LSPosed)（推荐）、[TaiChi (太极)](https://github.com/taichi-framework/TaiChi)、[EdXposed](https://github.com/ElderDrivers/EdXposed)，可以访问他们的项目地址了解更多信息

> 相关讨论：[太极·Magisk和EdXposed和LSPosed如何选择？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/316497403)
>
> [安卓8及以下XPosed框架](https://www.duokaiya.com/xposed.html)

**在真机上安装Xposed有变砖的可能，所以尽量用模拟器**，推荐用雷电或者逍遥模拟器，Andriod5.1-32位、Andriod7.1-64位皆可，但不适用于Andriod8以上的系统。



#### 2.1.1 安装Xposed

1. 安装雷电模拟器

2. 创建一个安卓虚拟机，Andriod5.1-32位或者Android7.1-64

3. 下载Xposed-3.1.5安装包及对应安装版本的框架sdk

   Xposed官方网站已被DNS劫持，任何资源暂时都无法访问，我已将所需资源打包上传，链接：https://pan.baidu.com/s/1vWeRWmAw87KjxljMvP2jiQ?pwd=6666   

   包含以下各种文件：![xposed-resource](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/xposed%E8%B5%84%E6%BA%90%E8%AF%B4%E6%98%8E.jpg)

> 如果你需要其他Andriod版本的sdk，可以访问热心网友保存的镜像仓库：[XposedFrameworkMirror (github.com)](https://github.com/ZhReimu/XposedFrameworkMirror/tree/main/framework)

4. 将Xposed-3.1.5.apk 拖到安装模拟器中完成安装。

5. sdk安装

   本来软件安装完就可以自动下载所需资源，但是Xposed官方的链接无法访问，只能将资源上传到Android系统上手动安装

   - 在PC某个目录下（例如：D:\tmp）创建xposed文件夹，然后把xposed-v89-sdkxxx.zip解压到xposed文件夹（其实只需要解压出来system目录）

   - 把script.sh 安装脚本放到xposed里

     ![image-20230725225602207](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/xposed-dir.png)

   - 在D:\tmp 下打开终端，执行：
   
   ```sh
   adb connect 127.0.0.1:端口
   adb remount
   adb push D:\tmp\xposed /system
   adb shell
   #获取权限
   su
   cd /system   # 注意，不同版本的adb.exe上传文件夹后目录结构可能不一样，也可能是 cd /system/xpopsed，请用 ls 命令检查一下文件
   mount -o remount -w /system
   cd /system
   sh script.sh
   ```
   
   看到 - Done 就是安装成功了
   
   ![image-20230725223202246](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/xposed-done.png)

   

   重启模拟器，打开Xposed软件应当显示已激活。
   
   ![image-20230725222900764](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/xposed-ok.png)
   
   如果显示红色，提示未安装，则重新执行最后一步命令 `sh script.sh`，直到显示 -Done

#### 2.1.2 安装JustTrustMe模块

项目地址：[Fuzion24/JustTrustMe](https://github.com/Fuzion24/JustTrustMe)

针对代码混淆升级版 - 项目地址：[JustTrustMePP](https://github.com/JunGe-Y/JustTrustMePP) - 安装包下载地址：[app-release.apk](https://github.com/JunGe-Y/JustTrustMePP/blob/master/app/release/app-release.apk)

> JustTrustMe 一个用来禁用、绕过 SSL 证书检查的基于 Xposed 模块。简单来说，JustTrustMe 是将 APK 中所有用于校验 SSL 证书的 API 都进行了 Hook，从而绕过证书检查。
>
> 原版的JustTrustMe 的原理是针对特定的包名进行Hook，但是如果app代码混效过，包名就会变成a.b.c.d的形式，JustTrustMe将会失去部分效果，因此有了升级版的JustTrustMePP。
>
> 这里我在测试过原版JustTrustMe后，测试发现效果不太好，可能现在大部分App打包前都启用了代码混淆，换到升级版后就好多了，但也不是全部的https都成功了，剩下个别失败的请求就可能是双向绑定的问题了，后续再介绍解决办法。

把 JustTrustMe.apk 拖进模拟器安装，正常情况下会在模拟器通知栏提示激活该模块并重启。
过程中会申请 root 权限，选择永久记住。
上面全部配置好后，重启模拟器后就可以直接抓取 https 包了。

### 2.2 逆向反编译

反编译apk，找到校验证书方法，将校验部分删除，再编译apk，成功抓取数据包。

// TODO 这个不是我擅长的领域，破解步骤也不是所有的应用都一样，等我再研究研究。。。



## 三、实测效果

### 未开启JustTrustMe++

这里以华为应用市场为例（仅做效果演示），在未开启JustTruseMePP模块的情况下用Charles抓包是这样的，几乎全都是SSL握手失败，软件也法进入主页面

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/Xpose-JustTruseMe-NO.png" alt="image-20230727172553516" style="zoom:67%;" />



### 开启模块

开启模块后记得重启模拟器才生效。

<img src="C:\Users\wzz\AppData\Roaming\Typora\typora-user-images\image-20230727172919433.png" alt="image-20230727172919433" style="zoom:50%;" />

![image-20230727173330659](C:\Users\wzz\AppData\Roaming\Typora\typora-user-images\image-20230727173330659.png)

可以看到大部分请求都通过了，软件也加载进去了，但还有几个失败的请求，经过查看还是提示SSL证书有问题，这些大概就是有双向证书认证的，只能通过逆向或者 **frida hook** 去解决了。

## 四、备注

最后再强调一次，安装Xposed是有风险的，请尽量在模拟器中操作。

---

参考：

- https://blog.csdn.net/benmel/article/details/125075908