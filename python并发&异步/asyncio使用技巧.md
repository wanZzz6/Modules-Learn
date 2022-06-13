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

# 终止loop循环示例1 - 信号

```python
from signal import signal, SIGINT
import asyncio

async def server():
    while True:
        print('run')
        await asyncio.sleep(1)


def callback(*args, **kwargs):
    print('收到信号', args, kwargs)
    loop.stop()


loop = asyncio.get_event_loop()
asyncio.ensure_future(server(), loop=loop)
# 注册信号
signal(SIGINT, callback)
try:
    loop.run_forever()
except:
    loop.stop()
    print('未收到信号，异常退出')
```

# 终止loop循环示例 2 - 信号（UNIX only）



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

`loop.call_at()` 和 `loop.call_later` 的时间参数是浮点型的小数，单位：秒，本质上都是调用`call_at()`

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

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20210120230439.png" style="zoom: 67%;" />

# gather() 和 wait() 区别

常见用法的区别见我的另一篇文章，这里主要说明其在执行过程中发生任务取消cancel()时的不同

- 如果`wait()`被取消，只是抛出`CancelledError`异常，其第一个参数中等待执行的任务是不受影响的。

- 如果`gather()`被取消，其提交的所有（未完成）的任务都会被取消。

示例：

```python
import asyncio


async def task(arg):
    await asyncio.sleep(5)
    return arg


async def cancel_waiting_task(work_task, waiting_task):
    await asyncio.sleep(2)
    waiting_task.cancel()
    try:
        await waiting_task
        print("Waiting done")
    except asyncio.CancelledError:
        print("Waiting task cancelled")

    try:
        res = await work_task
        print(f"Work result: {res}")
    except asyncio.CancelledError:
        print("Work task cancelled")


async def main():
    work_task = asyncio.create_task(task("done"))
    waiting = asyncio.create_task(asyncio.wait([work_task]))
    await cancel_waiting_task(work_task, waiting)
    print("-------------------")
    work_task = asyncio.create_task(task("done"))
    waiting = asyncio.gather(work_task)
    await cancel_waiting_task(work_task, waiting)


asyncio.run(main())
```

执行结果:

```
Waiting task cancelled
Work result: done
-------------------
Waiting task cancelled
Work task cancelled
```

在 `waiting_task.cancel()` 取消等待任务时，第一次是取消`wait()`, 发现其提交的 `work_task` 子任务仍然执行完毕，而第二次取消`gather()`，其提交的任务 `work_task` 也被取消了。

# 任一任务完成后取消其他任务



在使用`wait()`和`gather()`过程中，假如我们想在至少一个任务完成后，取消其他未完成的任务，或者取消`wait()`本身的任务后，也想将其提交的子任务取消。举个例子，当连接丢失后，取消所有后续等待任务。或者并行很多个连接任务，当其中一个收到请求后，取消其他连接任务。

让我们模拟出上述需求：

```python
import asyncio
from typing import Optional, Tuple, Set


async def wait_any(
        tasks: Set[asyncio.Future], *, timeout: Optional[int] = None,
) -> Tuple[Set[asyncio.Future], Set[asyncio.Future]]:
    """任一任务完成后，返回并取消其他未完成的任务"""
    tasks_to_cancel: Set[asyncio.Future] = set()
    try:
        done, tasks_to_cancel = await asyncio.wait(
            tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED
        )
        return done, tasks_to_cancel
    except asyncio.CancelledError:
        tasks_to_cancel = tasks
        raise
    finally:
        for task in tasks_to_cancel:
            task.cancel()


async def task():
    await asyncio.sleep(5)


async def cancel_waiting_task(work_task, waiting_task):
    await asyncio.sleep(2)
    waiting_task.cancel()
    try:
        await waiting_task
        print("Waiting done")
    except asyncio.CancelledError:
        print("Waiting task cancelled")

    try:
        res = await work_task
        print(f"Work result: {res}")
    except asyncio.CancelledError:
        print("Work task cancelled")


async def check_tasks(waiting_task, working_task, waiting_conn_lost_task):
    try:
        await waiting_task
        print("waiting is done")
    except asyncio.CancelledError:
        print("waiting is cancelled")

    try:
        await waiting_conn_lost_task
        print("connection is lost")
    except asyncio.CancelledError:
        print("waiting connection lost is cancelled")

    try:
        await working_task
        print("work is done")
    except asyncio.CancelledError:
        print("work is cancelled")


async def work_done_case():
    """Case1: 任务正常执行，没有收到断开连接的信号"""
    working_task = asyncio.create_task(task())
    connection_lost_event = asyncio.Event()
    waiting_conn_lost_task = asyncio.create_task(connection_lost_event.wait())
    waiting_task = asyncio.create_task(wait_any({working_task, waiting_conn_lost_task}))
    await check_tasks(waiting_task, working_task, waiting_conn_lost_task)


async def conn_lost_case():
    """Case2: 任务在执行过程中，收到断开连接的信号后被取消"""
    working_task = asyncio.create_task(task())
    connection_lost_event = asyncio.Event()
    waiting_conn_lost_task = asyncio.create_task(connection_lost_event.wait())
    waiting_task = asyncio.create_task(wait_any({working_task, waiting_conn_lost_task}))
    await asyncio.sleep(2)
    connection_lost_event.set()  # <---
    await check_tasks(waiting_task, working_task, waiting_conn_lost_task)


async def cancel_waiting_case():
    """Case3: wait() 本身被取消，所有任务都被取消"""
    working_task = asyncio.create_task(task())
    connection_lost_event = asyncio.Event()
    waiting_conn_lost_task = asyncio.create_task(connection_lost_event.wait())
    waiting_task = asyncio.create_task(wait_any({working_task, waiting_conn_lost_task}))
    await asyncio.sleep(2)
    waiting_task.cancel()  # <---
    await check_tasks(waiting_task, working_task, waiting_conn_lost_task)


async def main():
    print("Case1: Work done")
    print("-------------------")
    await work_done_case()
    print("\nCase2: Connection lost")
    print("-------------------")
    await conn_lost_case()
    print("\nCase3: Cancel waiting")
    print("-------------------")
    await cancel_waiting_case()


asyncio.run(main())
```

执行结果：

```
Case1: Work done
-------------------
waiting is done
waiting connection lost is cancelled
work is done

Case2: Connection lost
-------------------
waiting is done
connection is lost
work is cancelled

Case3: Cancel waiting
-------------------
waiting is cancelled
waiting connection lost is cancelled
work is cancelled
```

# 坑

- 不要在async 声明的方法（协程）里调用 create_task()、run_coroutine_threadsafe() 等方法，否则会卡住不调度