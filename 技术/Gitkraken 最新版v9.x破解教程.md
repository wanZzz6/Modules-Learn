# Gitkraken 最新版v9.x全平台破解教程

## 一、 免责声明

所有内容资源均来源于网络，仅供交流学习与研究使用，版权归属原版权方所有，版权争议与本人无关，用户本人下载后不能用作商业或非法用途，否则后果均由用户承担责任;
如果您访问和下载此文件，表示您同意只将此软件用于参考、学习而非其他用途，否则一切后果请您自行承担，请于下载后24小时内删除，不允许用于商业用途，否则法律问题自行承担。
如果您喜欢该软件，请支持正版软件，购买注册，得到更好的正版服务。

## 二、软件安装

此工具支持破解 Gitkraken V7.7.0 ~ V9.x(最新版)，直接从官网下载最新的安装包即可，如后续破解工具失效，可回退到旧版进行激活

(亲测9.6.0可用)

官网下载地址：[Gitkraken](https://www.gitkraken.com/download)

### MacOS用户

1. 如果你之前安装过该软件，请先卸载，并清理用户缓存（`rm -r ~/.gitkraken`)

2. 下载安装包

​	如果是从官网下载的最新安装包，后缀为 `.dmg`，下载完直接双击运行，会提示拖动到 **Applications** 中，然后就会在启动台（开始菜单）看到图标。

​	如果你下载的稍旧点的版本（后缀为 `.zip`），在"**访达**"页面解压完后双击运行，如果是进入了软件主界面而不是（如下图）提示拖动到 **Applications** 中，那么你需要关闭软件，手动将安装包拖动到访达左侧的 **Applications**(应用程序)中

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/gitkraken-step1.jpg" alt="Snipaste_2023-07-14_09-32-17" style="zoom:67%;" />

3. 安装完成后，在**启动台**（开始菜单）中找到Gitkraken图标，并点击运行。

4. 进入引导页面

   这里以9.6.0 版本为例，用户界面如下所示，点击绿色按钮开始使用，不用点击下方的登录。

   <img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/gitkraken-step2.jpg" alt="Snipaste_2023-07-14_09-36-12" style="zoom: 67%;" />

5. 输入你的用户名、邮箱后，点击绿色按钮

   （注：这里的用户名、邮箱就是你以后git push后显示的个人信息）

   <img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/gitkraken-step3.jpg" alt="Snipaste_2023-07-14_09-36-54" style="zoom:67%;" />

6. 按提示打开一个git仓库，可以是本地的，或者clone远程的

7. 关闭Gitkran，并确保在底部 Dock 栏也**完全退出**

>MacOS上如果遇到软件**已损坏**的问题，请参考：[解决方法](https://zhuanlan.zhihu.com/p/114919138)

### Windows 用户

下载v9.x安装包，双击运行，会自动安装到C盘并进入主页面，操作步骤同前面Mac一样，按绿色按钮，输入用户名、邮箱后再点击绿色按钮，随便打开一个git仓库，然后关闭软件。



关闭Girkraken后若发现其未自动创建桌面快捷方式，可到 `C:\Users\{用户名}\AppData\Local\gitkraken` 目录，找到 gitkraken.exe 为其创建快捷方式.

## 三、破解步骤

此工具 `GNU/Linux` (without `snap`), `Windows`和`macOS` 全平台可用

### 1. 下载破解工具

下载链接: [百度网盘](https://pan.baidu.com/s/1dFEWCdzVg1bibn3GSYjuTw?pwd=6666)

此破解工具之前发布于github上的源码已被和谐，此次用到的破解工具来源于同一作者，程序开源，**切勿用于商业用途**。

（原地址：https://github.com/PMExtra/GitCracken.git）

### 2. 环境准备

- 安装 Node.js >=12
- 安装yarn包管理工具

	```sh
	npm install --global yarn
	```

### 3. 开始破解

**⚠️警告：破解之前先关闭 Gitkraken 软件**

解压破解工具，进入 GitCracken 目录，然后在此目录打开命令行，依次执行以下3条命令：

```bash
yarn install
yarn build
yarn gitcracken patcher     # Mac\Linux 用户可能需要root权限，需在前面加上 sudo
```

如图所示：

![image-20230307235617800](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/gitkraken9.png)

如有遇到错误，可通过issue或者邮件，将错误信息、平台、软件版本等信息告知于我。  

(issue回复不及时，可邮箱联系：1343837706@qq.com)

### 4. 验证是否成功

v9.x 版本：重新打开Gitkraken，破解成功会在右下角看到 Pro 标志，如果破解失败就依然是 Free 标志。



稍旧点的v7、v8版本：Gitkraken 初次使用会让你先登录账号，建议用 github 账号授权登录（记得用梯子）

- 若点击用 Github 授权登录没反应，检查 hosts 文件是不是把 gitkraken 网址屏蔽了
- 若在浏览器中显示授权失败，xxx error之类的，多尝试登录几次即可

登录账号后你会看到右下角显示 **Pro**，如果显示 free 可能是你之前的账号信息未清理干净，请尝试删除目录： `C:\Users\{用户名}\AppData\Roaming\\.gitkraken` （Windows用户）或  `~/.gitkraken` （Mac、Linux用户）

![image-20230704223447045](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202307042234098.png)

### 5. 禁用更新（可选）

> 到目前最新版的 v9.x 都可破解使用，所以你 duck 不必禁用更新，继续白嫖最新功能😂。
>
> 如果自动更新了，再次运行破解命令就行，不用删除`.gitkraken` 文件夹，你也不想你的项目和账号信息都清空吧



Window 平台直接删除： `C:\Users\{用户名}\AppData\Local\gitkraken\Update.exe` 即可。

其他平台：

将以下内容添加到你的 `hosts` 文件中

```
0.0.0.0 release.gitkraken.com
0.0.0.0 api.gitkraken.com
0.0.0.0 gloapi.gitkraken.com
```

hosts 文件路径：

- C:\Windows\System32\drivers\etc

或者 
- /etc/hosts



## 其他

### Windows卸载残留

- `C:\Users\{用户名}\AppData\Roaming\\.gitkraken` （**注**：这里存放账号信息、打开过的项目、用户设置等，如果你只是升级版本，可以不用删除）
- `C:\Users\{用户名}\AppData\Roaming\GitKraken` 
- `C:\Users\{用户名}\AppData\Local\gitkraken` （**注**：这是默认安装位置，如果安装完成后桌面没有快捷方式，可从这里启动）

### Mac 卸载残留

```sh
rm -r ~/.gitkraken
```



### 查询所有历史版本

可能需要梯子

[GitKraken Client v7.x 更新记录](https://help.gitkraken.com/gitkraken-client/7x/)

[GitKraken Client v8.x 更新记录](https://help.gitkraken.com/gitkraken-client/8x/)

[GitKraken Client v9.x 更新记录](https://help.gitkraken.com/gitkraken-client/current/)

### 历史版本下载

改改版本号就行

- Linux-deb : https://release.axocdn.com/linux/GitKraken-v7.7.0.deb
- Linux-rpm : https://release.axocdn.com/linux/GitKraken-v7.7.0.rpm
- Linux-tar.gz : https://release.axocdn.com/linux/GitKraken-v7.7.0.tar.gz
- Win64： https://release.axocdn.com/win64/GitKrakenSetup-7.7.0.exe
- Mac (Intel) : https://release.axocdn.com/darwin/GitKraken-v7.7.0.zip
- Mac (Apple Silicon) 从v9.0.0开始支持：(https://release.axocdn.com/darwin-arm64/GitKraken-v9.0.0.zip)

### 百度云地址

- 7.5.1 版本
链接: [https://pan.baidu.com/s/1MyN54U_r3lQ-PAIcmt9vcg](https://pan.baidu.com/s/1MyN54U_r3lQ-PAIcmt9vcg) 
提取码: tjfj 

- 6.5.0 版本
链接：[https://pan.baidu.com/s/1ysDsu41C5RggfllPPoVGPA](https://pan.baidu.com/s/1ysDsu41C5RggfllPPoVGPA)
提取码：bjik

- 6.0.0版本
链接：[https://pan.baidu.com/s/1qZyxd9uceVoXDXag-FvdfA](https://pan.baidu.com/s/1qZyxd9uceVoXDXag-FvdfA)
提取码：cnfn



---

## 常见问题

### 1. 不开代理软件无法拉取代码

可能是在安装Gitkraken时，你有正在使用的代理软件，Gitkraken自动将其设置成了 git 代理，可通过以下命令查看

```sh
git config --global http.proxy
```

如果显示了你代理软件的地址，请将其移除：

```sh
git config --global --unset http.proxy
```

### 2. Mac上加了sudo仍然提示权限不足

当你使用第三方终端软件时（如iTerm、Warp等），系统为了保证用户数据安全，默认不允许这些软件用命令更新或者删除其他应用，可在设置->隐私与安全性中找到相关设置，当然最简单的解决方法是用系统默认的 Terminal 终端软件。

