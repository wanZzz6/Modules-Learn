## 配置教程

https://blog.csdn.net/twi_twi/article/details/128417329



## 配置文件、日志存放位置

- `C:\Users\你的用户名\AppData\Roaming\picgo\data.json`

- `~/.config/picgo/data.json`

  

## 插件安装

插件收录列表：[PicGo/Awesome-PicGo: A collection of awesome projects using PicGo. (github.com)](https://github.com/PicGo/Awesome-PicGo)

### 1. 在线安装

在PicGo GUI页面 插件设置中直接搜索关键字

### 2. 离线安装

在PicGo存放配置文件的目录中执行：

```sh
npm install picgo-plugin-xxxx --save --ignore-scripts --registry=https://registry.npm.taobao.org
```

遇到问题可以从日志文件中查看具体错误日志：`C:\Users\你的用户名\AppData\Roaming\picgo\picgo.log`

> 安装完插件或者修改了插件配置需要重启PicGo才能生效。

## 常用插件

### 1. 图片压缩

- 联网调用Api压缩：[picgo-plugin-compression: 基于"色彩笔"的picgo图片压缩插件](https://github.com/Redns/picgo-plugin-compression)
- 本地压缩：[picgo-plugin-squoosh](https://github.com/JolyneAnasui/picgo-plugin-squoosh)

### 2. 添加水印

[picgo-plugin-watermark](https://github.com/fhyoga/picgo-plugin-watermark)
