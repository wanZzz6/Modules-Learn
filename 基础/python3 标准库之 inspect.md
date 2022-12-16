> 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/hOmLjj3IpDtjTXkLDwS_yA)

inspect 模块提供了得知活动对象的函数，包括模块、类、实例、函数和方法。该模块中的函数可用于检索函数的原始源代码，查看堆栈上方法的参数，并从中提取有用的信息用以生成源代码的库文档。

实例模块
----

本节的其余示例会使用到这个示例文件， `example.py`。

```python
# example.py
# This comment appears first
# and spans 2 lines.
# This comment does not show up in the output of getcomments().
"""Sample file to serve as the basis for inspect examples.
"""
def module_level_function(arg1, arg2='default', *args, **kwargs):
    """This function is declared in the module."""
    local_variable = arg1 * 2
    return local_variable

class A(object):
    """The A class."""
    def __init__(self, name):
        self.name = name
    def get_name(self):
        "Returns the name of the instance."
        return self.name

instance_of_a = A('sample_instance')

class B(A):
    """This is the B class.
    It is derived from A.
    """
    # This method is not part of A.
    def do_something(self):
        """Does some work"""
    def get_name(self):
        "Overrides version from A"
        return 'B(' + self.name + ')'
```

检测模块
----

第一类为内省探测活动对象，用以了解活动对象。使用 `getmembers()` 来发现对象的成员属性。返回的可能成员类型取决于扫描对象的类型。模块可以包含类和函数; 类可以包含方法和属性; 等等。

`getmembers()` 的参数包含一个用于扫描 (模块、类或实例) 的对象，以及用于筛选返回的对象的可选断言函数。返回值是包含两个值的元组列表: 成员的名称和成员的类型。检查模块包括几个这样的断言函数，它们叫 `ismodule()`、 `isclass()` 等。

```python
# inspect_getmembers_module.py
import inspect
import example

for name, data in inspect.getmembers(example):
    if name.startswith('__'):
        continue
    print('{} : {!r}'.format(name, data))
```

此示例打印例子 example 模块中的成员。模块有几个私有属性，它们作为导入实现的一部分，以及一组 `__builtins__` 会出现在这个示例的输出中， 在这里所有这些都被忽略了，因为它们实际上并不是该模块的一部分，而且它们组成的列表很长，影响到了输出。

```python
$ python3 inspect_getmembers_module.py
A : <class 'example.A'>
B : <class 'example.B'>
instance_of_a : <example.A object at 0x1045a6978>
module_level_function : <function module_level_function at
0x1045be8c8>
```

用来断言的参数可以用于过滤返回的对象类型。

```python
# inspect_getmembers_module_class.py
import inspect
import example

for name, data in inspect.getmembers(example, inspect.isclass):
    print('{} : {!r}'.format(name, data))
```

现在输出中只包含类。

```python
$ python3 inspect_getmembers_module_class.py
A : <class 'example.A'>
B : <class 'example.B'>
```

检测类
---

使用 `getmembers()` 来扫描类的方式与模块相同，不过它的成员类型会不同。

```python
# inspect_getmembers_class.py
import inspect
from pprint import pprint
import example

pprint(inspect.getmembers(example.A), width=65)
```

由于没有进行过滤，所以输出中显示了类的属性、方法、槽 (slots) 和其他类成员。

```python
$ python3 inspect_getmembers_class.py
[('__class__', <class 'type'>),
 ('__delattr__',
  <slot wrapper '__delattr__' of 'object' objects>),
 ('__dict__',
  mappingproxy({'__dict__': <attribute '__dict__' of 'A'
objects>,
                '__doc__': 'The A class.',
                '__init__': <function A.__init__ at
0x1045b3158>,
                '__module__': 'example',
                '__weakref__': <attribute '__weakref__' of 'A'
objects>,
                'get_name': <function A.get_name at
0x1045b31e0>})),
 ('__dir__', <method '__dir__' of 'object' objects>),
 ('__doc__', 'The A class.'),
 ('__eq__', <slot wrapper '__eq__' of 'object' objects>),
 ('__format__', <method '__format__' of 'object' objects>),
 ('__ge__', <slot wrapper '__ge__' of 'object' objects>),
 ('__getattribute__',
  <slot wrapper '__getattribute__' of 'object' objects>),
 ('__gt__', <slot wrapper '__gt__' of 'object' objects>),
 ('__hash__', <slot wrapper '__hash__' of 'object' objects>),
 ('__init__', <function A.__init__ at 0x1045b3158>),
 ('__init_subclass__',
  <built-in method __init_subclass__ of type object at
0x101d12d58>),
 ('__le__', <slot wrapper '__le__' of 'object' objects>),
 ('__lt__', <slot wrapper '__lt__' of 'object' objects>),
 ('__module__', 'example'),
 ('__ne__', <slot wrapper '__ne__' of 'object' objects>),
 ('__new__',
  <built-in method __new__ of type object at 0x100996700>),
 ('__reduce__', <method '__reduce__' of 'object' objects>),
 ('__reduce_ex__', <method '__reduce_ex__' of 'object'
objects>),
 ('__repr__', <slot wrapper '__repr__' of 'object' objects>),
 ('__setattr__',
  <slot wrapper '__setattr__' of 'object' objects>),
 ('__sizeof__', <method '__sizeof__' of 'object' objects>),
 ('__str__', <slot wrapper '__str__' of 'object' objects>),
 ('__subclasshook__',
  <built-in method __subclasshook__ of type object at
0x101d12d58>),
 ('__weakref__', <attribute '__weakref__' of 'A' objects>),
 ('get_name', <function A.get_name at 0x1045b31e0>)]
```

要找到类的方法，可以使用 `isfunction()` 断言。`ismethod()` 断言只识别实例的绑定方法。

```python
# inspect_getmembers_class_methods.py
import inspect
from pprint import pprint
import example
pprint(inspect.getmembers(example.A, inspect.isfunction))
```

现在只返回未绑定的方法。

```sh
$ python3 inspect_getmembers_class_methods.py
[('__init__', <function A.__init__ at 0x1045b2158>),
 ('get_name', <function A.get_name at 0x1045b21e0>)]
```

B 的输出包括了 `get_name()`，以及父类中没有的方法，还有继承自 A 中实现的 `__init__()` 方法。

```python
# inspect_getmembers_class_methods_b.py
import inspect
from pprint import pprint
import example
pprint(inspect.getmembers(example.B, inspect.isfunction))
```

从 A 继承的方法，例如 `__init__()`，被认为是 B 的方法。

```sh
$ python3 inspect_getmembers_class_methods_b.py
[('__init__', <function A.__init__ at 0x103dc5158>),
 ('do_something', <function B.do_something at 0x103dc5268>),
 ('get_name', <function B.get_name at 0x103dc52f0>)]
```

检测实例
----

内省实例的工作方式与其他对象相同。

```python
# inspect_getmembers_instance.py
import inspect
from pprint import pprint
import example
a = example.A(name='inspect_getmembers')
pprint(inspect.getmembers(a, inspect.ismethod))
```

断言 `ismethod()` 从例子实例中识别出两个绑定方法。

```sh
$ python3 inspect_getmembers_instance.py
[('__init__', <bound method A.__init__ of <example.A object at 0
x101d9c0f0>>),
 ('get_name', <bound method A.get_name of <example.A object at 0
x101d9c0f0>>)]
```

文档字符串
-----

可以通过 `getdoc()` 检索对象的 docstring。返回值是带有制表符的 `__doc__` 属性，并使用统一缩进，其中制表符扩展为空格。

```python
# inspect_getdoc.py
import inspect
import example
print('B.__doc__:')
print(example.B.__doc__)
print()
print('getdoc(B):')
print(inspect.getdoc(example.B))
```

当它通过 `__doc__` 属性直接检索时，docstring 的第二行是缩进的，但是通过 `getdoc()` 获取时则第二行移动到了左边缘。

```sh
$ python3 inspect_getdoc.py
B.__doc__:
This is the B class.
    It is derived from A.
getdoc(B):
This is the B class.
It is derived from A.
```

除了获得实际的 docstring 之外，如果包含源文件注释，还可以从源文件实现的对象中检索到它的注释。`getcomments()` 函数查看对象的源，并在对象实现的前面找到它的一行行注释。

```python
# inspect_getcomments_method.py
import inspect
import example
print(inspect.getcomments(example.B.do_something))
```

返回的行包括注释的前缀（#），但去掉了前缀（#）前面的空格。

```sh
$ python3 inspect_getcomments_method.py
# This method is not part of A.
```

当一个模块被传递给 `getcomments()` 时，返回值始终是模块中的第一个注释。

```python
# inspect_getcomments_module.py
import inspect
import example
print(inspect.getcomments(example))
```

示例文件中的连续行被视为单个注释，但是一旦空白行出现，注释就被截止了。

```sh
$ python3 inspect_getcomments_module.py
# This comment appears first
# and spans 2 lines.
```

检索源文件
-----

如果 `.py` 文件是可用的模块，则可以使用 `getsource()` 和 `getsourcelines()` 检索类或方法的原始源代码

```python
# inspect_getsource_class.py
import inspect
import example
print(inspect.getsource(example.A))
```

当传入一个类时，该类的所有方法都包含在输出中。

```python
$ python3 inspect_getsource_class.py
class A(object):
    """The A class."""
    def __init__(self, name):
        self.name = name
    def get_name(self):
        "Returns the name of the instance."
        return self.name
```

要检索单个方法的源代码，请将方法的引用传递给 `getsource()`。

```python
# inspect_getsource_method.py
import inspect
import example
print(inspect.getsource(example.A.get_name))
```

在这种情况下会保留原始代码的缩进格式。

```sh
$ python3 inspect_getsource_method.py
    def get_name(self):
        "Returns the name of the instance."
        return self.name
```

使用 `getsourcelines()` 而不是 `getsource()` 来检索源文件，会将其分割成单独字符串的行。

```python
# inspect_getsourcelines_method.py
import inspect
import pprint
import example
pprint.pprint(inspect.getsourcelines(example.A.get_name))
```

`getsourcelines()` 的返回值是一个元组，其中包含一个字符串列表 (来自源文件的行)，以及源代码出现在文件中的起始行号。

```sh
$ python3 inspect_getsourcelines_method.py
(['    def get_name(self):\n',
  '        "Returns the name of the instance."\n',
  '        return self.name\n'],
 23)
```

如果源文件是不可用的， `getsource()` 和 `getsourcelines()` 引发 IOError。

方法和函数的签名
--------

除了用于内省函数或方法的文档之外，还可以获得可调用函数的参数的完整说明 (包括默认值)。`signature()` 函数返回一个实例的签名，其中包含关于函数参数的信息。

```python
# inspect_signature_function.py
import inspect
import example
sig = inspect.signature(example.module_level_function)
print('module_level_function{}'.format(sig))
print('\nParameter details:')
for name, param in sig.parameters.items():
    if param.kind == inspect.Parameter.POSITIONAL_ONLY:
        print('  {} (positional-only)'.format(name))
    elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
        if param.default != inspect.Parameter.empty:
            print('  {}={!r}'.format(name, param.default))
        else:
            print('  {}'.format(name))
    elif param.kind == inspect.Parameter.VAR_POSITIONAL:
        print('  *{}'.format(name))
    elif param.kind == inspect.Parameter.KEYWORD_ONLY:
        if param.default != inspect.Parameter.empty:
            print('  {}={!r} (keyword-only)'.format(
                name, param.default))
        else:
            print('  {} (keyword-only)'.format(name))
    elif param.kind == inspect.Parameter.VAR_KEYWORD:
        print('  **{}'.format(name))
```

函数参数可通过签名的 parameters 属性获得。parameters 是一个有序的字典，它将参数名称映射到描述参数的参数实例。在本例中，函数的第一个参数 arg1 没有默认值，而 arg2 是有的。

```sh
$ python3 inspect_signature_function.py
module_level_function(arg1, arg2='default', *args, **kwargs)
Parameter details:
  arg1
  arg2='default'
  *args
  **kwargs
```

函数的签名可以被用作修饰符或用于其他函数，用以验证参数输入并提供不同的默认值。编写一个适当通用的、可重用的验证装饰器是一项特殊的挑战, 由于函数接受参数命名和位置的组合，因为将传入的参数与其名称匹配起来可能会比较复杂。

`bind()` 和 `bind_partial()` 方法提供了处理映射的必要逻辑。它们返回一个 `BoundArguments` 实例，该实例填充与指定参数名称相关联的参数

```python
# inspect_signature_bind.py
import inspect
import example
sig = inspect.signature(example.module_level_function)
bound = sig.bind(
    'this is arg1',
    'this is arg2',
    'this is an extra positional argument',
    extra_named_arg='value',
)
print('Arguments:')
for name, value in bound.arguments.items():
    print('{} = {!r}'.format(name, value))
print('\nCalling:')
print(example.module_level_function(*bound.args, **bound.kwargs))
```

`BoundArguments` 实例含有属性 `args` 和 `kwargs`，可以用来调用函数，我们使用语法将 `tuple` 和 `dictionary` 扩展到堆栈中以用作参数。

```sh
$ python3 inspect_signature_bind.py
Arguments:
arg1 = 'this is arg1'
arg2 = 'this is arg2'
args = ('this is an extra positional argument',)
kwargs = {'extra_named_arg': 'value'}
Calling:
this is arg1this is arg1
```

如果只有一些参数可用， `bind_partial()` 仍然会创建一个 `BoundArguments` 实例。但在添加剩下的参数之前，它可能不能完全使用。

```python
# inspect_signature_bind_partial.py
import inspect
import example
sig = inspect.signature(example.module_level_function)
partial = sig.bind_partial(
    'this is arg1',
)
print('Without defaults:')
for name, value in partial.arguments.items():
    print('{} = {!r}'.format(name, value))
print('\nWith defaults:')
partial.apply_defaults()
for name, value in partial.arguments.items():
    print('{} = {!r}'.format(name, value))
```

`apply_defaults()` 将从参数的默认值中添加值。

```sh
$ python3 inspect_signature_bind_partial.py
Without defaults:
arg1 = 'this is arg1'
With defaults:
arg1 = 'this is arg1'
arg2 = 'default'
args = ()
kwargs = {}
```

类层次结构
-----

inspect 包括两种直接在类层次结构上使用的方法。第一个是 `getclasstree()`，它基于给定类和它们的基类创建树状的数据结构。返回的是列表中的每个元素，要么是带有类的 tuple，要么是它的基类，或者是另一个包含子类的元组的列表。

```python
# inspect_getclasstree.py
import inspect
import example
class C(example.B):
    pass
class D(C, example.A):
    pass
def print_class_tree(tree, indent=-1):
    if isinstance(tree, list):
        for node in tree:
            print_class_tree(node, indent + 1)
    else:
        print('  ' * indent, tree[0].__name__)
    return
if __name__ == '__main__':
    print('A, B, C, D:')
    print_class_tree(inspect.getclasstree(
        [example.A, example.B, C, D])
    )
```

这个示例的输出是 A、B、C 和 D 类的继承树。D 出现了两次，因为它从 C 和 A 继承。

```sh
$ python3 inspect_getclasstree.py
A, B, C, D:
 object
   A
     D
     B
       C
         D
```

如果调用 `getclasstree()` 时将 unique 设置为 ture 值，则输出会不同。

```python
# inspect_getclasstree_unique.py
import inspect
import example
from inspect_getclasstree import *
print_class_tree(inspect.getclasstree(
    [example.A, example.B, C, D],
    unique=True,
))
```

这一次，D 只出现在输出中一次：

```sh
$ python3 inspect_getclasstree_unique.py
 object
   A
     B
       C
         D
```

方法解析顺序
------

与类层次结构一起工作的另一个函数是 `getmro()`，它按顺序返回一个类的元组，当使用 "方法解析顺序 (MRO)" 来获取可能从基类继承的属性时会扫描该元组中的类。该元组中的每个类只出现一次。

```python
# inspect_getmro.py
import inspect
import example
class C(object):
    pass

class C_First(C, example.B):
    pass

class B_First(example.B, C):
    pass

print('B_First:')
for c in inspect.getmro(B_First):
    print('  {}'.format(c.__name__))

print()
print('C_First:')
for c in inspect.getmro(C_First):
    print('  {}'.format(c.__name__))
```

这个输出显示了 MRO 搜索的特性为 “深度优先” 。对于 `B_First`, A 也在 C 之前出现在搜索顺序中，因为 B 继承自于父类 A。

```sh
$ python3 inspect_getmro.py
B_First:
  B_First
  B
  A
  C
  object
C_First:
  C_First
  C
  B
  A
  object
```

堆栈和帧
----

除了对代码对象进行内省之外，inspect 还包括在执行程序时检查运行时环境的函数。这些函数中的大多数都与调用堆栈一起工作，并在调用帧（call frames）上操作。帧（frame)对象保存当前的执行上下文，包括对正在运行的代码的引用、正在执行的操作以及本地和全局变量的值。通常情况下，在抛出异常时， 会使用这些信息来构建回溯 (tracebacks)。它还可以用于日志记录或调试程序，因为可以对堆栈帧(stack frames) 进行查询，以发现传入函数的参数值。

对于当前函数, `currentframe()` 返回堆栈顶部的帧。

```python
# inspect_currentframe.py
import inspect
import pprint

def recurse(limit, keyword='default', *, kwonly='must be named'):
    local_variable = '.' * limit
    keyword = 'changed value of argument'
    frame = inspect.currentframe()
    print('line {} of {}'.format(frame.f_lineno,
                                 frame.f_code.co_filename))
    print('locals:')
    pprint.pprint(frame.f_locals)
    print()
    if limit <= 0:
        return
    recurse(limit - 1)
    return local_variable

if __name__ == '__main__':
    recurse(2)
```

传递给 `recurse()` 的参数值都包含在帧的局部变量字典中。

```sh
$ python3 inspect_currentframe.py
line 14 of inspect_currentframe.py
locals:
{'frame': <frame object at 0x10458d408>,
 'keyword': 'changed value of argument',
 'kwonly': 'must be named',
 'limit': 2,
 'local_variable': '..'}
line 14 of inspect_currentframe.py
locals:
{'frame': <frame object at 0x101b1ba18>,
 'keyword': 'changed value of argument',
 'kwonly': 'must be named',
 'limit': 1,
 'local_variable': '.'}
line 14 of inspect_currentframe.py
locals:
{'frame': <frame object at 0x101b2cdc8>,
 'keyword': 'changed value of argument',
 'kwonly': 'must be named',
 'limit': 0,
 'local_variable': ''}
```

使用 `stack()` 可以访问从当前帧到第一个调用者的所有堆栈帧。这个示例类似于前面所示示例，但是它等待直到递归的末尾来打印堆栈信息。

```python
# inspect_stack.py
import inspect
import pprint

def show_stack():
    for level in inspect.stack():
        print('{}[{}]\n  -> {}'.format(
            level.frame.f_code.co_filename,
            level.lineno,
            level.code_context[level.index].strip(),
        ))
        pprint.pprint(level.frame.f_locals)
        print()

def recurse(limit):
    local_variable = '.' * limit
    if limit <= 0:
        show_stack()
        return
    recurse(limit - 1)
    return local_variable

if __name__ == '__main__':
    recurse(2)
```

输出的最后一部分表示主程序，它在 `recurse()` 函数之外。

```sh
$ python3 inspect_stack.py
inspect_stack.py[11]
  -> for level in inspect.stack():
{'level': FrameInfo(frame=<frame object at 0x1045823f8>,
filename='inspect_stack.py', lineno=11, function='show_stack',
code_context=['    for level in inspect.stack():\n'], index=0)}
inspect_stack.py[24]
  -> show_stack()
{'limit': 0, 'local_variable': ''}
inspect_stack.py[26]
  -> recurse(limit - 1)
{'limit': 1, 'local_variable': '.'}
inspect_stack.py[26]
  -> recurse(limit - 1)
{'limit': 2, 'local_variable': '..'}
inspect_stack.py[31]
  -> recurse(2)
{'__annotations__': {},
 '__builtins__': <module 'builtins' (built-in)>,
 '__cached__': None,
 '__doc__': 'Inspecting the call stack.\n',
 '__file__': 'inspect_stack.py',
 '__loader__': <_frozen_importlib_external.SourceFileLoader
object at 0x101f9c080>,
 '__name__': '__main__',
 '__package__': None,
 '__spec__': None,
 'inspect': <module 'inspect' from
'.../lib/python3.6/inspect.py'>,
 'pprint': <module 'pprint' from '.../lib/python3.6/pprint.py'>,
 'recurse': <function recurse at 0x1045b9f28>,
 'show_stack': <function show_stack at 0x101f21e18>}

```

在不同的上下文中，还有其他用于构建帧列表的函数，例如处理异常时的上下文。可以查看 `trace()`、 `getouterframe()` 和 `getinnerframe()` 的文档，了解更多细节。

命令行接口
-----

inspect 模块还包括一个命令行接口，用于获取对象的详细信息，而不必在单独的 Python 程序中编写调用代码。输入是模块名和模块中的可选对象。默认输出是输入对象的源代码。使用 `--details` 参数会导致输出是打印的元数据而不是源文件。

```sh
$ python3 -m inspect -d example
Target: example
Origin: .../example.py
Cached: .../__pycache__/example.cpython-36.pyc
Loader: <_frozen_importlib_external.SourceFileLoader object at 0
x103e16fd0>
$ python3 -m inspect -d example:A
Target: example:A
Origin: .../example.py
Cached: .../__pycache__/example.cpython-36.pyc
Line: 16
$ python3 -m inspect example:A.get_name
    def get_name(self):
        "Returns the name of the instance."
        return self.name
```

相关链接
----

*   原稿地址 (https://pymotw.com/3/inspect/index.html)
    
*   inspect 的标准库文档 (https://docs.python.org/3.6/library/inspect.html)
    
*   Python 2 到 3 移植 inspect 的笔记 (https://pymotw.com/3/porting_notes.html#porting-inspect)
    
*   Python 2.3 方法解析顺序 (http://json.org/) Python 2.3 和以后的版本使用的 C3 方法解析顺序的文档。
    
*   pyclbr(https://pymotw.com/3/pyclbr/index.html#module-pyclbr) pyclbr 模块可以通过解析模块而不导入它来访问一些相同的信息。
    
*   PEP 362(https://www.python.org/dev/peps/pep-0362) 函数签名对象
    
*   代码地址 (https://gitee.com/max184/python-library/blob/master/languages_tools/inspect.ipynb)
    
