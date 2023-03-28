在使用 PyCharm 时会在 C:\Users\<username>\.PyCharm < 版本号 > 下创建一大堆文件，里边包括了配置信息，项目缓存信息等。要为了解决 Pycharm 大量占用 C 盘问题，需要把一些配置信息搬迁到指定位置。

通过 PyCharm 修改
-------------

在启动 PyCharm 后选择 Help -> Edit Custom Properties 的选项，弹出：

![](https://img-blog.csdnimg.cn/20200322105304289.png)

选择 Create ，之后在文件中添加以下内容即可：

```ini
idea.config.path=D:/Program Files/.PyCharm/config
idea.system.path=D:/Program Files/.PyCharm/system
```

最后将原文件夹下的 C:\\Users\\<username>\\.PyCharm \< 版本号 \> 复制到目标搬迁文件夹下，并关闭 PyCharm 之后删除 system 文件夹并重启 PyCharm 就完成了配置的搬迁。其实只保留 config 目录下的一个 idea.properties 文件即可，其余文件都可以删除。

