# 移动端抓包进阶



## 一、问题：安装了ssl证书后抓包失败

这里以 Charlse 为例，Fiddler、mitmproxy 也会出现这种问题



电脑和手机都安装 ssl\tls 证书后，抓包依然提示红色的 `unkown` 错误，在右侧的 Failure 和 Notes 字段也都给出了相应的提示，问题出在证书上。

![image-20221029221143433](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202210292211203.png)

### 原因

Android7.0 (SDK24) 之后默认不信任用户添加到系统的CA证书：

```
To provide a more consistent and more secure experience across the Android ecosystem, beginning with Android Nougat, compatible devices trust only the standardized system CAs maintained in AOSP.
```

也就是说对基于 Android7 及以上的APP来说，不再信任用户或管理员添加的CA用于安全连接，在 https 连接握手阶段就失败了。

请参考此链接：https://android-developers.googleblog.com/2016/07/changes-to-trusted-certificate.html

### 解决方法

Android **开发者**可以参考 https://developer.android.com/training/articles/security-config 进行相关配置。



对于我们非开发者而言，要么使用安卓7以下的模拟器运行应用，要么在**获取 root 权限**后才能解决这个问题

#### 情形一：可 root 环境

此部分针对已经 root 了的环境，如果真机无法 root，则推荐用夜神、雷电等**模拟器**



首先，要知道安卓**系统证书**存放目录：`/system/etc/security/cacerts/`

该目录下的文件是这样的：

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202210292254900.png" alt="image-啊20221029225400978" style="zoom:50%;" />

文件名必须符合以下格式：
`<Certificate_Hash>.<Number>`

文件名是一个8位的 Hash 值，而后缀是一个数字。

数字是为了区分相同文件名的不同文件，如果你没有重复安装证书，这个后缀应该是 0，所以最好将之前安装的 charlse 证书卸载。



（证书）文件名可以用 openssl 命令计算得出，openssl 的安装比较简单，请自行百度安装。

将 Charles（或者 Fiddler、mitmproxy）的证书导出，并按下面命令计算得到 hash 值

```sh
# 注意：部分手机只能识别pem格式证书,如果是 cer、crt 格式需要预先转成 pem 格式再执行后续操作
openssl x509 -inform der -in <xxx.cer> -out <xxx.pem>

# 计算 hash
openssl x509 -subject_hash_old -in <xxx.pem>
```

Windows 系统输出如下图所示：

<img src="C:\Users\wzz\AppData\Roaming\Typora\typora-user-images\image-20221029232747113.png" alt="image-20221029232747113" style="zoom:50%;" />



然后，根据得到的hash值将上面的 pem 证书重命名(上图示例：`c78bfbff.0`)，并上传到手机目录：`/system/etc/security/cacerts/`

如果你有 **ADB** 软件，可用以下命令上传文件到手机；如果没有，那就用 **MT文件管理器** 或者 [**Root Explorer**](https://www.ghxi.com/rootexplorer.html) 等软件。

```sh
adb devices -l #显示所有已连接的设备详细信息

# 如果是模拟器，先连接，地址在上条命令输出结果中
# adb connect 127.0.0.1:62001

adb root
adb shell mount -o remount,rw /
adb push c78bfbff.0 /system/etc/security/cacerts
# 修改文件权限
adb shell chmod 644 /system/etc/security/cacerts/c78bfbff.0
```

如遇到上传失败问题请参考：https://blog.csdn.net/tiancheng1016/article/details/59102018



完成上述全部操作后，你应该可以在 设置->安全->加密与凭据->信任的凭据 的**系统**（注意不是用户证书）标签页看到你新加入的证书，确认其启用即可顺利抓包。

（应该会看到很多系统证书，按照首字母升序排列，名为 `DO_NOT_TRUST` 的是 Fiddler 的证书，滑倒底部一页查找名为 `XK72 Ltd` 的就是 Charlse 的证书）


#### 情形二：手机上装虚拟机

无法 root 的用户可以在手机上安装一个能 root 的虚拟环境，并将应用装在虚拟环境中，然后按照**情形一**的步骤用 root 身份安装证书。

推荐使用 VMOS，官方最新版本的 root 功能需要收费，可选择用 pojie 版或者支持正版。

**VMOS 下载地址1**：[lxapk.com](https://www.lxapk.com/447.html)

下载地址2：[百度网盘](https://pan.baidu.com/s/1csFt5Tx15Y7mo4YDZ3NYLg?pwd=6666) （仅安卓5.1极客版ROM可用）

> 注: `VMOS` 应用就是一台 Android 虚拟机,大部分应用都可以使用, 类似软件还有很多（比如 x8 沙箱、虚拟大师），但好像最新版都不能 root 了，得用充钱或者pojie

（ 你可能需要看：[安卓12解除进程限制方法汇总](https://blog.csdn.net/Amy_mumu/article/details/126759203)）



**tips1：**

往 VMOS 虚拟机中传文件可以使用其远程 adb 功能，在虚拟机中打开网络adb选项，在选项后面会显示虚拟机 adb 连接的地址和端口，形如 192.168.50.100:5666

然后 PC 端与手机端连入同一网络，在 pc 用上面adb命令上传文件很方便



**tpis2：**

设置模拟器中的网络代理也可以用 adb 命令：

```powershell
 # adb 连接到 vmos 虚拟机
adb connect 192.168.50.100:5666
# 设置 vmos 的全局代理为 charlse 监听地址
adb shell settings put global http_proxy 192.168.50.14:8888
```



*相关链接：*

- *[Charles Android 抓包失败](https://blog.csdn.net/mrxiagc/article/details/75329629)*
- *[最全面的解决Charles手机抓包的证书问题](https://zhuanlan.zhihu.com/p/281126584)*
- [部分APP无法代理抓包的原因及解决方法（flutter 抓包）](https://www.cnblogs.com/lulianqi/p/11380794.html)

---

## 二、抓指定app的数据包



使用场景：

1. 手机上所有的数据包都经过 Charlse 等抓包软件会显得很混乱，我们只想关注抓包应用的数据包
2. 连上了代理，抓包 app 以外的应用可能无法使用
3. 每次抓包都得在系统设置里改网络代理，不能永久保存配置
4. 某些 APP 使用的是Okhttp框架，那只需要在源代码上加入`proxy(Proxy.NO_PROXY)`就可以让 Charlse 抓不到包。



这里使用一个安卓上十分方便的 VPN 软件：drony  （PS：在ios也有许多与drony功能类似的软件，比如：Shadowrocket）



drony会在你的手机上创建一个VPN，将手机上的所有流量都重定向到drony自身（不是流向vpn服务器） ，这样drony就可以管理所有手机上的网络流量，甚至可以对手机上不同APP的流量进行单独配置。

- [下载地址1](https://mobile.softpedia.com/apk/drony/)
- [下载地址2](https://files.cnblogs.com/files/lulianqi/Drony_102.apk)

尽量用新版本，否则会有bug，我下载下来是繁体中文的，看着有点别扭。。。。

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony1.png" alt="image-20221031181301909" style="zoom:50%;" />

向右划到设置页面，选择 网络：无线网络，点击当前在用的wifi名，进入网络列表页面，选择要设置代理的 wifi 名



<center>
    <img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony2.png" alt="image-20221031181758170" style="zoom:50%;" />
	<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony3.png" alt="image-20221031182120224" style="zoom:50%;" />
</center>



输入 Charlse 的代理地址、端口

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony4.png" alt="image-20221031182518443" style="zoom: 67%;" />

往下滑，代理类型默认**普通** http，也可以根据实际情况修改。（PS：如果你用Charles抓包，建议用Socks5类型)

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony5.png" alt="image-20221031182718084" style="zoom:50%;" />

往下滑，過濾默認值（默认代理规则）选择 **引導全部**（即：Direct all）

接着点击下方的 **編輯過濾規則**，为我们的抓包应用单独配置代理：

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony6.png" alt="image-20221031185423980" style="zoom: 67%;" />



点击右上方加号，添加一条规则。

**行動**栏 选择 **本地代理鏈全部**，然后选择抓包的应用程序，最后记得点击**保存**

**主機名** 及 **端口** 不填 表示应用内所有的流量都会被强制代理。

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony7.png" alt="image-20221031190133208" style="zoom:67%;" />



以上就配置完了，然后一路返回，返回到settings里，左滑到日志页面，点击下方开关按钮，使其变为 **開** 状态，然后就可以抓包了。

![image-20221031222211722](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/drony8.png)



>注: Drony 转发 https 包时可能会遇到上面的第一部分介绍的证书问题，所以请使用 Android 7 以下的系统或者通过 root 安装证书。
