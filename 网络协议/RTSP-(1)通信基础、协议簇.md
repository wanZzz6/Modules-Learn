---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

[toc]

# RTSP 协议概述

RTSP(Real-TimeStream Protocol )是一种基于文本的应用层协议，在语法及一些消息参数等方面，RTSP 协议与 HTTP 协议类似。

RTSP 被用于建立的控制媒体流的传输，它为多媒体服务扮演“网络远程控制”的角色。尽管有时可以把 RTSP 控制信息和媒体数据流交织在一起传送，但一般情况 RTSP 本身并不用于转送媒体流数据。媒体数据的传送可通过`RTP/RTCP`等协议来完成。

- `RTSP协议`：负责服务器与客户端之间的请求与响应
- `RTP协议`：负责传输媒体数据
- `RTCP协议`：在 RTP 传输过程中提供传输信息

rtsp 承载与 rtp 和 rtcp 之上，rtsp 并不会发送媒体数据，而是使用 rtp 协议传输
rtp 并没有规定发送方式，可以选择 udp 发送或者 tcp 发送。

## 基本通信流程

**一次基本的 RTSP 操作过程是**:首先，客户端连接到流服务器并发送一个 RTSP 描述命令（`DESCRIBE`）。流服务器通过一个`SDP描述`来进行反馈，反馈信息包括流数量、媒体类型等信息。客户端再分析该 SDP 描述，并为会话中的每一个流发送一个 RTSP 建立命令(`SETUP`)，**RTSP 建立命令告诉服务器客户端用于接收媒体数据的端口**。流媒体连接建立完成后，客户端发送一个播放命令(`PLAY`)，服务器就开始在**UDP 上传送媒体流（RTP 包）**到客户端。 在播放过程中客户端还可以向服务器发送命令来控制快进、快退和暂停等。最后，客户端可发送一个终止命令(`TERADOWN`)来结束流媒体会话。

## RTSP 协议与 HTTP 协议区别

1.  RTSP 引入了几种新的方法，比如 DESCRIBE、PLAY、SETUP 等，并且有不同的协议标识符，例如：RTSP 为 rtsp 1.0（版本号，现在有 2.0）,HTTP 为 http 1.1；
2.  HTTP 是无状态的协议，而 RTSP 为每个会话保持状态；
3.  RTSP 协议的客户端和服务器端都可以发送 Request 请求，而在 HTTPF 协议中，只有客户端能发送 Request 请求。
4.  在 RTSP 协议中，载荷数据一般是通过带外方式来传送的(除了交织的情况)，及通过 RTP 协议在不同的通道中来传送载荷数据。而 HTTP 协议的载荷数据都是通过带内方式传送的，比如请求的网页数据是在回应的消息体中携带的。
5.  使用 ISO10646(UTF-8) 而不是 ISO 8859-1，以配合当前 HTML 的国际化；
6.  RTSP 使用 URI 请求时包含绝对 URI。而由于历史原因造成的向后兼容性问题，HTTP/1.1 只在请求中包含绝对路径，把主机名放入单独的标题域中；

## 重要术语

1. 集合控制(Aggregatecontrol )

对多个流的同时控制。对音频/视频来讲，客户端仅需发送一条播放或者暂停消息就可同时控制音频流和视频流。

2. 实体(Entity)

作为请求或者回应的有效负荷传输的信息。由以实体标题域（entity-header field）形式存在的元信息和以实体主体（entity body）形式存在的内容组成

3. 容器文件（Containerfile）

可以容纳多个媒体流的文件。RTSP 服务器可以为这些容器文件提供集合控制。

4. RTSP 会话(RTSP session )

RTSP 交互的全过程。对一个电影的观看过程,会话(session)包括由客户端建立媒体流传输机制(`SETUP`)，使用播放(`PLAY`)或录制(`RECORD`)开始传送流，用停止(TEARDOWN)关闭流。

# RTSP 协议详解

## RTSP 请求消息

RTSP 协议格式与 HTTP 协议格式类似

```
method url vesion\r\n
CSeq: x\r\n
xxx\r\n
...
\r\n

```

- method：方法，表明这次请求的方法，包括 OPIONS、DESCRIBE、SETUP、PLAY、TEARDOWN 等.
- url：格式一般为 rtsp://ip:port/session，ip 表主机 ip，port 表端口好，如果不写那么就是默认端口，rtsp 的默认端口为 554，session 表明请求哪一个会话
- version：表示 rtsp 的版本，常见的是 RTSP/1.0
- CSeq：序列号，每个 RTSP 请求和响应都对应一个序列号，序列号是递增的

每行后面的 CR LF(\r\n)表示回车换行，需要接受端有相应的解析，最后一个消息头需要有两个 CR LF

消息体是可选的，有的 Request 消息并不带消息体。

## RTSP 服务端响应消息

```
vesion 200 OK\r\n
CSeq: x\r\n
xxx\r\n
...
\r\n
```

- version：表示 rtsp 的版本，常见为 RTSP/1.0
- CSeq：序列号，这个必须与对应请求的序列号相同

| 方法          | 方向       | 描述                               | 要求            |
| ------------- | :--------- | :--------------------------------- | --------------- |
| OPTIONS       | C->S, C->S | 获取服务端提供的可用方法           | 必须(S->C:可选) |
| DESCRIBE      | C->S       | 向服务端获取对应会话的媒体描述信息 | 建议            |
| SETUP         | C->S       | 向服务端发起建立请求，建立连接会话 | 必须            |
| PLAY          | C->S       | 向服务端发起播放请求               | 必须            |
| TEARDOWN      | C->S       | 向服务端发起关闭连接会话请求       | 必须            |
| PAUSE         | C->S       | 向服务端发起媒体流传输的暂时中断   | 可选            |
| ANNOUNCE      | C->S, S->C |                                    | 可选            |
| GET_PARAMERTE | C-S, S->C  |                                    | 可选            |
| RECORD        | C->S       |                                    | 可选            |
| REDIRECT      | S->C       |                                    | 可选            |
| SET_PARAMETER | C->S, S->C |                                    | 可选            |

## 重要请求头参数

1. Accept:

用于指定客户端可以接受的媒体描述信息类型。比如:

```
Accept: application/rtsl, application/sdp;level=2
```

2. Bandwidth:

用于描述客户端可用的带宽值。

3. CSeq：

指定了 RTSP 请求回应对的序列号，在每个请求或回应中都必须包括这个头字段。对每个包含一个给定序列号的请求消息，都会有一个相同序列号的回应消息。

4. Range：

用于指定一个时间范围，可以使用 SMPTE、NTP 或 clock 时间单元。

5. **Session**:

Session 头字段标识了一个 RTSP 会话。Session ID 是由服务器在 SETUP 的回应中选择的，客户端一当得到 Session ID 后，在以后的对 Session 的操作请求消息中都要包含 Session ID.

6. **Transport**:

Transport 头字段包含客户端可以接受的转输选项列表，包括传输协议，地址端口，TTL 等。服务器端也通过这个头字段返回实际选择的具体选项。如:

```http
Transport: RTP/AVP;multicast;ttl=127;mode="play"
Transport: RTP/AVP;unicast;client_port=3456-3457;mode="play"
```

<!-- #region -->

## 交互过程举例

根据一般的 RTSP 流媒体播放流程**大致**讲解前 5 个方法，一般摄像头 RTSP 会设计到认证加密，请参考本人其他文章讲解。

### 1. OPTIONS

- C->S

```http
OPTIONS rtsp://192.168.31.115:8554/live RTSP/1.0\r\n
CSeq: 2\r\n
\r\n
```

客户端向服务器请求可用方法

- S->C

```http
RTSP/1.0 200 OK\r\n
CSeq: 2\r\n
Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY\r\n
\r\n
```

服务端回复客户端，当前可用方法`OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY`

### 2. DESCRIBE

- C–>S

```http
DESCRIBE rtsp://192.168.31.115:8554/live RTSP/1.0\r\n
CSeq: 3\r\n
Accept: application/sdp\r\n
\r\n
```

客户端向服务器请求媒体描述文件，格式为 sdp，客户端通过 Accept 头指定客户端可以接受的媒体述信息类型。

- S–>C

```http
RTSP/1.0 200 OK\r\n
CSeq: 3\r\n
Content-length: 146\r\n
Content-type: application/sdp\r\n
\r\n
// 这里为一个空行， 以下为具体的SDP信息//
v=0\r\n
o=- 91565340853 1 in IP4 192.168.31.115\r\n
t=0 0\r\n
a=contol:*\r\n
m=video 0 RTP/AVP 96\r\n
a=rtpmap:96 H264/90000\r\n
a=framerate:25\r\n
a=control:rtsp://192.168.31.115:8554/live/track0\r\n
```

服务器回复了 sdp 文件，这个文件告诉客户端当前服务器有哪些音视频流，有什么属性，**sdp 具体稍后再讲解**.

这里只需要直到客户端可以根据这些信息得知有哪些音视频流可以发送.

媒体初始化是任何基于 RTSP 系统的必要条件，但 RTSP 规范并没有规定它必须通过 DESCRIBE 方法完成。RTSP 客户端可以通过以下方法来接收媒体描述信息：

    a)  通过DESCRIBE方法；
    
    b)  其它一些协议（HTTP，email附件，等）；
    
    c)  通过命令行或标准输入设备

### 3. SETUP

UDP 方式：需要发送两个端口信息

- C–>S

```http
SETUP rtsp://192.168.31.115:8554/live/track0 RTSP/1.0\r\n
CSeq: 4\r\n
Transport: RTP/AVP;unicast;client_port=54492-54493\r\n
\r\n
```

客户端发送建立请求，请求建立连接会话，准备接收音视频数据，请求的 URI 地址从上一步 sdp 的 control 属性 获得，如果已知该 URI，可以直接发起 SETUP 请求建立连接。

**解析一下 Transport**: RTP/AVP;unicast;client_port=54492-54493\r\n

- **RTP/AVP：表示 RTP 通过 UDP 发送，如果是`RTP/AVP/TCP`则表示 RTP 通过 TCP 发送**
- **unicast**：表示单播，如果是`multicast`则表示多播
- client_port=54492-54493：由于这里希望采用的是 RTP OVER UDP，所以客户端发送了两个用于传输数据的端口，客户端已经将这两个端口绑定到两个 udp 套接字上，54492 表示是 RTP 端口，54493 表示 RTCP 端口(RTP 端口为某个偶数，RTCP 端口为 RTP 端口+1)，如果是 RTP/AVP/TCP 则可以不用 client_port 声明两个端口，直接复用该 RTSP 协议的端口，即整个过程只用到一个端口。

- S–>C

```http
RTSP/1.0 200 OK\r\n
CSeq: 4\r\n
Transport: RTP/AVP;unicast;client_port=54492-54493;server_port=56400-56401\r\n
Session: 66334873\r\n
\r\n
```

服务器端对 SETUP Request 产生一个**Session Identifiers**。

服务端接收到请求之后，得知客户端要求采用 RTP OVER UDP 发送数据，单播，客户端用于传输 RTP 数据的端口为 54492，RTCP 的端口为 54493

服务器也有两个 udp 套接字，绑定好两个端口，一个用于传输 RTP，一个用于传输 RTCP，这里的端口号为 56400-56401

之后客户端会使用 54492-54493 这两端口和服务器通过 udp 传输数据，服务器会使用 56400-56401 这两端口和这个客户端传输数据

### 4. PLAY

`PLAY`方法告知服务器通过`SETUP`中指定的机制开始发送数据。

**在尚未收到`SETUP`请求的成功应答之前，客户端不可以发出`PLAY`请求。**

`PLAY`请求将正常播放时间（`npt`=normal play time）定位到指定范围的起始处，并且传输数据流直到播放范围结束。

PLAY 请求可能被管道化（pipelined），即放入队列中（queued）；服务器必须将 PLAY 请求放到队列中有序执行。也就是说，后一个 PLAY 请求需要等待前一个 PLAY 请求完成才能得到执行。

- C–>S

```http
PLAY rtsp://192.168.31.115:8554/live RTSP/1.0\r\n
CSeq: 5\r\n
Session: 66334873\r\n
Range: npt=0.000-\r\n
\r\n
```

客户端请求播放媒体

- S–>C

```http
RTSP/1.0 200 OK\r\n
CSeq: 5\r\n
Range: npt=0.000-\r\n
Session: 66334873; timeout=60\r\n
\r\n
```

**服务器回复之后，会开始使用 RTP 通过 udp 向客户端的 54492 端口发送数据。如果是 TCP 方式建立的请求，则复用该 TCP 端口。**

Range 头可能包含一个时间参数。该参数以 UTC 格式指定了播放开始的时间。如果在这个指定时间后收到消息，那么播放立即开始。时间参数可能用来帮助同步从不同数据源获取的数据流。

不含 Range 头的 PLAY 请求也是合法的。它从媒体流开头开始播放，直到媒体流被暂停。如果媒体流通过 PAUSE 暂停，媒体流传输将在暂停点（the pause point）重新开始。

如果媒体流正在播放，那么这样一个 PLAY 请求将不起更多的作用，只是客户端可以用此来测试服务器是否存活。

### \* Server 开始发送 RTP 数据

- S-> C

  服务端发送 PLAY 响应后，立刻发送**RTP**媒体数据包。RTP 包格式请看下文。

### \* PAUSE

PAUSE 请求引起媒体流传输的暂时中断。如果请求 URL 中指定了具体的媒体流，那么只有该媒体流的播放和记录被暂停（halt）。比如，指定暂停音频，播放将会无声。如果请求 URL 指定了一组流，那么在该组中的所有流的传输将被暂停。如

- C->S:

```http
PAUSE rtsp://example.com/fizzle/foo RTSP/1.0
CSeq: 834
Session: 66334873
```

- S->C

```http
RTSP/1.0 200 OK
CSeq: 834
Date: 23 Jan 1997 15:35:06 GMT
```

PAUSE 请求中可能包含一个 Range 头用来指定何时媒体流暂停，我们称这个时刻为暂停点（pause point）。该头必须包含一个精确的值，而不是一个时间范围。媒体流的正常播放时间设置成暂停点。当服务器遇到在任何当前挂起（pending）的 PLAY 请求中指定的时间点后，暂停请求生效。如果 Range 头指定了一个时间超出了任何一个当前挂起的 PLAY 请求，将返回错误"457 Invalid Range" 。如果一个媒体单元（比如一个音频或视频禎）正好在一个暂停点开始，那么表示将不会被播放或记录。如果 Range 头缺失，那么在收到暂停消息后媒体流传输立即中断，并且暂停点设置成当前正常播放时间。

### 5. TEARDOWN

- C–>S

```http
TEARDOWN rtsp://192.168.31.115:8554/live RTSP/1.0\r\n
CSeq: 6\r\n
Session: 66334873\r\n
\r\n
```

- S–>C

  服务端也可能不返回响应

```http
RTSP/1.0 200 OK\r\n
CSeq: 6\r\n
\r\n
```

TEARDOWN 请求终止了给定 URI 的媒体流传输，并释放了与该媒体流相关的资源

### 总结

上述的过程只是标准的、友好的 rtsp 流程，但实际的需求中并不一定按此过程。
**其中第三步`SETUP`和第四步`PLAY`是必需的！**  
第一步，只要服务器客户端约定好，有哪些方法可用，则 option 请求可以不要。第二步，如果我们有其他途径得到媒体初始化描述信息（比如 http 请求等等），则我们也不需要通过 rtsp 中的 describe 请求来完成。

# SDP 协议格式

我们上面避开没有讲 sdp 文件，这里来好好补一补

## 协议说明

SDP(SessionDescription Protocol )会话描述协议，用于描述多媒体会话，它为会话通知、会话初始和其它形式的多媒体会话初始等操作提供服务。

SDP 的设计宗旨是通用性协议，所有它可以应用于很大范围的网络环境和应用程序，但 SDP 不支持会话内容或媒体编码的协商操作。

SDP 信息包括：

- 会话名称和目标；
- 会话活动时间；
- 构成会话的媒体；
- 有关接收媒体的信息、地址等。

## Key-Value 字段说明

sdp 格式由多行的`type=value`组成，SDP 信息是文本信息，UTF-8 编码采用 ISO 10646 字符设置。

sdp 会话描述由**一个会话级描述**和**多个媒体级描述**组成。会话级描述的作用域是整个会话，媒体级描述描述的是一个视频流或者音频流.

- 会话级描述由`v=`开始到第一个媒体级描述结束

- 媒体级描述由`m=`开始到下一个媒体级描述开始之前

1. **SDP 会话描述如下**（标注\*符号的表示可选字段）

   - v= （协议版本）
   - o= （一系列会话参数）
   - s= （会话名称）
   - i=\* （会话信息）
   - u=\* （URI 描述）
   - e=\* （Email 地址）
   - p=\* （电话号码）
   - c=\* （连接信息 ― 如果包含在所有媒体中，则不需要该字段）
   - b=\* （带宽信息）

2. **一个或更多时间描述**

   - z=\* （时间区域调整）
   - k=\* （加密密钥）

3. **时间描述**

   - t= （会话活动时间）
   - r=\* （0 或多次重复次数）

4. **0 个或多个媒体描述**

   - m= （媒体名称和传输地址）
   - i=\* （媒体标题）
   - c=\* （连接信息 — 如果包含在会话层则该字段可选）
   - b=\* （带宽信息）
   - k=\* （加密密钥）
   - a=\* （0 个或多个会话属性线路）

## SDP 示例

```
v=0
o=mhandley 2890844526 2890842807 IN IP4 126.16.64.4
s=SDP Seminar
i=A Seminar on the session description protocol
u=http://www.cs.ucl.ac.uk/staff/M.Handley/sdp.03.ps
e=mjh@isi.edu (Mark Handley)
b=AS:5050
c=IN IP4 224.2.17.12/127
t=2873397496 2873404696
a=recvonly
m=audio 49170 RTP/AVP 0
m=video 51372 RTP/AVP 31
m=application 32416 udp wb
a=orient:portrait
a=rtpmap:96 H264/90000
a=control:rtsp://10.86.77.14:554/h264/ch1/sub/av_stream/trackID=1


//字段解释
V=0     ;Version 给定了SDP协议的版本
 o=<用户名> <会话id> <会话版本> <网络类型><地址类型> <地址>
<address>； Origin ,给定了会话的发起者信息
s=<sessionname> ;给定了Session Name
i=<sessiondescription> ; Information 关于Session的一些信息
u=<URI> ; URI
b=<modifier>:<value>; AS:5050：带宽5050 kb/s
e=<emailaddress>    ;Email
c=<networktype> <address type> <connection address> ;Connect Data包含连接数据
t=<会话起始时间> <结束时间>
a=<属性>:<值>
m=<媒体类型> <端口号> <传输协议> <媒体格式
a=rtpmap:96 H264/90000
格式为a=rtpmap:<媒体格式><编码格式>/<时钟频率>
a=framerate:25
表示帧率
a=control:rtsp://10.86.77.14:554/h264/ch1/sub/av_stream/trackID=1
表示这路视频流在这个会话中的编号

```

# RTP 协议

## RTP 包格式

rtp 包由 rtp 头部和 rtp 荷载构成

### RTP 固定头部

![rtpHeader](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/rtp.png)

- 版本号(V)：

  2Bit，用来标志使用 RTP 版本，当前协议版本号为 2。

- 填充位(P)：

  1Bit，若 P=1 则在该报文的尾部填充一个或多个额外的八位组，数值为一串 0，**它们不是有效载荷的一部分**，表示报文对齐。RTP 报文的最后一个字节（8bit) 指明可以忽略多少个填充比特，填充可能用于某些具有固定长度的加密算法，或者用于在底层数据单元中传输多个 RTP 包。当一个 TCP 报文 携带多个 RTP 包的时候，由于每个 RTP 包的载荷长度不固定，RTP 报文需要将长度填充为 8 的倍数，即填充一串 0，来方便报文解析。

- 扩展位(X)

  1Bit，若 X=1，则在 RTP 报头后跟有一个扩展头。

- CSRC 技术器(CC)：

  4Bit，含有固定头部后面跟着的 CSRC 的数据, 指示 CSRC 标识符的个数

- **标记位(M)**：

  1Bit，不同的有效载荷有不同的含义，**对于视频，标记一帧的结束；对于音频，标记会话的开始。**

- **载荷类型**(PT)：

  7Bit，标识了 RTP 载荷的类型，如 GSM 音频、JPEM 图像等。

  **注**：rfc 里面对一些早期的格式定义了这个 payload type。**但是后来的，如 h264 并没有分配，那就用 96 来代替。因此现在 96 以上都不表示特定的格式，具体表示什么要用 sdp 或者其他协议来协商。**

- **序列号**(SN)：

  16Bit，序列号的初始值是随机的， 发送方在每发送完一个 RTP 包后就将该域的值增加 1，接收者用序列号来检测报文丢失，排序报文，恢复数据。

- 时间戳：

  32 比特，反映该 RTP 报文的第一个八位组的采样时刻。接收者使用时戳来计算延迟和延迟抖动，并进行同步控制。时钟频率依赖于负载数据格式，并在描述文件（profile）中进行描述。也可以通过 RTP 方法对负载格式动态描述。

- **同步源标识符(SSRC)**：

  32 比特，**同步源就是 RTP 包源的来源。该标识符是随机选择的**，在同一个 RTP 会话中不能有两个相同的 SSRC 值。参加同一视频会议的两个同步信源不能有相同的 SSRC。

- 贡献源列表(CSRC List)：

  可以有 0 ～ 15 个，每个 32 比特，这个不常用。

  每个 CSRC 标识了包含在该 RTP 报文有效载荷中的所有特约信源。CSRC 识别符由混合器插入，并列出所有贡献源的 SSRC 识别符。

  在共流源标识并且没有拓展头部（X=0）的情况下，RTP 头部为 12 个字节。

```c
//RTP固定头
typedef struct RTP_FIXED_HEADER{
	/* byte 0 */
	unsigned char csrc_len:4;       /* expect 0 */
	unsigned char extension:1;      /* expect 1 */
	unsigned char padding:1;        /* expect 0 */
	unsigned char version:2;        /* expect 2 */
	/* byte 1 */
	unsigned char payload:7;
	unsigned char marker:1;        /* expect 1 */
	/* bytes 2, 3 */
	unsigned short seq_no;
	/* bytes 4-7 */
	unsigned  long timestamp;
	/* bytes 8-11 */
	unsigned long ssrc;            /* stream number is used here. */
} RTP_FIXED_HEADER;
```

### RTP 荷载 Payload

**rtp 载荷为压缩编码过的压缩编码过的音频或者视频数据**。

### RTP 拓展头部

RTP 提供拓展机制以允许实现个性化，某些与常规负载格式功能要求相独立的附加信息在 RTP 拓展头的定义中实现。

![rtpExample](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/rtp4.jpg)

若 RTP 固定头中的扩展标志位 X 置 1，则一个长度可变的扩展头部分被加到 RTP 固定头之后。扩展包含 16 比特的长度域，指示扩展项中 32 比特字的个数，不包括 4 个字节扩展头(因此零是有效值)。RTP 固定头之后只允许有一头个头扩展。为了使拓展头具有特定的含义,扩展头的前 16 比特用来作为特定含义的识别标识符或参数。这 16 比特的格式由具体实现的上层协议定义。基本的 RTP 说明并不定义任何头扩展本身。

#### RTP 规格级别(profile)

profile 定义了一系列负载类型和对应的负载格式，也定义了特定于具体应用的 RTP 扩展和修改。典型地，某个应用仅基于一个规格级别运行。IETF 针对 RFC3550 在档次方面定义了一系列扩展协议。

![rtpExample](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/rtp5.png)

**RFC3551**(RTP/AVP)在 RFC3550 的基础上针对 RTP 档次进行补充形成 RTP/APVP 档次，被用在具有最小会话控制的音视频会议中，是其它扩展档次的基础。该档次在没有参数协商和成员控制的会话中非常有用。该档次也为音视频定义一系列编码和负载格式。对于具体的流媒体负载格式，IETF 也定义一系列协议详细描述，如 VP8 视频负载格式[6]和 H264 视频负载格式[7]，等等。

RFC3711(SRTP，也即 RTP/SAVP)是 RTP/AVP 在安全方面进行扩展形成的档次，为 RTP/RTCP 提供数据加密、消息认证、重放保护等功能。SRTP 具有高吞吐量和低数据膨胀等特点，是异构环境下对 RTP/RTCP 数据的有效保护。

RFC4585(RTP/AVPF)是 RTP/AVP 在及时反馈方面进行扩展形成的档次，使得接收端能够向发送端提供及时反馈，实现短时调整和基于反馈的修复机制。该协议定义早期 RTCP 报文以实现及时反馈，并定义一系列通用 RTCP 反馈报文和特定于应用的反馈报文，如 NACK、PLI、SLI、RPSI 等。

RFC5124(RTP/SAVPF)则是 RTP/SAVP 和 RTP/AVPF 的综合。SAVP 和 AVPF 在使用时，需要参与者借助于 SDP 协议[8]就档次和参数信息达成一致。但是对一个 RTP 会话来说，这两种档次不能同时被协商。而实际应用中，我们有同时使用这两种档次的需要。因此，RTP/SAVPF 档次应运而生，它能够使得 RTP 会话同时具有安全和及时反馈两方面的特性。

## 3.2 RTP OVER TCP

RTP 默认是采用 UDP 发送的，格式为 RTP 头+RTP 载荷，**如果是使用 TCP，那么需要在 RTP 头之前再加上四个字节**

- 第一个字节：Magic(0x24)--辨识符

- 第二个字节：Channel--通道，在 SETUP 的过程中获取

- 第三第四个字节：Length--RTP 包(头部+载荷）的大小，最多只能 12 位，第三个字节保存高 4 位，第四个字节保存低 8 位

### RTP OVER TCP 包示例

#### 说明

本人使用 Wireshark 抓包工具，开始监听网口后，用 openCV 的 VideoCapture() 方法播放了一个网络摄像头的画面，代码如下。（按 q 退出播放）

```python
import cv2
cap = cv2.VideoCapture('rtsp://admin:admin777@10.86.77.14:554/h264/ch1/sub/av_stream')

while (1):
    ret, img = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 释放窗口资源
```

如下是整个 RTSP 通信流程的 Wireshark 抓包界面，我们看到第一个 RTP 包的序号（SN），是随机的 64758，第一个报文展开后看到其携带了 3 个 RTP 包，所以下一个报文的序号是 64758 + 3 = 64761

![rtpExample](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/rtp3.png)

一个报文中可以携带多个 RTP 包， 如下图显示为 3 个 RTP 包，每个包的序列号递增。
![rtpExample](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/rtp1.png)

继续展开第一组 RTP 包

![rtpExample](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/rtp2.png)

**字段含义：**

- 版本 V=2
- P=1 ，尾部填充对齐
- X=0，无扩展头
- M=0， 视频流的帧未结束。
- PT=96：查阅[RFC3551](https://www.iana.org/assignments/rtp-parameters/rtp-parameters.xhtml), 为 dynamicRTP 类型
- SN=64758：包序列号
- TimeStamp：2794043652 ，时间戳
- PayLoad：载荷
- Padding count=1：载荷最后有 1 个 0 是填充上去的。

# RTCP 协议

RTCP 需要与 RTP 协议一起配合使用，当应用程序启动一个 RTP 会话时将同时占用两个端口（复用情况下占用同一个端口），分别供 RTP 和 RTCP 使用。RTP 本身并不能为数据包提供可靠传输的保证，也不提供流量控制和拥塞控制，这些都由 RTCP 来负责完成。通常 RTCP 会采用与 RTP 相同的分发机制，向会话中的所有成员周期性地发送控制信息，应用程序通过接收这些数据，从中获取会话参与者的相关资料，以及网络状况、分组丢失概率等反馈信息，从而能够对服务质量进行控制或者对网络状况进行诊断。

[更多介绍](https://blog.csdn.net/Explorer_day/article/details/78641723)

## RTCP 功能概括

RTCP 的主要功能可以概括为 3 个方面，服务质量的监视与反馈、媒体间的同步、多播组中成员的标识。此外还可以进行丢包重传或者 I 帧重传的控制。下面是消息类型

| Type    | Description                              | References |
| :------ | :--------------------------------------- | :--------: |
| 0-191   |                                          |            |
| 192     | FIR, full INTRA-frame request.           |  RFC 2032  |
| 193     | NACK, negative acknowledgement.          |  RFC 2032  |
| 194     | SMPTETC, SMPTE time-code mapping.        |  RFC5484   |
| 195     | IJ,extended inter-arrival jitter report. |  RFC 5450  |
| 196-199 |                                          |
| 200     | SR, sender report.                       |  RFC 3550  |
| 201     | RR, receiver report.                     |  RFC 3550  |
| 202     | SDES, source description.                |  RFC 3550  |
| 203     | BYE, goodbye.                            |  RFC 3550  |
| 204     | APP, application defined.                |  RFC 3550  |
| 205     | RTPFB, Generic RTP Feedback.             |
| 206     | PSFB, Payload-specific Feedback.         |
| 207     | XR, RTCP extension.                      |  RFC 3611  |
| 208     | AVB, AVB RTCP packet.                    | IEEE 1733  |
| 209     | RSI, Receiver Summary Information.       |  RFC 5760  |
| 210-255 |                                          |

其中以发送者报告举例

![rtcp](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/rtcp.png)

- 版本(V)：同 RTP 包头域.
- 填充(P)：同 RTP 包头域.
- 接收报告计数器(RC)：5 比特, 该 SR 包中的接收报告块的数目, 可以为零.
- 包类型(PT)：8 比特, SR 包是 200.
- 长度域(Length)：16 比特, 其中存放的是该 SR 包以 32 比特为单位的总长度减一.
- 同步源(SSRC)：SR 包发送者的同步源标识符, 对应 RTP 包中的 SSRC 一样.
- NTP timestamp：SR 包发送时的绝对时间值, NTP 的作用是同步不同的 RTP 媒体流, 一共 8 个字节，前 4 个字节代表
- RTP timestamp：与 NTP 时间戳对应, 与 RTP 数据包中的 RTP 时间戳具有相同的单位和随机初始值.
- Sender's packet count：从开始发送包到产生这个 SR 包这段时间里, 发送者发送的 RTP 数据包的总数, SRC 改变时这个域清零.
- Sender's octet count：从开始发送包到产生这个 SR 包这段时间里, 发送者发送的净荷数据的总字节数(不包括头部和填充), 发送者改变其 SSRC 时这个域要清零.
- 同步源 n 的 SSRC 标识符：该报告块中包含的是从该源接收到的包的统计信息.
- 丢失率(Fraction Lost)：表明从上一个 SR 或 RR 包发出以来从同步源 n(SSRC_n)来的 RTP 数据包的丢失率.
- 累计的包丢失数目：从开始接收到 SSRC_n 的包到发送 SR, 从 SSRC_n 传过来的 RTP 数据包的丢失总数.
- 收到的扩展最大序列号：从 SSRC_n 收到的 RTP 数据包中最大的序列号.
- 接收抖动(Interarrival jitter)：RTP 数据包接受时间的统计方差估计.
- 上次 SR 时间戳(Last SR,LSR)：取最近从 SSRC_n 收到的 SR 包中的 NTP 时间戳的中间 32 比特, 如果目前还没收到 SR 包, 则该域清零.
- 上次 SR 以来的延时(Delay since last SR,DLSR)：上次从 SSRC_n 收到 SR 包到发送本报告的延时.

参考：

- [[雷神]视音频编解码技术零基础学习方法](https://blog.csdn.net/leixiaohua1020/article/details/18893769)
- [从零开始写一个 RTSP 服务器（一）RTSP 协议讲解](https://blog.csdn.net/weixin_42462202/article/details/98986535)

- <https://blog.csdn.net/leixiaohua1020/article/details/11955341>

- https://blog.csdn.net/qq_29621351/article/details/81096857

RFC 文档：

- [Real-Time Transport Protocol (RTP) Parameters](https://www.iana.org/assignments/rtp-parameters/rtp-parameters.xhtml)

- [RFC6184-RTP 载荷 H.264 视频格式](https://tools.ietf.org/html/rfc6184)
<!-- #endregion -->
