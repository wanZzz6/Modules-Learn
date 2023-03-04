
## 1. 声明

此破解工具来源于github，程序开源，**切勿用于商业用途** 

## 2. 破解工具

亲测7.7.0版本破解可用（全平台）

- 项目地址：~~https://github.com/5cr1pt/GitCracken~~  
（备用地址）https://github.com/happyhope/GitCracken

## 3. Mac系统注意事项

Mac平台用户下载完安装包后解压得到一个可执行程序，但是不要直接双击运行，将其拖到左侧快捷菜单中的“应用程序”中，然后从启动台（开始菜单）中打开。

安装完成后打开运行一次，显示主界面即可退出。

另外你可能遇到软件**已损坏**的问题，请参考：[解决方法](https://zhuanlan.zhihu.com/p/114919138)

## 3. 环境准备

- 安装 Node.js >=12
- [安装yarn包管理工具](https://yarn.bootcss.com/docs/install/#mac-stable)

## 4. 开始破解

>破解工具最后一次Git提交记录显示 8.2.2 已被破解，如果不能破解可自行尝试 8.2 之前的版本，本人测试的7.7.0版本是OK的。

**⚠️警告：破解之前先关闭 Gitkraken 软件，MAC用户需要先启动一次再关闭软件**



依次执行以下命令

1. `git clone https://github.com/happyhope/GitCracken`

2. `cd GitCracken/GitCracken/`

3. 如果是对 <=7.7.0版本的激活，需要执行：`git reset 07f422 --hard` （即，切换到git倒数第二次提交记录）

4. `yarn install`

5. `yarn build`

6. `node dist/bin/gitcracken.js patcher`

   （如提示权限不足可切换到root用户再执行）

![image-20230303201125921](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202303032011237.png)

如果最后一步没有错误发生，就破解成功啦，如有发生错误，可通过issue或者邮件，将错误信息、平台、软件版本等信息告知于我。

初次使用会让你先登录账号，建议用 github 账号授权登录（记得用梯子）。

破解后你会看到右下角显示 **Pro**，如果显示 free 或者其他，表示没有破解成功，可卸载干净后选择其他版本重试。 

![image-20221216160521606](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202212161618492.png)

### 禁用更新（可选）

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

## Windows卸载残留

C:\Users\xxxxx\AppData\Roaming\.gitkraken 
C:\Users\xxxxx\AppData\Roaming\GitKraken 
C:\Users\xxxxx\AppData\Local\gitkraken

## 历史版本下载

（改改版本号就行）

- Linux-deb : https://release.axocdn.com/linux/GitKraken-v7.7.0.deb
- Linux-rpm : https://release.axocdn.com/linux/GitKraken-v7.7.0.rpm
- Linux-tar.gz : https://release.axocdn.com/linux/GitKraken-v7.7.0.tar.gz
- Win64 https://release.axocdn.com/win64/GitKrakenSetup-7.7.0.exe
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



---

- 其他备用地址：[wcxo/GitCracken](https://github.com/wcxo/GitCracken/tree/BoGnY)
