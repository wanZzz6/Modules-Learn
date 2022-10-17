> 原文地址 [zhuanlan.zhihu.com](https://zhuanlan.zhihu.com/p/92152648)

背景
--

最近有个需求，需要实现一个定时或定期任务的功能，需要实现每月、每日、每时、一次性等需求，必须是轻量级不依赖其它额外组件，并能支持动态添加任务。由于当前任务信息保存在集群 ETCD 数据库中，因此对任务持久化要求不高，每次重启都直接读取 ETCD 任务信息，为了后面扩展，还需要添加任务持久化功能。

定时任务库对比
-------

根据上面需求，从社区中找到了几个 Python 好用的任务调度库。有以下几个库：

*   schedule：Python job scheduling for humans. 轻量级，无需配置的作业调度库
*   python-crontab： 针对系统 Cron 操作 crontab 文件的作业调度库
*   Apscheduler：一个高级的 Python 任务调度库
*   Celery： 是一个简单，灵活，可靠的分布式系统，用于处理大量消息，同时为操作提供维护此类系统所需的工具, 也可用于任务调度

优缺点对比：

*   schedule 优点是简单、轻量级、无需配置、语法简单，缺点是阻塞式调用、无法动态添加或删除任务
*   Python-crontab 优点是针对于系统 crontab 操作，支持定时、定期任务，能够动态添加任务，不能实现一次性任务需求
*   Apscheduler 优点支持定时、定期、一次性任务，支持任务持久化及动态添加、支持配置各种持久化存储源 (如 redis、MongoDB)，支持接入到各种异步框架 (如 gevent、asyncio、tornado)
*   Celery 支持配置定期任务、支持 crontab 模式配置，不支持一次性定时任务

schedule 库
----------

人类的 Python 任务调度库，和 requests 库一样 for humans. 这个库也是最轻量级的一个任务调度库，schedule 允许用户使用简单、人性化的语法以预定的时间间隔定期运行 Python 函数 (或其它可调用函数)。

直接使用 `pip install schedule`进行安装使用，下面来看看官网给的示例：

```python
import schedule
import time

# 定义你要周期运行的函数
def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)               # 每隔 10 分钟运行一次 job 函数
schedule.every().hour.do(job)                    # 每隔 1 小时运行一次 job 函数
schedule.every().day.at("10:30").do(job)         # 每天在 10:30 时间点运行 job 函数
schedule.every().monday.do(job)                  # 每周一 运行一次 job 函数
schedule.every().wednesday.at("13:15").do(job)   # 每周三 13：15 时间点运行 job 函数
schedule.every().minute.at(":17").do(job)        # 每分钟的 17 秒时间点运行 job 函数

while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)
```

通过上面示例，可以很容易学会使用 schedule 库，可以设置秒、分钟、小时、天、周来运行任务，然后通过一个死循环，一直不断地运行所有的计划任务。

### schedule 常见问题

**1、如何并行执行任务？**

schedule 是阻塞式的，默认情况下， schedule 按顺序执行所有的作业，不能达到并行执行任务。如下所示：

```python
import arrow
import schedule

def job1():
    print("job1 start time: %s" % arrow.get().format())
    time.sleep(2)
    print("job1 end time: %s" % arrow.get().format())

def job2():
    print("job2 start time: %s" % arrow.get().format())
    time.sleep(5)
    print("job2 end time: %s" % arrow.get().format())

def job3():
    print("job3 start time: %s" % arrow.get().format())
    time.sleep(10)
    print("job3 end time: %s" % arrow.get().format())

if __name__ == '__main__':
    schedule.every(10).seconds.do(job1)
    schedule.every(30).seconds.do(job2)
    schedule.every(5).to(10).seconds.do(job3)

    while True:
        schedule.run_pending()
```

返回部分结果如下所示，几个任务并不是并行开始的，是安装时间顺序先后开始的：

```
job3 start time: 2019-06-01 09:27:54+00:00
job3 end time: 2019-06-01 09:28:04+00:00
job1 start time: 2019-06-01 09:28:04+00:00
job1 end time: 2019-06-01 09:28:06+00:00
job3 start time: 2019-06-01 09:28:13+00:00
job3 end time: 2019-06-01 09:28:23+00:00
job2 start time: 2019-06-01 09:28:23+00:00
job2 end time: 2019-06-01 09:28:28+00:00
job1 start time: 2019-06-01 09:28:28+00:00
job1 end time: 2019-06-01 09:28:30+00:00
job3 start time: 2019-06-01 09:28:30+00:00
job3 end time: 2019-06-01 09:28:40+00:00
job1 start time: 2019-06-01 09:28:40+00:00
job1 end time: 2019-06-01 09:28:42+00:00
```

如果需要实现并行，那么使用多线程方式运行任务，官方给出的并行方案如下：

```python
import threading
import time
import schedule

def job():
    print("I'm running on thread %s" % threading.current_thread())

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)
schedule.every(10).seconds.do(run_threaded, job)

while 1:
    schedule.run_pending()
    time.sleep(1)


# 我在项目里也是通过对每个任务运行后台线程方式, 可以通过 run_daemon_thread 起一个守护线程方式来达到动态
添加任务的功能，每个任务最终通过新开线程方式执行
import threading


def ensure_schedule():
    schedule.every(5).seconds.do(do_some)

def ensure_schedule_2():
    schedule.every(10).seconds.do(print_some)

def run_daemon_thread(target, *args, **kwargs):
    job_thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    job_thread.setDaemon(True)
    job_thread.start()

def __start_schedule_deamon():
    def schedule_run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=schedule_run)
    t.setDaemon(True)
    t.start()

def init_schedule_job():
        run_daemon_thread(ensure_schedule)
        run_daemon_thread(ensure_schedule_2)

init_schedule_job()
__start_schedule_deamon()
```

**2、如何在不阻塞主线程的情况下连续运行调度程序？**

官方推荐了这个方式，在单独的线程中运行调度程序，如下，在单独的线程中运行 run_pending 调度程序。通过 threading 库的 Event 来实现

```python
# https://github.com/mrhwick/schedule/blob/master/schedule/__init__.py
 def run_continuously(self, interval=1):
        """Continuously run, while executing pending jobs at each elapsed
        time interval.
        @return cease_continuous_run: threading.Event which can be set to
        cease continuous run.
        Please note that it is *intended behavior that run_continuously()
        does not run missed jobs*. For example, if you've registered a job
        that should run every minute and you set a continuous run interval
        of one hour then your job won't be run 60 times at each interval but
        only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run
```

**3、是否支持时区**

```
# 官方不计划支持时区，可使用： 
讨论：https://github.com/dbader/schedule/pull/16
时区解决：https://github.com/imiric/schedule/tree/feat/timezone
```

**4、如果我的任务抛出异常怎么办?**

schedule 不捕获作业执行期间发生的异常，因此在任务执行期间的任何异常都会冒泡并中断调度的 run_xyz(如 run_pending) 函数, 也就是 run_pending 中断退出，导致其它任务无法执行

```python
import functools

def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

@catch_exceptions(cancel_on_failure=True)
def bad_task():
    return 1 / 0

schedule.every(5).minutes.do(bad_task)

另外一种解决方案：
https://gist.github.com/mplewis/8483f1c24f2d6259aef6
```

**5、如何设置只跑一次的任务?**

```python
def job_that_executes_once():
    # Do some work ...
    return schedule.CancelJob

schedule.every().day.at('22:30').do(job_that_executes_once)
```

**6、如何一次取消多个任务？**

```python
# 通过 tag 函数给它们添加唯一标识符进行分组，取消时通过标识符进行取消相应组的任务
def greet(name):
    print('Hello {}'.format(name))

schedule.every().day.do(greet, 'Andrea').tag('daily-tasks', 'friend')
schedule.every().hour.do(greet, 'John').tag('hourly-tasks', 'friend')
schedule.every().hour.do(greet, 'Monica').tag('hourly-tasks', 'customer')
schedule.every().day.do(greet, 'Derek').tag('daily-tasks', 'guest')

schedule.clear('daily-tasks')
```

**7、如何传递参数给任务函数**

```python
def greet(name):
    print('Hello', name)

schedule.every(2).seconds.do(greet, name='Alice')
schedule.every(4).seconds.do(greet, name='Bob')
```

### schedule 源码阅读

使用 0.6.0 版本最新代码进行分析，加起来才 6 百多行，实现很简洁，先来看看当前的文件结构

```python
"""
➜ tree
# 省略部分文件，代码全部在 __init__.py 中
.
├── schedule
│   └── __init__.py
├── setup.py
├── test_schedule.py
└── tox.ini

先从一段简单的代码分析
"""
import schedule
import time
import arrow

def job():
    print(f"time: {arrow.now().format('YYYY-MM-DD HH:mm:ss')}, I'm working...")

if __name__ == '__main__':
    print('start schedule...')
    schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

"""
start schedule...
time: 2019-09-27 21:28:14, I'm working...
time: 2019-09-27 21:28:24, I'm working...
time: 2019-09-27 21:28:34, I'm working...
"""
```

先来看看 run_pending 做了什么事情：

```python
def run_pending():
    """Calls :meth:`run_pending <Scheduler.run_pending>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    default_scheduler.run_pending()  # what? default_scheduler 又是什么？


#: Default :class:`Scheduler <Scheduler>` object
default_scheduler = Scheduler()
```

原来是 Scheduler 类的一个实例，接下来去 Scheduler 找 run_pending 看看这个方法做了什么操作.

### Scheduler 类

```python
class Scheduler(object):
    """
    Objects instantiated by the :class:`Scheduler <Scheduler>` are
    factories to create jobs, keep record of scheduled jobs and
    handle their execution.
    """
    def __init__(self):
        self.jobs = []
```

1、初始化函数 `__init__` 做了什么初始化操作，结果只是简单地设置了一个保存 Job 的列表，这也是 schedule 简洁设计的一个重要点，所有运行的任务都使用一个列表来保存在内存中，不提供任何接入不同存储的配置项。

```python
class Scheduler(object):
    """
    Objects instantiated by the :class:`Scheduler <Scheduler>` are
    factories to create jobs, keep record of scheduled jobs and
    handle their execution.
    """
        # 省略部分代码
    def run_pending(self):
        """
        运行所有计划运行的作业
        Run all jobs that are scheduled to run.

        Please note that it is *intended behavior that run_pending()
        does not run missed jobs*. For example, if you've registered a job
        that should run every minute and you only call run_pending()
        in one hour increments then your job won't be run 60 times in
        between but only once.
        """
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            self._run_job(job)
```

2、接着看看 run_pending 方法做了什么，可以看到 run_pending 从 jobs 列表中获取当前可以运行的 job 保存在 runnable_jobs， 并对 runnable_jobs 元祖进行排序并对每一个 job 执行 _run_job 方法, 这个地方可能有人会有疑问，Job 到底是个什么对象，为什么可以用 sorted 方法排序，难道 Job 对象实现了一些 Python 黑魔法函数，例如 `__lt__` 等?

```python
def _run_job(self, job):
        ret = job.run()
        if isinstance(ret, CancelJob) or ret is CancelJob:
            self.cancel_job(job)

    def cancel_job(self, job):
        """
        Delete a scheduled job.

        :param job: The job to be unscheduled
        """
        try:
            self.jobs.remove(job)
        except ValueError:
            pass
```

3、进入 _run_job 方法，可以看到这个方法只是负责调用 job 对象的 run 方法运行这个 job 而已，并且根据 run 返回的对象判断是否取消该任务. 取消一个 job 就是从 jobs 列表中将这个 job 对象去除即可

### Job 类

从上面 Schedule 追踪下面，最后还是调用 job 的 run 方法进行操作，接下来就继续对 Job 追踪

1、**Job 的初始化方法做了什么**

```python
class Job(object):
    """
    A periodic job as used by :class:`Scheduler`.

    :param interval: A quantity of a certain time unit
    :param scheduler: The :class:`Scheduler <Scheduler>` instance that
                      this job will register itself with once it has
                      been fully configured in :meth:`Job.do()`.

    Every job runs at a given fixed time interval that is defined by:

    * a :meth:`time unit <Job.second>`
    * a quantity of `time units` defined by `interval`

    A job is usually created and returned by :meth:`Scheduler.every`
    method, which also defines its `interval`.
    """
    def __init__(self, interval, scheduler=None):
        self.interval = interval  # pause interval * unit between runs（配置运行任务的时间单位数量，如 seconds(10).do(job),10 就是这个时间单位数量）
        self.latest = None  # upper limit to the interval（ interval 的上限)
        self.job_func = None  # the job job_func to run   (运行任务的函数，通常是我们定义需要定时执行的代码逻辑)
        self.unit = None  # time units, e.g. 'minutes', 'hours', ... （时间单位）
        self.at_time = None  # optional time at which this job runs   (设置在某个时间点运行)
        self.last_run = None  # datetime of the last run   （上次执行的时间)
        self.next_run = None  # datetime of the next run    (下次执行的时间)
        self.period = None  # timedelta between runs, only valid for
        self.start_day = None  # Specific day of the week to start on （指定一周中的第几天运行）
        self.tags = set()  # unique set of tags for the job  （Job 的唯一tag 标识）
        self.scheduler = scheduler  # scheduler to register with  （Scheduler 类，可继承并使用自己实现的 Scheduler 类）

   def __lt__(self, other):
        """
        看这个黑魔法函数，就是上面 Scheduler 类中 job 可以使用 sorted 排序的原因
        PeriodicJobs are sortable based on the scheduled time they
        run next.
        """
        return self.next_run < other.next_run
```

2、**job run 方法的逻辑**

```python
def run(self):
        """
        Run the job and immediately reschedule it.

        :return: The return value returned by the `job_func`
        """
        logger.info('Running job %s', self)
        ret = self.job_func()
        self.last_run = datetime.datetime.now()
        self._schedule_next_run()
        return ret
```

3、**every 函数操作**

可能看到这里的朋友觉得有点混乱了，job 是什么时候实例化的，又是什么时候加入 Scheduler 的 jobs 列表的，其实我没有按照 示例代码的顺序来讲话，可以回到前面代码示例中有下面这句代码在 run_pending 之前：

```python
schedule.every(10).seconds.do(job)
```

也就是这个地方实例化 Job 类的，可以跳到这段代码分析分析：

```python
class Scheduler(object):
        # 省略部分代码
    def every(self, interval=1):
        """
        Schedule a new periodic job.

        :param interval: A quantity of a certain time unit
        :return: An unconfigured :class:`Job <Job>`
        """
        job = Job(interval, self)
        return job

def every(interval=1):
    """Calls :meth:`every <Scheduler.every>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    return default_scheduler.every(interval)
```

4、**do 函数操作**

可以看到在调用 every 函数时，最终调用的是 Scheduler 类的 every 方法，该方法主要是根据设置的间隔时间（interval) 实例化 Job 类并返回该实例，这段代码同样没有 job 加入 Scheduler 的 jobs 列表的逻辑，那就是在 seconds.do 方法进行的操作，接着翻代码看看：

```python
def do(self, job_func, *args, **kwargs):
        """
        Specifies the job_func that should be called every time the
        job runs.

        Any additional arguments are passed on to job_func when
        the job runs.

        :param job_func: The function to be scheduled
        :return: The invoked job instance
        """
        self.job_func = functools.partial(job_func, *args, **kwargs)
        try:
            functools.update_wrapper(self.job_func, job_func)
        except AttributeError:
            # job_funcs already wrapped by functools.partial won't have
            # __name__, __module__ or __doc__ and the update_wrapper()
            # call will fail.
            pass
        self._schedule_next_run()
        self.scheduler.jobs.append(self)
        return self
```

*   首先使用标准库的 partial (偏函数) 先提前为 job_func(我们提供的业务逻辑代码) 设置参数，用一些默认参数包装一个可调用对象, 返回结果是可调用对象，并且可以像原始对象一样对待，冻结部分函数位置函数或关键字参数，简化函数, 更少更灵活的函数参数调用。
*   update_wrapper 做了什么操作，这个函数的作用就是从 **被修饰的函数 (job_func)** 中取出一些属性值来，赋值给 **修饰器函数 (self.job_func)** 。默认 partial 对象没有 **name** 和 **doc**, 这种情况下，对于装饰器函数非常难以 debug.
*   接着就是 self._schedule_next_run 方法，这个是 schedule 库的核心代码，有点复杂，下面慢慢解释
*   接下来一行就是想要的答案了，这个时候将当前 Job 类加入 Scheduler 类的 jobs 列表中，append(self) 这个 self 就是当前的 Job 类

5、**核心 _schedule_next_run**

```python
def _schedule_next_run(self):
        """
        Compute the instant when this job should run next.
        """
        # 第一步，判断当前运行的时间单位是否在指定范围内，不在则报错
        if self.unit not in ('seconds', 'minutes', 'hours', 'days', 'weeks'):
            raise ScheduleValueError('Invalid unit')

                # 如果 interval 的上限时间不为 None, 判断 interval 上限时间是否小于 interval
        # 小于则报错，latest 用于 every(A).to(B).seconds 每 N 秒执行一次 job 任务，
        # 其中 A <= N <= B. 所以 A(interval) <= B (latest)
        if self.latest is not None:
            if not (self.latest >= self.interval):
                raise ScheduleError('`latest` is greater than `interval`')
            # 执行时间随机从 interval 到 latest 之前取值
            interval = random.randint(self.interval, self.latest)
        else:
            interval = self.interval

        # 下面两行用于获取下一次执行的时间
        self.period = datetime.timedelta(**{self.unit: interval})
        self.next_run = datetime.datetime.now() + self.period

        # start_day 这个只会在设置一周的第几天执行才会有，所以 unit 时间单位不是 weeks 就报错
        if self.start_day is not None:
            if self.unit != 'weeks':
                raise ScheduleValueError('`unit` should be \'weeks\'')
            weekdays = (
                'monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday'
            )
            # 如果天数的标识不是上面的，报错
            if self.start_day not in weekdays:
                raise ScheduleValueError('Invalid start day')

            weekday = weekdays.index(self.start_day)
            # datetime 的 weekday() 函数，计算目标时间是否已经在本周发送
            days_ahead = weekday - self.next_run.weekday() 
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            self.next_run += datetime.timedelta(days_ahead) - self.period
        if self.at_time is not None:
            if (self.unit not in ('days', 'hours', 'minutes')
                    and self.start_day is None):
                raise ScheduleValueError(('Invalid unit without'
                                          ' specifying start day'))
            kwargs = {
                'second': self.at_time.second,
                'microsecond': 0
            }
            if self.unit == 'days' or self.start_day is not None:
                kwargs['hour'] = self.at_time.hour
            if self.unit in ['days', 'hours'] or self.start_day is not None:
                kwargs['minute'] = self.at_time.minute
            self.next_run = self.next_run.replace(**kwargs)
            # If we are running for the first time, make sure we run
            # at the specified time *today* (or *this hour*) as well
            if not self.last_run:
                now = datetime.datetime.now()
                if (self.unit == 'days' and self.at_time > now.time() and
                        self.interval == 1):
                    self.next_run = self.next_run - datetime.timedelta(days=1)
                elif self.unit == 'hours' \
                        and self.at_time.minute > now.minute \
                        or (self.at_time.minute == now.minute
                            and self.at_time.second > now.second):
                    self.next_run = self.next_run - datetime.timedelta(hours=1)
                elif self.unit == 'minutes' \
                        and self.at_time.second > now.second:
                    self.next_run = self.next_run - \
                                    datetime.timedelta(minutes=1)
        if self.start_day is not None and self.at_time is not None:
            # Let's see if we will still make that time we specified today
            if (self.next_run - datetime.datetime.now()).days >= 7:
                self.next_run -= self.period
```

APScheduler 库
-------------

APScheduler（Advanced Python Scheduler）是基于 Quartz 的一个 Python 定时任务框架，实现了 Quartz 的所有功能, 是一个轻量级但功能强大的进程内任务调度程序。它有以下三个特点：

*   类似于 Liunx Cron 的调度程序 (可选的开始 / 结束时间)
*   基于时间间隔的执行调度 (周期性调度，可选的开始 / 结束时间)
*   一次性执行任务 (在设定的日期 / 时间运行一次任务)

可以按照个人喜好来混合和匹配调度系统和存储作业的后端存储，支持以下几种后台作业存储：

*   Memory
*   SQLAlchemy (任何 SQLAlchemy 支持的关系型数据库)
*   MongoDB
*   Redis
*   ZooKeeper
*   RethinkDB

APScheduler 集成了以下几个 Python 框架：

*   asyncio
*   gevent
*   Tornado
*   Twisted
*   Qt

总结以上，APScheduler 支持基于日期、固定时间、crontab 形式三种形式的任务调度，可以灵活接入各种类型的后台作业存储来持久化作业，同时提供了多种调度器 (后面提及)，集成多种 Python 框架，可以根据实际情况灵活组合后台存储以及调度器来使用。

### APScheduler 的架构及工作原理

**1、APScheduler 基本概念**

APScheduler 由四个组件构成（注：该部分翻译至官方文档）：

*   triggers 触发器

触发器包含调度逻辑。每个作业（job）都有自己的触发器，用于确定下一个作业何时运行。除了最初的配置，触发器是完全无状态的

*   job stores 作业存储

job stores 是存放作业的地方，默认保存在内存中。作业数据序列化后保存至持久性数据库，从持久性数据库加载回来时会反序列化。作业存储 (job stores) 不将作业数据保存在内存中(默认存储除外)，相反，内存只是充当后端存储在保存、加载、更新、查找作业时的中间人角色。作业存储不能在调度器（schedulers) 之间共享

*   executors 执行器

执行器处理作业的运行。它们通常通过将作业中的指定可调用部分提交给线程或进程池来实现这一点。 当作业完成后，执行器通知调度器，然后调度器发出一个适当的事件

*   schedulers 调度器

调度器是将其余部分绑定在一起的工具。通常只有一个调度器 (scheduler) 在应用程序中运行。应用程序开发者通常不直接处理作业存储 (job stores)、执行器(executors) 或者触发器 (triggers)。相反，调度器提供了适当的接口来处理它们。配置作业存储(job stores) 和执行器 (executors) 是通过调度器 (scheduler) 来完成的, 就像添加、修改和删除 job(作业)一样

**2、APScheduler 架构图**

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/v2-11c7e4b859e845afe6db25a2f413ba21_r.jpg)