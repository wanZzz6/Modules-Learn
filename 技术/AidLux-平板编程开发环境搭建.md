# 移动设备（平板）开发环境搭建教程

## 前言

平板设备由于携带方便，屏幕也算大，我常常用来在图书馆刷算法题或者远程检查一下线上bug，可以说是非常棒😁！

（本人 Matepad pro 12.6 配合华为电脑管家可以当做副屏用，共享键鼠和剪切板，还能平板管理文件👍👍）

此文说明下我用平板设备如何搭建一个简易的 vscode 开发环境，实际上你可以胜任任何语言的开发工作，比如我在本地就可以运行前后端分离的 vue + springboot 项目。

说明一点，平板等移动设备的毕竟性能有限，千万别把它当作主力开发工具。

（本教程仅支持 Android/鸿蒙设备）

## 开始

> 先放出官方文档 [Aidlux](https://docs.aidlux.com/#/)

### 安装 Aidlux

**系统要求**：

- 鸿蒙或者Android 系统版本 >= 6
- 剩余存储空间 > 1.75GB 
- CPU 支持 arm64-v8a 架构

在应用商店搜索并安装 AidLux，首次启动，软件将进行一次Linux环境配置。

该环节根据网络环境及手机性能，大约消耗1~3分钟。

配置完成之后即可进入主界面。

![进入命令行模式](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202206112218955.png)

### 菜单功能说明

底部导航栏自己点开体验一下就知道啥功能了，详见官方文档：[Aid桌面环境 ](https://docs.aidlux.com/#/intro/aid-desktop)

examples 内置了很多 AI 的示例，比如人脸关键点识别、肢体识别、手势识别等，也可以体验一下

常用的就是第二个命令行终端和倒数第三个应用中心

### 安装 vscode

从底部导航栏进入应用中心，就是上图倒数第三个图标样式。

在“Linux”栏目下（可同时支持Aid 源和Debian官方源应用操作），这里内置了大量 AI开发人员常用的软件，你也可以安装你所感兴趣的应用，这里我们先找到 vscode 并安装，（还有一个 vode-server， 这俩图标一样，但是后者是在浏览器中运行的，个人觉得后者插件支持不是很好，就没怎么用）

![Screenshot_20220611_222902_com.aidlux](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202206112229004.png)

## Python开发环境

内置python3 版本

```python
root@localhost:/# python3 -V
Python 3.7.3
```

也可在应用中心安装其他版本

或者用命令安装

```sh
aid install python-3.9.10
```

![在AidLux使用命令行安装python](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202206112246931.png)

python开发的话我一般用 jupyter（应用中心安装） 或者 vscode加插件，pycharm也能运行，但是它太占内存了，我没敢尝试，机器性能好的朋友可以试试😂  - [pycharm安装文档](https://docs.aidlux.com/#/intro/linux-native?id=e）-pycharm-community)

## Java 环境

- OpenJDK 11 安装

  ```sh
  apt install openjdk-11-jdk
  ```

- 验证

  ```bash
  root@localhost:/home# java --version
  openjdk 11.0.14 2022-01-18
  OpenJDK Runtime Environment (build 11.0.14+9-post-Debian-1deb10u1)
  OpenJDK 64-Bit Server VM (build 11.0.14+9-post-Debian-1deb10u1, mixed mode)
  ```

- 安装maven

  ```sh
  apt install maven
  ```

- mysql

  注意这个有点坑，内置且只支持 Maria DB


- 安装 vscode 插件

  - Extension Pack for Java：一键安装包含java开发常用的6个插件，省去挨个安装的麻烦
  - Spring Boot Extension Pack：spring 开发插件合集

  安装完插件你就可以创建并运行 spring boot项目了

  常见功能在vscode中 `Ctrl+Shft+P` 搜索关键字：java 或者 spring

## 前端开发环境

应用中心或命令行终端中安装 nodejs

```sh
apt install nodejs
```

验证

```bash
node -v
# 输出
# v16.15.0
npm -v
8.5.5
```

npm 换源

```sh
npm config set registry https://registry.npmmirror.com
```

vscode 安装插件

- Vetur
- 其他

前端开发肯定少不了浏览器 F12 等界面，所以还得装Linux图形界面，请往下看



## Linux 图形界面

旧版本aidlux 需要手动安装 xfce4 桌面环境，最新版本已经内置了，在桌面直接点击即可使用，选择 `Wayland` 方式进入


### 其他说明

不建议从外部用 VNC 方式连接到桌面环境，延迟高，操作不方便，不如直接在 aidlux 里玩。

### 安装 Chrom

命令安装

```sh
aid install chromium
```

安装完成后在xfce4 中打开

**解决中文乱码**

```
apt-get install ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy
```

**解决无法启动**

```
vi /usr/share/applications/chromium.desktop
```

替换131行

```
Exec=/usr/bin/chromium --no-sandbox
```
