# Client 常用方法

- 创建客户端实例
- 连接到服务器： connect\*() 方法
- 与服务器保持网络连接：loop\*() 方法
- 使用 subscribe() 方法订阅与接受消息
- 使用 publish() 方法向服务器发送消息
- 使用 disconnect() 与服务器断开连接

# Client

## 构造器

```python
Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")

```

### 参数

- client_id

连接到代理时使用的唯一客户端 ID 字符串。如果 client_id 是空字符串或者为 None，则将随机生成一个。在这种情况下，clean_session 参数必须是 True。

- clean_session

一个确定客户端类型的布尔值。如果 True，在该客户端断开连接时服务器将删除有关此客户端的所有信息。如果 False，客户端是持久客户端，即使客户端断开连接，服务器也保留其订阅信息和排队消息。

请注意，客户端永远不会在断开连接时丢弃自己的传出消息。调用 connect（）或 reconnect（）将导致重新发送消息。使用 reinitialise（）将客户端重置为其原始状态。

- userdata

用户定义的任何类型的数据，作为 userdata 参数传递给回调。它可以在稍后用该 user_data_set()功能更新 。

- protocol

用于此客户端的 MQTT 协议版本。可以是 MQTTv31 或 MQTTv311

- transport
  设置为“websockets”以通过 WebSockets 发送 MQTT。用默认值“tcp”以使用原始 TCP。

示例：

```python
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
```

## 常用方法

### reinitialise()

```python
reinitialise(client_id="", clean_session=True, userdata=None)
```

该 reinitialise()函数将客户端重置为其初始状态，就像刚刚创建它一样。**它采用与 Client()构造函数相同的参数。**

## Option functions 可选方法

这些函数可以**修改**客户端的执行行为。在大多数情况下，**此操作必须在连接到服务器之前完成。**

### max_inflight_messages_set()

```python
max_inflight_messages_set(self，inflight)
```

设置 QoS> 0 一次性通过其网络流量的最大消息数。默认为 20.增加此值将消耗更多内存，但可以增加吞吐量。

### max_queued_messages_set()

```python
max_queued_messages_set(self，queue_size)
```

设置 QoS> 0 的在传出消息队列中挂起的最大数量。默认为 0. 表示无限制。当队列已满时，将丢弃任何后续传出的消息。

### message_retry_set()

```python
message_retry_set(retry)
```

如果代理没有响应，则设置 QoS> 0 消息的重试间隔（以秒为单位）。默认设置为 5 秒，通常不需要更改。

### ws_set_options()

```python
ws_set_options(self, path='/mqtt'，headers=None)
```

设置 websocket 连接选项。只有在 transport="websockets"传递给 Client()构造函数时才会使用这些选项。

- path

  > 要在服务器上使用的 mqtt 路径。

- headers
  > 指定应附加到标准 websocket 标头的额外标头列表的字典。
  > 或者是可调用的函数，传入正常 websocket 标头并返回一个字典，包含连接到服务器的的一系列 header。

**必须先调用 connect\*()。在** examples 文件夹下有配合 AWS IoT 平台使用的 Demo。

### tls_set()

```python
tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
```

配置网络加密和身份验证选项。启用 S​​SL / TLS 支持。

- ca_certs（单独需要）

  证书颁发机构证书文件的**字符串路径**，该文件将被此客户端视为受信任。

  如果这是给出的唯一选项，则客户端将以与 Web 浏览器类似的方式运行。也就是说，它将要求服务器拥有证书颁发机构签署的证书 ca_certs，并将使用 TLS v1 进行通信，但不会尝试任何形式的身份验证。

  这提供了基本的网络加密，但可能不够，具体取决于服务器的配置方式。默认情况下，在 Python 2.7.9+或 3.4+上，使用系统的默认证书颁发机构。在较旧的 Python 版本中，此参数是必需的。

- certfile，keyfile （同时需要）

  字符串分别指向 PEM 编码的客户端证书和私钥。
  如果这些参数不是 None 则它们将用作基于 TLS 的身份验证的客户端信息。对此功能的支持取决于服务器。
  请注意，如果这些文件中的任何一个加密并需要密码才能解密，Python 将在命令行中询问密码。目前无法定义回调函数来提供密码。

- cert_reqs

  定义客户端对代理施加的证书要求。默认情况下 ssl.CERT_REQUIRED，这意味着代理必须提供证书。有关此参数的更多信息，请参见 ssl pydoc。

- tls_version

  指定要使用的 SSL / TLS 协议的版本。默认情况下（如果 python 版本支持它），检测到最高的 TLS 版本。如果不可用，则使用 TLS v1。以前的版本（所有以 SSL 开头的版本）都是可能的，但由于可能存在安全问题，因此不推荐使

- ciphers
  一个字符串，指定允许此连接使用哪些加密密码，如果 None 则使用默认值。有关更多信息，请参阅 ssl pydoc。

必须先调用 connect\*()。

### tls_set_context()

```python
tls_set_context(context=None)
```

配置网络加密和认证上下文。启用 S​​SL / TLS 支持。

- context

  一个 ssl.SSLContext 对象。默认情况下，ssl.create_default_context()如果可用，则由（在 Python 3.4 中添加）给出。
  如果您不确定使用此方法，请使用默认上下文，或使用该 tls_set 方法。有关更多信息，请参阅 ssl 模块文档部分中有关安全性注意事项

必须先调用 connect\*()。

### tls_insecure_set()

```python
tls_insecure_set(value)
```

配置服务器证书中服务器**主机名**的验证。

如果 value 设置为 True，则无法保证您连接的主机不会模拟（冒充）您的服务器。这在初始测试服务器中非常有用，但可以使恶意第三方通过 DNS 欺骗来模拟您的服务器。

请勿在实际系统中使用此功能。将值设置为 True 意味着使用加密没有意义。

必须调用 connect\*()后 tls_set()或 tls_set_context()。

### enable_logger()

- enable_logger（logger = None）

  使用标准 python 日志包启用日志记录（请参阅 PEP 282）。这可以与 on_log 回调方法同时使用。

如果 logger 已指定，则将使用该 logging.Logger 对象，否则将自动创建一个对象。

根据以下映射将 Paho 日志记录级别转换为标准级别：

| Paho             | logging                             |
| ---------------- | ----------------------------------- |
| MQTT_LOG_ERR     | logging.ERROR                       |
| MQTT_LOG_WARNING | logging.WARNING                     |
| MQTT_LOG_NOTICE  | logging.INFO (no direct equivalent) |
| MQTT_LOG_INFO    | logging.INFO                        |
| MQTT_LOG_DEBUG   | logging.DEBUG                       |

### disable_logger()

```python
disable_logger()
```

禁用 logging 使用 python 标准模块，这对 on_log 回调没有影响。

### username_pw_set()

```python
username_pw_set()
```

为服务器身份验证设置用户名和密码。必须先调用 connect\*()。

### user_data_set()

```python
user_data_set(userdata)
```

设置事件发生时将传递给回调的私有用户数据，根据自己的需要提供程序支持。

### will_set()

```python
will_set(topic, payload=None, qos=0, retain=False)
```

设置要发送给服务器的遗愿。如果客户端在未调用 disconnect()的情况下断开连接 ，则服务器将代表其发布消息。

- topic
  应该发布遗嘱消息的主题。

- payload
  要作为遗嘱发送的消息。如果没有给出，或设置 None 为零长度消息将被用作遗嘱。传递 int 或 float 将导致有效负载转换为表示该数字的字符串。如果您希望发送一个真正的 int / float，请使用 struct.pack()创建所需的有效负载。

- qos
  用于遗愿的服务质量水平。

- retain
  如果设置为 True，则将消息设置为主题的“最后已知好”/保留消息。

引发 ValueError 如果 qos 不是 0,1 或 2，或者 topic 为 None 或空字符串。

### reconnect_delay_set

```python
reconnect_delay_set（min_delay = 1，max_delay = 120）
```

客户端将自动重试连接。在每次尝试之间，它将在 min_delay 和 max_delay 之间等待几秒钟。

当连接丢失时，最初重新连接尝试会延迟 min_delay 几秒钟。在随后的尝试中，每次延迟时间为上一次的两倍，直到最大 max_delay。

连接完成时将 延迟重置为 min_delay. （例如，收到 CONNACK 信号，而不仅仅建立 TCP 连接）。

## Connect / reconnect / disconnect

### connect()

```python
connect(host, port=1883, keepalive=60, bind_address="")
```

客户端连接到服务器，这是个阻塞的方法。参数如下：

- host

  远程服务器的主机名或 IP 地址

- port

  要连接的服务器主机的网络端口。默认为 1883.请注意，MQTT over SSL / TLS 的默认端口为 8883，因此如果您使用 tls_set()或 tls_set_context()，端口可能需要手动提供

- keepalive
  与服务器通信之间允许的最长时间（以秒为单位）。如果没有交换其他消息，则控制客户端发送 ping 的速率

- bind_address
  假设存在多个接口，则绑定此客户端的本地网络接口的 IP 地址

**回调函数**
当客户端从代理接收到 CONNACK 消息以响应连接时，它会生成 on_connect()回调。

连接示例

```python
mqttc.connect("iot.eclipse.org")
```
