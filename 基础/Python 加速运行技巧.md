> 原文地址 [zhuanlan.zhihu.com](https://zhuanlan.zhihu.com/p/143052860)

Python 是一种脚本语言，相比 C/C++ 这样的编译语言，在效率和性能方面存在一些不足。但是，有很多时候，Python 的效率并没有想象中的那么夸张。本文对一些 Python 代码加速运行的技巧进行整理。

**0. 代码优化原则**
-------------

本文会介绍不少的 Python 代码加速运行的技巧。在深入代码优化细节之前，需要了解一些代码优化基本原则。

第一个基本原则是不要过早优化。很多人一开始写代码就奔着性能优化的目标，“让正确的程序更快要比让快速的程序正确容易得多”。因此，优化的前提是代码能正常工作。过早地进行优化可能会忽视对总体性能指标的把握，在得到全局结果前不要主次颠倒。

第二个基本原则是权衡优化的代价。优化是有代价的，想解决所有性能的问题是几乎不可能的。通常面临的选择是时间换空间或空间换时间。另外，开发代价也需要考虑。

第三个原则是不要优化那些无关紧要的部分。如果对代码的每一部分都去优化，这些修改会使代码难以阅读和理解。如果你的代码运行速度很慢，首先要找到代码运行慢的位置，通常是内部循环，专注于运行慢的地方进行优化。在其他地方，一点时间上的损失没有什么影响。

**1. 避免全局变量**
-------------

```python
# 不推荐写法。代码耗时：26.8秒
import math

size = 10000
for x in range(size):
    for y in range(size):
        z = math.sqrt(x) + math.sqrt(y)
```

许多程序员刚开始会用 Python 语言写一些简单的脚本，当编写脚本时，通常习惯了直接将其写为全局变量，例如上面的代码。但是，由于全局变量和局部变量实现方式不同，定义在全局范围内的代码运行速度会比定义在函数中的慢不少。通过将脚本语句放入到函数中，通常可带来 15% - 30% 的速度提升。

```python
# 推荐写法。代码耗时：20.6秒
import math

def main():  # 定义到函数中，以减少全部变量使用
    size = 10000
    for x in range(size):
        for y in range(size):
            z = math.sqrt(x) + math.sqrt(y)

main()
```

**2. 避免`.`**
------------

**2.1 避免模块和函数属性访问**

```python
# 不推荐写法。代码耗时：14.5秒
import math

def computeSqrt(size: int):
    result = []
    for i in range(size):
        result.append(math.sqrt(i))
    return result

def main():
    size = 10000
    for _ in range(size):
        result = computeSqrt(size)

main()
```

每次使用`.`（属性访问操作符时）会触发特定的方法，如`__getattribute__()`和`__getattr__()`，这些方法会进行字典操作，因此会带来额外的时间开销。通过`from import`语句，可以消除属性访问。

```python
# 第一次优化写法。代码耗时：10.9秒
from math import sqrt

def computeSqrt(size: int):
    result = []
    for i in range(size):
        result.append(sqrt(i))  # 避免math.sqrt的使用
    return result

def main():
    size = 10000
    for _ in range(size):
        result = computeSqrt(size)

main()
```

在第 1 节中我们讲到，局部变量的查找会比全局变量更快，因此对于频繁访问的变量`sqrt`，通过将其改为局部变量可以加速运行。

```python
# 第二次优化写法。代码耗时：9.9秒
import math

def computeSqrt(size: int):
    result = []
    sqrt = math.sqrt  # 赋值给局部变量
    for i in range(size):
        result.append(sqrt(i))  # 避免math.sqrt的使用
    return result

def main():
    size = 10000
    for _ in range(size):
        result = computeSqrt(size)

main()
```

除了`math.sqrt`外，`computeSqrt`函数中还有`.`的存在，那就是调用`list`的`append`方法。通过将该方法赋值给一个局部变量，可以彻底消除`computeSqrt`函数中`for`循环内部的`.`使用。

```python
# 推荐写法。代码耗时：7.9秒
import math

def computeSqrt(size: int):
    result = []
    append = result.append
    sqrt = math.sqrt    # 赋值给局部变量
    for i in range(size):
        append(sqrt(i))  # 避免 result.append 和 math.sqrt 的使用
    return result

def main():
    size = 10000
    for _ in range(size):
        result = computeSqrt(size)

main()
```

**2.2 避免类内属性访问**
----------------

```python
# 不推荐写法。代码耗时：10.4秒
import math
from typing import List

class DemoClass:
    def __init__(self, value: int):
        self._value = value
    
    def computeSqrt(self, size: int) -> List[float]:
        result = []
        append = result.append
        sqrt = math.sqrt
        for _ in range(size):
            append(sqrt(self._value))
        return result

def main():
    size = 10000
    for _ in range(size):
        demo_instance = DemoClass(size)
        result = demo_instance.computeSqrt(size)

main()
```

避免`.`的原则也适用于类内属性，访问`self._value`的速度会比访问一个局部变量更慢一些。通过将需要频繁访问的类内属性赋值给一个局部变量，可以提升代码运行速度。

```python
# 推荐写法。代码耗时：8.0秒
import math
from typing import List

class DemoClass:
    def __init__(self, value: int):
        self._value = value
    
    def computeSqrt(self, size: int) -> List[float]:
        result = []
        append = result.append
        sqrt = math.sqrt
        value = self._value
        for _ in range(size):
            append(sqrt(value))  # 避免 self._value 的使用
        return result

def main():
    size = 10000
    for _ in range(size):
        demo_instance = DemoClass(size)
        demo_instance.computeSqrt(size)

main()
```

**3. 避免不必要的抽象**
---------------

```python
# 不推荐写法，代码耗时：0.55秒
class DemoClass:
    def __init__(self, value: int):
        self.value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, x: int):
        self._value = x

def main():
    size = 1000000
    for i in range(size):
        demo_instance = DemoClass(size)
        value = demo_instance.value
        demo_instance.value = i

main()
```

任何时候当你使用额外的处理层（比如装饰器、属性访问、描述器）去包装代码时，都会让代码变慢。大部分情况下，需要重新进行审视使用属性访问器的定义是否有必要，使用`getter/setter`函数对属性进行访问通常是 C/C++ 程序员遗留下来的代码风格。如果真的没有必要，就使用简单属性。

```python
# 推荐写法，代码耗时：0.33秒
class DemoClass:
    def __init__(self, value: int):
        self.value = value  # 避免不必要的属性访问器

def main():
    size = 1000000
    for i in range(size):
        demo_instance = DemoClass(size)
        value = demo_instance.value
        demo_instance.value = i

main()
```

**4. 避免数据复制**
-------------

**4.1 避免无意义的数据复制**

```python
# 不推荐写法，代码耗时：6.5秒
def main():
    size = 10000
    for _ in range(size):
        value = range(size)
        value_list = [x for x in value]
        square_list = [x * x for x in value_list]

main()
```

上面的代码中`value_list`完全没有必要，这会创建不必要的数据结构或复制。

```python
# 推荐写法，代码耗时：4.8秒
def main():
    size = 10000
    for _ in range(size):
        value = range(size)
        square_list = [x * x for x in value]  # 避免无意义的复制

main()
```

另外一种情况是对 Python 的数据共享机制过于偏执，并没有很好地理解或信任 Python 的内存模型，滥用 `copy.deepcopy()`之类的函数。通常在这些代码中是可以去掉复制操作的。

**4.2 交换值时不使用中间变量**

```python
# 不推荐写法，代码耗时：0.07秒
def main():
    size = 1000000
    for _ in range(size):
        a = 3
        b = 5
        temp = a
        a = b
        b = temp

main()
```

上面的代码在交换值时创建了一个临时变量`temp`，如果不借助中间变量，代码更为简洁、且运行速度更快。

```python
# 推荐写法，代码耗时：0.06秒
def main():
    size = 1000000
    for _ in range(size):
        a = 3
        b = 5
        a, b = b, a  # 不借助中间变量

main()
```

**4.3 字符串拼接用`join`而不是`+`**

```python
# 不推荐写法，代码耗时：2.6秒
import string
from typing import List

def concatString(string_list: List[str]) -> str:
    result = ''
    for str_i in string_list:
        result += str_i
    return result

def main():
    string_list = list(string.ascii_letters * 100)
    for _ in range(10000):
        result = concatString(string_list)

main()
```

当使用`a + b`拼接字符串时，由于 Python 中字符串是不可变对象，其会申请一块内存空间，将`a`和`b`分别复制到该新申请的内存空间中。因此，如果要拼接 ![](https://www.zhihu.com/equation?tex=n) 个字符串，会产生 ![](https://www.zhihu.com/equation?tex=n-1) 个中间结果，每产生一个中间结果都需要申请和复制一次内存，严重影响运行效率。而使用`join()`拼接字符串时，会首先计算出需要申请的总的内存空间，然后一次性地申请所需内存，并将每个字符串元素复制到该内存中去。

```python
# 推荐写法，代码耗时：0.3秒
import string
from typing import List

def concatString(string_list: List[str]) -> str:
    return ''.join(string_list)  # 使用 join 而不是 +

def main():
    string_list = list(string.ascii_letters * 100)
    for _ in range(10000):
        result = concatString(string_list)

main()
```

5. 利用if条件的短路特性
--------------------

```python
# 不推荐写法，代码耗时：0.05秒
from typing import List

def concatString(string_list: List[str]) -> str:
    abbreviations = {'cf.', 'e.g.', 'ex.', 'etc.', 'flg.', 'i.e.', 'Mr.', 'vs.'}
    abbr_count = 0
    result = ''
    for str_i in string_list:
        if str_i in abbreviations:
            result += str_i
    return result

def main():
    for _ in range(10000):
        string_list = ['Mr.', 'Hat', 'is', 'Chasing', 'the', 'black', 'cat', '.']
        result = concatString(string_list)

main()
```

`if` 条件的短路特性是指对`if a and b`这样的语句， 当`a`为`False`时将直接返回，不再计算`b`；对于`if a or b`这样的语句，当`a`为`True`时将直接返回，不再计算`b`。因此， 为了节约运行时间，对于`or`语句，应该将值为`True`可能性比较高的变量写在`or`前，而`and`应该推后。

```python
# 推荐写法，代码耗时：0.03秒
from typing import List

def concatString(string_list: List[str]) -> str:
    abbreviations = {'cf.', 'e.g.', 'ex.', 'etc.', 'flg.', 'i.e.', 'Mr.', 'vs.'}
    abbr_count = 0
    result = ''
    for str_i in string_list:
        if str_i[-1] == '.' and str_i in abbreviations:  # 利用 if 条件的短路特性
            result += str_i
    return result

def main():
    for _ in range(10000):
        string_list = ['Mr.', 'Hat', 'is', 'Chasing', 'the', 'black', 'cat', '.']
        result = concatString(string_list)

main()
```

**6. 循环优化**
-----------

**6.1 用`for`循环代替`while`循环**

```python
# 不推荐写法。代码耗时：6.7秒
def computeSum(size: int) -> int:
    sum_ = 0
    i = 0
    while i < size:
        sum_ += i
        i += 1
    return sum_

def main():
    size = 10000
    for _ in range(size):
        sum_ = computeSum(size)

main()
```

Python 的`for`循环比`while`循环快不少。

```python
# 推荐写法。代码耗时：4.3秒
def computeSum(size: int) -> int:
    sum_ = 0
    for i in range(size):  # for 循环代替 while 循环
        sum_ += i
    return sum_

def main():
    size = 10000
    for _ in range(size):
        sum_ = computeSum(size)

main()
```

**6.2 使用隐式`for`循环代替显式`for`循环**

针对上面的例子，更进一步可以用隐式`for`循环来替代显式`for`循环

```python
# 推荐写法。代码耗时：1.7秒
def computeSum(size: int) -> int:
    return sum(range(size))  # 隐式 for 循环代替显式 for 循环

def main():
    size = 10000
    for _ in range(size):
        sum = computeSum(size)

main()
```

**6.3 减少内层`for`循环的计算**

```python
# 不推荐写法。代码耗时：12.8秒
import math

def main():
    size = 10000
    sqrt = math.sqrt
    for x in range(size):
        for y in range(size):
            z = sqrt(x) + sqrt(y)

main()
```

上面的代码中`sqrt(x)`位于内侧`for`循环， 每次训练过程中都会重新计算一次，增加了时间开销。

```python
# 推荐写法。代码耗时：7.0秒
import math

def main():
    size = 10000
    sqrt = math.sqrt
    for x in range(size):
        sqrt_x = sqrt(x)  # 减少内层 for 循环的计算
        for y in range(size):
            z = sqrt_x + sqrt(y)

main()
```

**7. 使用`numba.jit`**
--------------------

我们沿用上面介绍过的例子，在此基础上使用`numba.jit`。 `numba`可以将 Python 函数 JIT 编译为机器码执行，大大提高代码运行速度。关于`numba`的更多信息见下面的主页：

```python
# 推荐写法。代码耗时：0.62秒
import numba

@numba.jit
def computeSum(size: float) -> int:
    sum = 0
    for i in range(size):
        sum += i
    return sum

def main():
    size = 10000
    for _ in range(size):
        sum = computeSum(size)

main()
```

**8. 选择合适的数据结构**
----------------

Python 内置的数据结构如`str`, `tuple`, `list`, `set`, `dict`底层都是 C 实现的，速度非常快，自己实现新的数据结构想在性能上达到内置的速度几乎是不可能的。

`list`类似于 C++ 中的`std::vector`，是一种动态数组。其会预分配一定内存空间，当预分配的内存空间用完，又继续向其中添加元素时，会申请一块更大的内存空间，然后将原有的所有元素都复制过去，之后销毁之前的内存空间，再插入新元素。删除元素时操作类似，当已使用内存空间比预分配内存空间的一半还少时，会另外申请一块小内存，做一次元素复制，之后销毁原有大内存空间。因此，如果有频繁的新增、删除操作，新增、删除的元素数量又很多时，list 的效率不高。此时，应该考虑使用`collections.deque`。`collections.deque`是双端队列，同时具备栈和队列的特性，能够在两端进行 ![](https://www.zhihu.com/equation?tex=%5Cmathcal+O%281%29) 复杂度的插入和删除操作。

`list`的查找操作也非常耗时。当需要在`list`频繁查找某些元素，或频繁有序访问这些元素时，可以使用`bisect`维护`list`对象有序并在其中进行二分查找，提升查找的效率。

另外一个常见需求是查找极小值或极大值，此时可以使用`heapq`模块将`list`转化为一个堆，使得获取最小值的时间复杂度是 ![](https://www.zhihu.com/equation?tex=%5Cmathcal+O%281%29) 。

下面的网页给出了常用的 Python 数据结构的各项操作的时间复杂度：

**参考资料**
--------

*   David Beazley & Brian K. Jones. Python Cookbook, Third edition. O'Reilly Media, ISBN: 9781449340377, 2013.
*   张颖 & 赖勇浩. 编写高质量代码：改善 Python 程序的 91 个建议. 机械工业出版社, ISBN: 9787111467045, 2014.