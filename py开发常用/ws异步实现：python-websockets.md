# websockets 使用文档(V10.4)

项目地址：[https://github.com/aaugustin/websockets](https://github.com/aaugustin/websockets)

官方文档：[https://websockets.readthedocs.io/](https://websockets.readthedocs.io/)



## 一、前言

`websockets` 是一个在 python中用于构建 Websocket 服务端、客户端的库，上层基于 python 标准异步框架 [`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio)开发, 具有高性能（就python而言）、简洁、稳定的特性.

本教程包含 websockets 的服务端和客户端开发两部分主要内容，以及实战中的技巧和模板，请仔细阅读，如有问题欢迎评论指正。

在开始之前，我假设你已经学会如何使用 [`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio) 和 `typing` 模块了😀。

## 二、安装

- 环境：>=python3.7

- 安装命令

```sh
pip install -U websockets
```

## 三、常用 API

你可以先跳过此部分枯燥的说明，先看后文示例。

代码中常用到三个类：`WebSocketServer`、`WebSocketServerProtocol`和 `WebSocketClientProtocol`

- **WebSocketServer**：其实例就是 server 对象，负责开启、关闭监听服务

在代码中我们主要操作两个类：，他们都继承自 `websockets.legacy.protocol.WebSocketCommonProtocol`，通过操作这两个类的实例对象

### 1. 连接对象

先来了解一下客户端可服务端都需要的 `WebSocketCommonProtocol`，实际不会直接使用此类，而是使用它的子类。

这部分关于父类中的构造参数、属性和方法在 server 对象和 client 对象中是通用的，后续就不展开解释了。

```python
class WebSocketCommonProtocol(*, logger=None, ping_interval=20, ping_timeout=20, close_timeout=10, max_size=2**20, max_queue=2**5, read_limit=2**16, write_limit=2**16)
```

**构造参数：**

- **logger**：默认为 `logging.getLogger("websockets.server")`
- **ping_interval**: 整形。当连接一建立，websockets 会每隔 `ping_interval` 秒发送 [Ping](https://www.rfc-editor.org/rfc/rfc6455.html#section-5.5.2) 数据帧用于保活。设为 `None` 可禁用此行为。
- **ping_timeout**：若服务端在发送 Ping 帧后的 `ping_timeout` 秒内没有收到客户端的 [Pong](https://www.rfc-editor.org/rfc/rfc6455.html#section-5.5.3) 帧响应，这个连接被认为是不可用的，并以 1011 状态码退出。设为 `None` 可禁用此行为。
- **close_timeout**：调用 [`close()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.close) 方法（或退出 serve 上下文管理器）关闭连接的最大等待时间。由于时延原因，调用[`close()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.close) 方法对于客户端会最多等待 `5 * close_timeout` 秒就会强制关闭，而对于服务端最多等待 `4 * close_timeout` 秒。关于超时问题的讨论请阅读：[timeouts](https://websockets.readthedocs.io/en/stable/topics/timeouts.html)
- **max_size**：限制单条输入消息的大小，默认 1M。如果超过此阈值，[`recv()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.recv) 方法会抛出 [`ConnectionClosedError`](https://websockets.readthedocs.io/en/stable/reference/exceptions.html#websockets.exceptions.ConnectionClosedError) 异常，并以 1009 状态码退出。
- **max_queue**：限制消息接收队列最大长度，默认32。server 对象收到消息后会先暂存到内存中的一个队列中，每次调用 [`recv()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.recv) 方法就会从队列头部（pop）取出一条数据，目的是为了防止接收数据过快而来不及消费。如果队列已满，server 对象会丢弃后续数据，直到调用 [`recv()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.recv) 方法使队列有空间存放。
- **read_limit**、**write_limit**：限制输入、输出缓冲区的大小，默认 64KB。根据实际自己实际情况调整，尽量每次能将消息完整读写又不浪费太多内存空间。

>python 中一个字符占 4 byte，若使用上述默认参数，一个连接最多会消耗内存: `4 * max_size * max_queue` (byte)，也就是 `4 * 1M * 32 = 128M`

**实例方法：**

- `await recv()`：等待接收下一条消息并返回接收到的数据，连接关闭后再调用会抛出 `ConnectionClosed` 异常。准确讲，正常关闭会抛出 [`ConnectionClosedOK`](https://websockets.readthedocs.io/en/stable/reference/exceptions.html#websockets.exceptions.ConnectionClosedOK)，因协议错误或网络中断会抛出  [`ConnectionClosedError`](https://websockets.readthedocs.io/en/stable/reference/exceptions.html#websockets.exceptions.ConnectionClosedError) 异常。

  `cancel()` 取消该协程是安全的，不会导致数据消息丢失。

  配合 [asyncio.wait_for()](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for) 可限制等待时间。

  返回 `str` 或者 `bytes` 类型数据。

- `await send(message)`：发送消息，message 类型可以是：`str、bytes、bytearray、memoryview`，也可以是返回这些类型的（异步）可迭代对象，如果是后者，要求可迭代对象中的数据类型必须一致。连接关闭后再调用会抛出 `ConnectionClosed` 异常。准确讲，正常关闭会抛出 [`ConnectionClosedOK`](https://websockets.readthedocs.io/en/stable/reference/exceptions.html#websockets.exceptions.ConnectionClosedOK)，因协议错误或网络中断会抛出  [`ConnectionClosedError`](https://websockets.readthedocs.io/en/stable/reference/exceptions.html#websockets.exceptions.ConnectionClosedError) 异常。

- `await close(code=1000, reason='')`：主动关闭连接。调用后就无需再调用 `wait_closed()` 方法了。有时等待需要一段时间 TCP 连接才会彻底关闭，如果你不想等太久，可以重设对象的`close_timeout` 属性值。

- `await wait_closed()`：被动等待连接关闭，可以轻松的检测因任何原因导致的连接断开。

- `await ping(data=None)`：发送 [Ping](https://www.rfc-editor.org/rfc/rfc6455.html#section-5.5.2) 帧，用于服务保活，data参数可以携带字符串类型数据。返回一个 future 对象，可用于等待 `Pong` 响应。

  如果你想知道 ping 和 pong 之间的响应间隔，可以这样写：

  ```python
  pong_waiter = await ws.ping()
  latency = await pong_waiter
  ```

- `await pong(data=b'')`：发送 [Pong](https://www.rfc-editor.org/rfc/rfc6455.html#section-5.5.3) 帧，没有收到 `Ping` 帧时也可主动发送，用作单向心跳包。

**实例属性**：

- **id**：UUID，唯一标识
- **local_address**：本地连接地址
- **remote_address**：对方连接地址
- **open**、**closed**：判断是否已连接
- **latency**：连接延迟，秒。发送 ping 帧并且收到 pong 帧响应后这个值才会更新，初始为 0.

以下属性在连接建立后才可用：

- **path**：请求路径
- **request_headers**、**response_headers**：请求头、响应头
- **subprotocol**：子协议（如果协商过）

以下属性在关闭连接后可用：

- **close_code**：连接关闭代号，具体定义：[section 7.1.5 of RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html#section-7.1.5).
- **close_reason**：连接关闭原因，具体定义： [section 7.1.6 of RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html#section-7.1.6)



###  2. 服务端



开启端口监听， websockets.serve方法定义：

```python
await websockets.serve(ws_handler, host=None, port=None, *, create_protocol=None, logger=None, compression='deflate', origins=None, extensions=None, subprotocols=None, extra_headers=None, server_header='Python/x.y.z websockets/X.Y', process_request=None, select_subprotocol=None, ping_interval=20, ping_timeout=20, close_timeout=10, max_size=2**20, max_queue=2**5, read_limit=2**16, write_limit=2**16, **kwds)
```

每当客户端连接，服务端就创建一个 [`WebSocketServerProtocol`](https://websockets.readthedocs.io/en/stable/reference/server.html#websockets.server.WebSocketServerProtocol)对象（简称 server 对象），用来处理连接握手，并将该 server 对象委托给 `ws_hadnler` 处理。

server 对象提供了 [`close()`](https://websockets.readthedocs.io/en/stable/reference/server.html#websockets.server.WebSocketServer.close) 和 [`wait_closed()`](https://websockets.readthedocs.io/en/stable/reference/server.html#websockets.server.WebSocketServer.wait_closed) 方法用于关闭服务，但更推荐作为异步上下文管理器使用，退出上下文管理器时会自动调用这两个方法，具体用法见下文示例。



参数说明：

- **ws_handler**：是一个异步方法（函数）对象，接收一个 server 对象（<=10.0版本中还接收第二个path参数，表示请求路径），实现消息收发的主要处理逻辑。一旦 handler 方法正常结束或因异常终止，就意味着服务端的处理逻辑完成，要主动与客户端断开连接了。
- **host**：绑定本机的网络 ip 地址。
- **port**: 指定监听的 TCP 端口，
- **create_protocol**：一般用不到，除非你的项目需要高级定制 server 类。
- 
- **compression**：默认开启 “permessage-deflate” 压缩扩展，压缩数据可降低网络通信数据量，但会增加 cpu 和内存消耗，设为 `None` 可禁此功能。详见： [Compression](https://websockets.readthedocs.io/en/stable/topics/compression.html).
- **origin**：设置允许访问的 `Origin` 请求头列表，字符串列表或者 `None`。这对于防御跨站点WebSocket劫持攻击非常有用。e.g.: origin=['https://www.example.com']
- **extensions**: 支持的扩展列表，关于如何编写扩展请参考：[Write an extension](https://websockets.readthedocs.io/en/stable/howto/extensions.html)。
- **subprotocols**：设置`Sec-WebSocket-Protocol` 请求头支持的子协议，字符串列表，按优先级递减顺序排列。
- **extra_headers**：额外向 request 中添加的请求头。接收一个key和value都是字符串的字典对象，或者一个 *Callable[[[str](https://docs.python.org/3/library/stdtypes.html#str),[Headers](https://websockets.readthedocs.io/en/stable/reference/utilities.html#websockets.datastructures.Headers)], [HeadersLike](https://websockets.readthedocs.io/en/stable/reference/types.html#websockets.datastructures.HeadersLike)]]* 类型的方法。
- **server_header**：`Server` 响应头字段。
- **process_request**：在开始握手之前拦截HTTP请求，可用于 health check 或请求认证（认证失败返回401、403）。[`process_request()`](https://websockets.readthedocs.io/en/stable/reference/server.html#websockets.server.WebSocketServerProtocol.process_request) 
- **select_subprotocol**：选择客户端支持的子协议。[select_subprotocol()](https://websockets.readthedocs.io/en/stable/reference/server.html#websockets.server.WebSocketServerProtocol.select_subprotocol)

### 3. 客户端

```python

```



## 四、开发指南

### 1. Hello World

先写一个简单的测试代码

#### 服务端

服务端监听客户端连接，当客户端发送一个 name 字符串后，返回一条 `'Hello' + name` 的问候消息。

```python
#!/usr/bin/env python

import asyncio
import websockets


async def handler(server):
    name = await server.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await server.send(greeting)
    print(f">>> {greeting}")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```

为了保证资源正确释放，使用了 `async with` 上下文管理器创建 server 对象并开启监听端口，**执行完 `async with` 代码块就意味着关闭 server 监听服务。**

而 `await asyncio.Future()` 这行代码让 server 端主线程一直被挂起，因为这个 `Future` 对象我们没有让它 `cancel()` 或者 `set_result（）`，你可以根据你的需求在合适的时机让这个 `Future` 对象执行完，从而退出 `async with` 上下文。



每当有客户端连接上就转到 handler 协程中进行消息收发处理，同理，若 handler 协程执行完毕 server 便会主动断开与这个客户端的连接。

此例中，服务端 handler 中接受一条消息并回复一条消息，然后 handler 协程结束，主动与客户端断开连接。



既然选择使用 websocket 协议，那客户端与服务端之间肯定会多次互发消息，你可以在 handler 中使用 `while True` 循环接收并处理消息，但更优雅的写法是迭代 server 对象，具体使用见下文[开发模板](#develop-pattern)部分。

#### 客户端

客户端同样使用 `async with` 上下文管理器连接到 server，保证了协程退出之前自动关闭连接。

```python
#!/usr/bin/env python

import asyncio
import websockets


async def handler():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as client:
        name = input("What's your name? ")

        await client.send(name)
        print(f">>> {name}")

        greeting = await client.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(handler())
```

client 对象同样可以作为迭代器使用，用来实现持续消息收发，见下文[开发模板](#develop-pattern)部分。

## 2. wss 安全连接示例

基于SSL 证书的安全连接可提高保密性和可靠性，降低使用不安全的代理服务的风险。

`WSS` 协议之于 `WS` 就像 `HTTPS` 之于 `HTTP`，连接是用传输层安全(TLS)加密的，TLS通常被称为安全套接字层(SSL)，WSS 需要类似 HTTPS 的 TLS 证书。

> TLS 就是指 SSL (Secure Sockets Layer)，SSL 是最早期的传输层加密协议，TLS 是基于 SSL3.0 设计的。

在进行 wss 服务端开发之前，你需要准备一个 CA 证书，这里我们将其放到与服务端代码 server_secure.py 同级目录下

（点击下载自签名证书：[`localhost.pem`](https://websockets.readthedocs.io/en/stable/_downloads/c350abd2963d053f49c19e58cceced69/localhost.pem)）



基于前面的 Hello word 代码进行补充完善

- server_secure.py

```python
#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets


async def handler(server):
    name = await server.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await server.send(greeting)
    print(f">>> {greeting}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhost_pem)


async def main():
    async with websockets.serve(handler, "localhost", 8765, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```

> 关于 TLS 上下文配置的详细信息，请参阅标准模块： [`ssl`](https://docs.python.org/3/library/ssl.html#module-ssl)



对客户端代码进行 wss 适配：

- client_secure.py

```python
#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)


async def hello():
    uri = "wss://localhost:8765"
    async with websockets.connect(uri, ssl=ssl_context) as client:
        name = input("What's your name? ")

        await client.send(name)
        print(f">>> {name}")

        greeting = await client.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())
```

> **说明：**
>
> 上述客户端代码连接前需要一个 TLS 上下文，因为 server 端使用的是**自签名**的 CA 证书。
>
> 如果你的服务端证书是由信任的机构颁发，或者安装为系统信任的 CA 证书，就不必构建 ssl_context，也就不需要传 `ssl` 参数。

## 3. 从前端浏览器连接 server

websocket 顾名思义，设计的初衷就是为 web 端服务的。



- show_time.py

写一个简单的 server 端程序，随机等待一小段时间，给客户端发送服务端的 UTC 时间，代码如下：

```python
#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets


async def show_time(server):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await server.send(message)
        await asyncio.sleep(random.random() * 2 + 1)


async def main():
    async with websockets.serve(show_time, "localhost", 5678):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```



- index.html

将以下代码写入html文件，并从浏览器里打开

```html
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket demo</title>
    </head>
    <body>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:5678/"),
                messages = document.createElement('ul');
            ws.onmessage = function (event) {
                var messages = document.getElementsByTagName('ul')[0],
                    message = document.createElement('li'),
                    content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
            document.body.appendChild(messages);
        </script>
    </body>
</html>
```
>关于在前端中如何使用 websocket 请参考：  [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

## 4. 广播消息

前面发送 UTC 时间的示例中，在每个客户端 handler 协程中各生成一个 message 并发送，其效率肯定不如生成一个 message 然后并发向所有相关客户端发送，这就需要一个广播消息的方法。


>**相关API**：
>
>`websockets.broadcast(websockets: Iterable[WebSocketCommonProtocol], message: Union[str, bytes]) -> None:` 
>
>这是个同步方法，依次向参数 websockets 中包含的客户端实例发送消息，如果 websockets 实例处于未连接状态则跳过。



对前面的代码进行优化：

- show_time_2.py

```python
#!/usr/bin/env python

import asyncio
import datetime
import random
import websockets

# 保存已连接的 client 对象
CONNECTIONS = set()


async def register(server):
    CONNECTIONS.add(server)
    try:
        await server.wait_closed()
    finally:
        CONNECTIONS.remove(server)


async def show_time():
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        # 向 CONNECTIONS 集合中的所有 server 对象广播消息
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(random.random() * 2 + 1)


async def main():
    async with websockets.serve(register, "localhost", 5678):
        await show_time()

if __name__ == "__main__":
    asyncio.run(main())
```

## <span id='manage-state'>5. 管理应用状态</span>

在复杂点的服务端开发中，经常需要维护一些客户端的状态数据，举个简单的例子，多人在线游戏中，一个玩家对某个对象进行了操作，其数值发生了改变，其他玩家页面中的数据也得实时更新，玩家加入、退出、发送了消息等等，都需要实时广播出去，这些数据如果需要持久化，还得涉及一些 SQL 操作。



下面是一个实时计数器示例，每当用浏览器打开 index.html 主页面就相当于加入了一个玩家，同时打开多个 index.html 页面，就相当于加入了多个玩家。

任意玩家都能点击页面中的加号或减号对数值 counter 进行操作，所有已连接的玩家都会看到 counter 值的实时变化。

- counter.py

```py
#!/usr/bin/env python

import asyncio
import json
import logging
import websockets

logging.basicConfig()

# 保存所有在线客户端
USERS = set()

# 计数器的值
VALUE = 0


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


def value_event():
    return json.dumps({"type": "value", "value": VALUE})


# 广播更新所有客户端显示的counter值
def notify_state():
    if USERS:
        websockets.broadcast(USERS, value_event())


# 广播通知客户端在线数量
def notify_users():
    if USERS:
        websockets.broadcast(USERS, users_event())


# 注册客户端
def register(ws):
    USERS.add(ws)
    notify_users()

# 注销客户端
def unregister(ws):
    USERS.remove(ws)
    notify_users()


async def counter(server):
    global USERS, VALUE
    # 用户登录
    register(server)
    try:
        await server.send(value_event())
        # 迭代websocket以不断接收消息，此处要求对象实现了 __iter__()、__await__()、 __aenter__()、 __aexit__() 方法。
        async for message in server:
            data = json.loads(message)
            if data["action"] == "minus":
                VALUE -= 1
                notify_state()
            elif data["action"] == "plus":
                VALUE += 1
                notify_state()
            else:
                logging.error("unsupported event: %s", data)
    finally:
        # 客户端断开后，用户注销
        unregister(server)


async def main():
    async with websockets.serve(counter, "localhost", 6789):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```

将以下代码写入html文件，并用浏览器打开多个页面模拟多个 ws 客户端

```html
<html>
  <head>
    <title>WebSocket demo</title>
    <style type="text/css">
      body {
        font-family: 'Courier New', sans-serif;
        text-align: center;
      }
      .buttons {
        font-size: 4em;
        display: flex;
        justify-content: center;
      }
      .button,
      .value {
        line-height: 1;
        padding: 2rem;
        margin: 2rem;
        border: medium solid;
        min-height: 1em;
        min-width: 1em;
      }
      .button {
        cursor: pointer;
        user-select: none;
      }
      .minus {
        color: red;
      }
      .plus {
        color: green;
      }
      .value {
        min-width: 2em;
      }
      .state {
        font-size: 2em;
      }
    </style>
  </head>
  <body>
    <div class="buttons">
      <div class="minus button">-</div>
      <div class="value">?</div>
      <div class="plus button">+</div>
    </div>
    <div class="state"><span class="users">?</span> online</div>
    <script>
      window.addEventListener('DOMContentLoaded', () => {
        const websocket = new WebSocket('ws://localhost:6789/');

        document.querySelector('.minus').addEventListener('click', () => {
          websocket.send(JSON.stringify({ action: 'minus' }));
        });

        document.querySelector('.plus').addEventListener('click', () => {
          websocket.send(JSON.stringify({ action: 'plus' }));
        });

        websocket.onmessage = ({ data }) => {
          const event = JSON.parse(data);
          switch (event.type) {
            case 'value':
              document.querySelector('.value').textContent = event.value;
              break;
            case 'users':
              const users = `${event.count} user${event.count == 1 ? '' : 's'}`;
              document.querySelector('.users').textContent = users;
              break;
            default:
              console.error('unsupported event', event);
          }
        };
      });
    </script>
  </body>
</html>
```

## <span id='develop-pattern'>6. 开发模板</span>

下面演示如何将 **生产者-消费者** 思想运用到 **server** 端开发中，在以下示例中我们用 `websocket` 变量表示 server 连接对象。

这种开发模式在 client 端开发中也通用，体现在代码上的区别就是，在 client 开发中 `websocket` 连接对象是由 `connect()` 方法创建的。

### 消费者

```py
async def consumer(message):
    # 模拟处理延迟
    await asyncio.sleep(1)
    print('consumer: ', message)

async def consumer_handler(websocket, path):
    async for message in websocket:
        await consumer(message)
```

此例中，`consumer()` 是一个协程用于处理你的业务逻辑，message 类型是  `str` 或者 `bytes`。

`async for` 循环结束意味着客户端断开连接。

### 生产者

```py
count = 0

async def producer():
    global count
    # 模拟消息产生延迟
    await asyncio.sleep(3)
    count += 1
    return 'message' + str(count)
    
async def producer_handler(websocket):
    while True:
        message = await producer()
        await websocket.send(message)
```
此处 `producer()` 协程代表你的产生下一条消息的业务逻辑，message 同样必须是 `str` 或者 `bytes` 类型。

**注意：**当客户端断开连接后，`send()` 会引发 [`ConnectionClosed`](https://websockets.readthedocs.io/en/stable/reference/exceptions.html#websockets.exceptions.ConnectionClosed)异常，从而退出 `while True` 循环。

### 生产者 + 消费者

你可以将上面两种模式结合起来，生产者、消费者的任务独立并行，不必互相等待。

```py
async def handler(websocket):
    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    # 直到其中一方退出
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()
```

`asyncio.wait()` 的等待条件设为 `asyncio.FIRST_COMPLETED` 表示生产者协程或者消费者协程任何一方正常结束或抛出异常就会立即返回，返回值为一个元组 `(done, pending)`

（等待条件有三个： `FIRST_COMPLETED`、`FIRST_EXCEPTION`、`ALL_COMPLETED`，分别表示任意一个正常或异常结束、任意一个异常结束、全部都正常或异常结束）

### 注册、注销客户端

在 server 端开发中，通常得记录所有已连接的客户端，可临时将连接实例保存到集合中。

也可以参考上面[管理应用状态](#manage-state)部分的代码

```py
connected = set()

async def handler(websocket):
    # Register.
    connected.add(websocket)
    try:
        # Implement logic here.
        await asyncio.wait([ws.send("Hello!") for ws in connected])
        await asyncio.sleep(10)
    finally:
        # Unregister.
        connected.remove(websocket)
```
这个简单的示例展示了如何在内存中跟踪连接的客户端，关键在于 `finally` 代码块中确保注销掉该连接对象。

这种管理方式只适用于小型的**单进程**应用中。

### 发布-订阅模型

如果你想在多进程中运行，并且需要让进程之间通信，你必须部署一套消息收发系统，基于**发布-订阅**的消息系统是非常好用的。

简单高效做法是借助 Redis 的 [Pub/Sub](https://redis.io/docs/manual/pubsub/) 功能，具体做法可参考：[Django 集成指南](https://websockets.readthedocs.io/en/stable/howto/django.html).



## 五、要点总结

### 1. Server 端开发

- handler 处理器: 一个用于处理单个连接的**协程**函数，接收两个参数（`server.WebSocketServerProtocol `实例对象和 path 路径参数）

    - 调用[`recv()`]([recv() (websockets.readthedocs.io)](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.recv))和 [`send()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.send) 来接收和发送消息。
    - 一定不要写阻塞事件循环的代码，否则会阻塞客户端连接。如 `time.sleep(1)` 要换成 `await asyncio.sleep(1)`
    - 在 handler 中进行 `recv()` 或 `send()` 引发 `ConnectionClosed` 异常时，在退出 handler 协程前，先退出在 handler 中创建的其他 `asyncio.Task`。
    - 如果你不需要接收客户端发送的消息，使用 [`wait_closed()`]([wait_closed() (websockets.readthedocs.io)](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.wait_closed)) 方法一直等待连接断开，而不是 `recv()` 等待消息到达。
    - 调用 [`ping()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.ping)或 [`pong()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.pong)` 方法保活，但一般不需要。
    
- 使用 [`serve()`](https://websockets.readthedocs.io/en/stable/reference/server.html#websockets.server.serve) 方法创建 server 服务器对象，与 `asyncio` 模块中的 [`create_server()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_server) 方法相似，一般都配合 `async with` 异步上下文管理器使用。

    - server 主要负责建立连接， handler 负责消息处理逻辑。server 退出前一定要让 handler 中创建的全部协程正常退出或抛异常退出。
    - 对于高级定制，您可以编写一个定制类并继承 `WebSocketServerProtocol`类，并将这个子类或工厂函数作为 `create_protocol` 参数传递。
    

### 2. Client 端开发

- 使用[`connect()`](https://websockets.readthedocs.io/en/stable/api.html#websockets.client.connect)创建一个客户端，它类似于 `asyncio` 模块中的 [`create_connection()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_connection)，一般都配合 `async with` 异步上下文管理器使用。

    - 对于高级定制，你可以继承 `WebSocketClientProtocol`的子类，并将这个子类或工厂函数作为 `create_protocol` 参数传递。
    
- 调用 [`recv()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.recv)和 [`send()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.send) 来接收和发送消息。
- 调用 [`ping()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.ping)或[`pong()`](https://websockets.readthedocs.io/en/stable/reference/common.html#websockets.legacy.protocol.WebSocketCommonProtocol.pong)` 方法保活，但一般不需要。
- 如果没有使用 [`connect()`](https://websockets.readthedocs.io/en/stable/reference/client.html#websockets.client.connect) 作为上下文管理器，需要主动调用 `close()` 方法来终止连接。

### 3. 其他

- 必须熟练使用 `asyncio` 模块，如果你不了解 `asyncio ` 模块， 建议查看官方文档[develop with asyncio.](https://docs.python.org/3/library/asyncio-dev.html)

## 六、常见问题

### 服务端

#### 1. 如何向handler传递额外的参数

在前面的代码中，hadnler 函数在实际调用的时候只接受了一个 websocket 实例对象，在实际应用中可能需要向 handler 传递更多参数。（类比 `threading.Thread` 方法，`target` 参数为一个函数对象，当这个函数在调用时可通过 `args` 参数传递实参）

在 python 中，可使用用**闭包**给某一方法预先绑定实参，你可以自己写一个装饰器完成这项工作，也可以借助 [`functools.partial()`](https://docs.python.org/3/library/functools.html#functools.partial)：

```py
import asyncio
import functools
import websockets

async def handler(websocket, extra_argument):
    ...

bound_handler = functools.partial(handler, extra_argument='spam')
start_server = websockets.serve(bound_handler, '127.0.0.1', 8765)
```

另一种方法是在存在 `extra_argument` 变量的范围内定义 `handler` 协程，而不是通过参数注入它。

#### 2. 如何关闭server

退出 server 的异步上下文管理器 `async with`。



在**Unix系统**上，可注册一个 `signal.SIGTERM` 信号，在回调方法中退出异步上下文管理器 `async with`。

```py
#!/usr/bin/env python

import asyncio
import signal
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def server():

    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(echo, "localhost", 8765):
        await stop

asyncio.run(server())
```

#### 3. 如何与http共享端口

Websocket是HTTP/1.1.的扩展，在同一个端口上同时提供HTTP和WebSocket是ok的。

WebSocket的作者并不认为这是一个好主意，因为HTTP和WebSocket的操作特性有很大的不同，提供 HTTP 服务超出了 websockets 模块的功能范畴

如果有需要，请将 http 服务分开运行。

或者选择一个构建在WebSocket之上的HTTP框架来支持WebSocket连接，例如：[Sanic](https://sanicframework.org/en/)。

### 客户端

#### 1. 断开后如何重连

将 [`connect()`](https://websockets.readthedocs.io/en/stable/reference/client.html#websockets.client.connect)方法用作异步迭代器：

```python
async for websocket in websockets.connect(...):
    try:
        ...
    except websockets.ConnectionClosed:
        continue
```

注意捕获 `async for` 循环内的异常。

#### 2. 如何关闭连接

同样可以通过信号回调完成

```python
#!/usr/bin/env python

import asyncio
import signal
import websockets

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Close the connection when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(
            signal.SIGTERM, loop.create_task, websocket.close())

        # Process messages received on the connection.
        async for message in websocket:
            ...

asyncio.run(client())
```

### 两端通用

#### 1. 如何设置 `recv()` 的超时时间？

使用 [`wait_for()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for):

```python
await asyncio.wait_for(websocket.recv(), timeout=10)
```

#### 2. 如何维持空闲连接？

websockets 默认间隔 20s 自动发送 ping 消息，如果此后的20s内没有收到 pong 消息就会关闭连接，你可以调整参数 `ping_interval` 和 `ping_timeout`.

#### 3. 在多线程中使用问题

不建议在多线程中使用 `asyncio`，尽量使用 `Task`。

事实上，当你选择了 websockets，就是选择了 `asyncio` 作为处理并发的主要框架，这是与 `threading` 互斥的。

如果非要在两个线程中处理，不妨试试 [`run_in_executor()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor) 。

相关建议请查阅 Python 文档：[Concurrency and Multithreading](https://docs.python.org/3/library/asyncio-dev.html#asyncio-multithreading) 



## 六、其他

### 1. 与Django集成

- [Integrate with Django](https://websockets.readthedocs.io/en/stable/howto/django.html)

### 2. 部署

- [Docker & Kubernetes](https://websockets.readthedocs.io/en/stable/howto/kubernetes.html)
- [Supervisor](https://websockets.readthedocs.io/en/stable/howto/supervisor.html)
- [nginx](https://websockets.readthedocs.io/en/stable/howto/nginx.html)

### 3. 打开调试信息

如果你不了解 websockets 的工作原理，请打开日志调试（关于 `logging` 模块的用法不做过多介绍）

```py
import logging

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
```
