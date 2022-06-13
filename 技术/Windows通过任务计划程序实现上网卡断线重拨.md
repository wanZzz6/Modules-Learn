---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

> 原文地址 [www.cnblogs.com](https://www.cnblogs.com/zhangshuyx/p/5383582.html)

由于工作中需要做一些服务器维护，为方便维护，在服务器上安装了一个 4G 无线上网卡。但是由于网络不稳定，经常在使用一两天后就断开，无法远程连接，甚是苦恼。在网上找了挺久也没有发现什么好的解决办法。

正好今天网络搜索发现了一个帖子《[待机唤醒后自动连接宽带](http://www.cnblogs.com/eineseite/archive/2009/06/16/1504247.html)》，和我要解决的问题有异曲同工的感觉，于是便试了一试，果然好用，赶紧分享给大家。

**1、首先新建文本文件，写入以下 vbs 代码，并保存为 vbs 文件；**

```
createobject("wscript.shell").run"rasdial 宽带连接名称 用户名 密码",0

```

这行代码可以实现指定宽带连接的拨号。我这里的无线上网卡，没有用户名密码，直接填上宽带名称就行，保存为 cmiot.vbs。

```
createobject("wscript.shell").run"rasdial cmiot",0

```

**2、新建任务计划，在网络断开时自动重拨；**

受这篇文章《[使用 Python 控制 DDNS 解析](https://www.forzw.com/archives/745)》的启发，观察了一下上网卡连接断开时的系统事件。

[![](https://images2015.cnblogs.com/blog/487962/201604/487962-20160412174049895-445662515.png)](http://images2015.cnblogs.com/blog/487962/201604/487962-20160412174043738-1199131914.png)

可以看到，在每次网络连接和断开时 Isatap 接口都会产生新事件，事件 ID 分别为 4200 和 4201，这样就好办了，我们只需要在 Isatap 接口产生 4201 事件时运行 cmiot.vbs 程序就可以实现断线重拨。

新建任务计划程序，触发器选择 “当特定事件被记录时”，触发器内容如下填写，操作选择 “启动程序”，并选定第一步保存的 vbs 文件，完成即可。

[![](https://images2015.cnblogs.com/blog/487962/201604/487962-20160412174055254-640580522.png)](http://images2015.cnblogs.com/blog/487962/201604/487962-20160412174051910-1194806338.png)

**3、实测效果**

断开网络进行测试，果然在 4201 事件出现后不久，上报 4200 事件，并且网络自动连接成功。

[![](https://images2015.cnblogs.com/blog/487962/201604/487962-20160412174101566-1170001798.png)](http://images2015.cnblogs.com/blog/487962/201604/487962-20160412174100238-687223802.png)
