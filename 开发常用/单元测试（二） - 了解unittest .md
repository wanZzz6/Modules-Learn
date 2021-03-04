## 前言

python内置的[unittest](https://docs.python.org/3.8/library/unittest.html)模块， 写起来稍微繁琐，比如都要写一个TestCase类，还得用 assertEqual, assertNotEqual等断言方法，业界使用更多的是 第三方的pytest包，稍后会介绍。

这里简单过一遍unitest的用法即可，没必要深入学习。

关于`unittest`有四个概念先得先知道下。

- **test fixture**：主要负责测试前的一些准备工作和一些清理操作，比如创建一些临时数据库、目录和启动服务器等。这个过程由系统负责执行，我们只需要写清楚`setUp`方法就可以了，关于这个方法后面再介绍吧。
- **test case**：这个比较重要，说三遍。每一个单独的测试方法都叫做一个test case，我们给待测的代码A一个input，A返回给我们一个response，我们最后check下response是不是所期望的，就能判断出A写的对不对。这整个测试过程都在test case中执行。`unittest`提供了一个基类`TestCase`，我们写的每个测试方法都必须是在一个类中，而这个类必须继承`TestCase`。
- **test suite**：这个是许多个`test case`的集合，通过`test case`可以让多个`test case`一起执行。这个过程也是系统负责执行的。
- **test runner**：这个负责`test case`的执行并把结果展示给用户。

## 基本用法

做一个简单的小实例：

![img](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/1496566-20190512160649874-492651896.png)



demo1.py

```python
class MyClass():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y

    def sub(self):
        return self.x - self.y
```

test.py

```python
import unittest
from demo1 import MyClass


class MyclassTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        测试之前的准备工作
        :return:
        """
        self.clac = MyClass(4, 3)

    def tearDown(self) -> None:
        """
        测试之后的收尾
        如关闭数据库
        :return:
        """
        pass

    def test_add(self):
        ret = self.clac.add()
        self.assertEqual(ret, 7)

    def test_sub(self):
        ret = self.clac.sub()
        self.assertEqual(ret, 1)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyclassTest('test_add'))
    suite.addTest(MyclassTest('test_sub'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
```

`setUp`就是帮我们做测试前的准备工作，比如实例化等.

`tearDown`可以帮我们关闭数据库等收尾操作.

一般测试方法**必须以test_开头**，里面可以写我们需要测试的业务逻辑，同时指定`self.assertEqual()`将我们的结果和运行的实际结果进行比对。

suite就是我们的测试集，之后添加测试用例，用runner实例化运行。

Pycharm执行结果如下：

```
Testing started at 15:05 ...
Launching unittests with arguments python -m unittest D:/git_dir/things-gateway/Scripts/test_sum.py in D:\git_dir\things-gateway\Scripts



Ran 2 tests in 0.002s

OK
```

如果我们将预计的结果写错，

```python
    def test_add(self):
        ret = self.clac.add()
        self.assertEqual(ret,2)

    def test_sub(self):
        ret = self.clac.sub()
        self.assertEqual(ret,3)
```

同时更改运行方式为:

```python
if __name__ == '__main__':
    unittest.main()
```



执行结果：

```
Testing started at 15:08 ...
Launching unittests with arguments python -m unittest test_sum.MyclassTest in D:\git_dir\things-gateway\Scripts


2 != 7

Expected :7
Actual   :2
<Click to see difference>

Traceback (most recent call last):
  File "D:\SoftInstall\PyCharm 2020.3.2\plugins\python\helpers\pycharm\teamcity\diff_tools.py", line 32, in _patched_equals
    old(self, first, second, msg)
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 839, in assertEqual
    assertion_func(first, second, msg=msg)
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 832, in _baseAssertEqual
    raise self.failureException(msg)
AssertionError: 7 != 2

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 59, in testPartExecutor
    yield
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 615, in run
    testMethod()
  File "D:\git_dir\things-gateway\Scripts\test_sum.py", line 23, in test_add
    self.assertEqual(ret, 2)


3 != 1

Expected :1
Actual   :3
<Click to see difference>

Traceback (most recent call last):
  File "D:\SoftInstall\PyCharm 2020.3.2\plugins\python\helpers\pycharm\teamcity\diff_tools.py", line 32, in _patched_equals
    old(self, first, second, msg)
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 839, in assertEqual
    assertion_func(first, second, msg=msg)
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 832, in _baseAssertEqual
    raise self.failureException(msg)
AssertionError: 1 != 3

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 59, in testPartExecutor
    yield
  File "D:\SoftInstall\Anacoda3\lib\unittest\case.py", line 615, in run
    testMethod()
  File "D:\git_dir\things-gateway\Scripts\test_sum.py", line 27, in test_sub
    self.assertEqual(ret, 3)




Ran 2 tests in 0.006s

FAILED (failures=2)
```

其他：

[廖雪峰博客 - 单元测试](https://www.liaoxuefeng.com/wiki/1016959663602400/1017604210683936#0)

