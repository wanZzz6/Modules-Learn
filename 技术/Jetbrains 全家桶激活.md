# 服务器激活Jetbrains 全家桶

> 2023-08-09测试：通过这种方式进行激活，不可用了

使用在线的激活服务器在短期内进行授权激活，缺点是经常到期，需要频繁更换激活服务器地址。

## 一、搜索服务器地址

### 1. Shodan 搜索

搜索语法：

```
Location: https://account.jetbrains.com/fls-auth
```
或者直接点击：

[https://www.shodan.io/search?query=Location%3A+https%3A%2F%2Faccount.jetbrains.com%2Ffls-auth](https://www.shodan.io/search?query=Location%3A+https%3A%2F%2Faccount.jetbrains.com%2Ffls-auth)

### 2. FOFA 搜索

[https://fofa.info/result?qbase64=TG9jYXRpb246IGh0dHBzOi8vYWNjb3VudC5qZXRicmFpbnMuY29tL2Zscy1hdXRo](https://fofa.info/result?qbase64=TG9jYXRpb246IGh0dHBzOi8vYWNjb3VudC5qZXRicmFpbnMuY29tL2Zscy1hdXRo)

![](https://zgao.top/wp-content/uploads/2022/06/image-98-1024x623.png)

二、激活 IDE
------

从搜索结果中随便选一个，右键复制连接地址，打开JetBrain软件，选择第三种License server 激活方式，粘贴服务器地址，点击激活。

![](https://zgao.top/wp-content/uploads/2022/06/image-104-1024x660.png)

![](https://zgao.top/wp-content/uploads/2022/06/image-105-1024x491.png)

![](https://zgao.top/wp-content/uploads/2022/06/image-106-1024x614.png)

如果失败就换一个地址重试。
