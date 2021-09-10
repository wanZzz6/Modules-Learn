## 安装

如需二次开发，请参考项目文档进行编译安装。

如果不是进行二次开发，建议docker安装，根据个人需求使用 http api 和 web hook即可完成需求。

```sh
docker pull panjjo/zlmediakit

docker run -id -p 1935:1935 -p 8080:80 -p 8554:554 -p 10000:10000 -p 10000:10000/udp -p 30000-30100:30000-30100 -p 30000-30100:30000-30100/udp --name zlm panjjo/zlmediakit
```

- 1935:  rtmp 播放地址
- 8554： rtsp 播放地址
- 8080: http 接口访问端口
- 10000：rtp流接收端口，tcp/udp
- 30000-30100:  我留作 rtp 推流端口，根据需要自省设定

## 拉流

就是将视频源传到ZLMeidiaKit，然后我们才能进行多路转发或播放

ZLM支持5种类型的视频源：分别是`RtspMediaSource`、`RtmpMediaSource`、`HlsMediaSource`、`TSMediaSource`、`FMP4MediaSource`。

不同的视频源最后播放的方式也不同

`RtspMediaSource`支持 rtsp播放、rtsp推流、webrtc播放、webrtc推流。

`RtmpMediaSource`支持 rtmp推流/播放、http-flv播放、ws-flv播放。

`HlsMediaSource`支持 hls播放。

`TSMediaSource` 支持 http-ts播放、ws-ts播放。

`FMP4MediaSource` 支持 http-fmp4播放、ws-fmp4播放。

比如我调用API添加了一路摄像头rtsp拉流：app为live，流ID为test

`http://127.0.0.1:8080/index/api/addStreamProxy?secret={{ZLMediaKit_secret}}&vhost={{defaultVhost}}&app=live&stream=test&url=rtsp://admin:admin123@192.168.11.124:554/Streaming/Channels/301?transportmode=unicast&rtp_type=0&timeout_sec=10&retry_count=3`

(作者提供了postman工程文件)

根据上面所描述的播放方式，我的客户端可以通过rtsp\rtmp\webrtc 多种方式进行播放，

比如通过VLC软件播放：rtsp://127.0.0.1:8554/live/test

> [播放url规则](https://github.com/ZLMediaKit/ZLMediaKit/wiki/播放url规则)

## 播放鉴权

ZLMediaKit会识别**播放url**中问号后面的字符串为url参数，其格式跟http一致，其中参数`vhost`是ZLMediaKit内置支持的参数，支持指定vhost。 url参数主要用于播放、推流鉴权，在触发hook api时，会把这些参数提交给第三方业务服务器

[鉴权· Issue #71](https://github.com/zlmediakit/ZLMediaKit/issues/71)

## 推流

调用接口

```
/index/api/startSendRtp
```

- src_port 参数从你映射的端口中选一个未使用的
- dst_url：流接收者的ip地址或域名，如需在docker宿主机测试，可以填宿主机的局域网ip
- 其他参数见接口文档

## GB28181 推流

ZLMediaKit支持GB28181的 ps-rtp推流，支持的编码格式分别为 `h264/h265/aac/g711/opus`

### 简单使用

ZLMediaKit默认开启10000端口用于接收UDP/TCP的GB28181推流。

如果大家没有摄像头的情况下，可以用FFmpeg或gstreamer 简单测试，基本上体验跟国标推流并无二致。

- ffmpeg推流命令 - udp

```sh
ffmpeg -re -i demo.mp4 -vcodec h264 -acodec aac -f rtp_mpegts rtp://127.0.0.1:10000
```

- gstreamer推流命令 - ump

```sh
gst-launch-1.0 videotestsrc pattern=ball ! x264enc ! rtph264pay ! udpsink host=127.0.0.1 port=10000
```

- gstreamer推流命令 - tcp 

  （有问题，还不能用）

```sh
gst-launch-1.0 videotestsrc pattern=ball ! x264enc ! rtph264pay mtu=1400 ssrc=1234567 ! tcpclientsink host=127.0.0.1 port=10000
```

随机生成 streamID，进入docker容器查看实时日志，日志文件在`/zlmediakit/log`目录下，例如

![image-20210909151854957](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/image-20210909151854957.png)

这个流的app为`rtp`, stream_id为`EADE328A`，您可以根据[wiki](https://github.com/xia-chu/ZLMediaKit/wiki/播放url规则)来组合成url并播放这个流。例如：

http://127.0.0.1:8080/rtp/EADE328A/hls.m3u8

http://127.0.0.1:8080/rtp/EADE328A.live.ts

**作者的话：**

需要指出的是，国标推流的app固定为rtp，你只能通过代码来修改它，stream_id为rtp流的ssrc，这个是随机的，在FFmpeg中貌似没法控制。

另外，每次推流时，请更换ssrc，否则ZLMediaKit发现推流端ip和端口变化后，会直接丢弃rtp包(现象如此[issue](https://github.com/xia-chu/ZLMediaKit/issues/267))；这样做的目的是为了防止两个设备使用同一个ssrc推流时互相干扰。

### 高阶使用

在推流给10000端口时，您可能发现有个缺陷，就是stream_id是ssrc，比较抽象，可能还没法控制。另外还需说明的时，**单端口情况下，如果是udp推流，那么性能会比较低下，原因是这样只能发挥一条线程的算力(tcp例外，可以发挥多线程性能)。**

那么我们能否自定义stream_id? 答案是肯定的，ZLMediaKit通过[restful api](https://github.com/xia-chu/ZLMediaKit/wiki/MediaServer支持的HTTP-API#24indexapiopenrtpserver)可以动态开启国标收流端口(同时支持udp/tcp模式)， 这样您既能控制流id，也能发挥多线程的效力。

在使用openRtpServer接口动态开启国标收流端口后，这个端口只能产生一个流，也就是说，一个摄像头需要一个服务器端口用于接收国标推流。

例如：

> /index/api/openRtpServer

参数

- secret: 本机请忽略
- port: 30001    **使用一个未占用的且docker映射的端口**
- enable_tcp: 1    同时监听 tcp
- stream_id:  test2   自定义的stream_id

正常返回：

```json
{
    "code": 0,
    "port": 30001
}
```

Udp推流测试

```sh
ffmpeg -re -i demo.mp4 -vcodec h264 -acodec aac -f rtp_mpegts rtp://127.0.0.1:30001
```

进入 docker 查看日志信息：

![image-20210909155610606](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/image-20210909155610606.png)

需要指出的是，如果openRtpServer接口创建的端口一直没收到流（或者解析不出流），那么会自动关闭和释放。

### 让ZLMediaKit往其他国标服务器推流

再创建一个docker容器来模拟其他国标服务器

```sh
docker run -id -p 1936:1935 -p 8081:80 -p 8555:554 -p 10001:10001 -p 10001:10000/udp -p 40000-40100:40000-40100 -p 40000-40100:40000-40100/udp --name zlm2 panjjo/zlmediakit
```

zlm2 做为其他国标服务器，调用api：

> `/index/api/startSendRtp`

参数：

- secret:{{ZLMediaKit_secret}}
- vhost:{{defaultVhost}}
- app:live
- stream:test
- ssrc:  1  自己生成个唯一ssrc值
- dst_url:  192.168.12.12 目标地址
- dst_port:  10001  目标端口号zlm2的
- is_udp: 0  用 tcp方式
- src_port:30099  源端口





## 录像、点播

调用接口开始录像

```
/index/api/startRecord
```

参数例如：

- type:1   mp4
- vhost: \_\_defaultVhost\_\_
- app: live
- stream:test

