> - [官方文档](https://mitmproxy.org/)
>
> - [github](https://github.com/mitmproxy/mitmproxy)
>
> - nodejs 类似框架：[anyproxy](https://github.com/alibaba/anyproxy)

# 一、功能简介

1. 实时拦截、修改 HTTP/HTTPS 请求和响应
2. 可保存完整的 http 会话，方便后续分析和**重放**
3. 支持反向代理模式将流量转发到指定服务器
4. 支持 macOS 和 Linux上的透明代理模式
5. 支持用 Python 脚本对 HTTP 通信进行修改



# 二、安装

```sh
pip3 install mitmproxy
```

使用 pip 快速安装 mitmproxy（前提已经安装了 python>=3.6 环境）：

```sh
pip3 install mitmproxy
```

![image-20220916183242131](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/mitmproxy1.png)


macOS 用户也可以用 brew 安装

```sh
brew install mitmproxy
```

> windows用户建议安装[Windows Terminal](https://aka.ms/terminal)以提高终端渲染效率

> [Docker 镜像地址](https://hub.docker.com/r/mitmproxy/mitmproxy/)

# 三、核心组件简介

mitmproxy 主要包含以下三个工具，你可以从 python 安装目录下的 Scripts 文件夹下找到，并为其创建快捷方式，方便以后使用

![image-20220916183557748](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/mitmproxy2.png)

这三个命令功能一致，且都可以加载自定义脚本，唯一的区别是交互界面的不同。

### 1. mitmproxy 

![img](https://docs.mitmproxy.org/stable/screenshots/mitmproxy.png)

**mitmproxy** 是一个控制台工具，允许交互式检查和修改 HTTP 流量。它与 mitmdump 的不同之处在于所有流都保存在内存中，这意味着它旨在获取和处理小样本。使用 <code>?</code> 问号键查看上下文相关使用文档。

（**windows 暂不支持**）

### 2. mitmweb

![img](https://docs.mitmproxy.org/stable/screenshots/mitmweb.png)

**mitmweb** 是 mitmproxy 的基于 Web 的用户界面，允许交互式检查和修改 HTTP 流量。与 mitmproxy 一样，所有流都保存在内存中.

>目前还处于beta测试阶段，许多 mitmproxy 特性还不支持。



个人觉得这个东西不好用，也不是我们着重学习的东西，可视化的抓包、过滤工具有很多，同类型比这个好用的有charles（强推）、fiddler、Burpsuit等，专业点的 Wireshark（不适合http），不管是做开发、运维、测试，总得熟练使用一款抓包工具，但肯定不是 minweb 🤣

### 3. mitmdump

mitmdump 提供了类似 [tcpdump](https://www.runoob.com/linux/linux-comm-tcpdump.html) 的功能（做过运维的同学应该都会用😁），让你可以查看、记录和以编程方式转换 HTTP 流量。有关完整文档，请参阅 `--help` 参数。

#### 示例1 ：保存流量包

```sh
# 开启代理监听模式（默认8080端口），并将抓到的所有包保存到 outfile
mitmdump -w outfile
```
#### 示例2：过滤并保存流量

```sh
mitmdump -nr infile -w outfile "~m post"
```

启动 mitmdump 在不绑定代理端口（-n）的情况下，从 infile 读取所有流，并按指定的表达式（仅匹配 POST）过滤后，写入 outfile。

#### 示例3：客户端重放

```sh
mitmdump -nC outfile
```

启动 mitmdump 在不绑定到代理端口 (-n)的情况下，然后重放来自 outfile (-C 文件名) 的所有请求。

显然，你也可以重放一个文件（srcfile），并将其写入另一个文件（dstfile）：

```sh
mitmdump -nC srcfile -w dstfile
```

客户端重放功能详见连接：[client-side replay](https://docs.mitmproxy.org/stable/overview-features/#client-side-replay)

#### 示例4：执行脚本

```sh
mitmdump -s examples/simple/add_header.py
```

运行 add_header.py 官方示例脚本，该脚本是为所有 response 添加一个新标头。

#### 示例5：数据转换

```sh
mitmdump -ns examples/simple/add_header.py -r srcfile -w dstfile
```

此命令从 srcfile 加载流，根据指定的脚本对其进行转换，然后将其写回 dstfile。



# 四、🚨安装ssl证书



mitmproxy 作为一个常规的http代理服务器使用时，默认监听 `http://localhost:8080`，因此要想数据包经过 mitmproxy，需要配置浏览器的代理（本机或其他机器），代理设置步骤请自行搜索（比如插件：SwitchyOmega)。

代理设置好后可打开 [http://mitm.it](http://mitm.it/) 验证http流量是否经过 mitmproxy。



如果显示以下文字，则代理配置的不对，流量不走 mitmproxy

```
If you can see this, traffic is not passing through mitmproxy.
```

如果配置正确，打开  [http://mitm.it](http://mitm.it/) 会显示如下界面：

![img](https://docs.mitmproxy.org/stable/certinstall-webapp.png)

mitmproxy 中可以看到抓到的数据包：

![image-20220920232445665](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/202209202324326.png)



**在上面的浏览器页面中根据你的操作系统，选择下载相应的证书文件，然后点击后面的 `Show Instructions` 按钮显示证书安装步骤**，看不懂英文的小伙伴可以直接翻译过来



使用 mitmproxy 抓包时，发现很多请求会返回 413 错误，找到解决方案是抓包时候，添加 `--set http2=false` 参数，比如：

```bash
mitmweb.exe -s .\gid.py --set http2=false
```

---

- [PC微信小程序抓包需要3.4.5及以前的版本 - 微信历史版本](https://mydown.yesky.com/pcsoft/44417133/versions/)
- [最全面的解决Charles手机抓包的证书问题(步骤非常详细) - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/281126584)