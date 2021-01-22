# 设置事件循环策略

```python
import asyncio
import os

if os.name == 'nt':  # sys.platform == 'win32':
    pass
elif os.name == 'posix':
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```



或者手动指定 loop 类型使用

```python
asyncio.set_event_loop(uvloop.new_event_loop())
```

# 终止loop循环示例1 - 信号

```python
from signal import signal, SIGINT

import uvloop

asyncio.set_event_loop(uvloop.new_event_loop())
# 启动一个http服务
server = app.create_server(host="0.0.0.0", port=7777)
loop = asyncio.get_event_loop()
asyncio.ensure_future(server)
# 注册信号
signal(SIGINT, lambda s, f: loop.stop())
try:
    loop.run_forever()
except:
    loop.stop()
```

# 终止loop循环示例 2 - 信号

```python
import asyncio
import signal
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def echo_server(stop):
    async with websockets.serve(echo, "localhost", 8765):
        # 等待退出条件，可以自定义
        await stop

loop = asyncio.get_event_loop()

# The stop condition is set when receiving SIGTERM.
stop = loop.create_future()
# 设置收到SIGTERM信号的回调函数，此处是设置 stop 协程执行结果为None，使其终止调度
loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

# Run the server until the stop condition is met.
loop.run_until_complete(echo_server(stop))
```

# 添加定时任务

`loop.call_later()` 和 `loop.call_later` 的时间参数是浮点型的小数，单位：秒，本质上都是调用`call_at()`

```python
import asyncio
import time

async def task():
    print(3, time.time())
    await asyncio.sleep(0)
    print('task')
    print(4, time.time())

async def main():
    print(1, time.time())
    loop.call_later(5, asyncio.run_coroutine_threadsafe, task(), loop)
    print(2, time.time())

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
```

# 不要简单的用done()判断是否执行完毕

在动态添加 `Future` 异步任务时，执行完毕的情况分正常退出和异常退出两种，使用 `future.done()`判断都会返回`True`,   如果仅仅是这样判断的就完事了，那可能会出现无法察觉的错误，因为动态添加的异步任务在执行中出现错误时**不会主动抛出异常**的，先测试如下代码：

```python
import asyncio


def my_callback(future):
    print('callback')
    print(future.done())
    print(future.exception())


async def coroutine_example():
    await asyncio.sleep(1)
    raise TypeError('F**k')
    return 'OK'


coro = coroutine_example()

loop = asyncio.get_event_loop()

task = loop.create_task(coro)
task.add_done_callback(my_callback)

loop.run_forever()
```

程序输出以下信息：

```sh
callback
True
F**k
```

我们在 `coroutine_example()`里抛出了`TypeError`异常，但是我们单从程序输出里是看不到任何异常堆栈信息的，通过`future.exception()` 方法可以简单的判断是否运行出错，如果返回值`is not None`就证明程序出错了，但是也不要使用  `if future.exception(): ` 判断是否运行出错，因为该方法只是返回错误信息的字符串，就像上面的 `'F**k'`， 但是若抛出异常是没有附加信息呢？ `raise TypeError()` 或者 `raise TypeError`

 要想捕获错误堆栈信息，正确的做法是在 future的回调函数里使用`future.result()` 或者，直接一段时间后**假定任务已经执行完**， 调用`future.result(self, timeout=None)`，（注：参数 timeout 表示等待时间，None表示无限等待，即阻塞式），该方法时获取异步任务的返回值，如果发生异常会直接打印异常的堆栈信息。



```python
import asyncio


def my_callback(future):
    print('callback')
    print(future.done())
    print(future.exception())
    print('返回值：', future.result())  # 增加此行


async def coroutine_example():
    await asyncio.sleep(1)
    raise TypeError
    return 'OK'


coro = coroutine_example()

loop = asyncio.get_event_loop()

task = loop.create_task(coro)
task.add_done_callback(my_callback)

loop.run_forever()
```

然后你就能正常看到错误信息了

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20210120230439.png)