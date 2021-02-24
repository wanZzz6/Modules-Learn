---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

### 获取签名: Signature类

```python
import inspect

# 测试方法
def func1(a, b: int = 0, *c, d, e=1, **f):
    pass

# 测试方法
def func2(a, b: int, c=0, *, d):
    pass

# 测试方法 python>=3，8
# def func3(a, /, b: int, c=0, *, d):
#     pass


class Foo:
    """测试类"""

    def __init__(self, name: str, age: int):
        """
        初始化
        :param name:
        :param age:
        """
        self.name = name
        self.age = age

    def run(self):
        """运行程序"""
        print('run....')
        print(self.name, self.age)


# 函数签名
sign = inspect.signature(func1)
# 类 构造方法签名
# sign = inspect.signature(Foo)


print(type(sign))
print(repr(sign))
print(str(sign))
```

### 获取参数字典

```python
import re
a =  """
        初始化
        :param name:
        :param age:a
        """
PARAM_PATTERN = re.compile('[:@]param (.*?):(.*)')
PARAM_PATTERN.findall(a)
```

```python
param_dict = sign.parameters

print(type(param_dict))
print(repr(param_dict))
print(str(param_dict))
```

```python
# 顺序字典
param_dict.keys()
```

```python
# 顺序字典
param_dict.values()
```

### 参数详情：Parameter类

```python
param_dict['a']
```

```python
def func1(a, b: int = 0, *c, d, e=1, **f):
    print(a, b, c, d, e, f)

func1(1, d=1, )
```

```python
# 打印每个参数的详情: 参数名，类型， 默认值，类型注释
attributes = ['name', 'kind', 'default', 'annotation']
for param in param_dict.values():
    for attr in attributes:
        value = getattr(param, attr)
        print(attr.ljust(10).title(), value)
    print('=' * 50)
```

### 返回值类型

```python
sign.return_annotation
```
