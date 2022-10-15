
## 声明

此破解工具来源于github，程序开源，**切勿用于商业用途** 

## 破解步骤

亲测7.7.0版本破解可用（全平台）

- 项目地址：~~https://github.com/5cr1pt/GitCracken~~  
（备份）https://github.com/happyhope/GitCracken

### 环境要求

- 安装 Node.js >=12
- [安装yarn包管理工具](https://yarn.bootcss.com/docs/install/#mac-stable)

### 开始破解

>破解工具最后一次提交记录显示 8.2.2 已被破解，如果不能破解请下载7.7.0版本

**⚠️警告：破解之前先关闭gitkraken软件，MAC用户需要先启动一次再关闭软件**

依次执行以下命令

1. git clone https://github.com/happyhope/GitCracken

（如果使用的是7.7.0版本激活，请查看该仓库git历史记录，切换代码到倒数第二次提交记录，再执行以下操作）

（`git reset 07f422 --hard` ）

2. cd GitCracken/GitCracken/
3. yarn install
4. yarn build
5. node dist/bin/gitcracken.js patcher

如果最后一步没有错误发生，就破解成功啦

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
