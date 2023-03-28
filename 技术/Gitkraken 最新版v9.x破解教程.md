# Gitkraken 最新版v9.x破解教程

## 一、 声明

此破解工具的作者之前的发布于github上的项目已被和谐，此次用到的破解工具来源于同一作者，程序开源，**切勿用于商业用途**。

（原地址：https://github.com/PMExtra/GitCracken.git）

## 二、 Mac系统注意事项

Mac平台用户下载完安装包后解压得到一个可执行程序，但是不要直接双击运行，将其拖到左侧快捷菜单中的“应用程序”中，然后从启动台（开始菜单）中打开。

安装完成后打开运行一次，显示主界面即可关闭。



另外你可能遇到软件**已损坏**的问题，请参考：[解决方法](https://zhuanlan.zhihu.com/p/114919138)

## 三、破解步骤

此工具适用于 `GNU/Linux` (without `snap`), `Windows`和`macOS`!

以下破解过程针对的是 Gitkraken >=7.7.0 版本，所以大家尽量换到官方最新版本

### 1. 下载破解工具

链接: [百度网盘](https://pan.baidu.com/s/1dFEWCdzVg1bibn3GSYjuTw?pwd=6666)

### 2. 环境准备

- 安装 Node.js >=12
- [安装yarn包管理工具](https://yarn.bootcss.com/docs/install/#mac-stable)

### 3. 开始破解

**⚠️警告：破解之前先关闭 Gitkraken 软件，MAC用户需要先启动一次再关闭软件**

解压破解工具，进入 GitCracken 目录，然后在此目录打开命令行，依次执行以下命令：

```bash
yarn install
yarn build
yarn gitcracken patcher
```

如图所示：

![image-20230307235617800](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/gitkraken9.png)

如有遇到错误，可通过issue或者邮件，将错误信息、平台、软件版本等信息告知于我。



### 4. 验证是否成功

初次使用会让你先登录账号，建议用 github 账号授权登录（记得用梯子）

- 若点击用 Github 授权登录没反应，检查 hosts 文件是不是把 gitkraken 网址屏蔽了
- 若在浏览器中显示授权失败，xxx error之类的，多尝试登录几次即可

登录账号后你会看到右下角显示 **Pro**，如果显示 free 可能是你之前的账号信息未清理干净，请尝试删除目录： `C:\Users\{用户名}\AppData\Roaming\\.gitkraken` （Windows用户）或  `~/.gitkraken` （Mac、Linux用户）

![image-20230307200157882](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/gitkraken911.png)

### 5. 禁用更新（可选）

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

- `C:\Users\{用户名}\AppData\Roaming\\.gitkraken` 
- `C:\Users\{用户名}\AppData\Roaming\GitKraken` 
- `C:\Users\{用户名}\AppData\Local\gitkraken`

### 查询所有历史版本

[GitKraken Client v7.x 更新记录](https://help.gitkraken.com/gitkraken-client/7x/)

[GitKraken Client v8.x 更新记录](https://help.gitkraken.com/gitkraken-client/8x/)

### 历史版本下载

（改改版本号就行）

- Linux-deb : https://release.axocdn.com/linux/GitKraken-v7.7.0.deb
- Linux-rpm : https://release.axocdn.com/linux/GitKraken-v7.7.0.rpm
- Linux-tar.gz : https://release.axocdn.com/linux/GitKraken-v7.7.0.tar.gz
- Win64： https://release.axocdn.com/win64/GitKrakenSetup-7.7.0.exe
- Mac : https://release.axocdn.com/darwin/GitKraken-v7.7.0.zip

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

