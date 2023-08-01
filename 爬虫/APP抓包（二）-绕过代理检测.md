# 绕过代理检测

## 一、概述

我们要在手机上抓包时，最直白的做法是在wifi属性界面手动设置代理服务的地址和端口，也就是抓包软件的监听地址，这种不依赖任何转发软件的方式有时会抓不到包，甚至一旦设置了代理App就提示网络错误，而关闭代理，App就能正常使用。

这种情况首先要判断是不是app中存在**禁用代理**或者**代理检测**手段，其次再考虑证书绑定的问题

### 1. 禁用代理

从App开发者角度来说，如果想让http\https 请求不走代理转发，即直连到服务器，就需要在网络连接库中开启禁用代理相关的属性。

以安卓开发常用的网络连接库 **[okhttp](https://github.com/square/okhttp)** 为例，可以在`OkHttpClient.Builder()`中设置[`.proxy(Proxy.NO_PROXY)`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/) ，这样一般使用中间人的抓包软件就使用不了。

### 2. 代理检测

还是从App开发者角度出发，判断用户是否开启了网络代理，如果开启就禁止App正常使用：

```java
public static boolean isWifiProxy() {
    final boolean IS_ICS_OR_LATER = Build.VERSION.SDK_INT >=    Build.VERSION_CODES.ICE_CREAM_SANDWICH;
    String proxyAddress;
    int proxyPort;
    if (IS_ICS_OR_LATER) {
        proxyAddress = System.getProperty("http.proxyHost");
        String portStr = System.getProperty("http.proxyPort");
        proxyPort = Integer.parseInt((portStr != null ? portStr : "-1"));
    } else {
        proxyAddress = android.net.Proxy.getHost(context);
        proxyPort = android.net.Proxy.getPort(context);
    }
        return (!TextUtils.isEmpty(proxyAddress)) && (proxyPort != -1);
}
```

## 二、解决办法

上述两种原因的解决办法是通用的，但是具体方法不唯一

### 1. 手机加装代理App

最推荐的方法就是在手机端按装vpn软件，装代理App的好处有很多：切换代理不必手动改wifi设置、排除其他App干扰数据包、方便切换不同上级代理地址等。

Android 和 iOS 都有适用的软件

- iOS：小飞机（SS）
- Android：Drony、Postern 等

Drony可以针对具体App抓包，更加灵活，Postern跟小飞机一样只能全局代理和按url规则转发。

各种代理软件的适用方法大同小异，无非就是设置上级抓包软件的地址和端口，然后设置代理规则，最后开启代理转发。只有一点需要注意，当你使用的抓包软件支持 SOCKS 代理方式时（比如Charles、mintmproxy)，**优先使用SOCKS 代理**方式，可以抓到更多非http类型的数据包。

> - HTTP代理：HTTP代理是基于HTTP协议的代理服务，它主要用于在客户端和服务器之间进行HTTP通信，并可以进行HTTP请求和响应的解析和修改。HTTP代理可以透明地改变HTTP报文的内容，包括请求和响应的头部、主体和方法等，并且支持HTTP的加密和认证等功能。HTTP代理通常工作在应用层，对应用层协议进行解析和处理。
>
> - SOCKS代理：SOCKS代理是一种通用的网络代理协议，它可以将任意的数据流转发给目标服务器。SOCKS代理不会对数据流进行解析和修改，它只是对数据流进行转发，不限于特定的协议。SOCKS代理通常工作在传输层，对网络层协议（如TCP和UDP）进行转发和处理。
>
>   (来自ChatGPT3.5的解释)

### 2. root环境下

