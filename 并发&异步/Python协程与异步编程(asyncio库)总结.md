> 原文地址 https://zhuanlan.zhihu.com/p/59621713

异步 IO：就是发起一个 IO 操作（如：网络请求，文件读写等），这些操作一般是比较耗时的，不用等待它结束，可以继续做其他事情，结束时会发来通知。  

----------------------------------------------------------------------------

协程：又称为微线程，在一个线程中执行，执行函数时可以随时中断，由程序（用户）自身控制，执行效率极高，与多线程比较，没有切换线程的开销和多线程锁机制。

Python 中异步 IO 操作是通过 asyncio 来实现的。



异步 IO（asyncio）
--------------

异步 IO 的 asyncio 库使用事件循环驱动的协程实现并发。用户可主动控制程序，在认为耗时 IO 处添加 `await`（`yield from`）。在 asyncio 库中，协程使用 `@asyncio.coroutine` 装饰，使用 `yield from` 来驱动，在 python3.5 中作了如下更改：

*   `@asyncio.coroutine` -> `async`
    
*   `yield from` -> `await`

Python3.8 之后 `@asyncio.coroutine` 装饰器就会被移除，推荐使用 `async` & `await` 关键字实现协程代码。

### asyncio 中几个重要概念

1. 事件循环

管理所有的事件，在整个程序运行过程中不断循环执行并追踪事件发生的顺序将它们放在队列中，空闲时调用相应的事件处理者来处理这些事件。

2.`Future`

Future 对象表示尚未完成的计算，还未完成的结果

3.`Task`

是 Future 的子类，作用是在运行某个任务的同时可以并发的运行多个任务。

asyncio.Task 用于实现协作式多任务的库，且 Task 对象不能用户手动实例化，通过下面 2 个函数创建：

*   `asyncio.async()`
    
*   `loop.create_task()` 或 `asyncio.ensure_future()`

### 最简单的异步 IO 示例

- `run_until_complete()`

阻塞调用，直到协程运行结束才返回。参数是 future，传入协程对象时内部会自动变为 future

- `asyncio.sleep()`

模拟 IO 操作，这样的休眠不会阻塞事件循环，前面加上 await 后会把控制权交给主事件循环，在休眠（IO 操作）结束后恢复这个协程。

_提示：_

_若在协程中需要有延时操作，应该使用 `await asyncio.sleep()`，而不是使用 time.sleep()，因为使用 time.sleep() 后会释放 GIL，阻塞整个主线程，从而阻塞整个事件循环。_

```python
import asyncio

async def coroutine_example():
    await asyncio.sleep(1)
    print('zhihu ID: Zarten')

coro = coroutine_example()

loop = asyncio.get_event_loop()
loop.run_until_complete(coro)
loop.close()

```

上面输出：会暂停 1 秒，等待 `asyncio.sleep(1)` 返回后打印

### 创建 Task

_`loop.create_task()`_:

接收一个协程，返回一个 `asyncio.Task` 的实例，也是 `asyncio.Future` 的实例，毕竟 Task 是 Future 的子类。返回值可直接传入 _`run_until_complete()`_

返回的 Task 对象可以看到协程的运行情况

```python
import asyncio

async def coroutine_example():
    await asyncio.sleep(1)
    print('zhihu ID: Zarten')

coro = coroutine_example()

loop = asyncio.get_event_loop()
task = loop.create_task(coro)
print('运行情况：', task)

loop.run_until_complete(task)
print('再看下运行情况：', task)
loop.close()

```

输出结果：

从下图可看到，当 task 为 finished 状态时，有个 `result()` 的方法，我们可以通过这个方法来获取协程的返回值

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640.png)

### 获取协程返回值

有 2 种方案可以获取返回值。

*   第 1 种方案：通过 `task.result()`
    

可通过调用 `task.result()` 方法来获取协程的返回值，**但是只有运行完毕后才能获取，若没有运行完毕，result() 方法不会阻塞去等待结果，而是抛出 `asyncio.InvalidStateError `错误**

```python
import asyncio

async def coroutine_example():
    await asyncio.sleep(1)
    return 'zhihu ID: Zarten'

coro = coroutine_example()

loop = asyncio.get_event_loop()
task = loop.create_task(coro)
print('运行情况：', task)
try:
    print('返回值：', task.result())
except asyncio.InvalidStateError:
    print('task状态未完成，捕获了 InvalidStateError 异常')

loop.run_until_complete(task)
print('再看下运行情况：', task)
print('返回值：', task.result())
loop.close()

```

运行结果可以看到：只有 task 状态运行完成时才能捕获返回值

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201211235344189.png)

*   ❤️ 第 2 种方案：通过 `add_done_callback()` 回调, 回调函数第一个参数必须接收future，如果需要传入其他参数，可以用`偏函数`或者 contex参数传入一个`contextvars.Context`对象
    

```python
import asyncio
import functools

def my_callback(name, future):
    print(name, '返回值：', future.result())

async def coroutine_example():
    await asyncio.sleep(1)
    return 'zhihu ID: Zarten'

coro = coroutine_example()

loop = asyncio.get_event_loop()

task = loop.create_task(coro)
task.add_done_callback(functools.partial(my_callback, 'test'))

loop.run_until_complete(task)
loop.close()
```

输出如下：

```
返回值： zhihu ID: Zarten
```



### 控制多任务

通过 `asyncio.wait()` 可以控制多任务

`asyncio.wait()` **是一个协程，不会阻塞，立即返回，返回的是协程对象。**传入的参数是 future 或协程构成的可迭代对象。最后将返回值传给 `run_until_complete()` 加入事件循环

最简单控制多任务

下面代码 `asyncio.wait()` 中，参数传入的是由协程构成的可迭代对象

```python
import asyncio

async def coroutine_example(name):
    print('正在执行name:', name)
    await asyncio.sleep(1)
    print('执行完毕name:', name)

loop = asyncio.get_event_loop()

tasks = [coroutine_example('Zarten_' + str(i)) for i in range(3)]
wait_coro = asyncio.wait(tasks)
loop.run_until_complete(wait_coro)
loop.close()

```

输出结果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201211235334666.jpeg)

多任务中获取返回值

*   方案 1：需要通过 `loop.create_task()` 创建 task 对象，以便后面来获取返回值
    

下面代码 `asyncio.wait()` 中，参数传入的是由 future（task）对象构成的可迭代对象

```python
import asyncio

async def coroutine_example(name):
    print('正在执行name:', name)
    await asyncio.sleep(1)
    print('执行完毕name:', name)
    return '返回值：' + name

loop = asyncio.get_event_loop()

tasks = [loop.create_task(coroutine_example('Zarten_' + str(i))) for i in range(3)]
wait_coro = asyncio.wait(tasks)
loop.run_until_complete(wait_coro)

for task in tasks:
    print(task.result())

loop.close()

```

*   方案 2：通过回调 `add_done_callback()` 来获取返回值
    

```python
import asyncio

def my_callback(future):
    print('返回值：', future.result())

async def coroutine_example(name):
    print('正在执行name:', name)
    await asyncio.sleep(1)
    print('执行完毕name:', name)
    return '返回值：' + name

loop = asyncio.get_event_loop()

tasks = []
for i in range(3):
    task = loop.create_task(coroutine_example('Zarten_' + str(i)))
    task.add_done_callback(my_callback)
    tasks.append(task)

wait_coro = asyncio.wait(tasks)
loop.run_until_complete(wait_coro)

loop.close()

```

输出结果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201211235326981.jpeg)

动态添加协程
------

方案是**创建一个线程，使事件循环在线程内永久运行**

### 相关函数介绍

- `loop.call_soon_threadsafe()` ：与 `call_soon()` 类似，等待此函数返回后马上调用回调函数，返回值是一个 asyncio.Handle 对象，此对象内只有一个方法为 `cancel()` 方法，用来取消回调函数。

- `loop.call_soon()` ： 与 `call_soon_threadsafe()` 类似，`call_soon_threadsafe()` 是线程安全的

- `loop.call_later()`：_延迟多少秒后执行回调函数_
- `loop.call_at()`：在指定时间执行回调函数，这里的时间统一使用 `loop.time()` 来替代 `time.sleep()`
- `asyncio.run_coroutine_threadsafe()`： 动态的加入协程，参数为一个回调函数和一个 loop 对象，返回值为 future 对象，通过 `future.result()` 获取回调函数返回值

### 动态添加协程: 同步任务

通过调用 `loop.call_soon_threadsafe()` 函数，传入一个回调函数 callback 和一个位置参数

注意：同步方式，**回调函数 thread_example() 为普通函数**

```python
import asyncio
from threading import Thread

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def thread_example(name):
    print('正在执行name:', name)
    return '返回结果：' + name

new_loop = asyncio.new_event_loop()
t = Thread(target=start_thread_loop, args=(new_loop,))
t.start()

handle = new_loop.call_soon_threadsafe(thread_example, 'Zarten1')
handle.cancel()

new_loop.call_soon_threadsafe(thread_example, 'Zarten2')

print('主线程不会阻塞')

new_loop.call_soon_threadsafe(thread_example, 'Zarten3')

print('继续运行中...')
```

输出结果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201211235317468.jpeg)

### 动态添加协程：异步任务

通过调用 `asyncio.run_coroutine_threadsafe()` 函数，传入一个回调函数 callback 和一个 loop 对象

注意：异步方式，**回调函数 thread_example() 为协程**

```python
import asyncio
from threading import Thread

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def thread_example(name):
    print('正在执行name:', name)
    await asyncio.sleep(1)
    return '返回结果：' + name

def callback(future):
    print('back', future.result())
    
new_loop = asyncio.new_event_loop()
t = Thread(target=start_thread_loop, args=(new_loop,))
t.start()

future = asyncio.run_coroutine_threadsafe(thread_example('Zarten1'), new_loop)
print(future.result(timeout=None))  # 阻塞、等待timeout

future.add_done_callback(callback) # 即使异步任务已经完成，也可以添加回调

asyncio.run_coroutine_threadsafe(thread_example('Zarten2'), new_loop)

print('主线程不会阻塞')

asyncio.run_coroutine_threadsafe(thread_example('Zarten3'), new_loop)

print('继续运行中...')
```

输出结果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201213171344.png)

从上面 2 个例子中，当主线程运行完成后，由于子线程还没有退出，故主线程还没退出，等待子线程退出中。若要主线程退出时子线程也退出，可以设置子线程为守护线程 t.setDaemon(True)

协程中生产 - 消费模型设计
--------------

通过上面的动态添加协程的思想，我们可以设计一个生产 - 消费的模型，至于中间件（管道）是什么无所谓，下面以内置队列和 redis 队列来举例说明。

提示：若想主线程退出时，子线程也随之退出，需要将子线程设置为守护线程，函数 setDaemon(True)

### 内置双向队列模型

使用内置双向队列 deque

```python
import asyncio
from threading import Thread
from collections import deque
import random
import time

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def consumer():
    while True:
        if dq:
            msg = dq.pop()
            if msg:
                asyncio.run_coroutine_threadsafe(thread_example('Zarten'+ msg), new_loop)


async def thread_example(name):
    print('正在执行name:', name)
    await asyncio.sleep(2)
    return '返回结果：' + name



dq = deque()

new_loop = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop,))
loop_thread.setDaemon(True)
loop_thread.start()

consumer_thread = Thread(target=consumer)
consumer_thread.setDaemon(True)
consumer_thread.start()

while True:
    i = random.randint(1, 10)
    dq.appendleft(str(i))
    time.sleep(2)
```

输出结果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201212082007204.jpeg)

### redis 队列模型

下面代码的主线程和双向队列的主线程有些不同，只是换了一种写法而已，代码如下

生产者代码：

```python
import redis

conn_pool = redis.ConnectionPool(host='127.0.0.1')
redis_conn = redis.Redis(connection_pool=conn_pool)

redis_conn.lpush('coro_test', '1')
redis_conn.lpush('coro_test', '2')
redis_conn.lpush('coro_test', '3')
redis_conn.lpush('coro_test', '4')
```

消费者代码：

```python
import asyncio
from threading import Thread
import redis

def get_redis():
    conn_pool = redis.ConnectionPool(host='127.0.0.1')
    return redis.Redis(connection_pool=conn_pool)

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def thread_example(name):
    print('正在执行name:', name)
    await asyncio.sleep(2)
    return '返回结果：' + name


redis_conn = get_redis()

new_loop = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop,))
loop_thread.setDaemon(True)
loop_thread.start()

#循环接收redis消息并动态加入协程
while True:
    msg = redis_conn.rpop('coro_test')
    if msg:
        asyncio.run_coroutine_threadsafe(thread_example('Zarten' + bytes.decode(msg, 'utf-8')), new_loop)
```

输出结果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201212082049930.jpeg)

asyncio 在 aiohttp 中的应用
----------------------

aiohttp 是一个异步库，分为客户端和服务端，下面只是简单对客户端做个介绍以及一个经常遇到的异常情况。aiohttp 客户端为异步网络请求库

### aiohttp 客户端最简单的例子

```python
import asyncio
import aiohttp

count = 0

async def get_http(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            global count
            count += 1
            print(count, res.status)

def main():
    loop = asyncio.get_event_loop()
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baiduerr&bar=&wd={0}'
    tasks = [get_http(url.format(i)) for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
if __name__ == '__main__':
    main()
```

### aiohttp 并发量太大的异常解决方案

在使用 aiohttp 客户端进行大量并发请求时，程序会抛出 ValueError: too many file descriptors in select() 的错误。

异常代码示例

说明：测试机器为 windows 系统

```python
import asyncio
import aiohttp

count = 0

async def get_http(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            global count
            count += 1
            print(count, res.status)

def main():
    loop = asyncio.get_event_loop()
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baiduerr&bar=&wd={0}'
    tasks = [get_http(url.format(i)) for i in range(600)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
if __name__ == '__main__':
    main()
```

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201212082120618.png)

原因分析：使用 aiohttp 时，python 内部会使用 select()，操作系统对文件描述符最大数量有限制，linux 为 1024 个，windows 为 509 个。

解决方案：

最常见的解决方案是：限制并发数量（一般 500），若并发的量不大可不作限制。其他方案这里不做介绍，如 windows 下使用 loop = asyncio.ProactorEventLoop() 以及使用回调方式等

### 限制并发数量方法

提示：此方法也可用来作为异步爬虫的限速方法（反反爬）

使用 semaphore = asyncio.Semaphore(500) 以及在协程中使用 async with semaphore: 操作

具体代码如下：

```python
import asyncio
import aiohttp


async def get_http(url):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                global count
                count += 1
                print(count, res.status)

if __name__ == '__main__':
    count = 0

    semaphore = asyncio.Semaphore(500)
    loop = asyncio.get_event_loop()
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baiduerr&bar=&wd={0}'
    tasks = [get_http(url.format(i)) for i in range(600)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
```

原文地址，原作 Zarten。  

https://zhuanlan.zhihu.com/p/59621713
