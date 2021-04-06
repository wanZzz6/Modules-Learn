python里与对象类型相关的模块有: types、typing、collections.abc、inspect，这些都是python的内置模块，第三方的有pydantic。

## types

该模块定义了一系列python内置类型的名称，比如`FunctionType`、`GeneratorType`、`MethodType`，阅读types模块的源码会发现，其对象类型的来源是相当的通俗易懂，比如：

定义`GeneratorType` 迭代器类型：

```python
def _g():
    yield 1
GeneratorType = type(_g())
```

定义`AsyncGeneratorType` 异步迭代器类型：

```python
async def _ag():
    yield
_ag = _ag()
AsyncGeneratorType = type(_ag)
```

就是先创建这样一个类型的临时对象，然后用 `type()` 方法获取其类型对象的引用，类似情况的在`types.py` 模块的源码中还有很多，这可以帮助我们学习如何创建某一类型的对象，该类型的创建需要有哪些必要关键字等。我们可以从types模块直接导入，然后用`isinstance()` 方法一个对象判断是否是某个类型的实例，比如：

```python
from types import BuiltinFunctionType

print(isinstance(all, BuiltinFunctionType))
# True
```

## inspect

该模块提供了一系列的**对象检查方法**，如：

> ismodule(), isclass(), ismethod(), isfunction(), isgeneratorfunction(),
>         isgenerator(), istraceback(), isframe(), iscode(), isbuiltin(),
>         isroutine()

inspect 模块还有其他一些高级的获取数据的方法，比如 `getclasstree()`获取类的继承关系树状结构, `stack()` 获取运行时的调用堆栈，`signature()` 获取对象签名等，详细用法可以参考我的其他文章。

