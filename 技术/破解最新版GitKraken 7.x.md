
### 亲测7.7.0版本破解可用（全平台）

## 声明

此破解工具来源于github，程序开源，**切勿用于商业用途**

## 破解步骤

- 项目地址：~~https://github.com/5cr1pt/GitCracken~~  
https://github.com/happyhope/GitCracken（备份）

### 环境要求

- 安装 Node.js >=12
- [安装yarn包管理工具](https://yarn.bootcss.com/docs/install/#mac-stable)

### 开始破解

>破解工具最后一次提交记录显示 8.2.2 已被破解，如果不能破解请按照下文列出的历史版本下载地址，使用7.7.0版本

**⚠️警告：破解之前先关闭gitkraken软件，MAC用户需要先启动一次再关闭软件**

依次执行以下命令

1. git clone https://github.com/happyhope/GitCracken

（如果使用的是7.7.0版本激活，请查看该仓库git历史记录，切换代码到倒数第二次提交记录，再执行以下操作）

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

历史版本下载（改改版本号就行）

- Linux-deb : https://release.axocdn.com/linux/GitKraken-v7.7.0.deb
- Linux-rpm : https://release.axocdn.com/linux/GitKraken-v7.7.0.rpm
- Linux-tar.gz : https://release.axocdn.com/linux/GitKraken-v7.7.0.tar.gz
- Win64 https://release.axocdn.com/win64/GitKrakenSetup-7.7.0.exe
- Mac : https://release.axocdn.com/darwin/GitKraken-v7.7.0.zip

---

卸载残留:

C:\Users\xxxxx\AppData\Roaming\.gitkraken  
C:\Users\xxxxx\AppData\Roaming\GitKraken  
C:\Users\xxxxx\AppData\Local\gitkraken\  