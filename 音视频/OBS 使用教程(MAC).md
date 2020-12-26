> 原文地址 [blog.csdn.net](https://blog.csdn.net/u010416101/article/details/92834578)

### 前言

之前在 Windows 的机器上录制视频, 发现电脑有点卡顿了. 于是尝试了在 Mac 上试试. 在过程中发现一系列的问题, 总结如下. 希望能够帮助到大家.

本章主要包括如下几个部分:

*   如何安装 OBS
*   如何配置场景录制 & 屏幕录制
*   如何在 Mac 上配置 OBS 的声音
*   其他相关配置

### 前置条件

*   平台: Mac

### 使用教程

##### 安装 OBS

OBS 官方地址如下: https://obsproject.com/  
我们看的很多主播使用的直播软件都是 OBS, 软件安装完成后的图标和界面如下:

*   图标  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20190619153725420.png)
*   界面  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70.png)

##### 场景 & 全屏录制

*   窗口捕获  
    窗口捕获可以捕获我们需要的窗口.  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215132926.png)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215137306.png)
*   显示捕获  
    显示捕获会捕获我们当前显示器的内容.

##### 声音设置

Mac 上的声音设置较为复杂. Mac 上的声音输入主要包括 2 种: 麦克风 & 内部音响设备. 其中麦克风可以直接获取, 内部音响设备需要通过软件进行获取.  
soundflower: http://blce.u.qiniudn.com/Soundflower-2.0b2.dmg

*   安装 soundflower. 完成后, 重启电脑.
*   检查安装情况: 通过`偏好设置`->`声音设置`  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215144543.png)
*   配置混合输入  
    找到电脑的`音频MIDI设置`.(可以通过`Command+空格+输入MIDI` 快速打开)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215150512.png)
*   创建多输出设备, 选择 (2ch) 和内置输出.  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215154715.png)![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215158577.png)
*   选择`偏好设置`->`声音设置`->`输入/输出设置`  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215203195.png)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215207855.png)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215212114.png)
*   返回 OBS 界面, 查看是否有 2 种声音来源.  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215217001.png)
*   其他设置`OBS`->`Preference`.  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly95YW54bWwuYmxvZy5jc2RuLm5ldA==,size_16,color_FFFFFF,t_70-20201220215220579.png)

### Tips

*   Mac 上声音设置后, 无法更改其他的设置. 如果需要更改声音大小, 需要重新配置.
*   Mac 上部分的界面可能无法捕捉, 使用屏幕捕捉代替.(`网易MUMU`说的就是你!)
*   如果有时间, 我会在 B 站录制一个简单的使用视频.
*   Windows 版本有可能需要管理员方式进行启动, 这边概不详述.
*   如果是直播的话, 可以直接推流. 高级的部分可以选择自己需要的码率和声音频率, 个人认为不懂的话直接默认的应该就够使用了.

### Reference

[1]. [Mac 版 OBS 设置详解](https://www.jianshu.com/p/ecfaac6ee7ab)  
[2]. [Mac 配合 Soundflower 进行带系统音频的屏幕录制](https://blce.me/2669.html)  
[3]. [Mac 录屏软件推荐，比 Quicktime 好用！](https://www.jianshu.com/p/84f363d8fc1f)  
[4]. [使用 soundflower 解决 Mac 中 OBS 没有电脑声音的问题](https://blog.csdn.net/ziliwangmoe/article/details/86796272)

### Official

[1]. [在 Mac 上的 “音频 MIDI 设置” 中同时通过多个设备播放音频](https://support.apple.com/zh-cn/guide/audio-midi-setup/ams7c093f372/3.3/mac/10.14)  
[2]. [OBS Studio](https://obsproject.com/)

### 补充 20200311

有朋友私信问我如何打开摄像头功能. 今天研究了一下, 补充在文章后面.

*   Step1 选择一个场景, 点加号, 添加数据源. (摄像头为视频捕捉设备)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTA0MTYxMDE=,size_16,color_FFFFFF,t_70.png)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTA0MTYxMDE=,size_16,color_FFFFFF,t_70-20201220215229866.png)
    
*   Step 2 配置视频捕捉设备. (注意选择设备时, Mac 系统需要赋予 OBS 软件访问摄像头到权限)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTA0MTYxMDE=,size_16,color_FFFFFF,t_70-20201220215233027.png)
    
*   Step 3 随便移动即可.  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTA0MTYxMDE=,size_16,color_FFFFFF,t_70-20201220215237476.png)
    
*   Tips 详细功能. 如设置滤镜等, 在配置栏直接配置即可. (选中需要配置的摄像源, 右击. 即可看到相应配置.)  
    ![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTA0MTYxMDE=,size_16,color_FFFFFF,t_70-20201220215242387.png)  
    以上内容为自行摸索. 美颜等功能或者软件还请自行搜索.
    
*   More  
    [(百度经验)OBS 如何插入摄像头、图片及抠背景](https://jingyan.baidu.com/article/fd8044fa31e9ee5030137a63.html)