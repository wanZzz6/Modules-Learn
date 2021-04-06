异步 IO：就是发起一个 IO 操作（如：网络请求，文件读写等），这些操作一般是比较耗时的，不用等待它结束，可以继续做其他事情，结束时会发来通知。  

----------------------------------------------------------------------------

协程：又称为微线程，在一个线程中执行，执行函数时可以随时中断，由程序（用户）自身控制，执行效率极高，与多线程比较，没有切换线程的开销和多线程锁机制。

异步 IO（asyncio）
--------------

异步 IO 的 asyncio 库使用事件循环驱动的协程实现并发。用户可主动控制程序，在认为耗时 IO 处添加 `await`（`yield from`）。在 asyncio 库中，协程使用 `@asyncio.coroutine` 装饰，使用 `yield from` 来驱动，在 python3.5 中作了如下更改：

*   `@asyncio.coroutine` -> `async`
    
*   `yield from` -> `await`

Python3.8 之后 `@asyncio.coroutine` 装饰器就会被移除，推荐使用 `async` & `await` 关键字实现协程代码。

### 1. asyncio 中几个重要概念

1. 事件循环

管理所有的事件，在整个程序运行过程中不断循环执行并追踪事件发生的顺序将它们放在队列中，空闲时调用相应的事件处理者来处理这些事件。

2.`Future`

Future 对象表示尚未完成的计算，还未完成的结果

3.`Task`

是 Future 的子类，作用是在运行某个任务的同时可以并发的运行多个任务。

asyncio.Task 用于实现协作式多任务的库，且 Task 对象不能用户手动实例化，通过下面 2 个函数创建：

*   `asyncio.async()`
    
*   `loop.create_task()` 或 `asyncio.ensure_future()`

### 2. 最简单的异步 IO 示例

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

## 创建 Task

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

## ❤️获取协程返回值

有 2 种方案可以获取返回值。

### 方法一：result()

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

### 方法二：add_done_callback()

通过 `add_done_callback()` 回调, 回调函数第一个参数必须接收future，如果需要传入其他参数，可以用`偏函数`或者 contex参数传入一个`contextvars.Context`对象

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
test 返回值： zhihu ID: Zarten
```

## ❤️控制多任务

通过 `asyncio.wait()`和 `asyncio.gather()` 可以控制多任务

### 1. asyncio.wait()

**作用**：等待多个任务执行完毕。在低层级精确的控制任务执行，注重执行过程。

**定义**：

```python
async def wait(fs, *, loop=None, timeout=None, return_when=ALL_COMPLETED)
```

**参数说明：**

- fs： **future 或协程构成的可迭代对象**
- loop：事件循环
- timeout: 限制执行时间，默认为`None`，表示不限时间。超时不会抛出异常，未执行完毕的任务存放在第二个返回值集合中。
- return_when：退出条件，可以是以下三个其一: `asyncio.FIRST_COMPLETED` 有一个任务执行完毕后退出；`asyncio.FIRST_EXCEPTION` 有一个任务发生异常后退出；`asyncio.ALL_COMPLETED` 所有任务正常执行完毕退出（默认值）

**返回值**：

coroutine 协程对象

**执行结果**：

​	两个由 Future 构成的集合

```python
done, pending = await asyncio.wait(fs)
```

**用法示例：**

```python
import asyncio
import random


async def coro(tag):
    print(">", tag)
    await asyncio.sleep(random.uniform(0.5, 5))
    print("<", tag)
    return tag


loop = asyncio.get_event_loop()

tasks = [coro(i) for i in range(1, 11)]

print("Get first result:")
finished, unfinished = loop.run_until_complete(
    asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))

for task in finished:
    print('result', task.result())
print("unfinished:", len(unfinished))

print("Get more results in 2 seconds:")
finished2, unfinished2 = loop.run_until_complete(
    asyncio.wait(unfinished, timeout=2))

for task in finished2:
    print('result', task.result())
print("unfinished2:", len(unfinished2))

print("Get all other results:")
finished3, unfinished3 = loop.run_until_complete(asyncio.wait(unfinished2))

for task in finished3:
    print('result', task.result())

loop.close()
```

上面代码展示了wait 不同参数的不同作用，一共创建了10个任务，第一次限定结束条件为 `FIRST_COMPLETED`，所以会有 9个任务未完成。第二次限定执行时间2s，且认为执行过程未发生异常。第三次未限定执行时间，且认为执行过程未发生异常，等待剩余所有任务执行完毕。

输出结果不定，请自行测试。

>**注意**：通过返回值的第一个参数获取执行结果时，其顺序与任务执行完毕的先后有关，与创建顺序无关。如下示例

```python
import asyncio


async def coro(tag):
    print('>', tag)
    await asyncio.sleep(tag)
    print('<', tag)
    return tag


loop = asyncio.get_event_loop()

tasks = [coro(i) for i in range(3, 0, -1)]

done, pending = loop.run_until_complete(
    asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION))

for task in done:
    print('result', task.result())
```

我执行的结果为:

```
> 3
> 1
> 2
< 1
< 2
< 3
result 1
result 2
result 3
```

先执行完毕的先输出。

### 2. asyncio.gather()

**作用**：支持多层级的组任务嵌套，注重任务的执行结果（result）

**定义：**

```python
def gather(*coros_or_futures, loop=None, return_exceptions=False)
```

传入多个协程或者 future对象，**如果是future对象，所有的future必须在同一个 loop 循环中**

**返回值：**

返回一个 `Future` 对象

**执行结果：**

列表，包含所有任务的返回值

**示例代码：**

```python
import asyncio
import random
from pprint import pprint


async def coro(tag):
    print(">", tag)
    await asyncio.sleep(random.uniform(1, 3))
    print("<", tag)
    return tag


loop = asyncio.get_event_loop()

group1 = asyncio.gather(*[coro("group 1.{}".format(i)) for i in range(1, 6)])
group2 = asyncio.gather(*[coro("group 2.{}".format(i)) for i in range(1, 4)])
group3 = asyncio.gather(*[coro("group 3.{}".format(i)) for i in range(1, 10)])
# 任意嵌套组和
group4 = asyncio.gather(group1, group2)
all_groups = asyncio.gather(group3, group4)

results = loop.run_until_complete(all_groups)
loop.close()

pprint(results)  # 或者 pprint(all_groups.result())
```

所有任务组可以通过 `cancel()` 方法取消执行，如果父任务组被 `cancel()`， 那么其所有子任务组都会被取消。如上述代码中，group2 被取消后，不会影响同级的 group1 和父级的 group4 的执行。

#### 使用`return_exceptions` 参数

任一任务被 cancel 后，会在`run_until_complete`阶段抛出 `asyncio.CancelledError` 异常，要想正常执行，就必须将第三个参数`return_exceptions`设为`True`

```python
group4 = asyncio.gather(group1, group2, return_exceptions=True)
all_groups = asyncio.gather(group3, group4)
# 取消group2, 因为 group2 包含在 group4 中，所以group4 要设置return_exceptions=True
group2.cancel()
results = loop.run_until_complete(all_groups)
loop.close()

pprint(results)  # 或者 pprint(all_groups.result())
```

`return_exceptions` 参数的作用是是否捕获**该任务组中**异步任务执行中出现的异常，如果设为True，当发生异常时会捕获异常当做其result，从而不影响该任务组中其他任务的执行。

> **开发建议**：所有调用gather的地方都将 `return_exceptions`设为`True`

```python
import asyncio
import random
from pprint import pprint


async def coro(tag):
    print(">", tag)
    await asyncio.sleep(random.uniform(1, 3))
    if tag[-1] == '3':
        raise ValueError
    print("<", tag)
    return tag


loop = asyncio.get_event_loop()

group1 = asyncio.gather(*[coro("group 1.{}".format(i)) for i in range(1, 6)], return_exceptions=True)
group2 = asyncio.gather(*[coro("group 2.{}".format(i)) for i in range(1, 4)], return_exceptions=True)
group3 = asyncio.gather(*[coro("group 3.{}".format(i)) for i in range(1, 10)], return_exceptions=True)
# 任意嵌套组和
group4 = asyncio.gather(group1, group2, return_exceptions=True)
all_groups = asyncio.gather(group3, group4, return_exceptions=True)

results = loop.run_until_complete(all_groups)
loop.close()

pprint(results)  # 或者 pprint(all_groups.result())
```

### 3. 小结

- gather从字面意思理解，注重对执行结果的收集，按照任务传入的先后顺序收集到一个列表中
- wait等待任务执行，注重过程控制，执行结果需要手动收集
- 参数不同，wait 接收一个序列，gather是通过收集参数接收多个值。
- 通过 wait 返回值的第一个集合获取执行结果result()，其顺序不确定 

### 4. 多任务中获取返回值

#### wait()

> 与上文提到的获取协程返回值方法相同， 使用 result() 或者 add_done_callback()。

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

#### gather()

>除了使用 result() 或者 add_done_callback()以外，`results = loop.run_until_complete(all_groups)` 可直接获取返回值, 或者 `result = await asyncio.gather(…)`

```python
import asyncio

async def coroutine_example(name):
    print('正在执行name:', name)
    await asyncio.sleep(1)
    print('执行完毕name:', name)
    return '返回值：' + name


async def main():
    tasks = []
    for i in range(3):
        task = asyncio.create_task(coroutine_example('Zarten_' + str(i)))
        tasks.append(task)
    result = await asyncio.gather(*tasks, return_exceptions=True)
    for i in result:
        print(i)

asyncio.run(main())
```

动态添加协程
------

方案是**创建一个线程，使事件循环在线程内永久运行**

### 相关函数介绍

- `loop.call_soon_threadsafe()` ：与 `call_soon()` 类似，等待此函数返回后马上调用回调函数，返回值是一个 asyncio.Handle 对象，此对象内只有一个方法为 `cancel()` 方法，用来取消回调函数。

- `loop.call_soon()` ： 与 `call_soon_threadsafe()` 类似，`call_soon_threadsafe()` 是线程安全的

- `loop.call_later()`：_延迟多少秒后执行回调函数_
- `loop.call_at()`：在指定时间执行回调函数，这里的时间统一使用 `loop.time()` 来替代 `time.sleep()`
- `asyncio.run_coroutine_threadsafe()`： 动态的加入协程，参数为一个回调函数和一个 loop 对象，返回值为 future 对象，通过 `future.result()` 获取回调函数返回值

### 动态添加协程: 同步任务loop.call_soon_threadsafe

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

### 动态添加协程：异步任务asyncio.run_coroutine_threadsafe

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

## 限制并发数量方法

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



---

## Tips

- `asyncio.create_task()`与 `loop.create_task()` 功能一样，都是向loop中动态注册任务，区别在于前者是向当前running正在运行状态的loop添加任务。后者在loop未启动时也能添加，并且在启动后自动调度。
- `asyncio.ensure_future()`创建的任务不能主动调度，需要手动 await，且创建loop与运行loop必须一致。
- `asyncio.current_task(loop=None)` 返回这个loop上当前正在运行的Task，loop没有运行或者没有任务则返回None
- `asyncio.all_tasks(loop=None)` 返回这个loop上正在运行(running)和等待运行(pending) 的所有Task集合
- `task.result()`和 `future.result()`在任务未完成时会抛出`asyncio.InvalidStateError`异常
- `asyncio.run_coroutine_threadsafe(coro, loop)` 返回的future，调用 `future.result(timeout=None)`时，其loop必须在running状态下，且没有正在运行的任务才可以，即 `loop.is_running() and asyncio.current_task(loop) is None`。否则会因为无法调度而阻塞直到timeout。
- `loop.call_soon_threadsafe`添加任务，后一个任务等前一个同步任务执行完才会运行。

## 参考

- https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait

- https://zhuanlan.zhihu.com/p/59621713