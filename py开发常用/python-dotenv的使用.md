## 简介

- 项目地址：https://github.com/theskumar/python-dotenv

首先看一下github上项目的介绍：

　　Reads the key,value pair from .env and adds them to environment variable. 

　　大概意思就是在我们做项目时，我们可以把所有用到的环境变量写到.env文件里，然后以k，v的方式读取作为环境变量。

**扩展阅读**：[12-factors](https://12factor.net/zh_cn/)

## 用法

最简单和最常见的用法是在应用程序启动时调用`load_dotenv`，从当前目录或其父目录中的`.env`文件或指定的路径加载环境变量，然后你可以调用`os.getenv`提供的与环境相关的方法。

### `.env` 文件内容写法

`.env` 文件内容差不多是这样的：

```ini
# a comment that will be ignored.
REDIS_ADDRESS=localhost:6379
MEANING_OF_LIFE=42
MULTILINE_VAR="hello\nworld"
```

你可以使用单词`export`作为每行的前缀，这将会使`python-dotenv` 忽略该变量，但是你可以使用 `source` 命令运行该文件。

`python-dotenv` 可以用来修改 `POSIX`系统的环境变量.

变量的值是下面列表中定义的第一个值:

- 系统环境变量
- `.env` 文件中定义的值
- 默认值，如果有的话
- 空字符串

确保引用其他变量时用大括号`{}`包围，就像`${HOME}`，因为像`$HOME`这样的字符串不会被认为是变量的引用。

```ini
CONFIG_PATH=${HOME}/.config/foo
DOMAIN=example.org
EMAIL=admin@${DOMAIN}
DEBUG=${DEBUG:-false}
```

### 项目中使用

#### 安装

>pip install -U python-dotenv

#### 基本用法

确保你的项目目录下 有 `.env` 文件

```sh
.
├── .env
└── settings.py
```

然后你可以在`settings.py`中添加以下代码：

```python
# settings.py
from dotenv import load_dotenv, find_dotenv
from pathlib import Path  # Python 3.6+ only

# 一、自动搜索 .env 文件
load_dotenv(verbose=True)


# 二、与上面方式等价
load_dotenv(find_dotenv(), verbose=True)

# 三、或者指定 .env 文件位置
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)
```

通过`load_dotenv` ，你就可以访问像访问系统环境变量一样使用`.env`文件中的变量了，比如通过 `os.genenv(key, default=None)`

```python
# settings.py
import os
SECRET_KEY = os.getenv("EMAIL")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
```

#### 参数

- `dotenv_path`: 指定`.env`文件路径，当然如果不传该参数的话（默认为`None`）也会自定调用`dotenv.find_dotenv()`去查找文件位置的，**但是你的文件名如果不是`.env`那就必须传递该参数了**

- `override`： 当`.env` 文件中有变量与系统中原来的环境变量有冲突时，按照上面的取值顺序，默认使用系统变量，如果要用`.env`中的变量覆盖系统变量，可以给`load_dotenv()` 传递参数`override=True`。**此时只是临时使用了`.env` 中的变量值**

- `encoding`: `load_dotenv()` 也可以传递`encoding` 参数指定文件的编码方式。

#### 从流对象加载

从可读的流对象中加载，记得把读指针调到要开始读取的位置。

```python
>>> from io import StringIO     # Python2: from StringIO import StringIO
>>> from dotenv import dotenv_values
>>> filelike = StringIO('SPAM=EGGS\n')
>>> filelike.seek(0)
>>> parsed = dotenv_values(stream=filelike)
>>> parsed['SPAM']
'EGGS'
```

**注意**：此时返回值是个字典

### Django

如果你在Django中使用，请将以上代码添加到 `wsgi.py` 或者 `manage.py`.

### IPython 支持

1. 加载扩展
```sh
%load_ext dotenv
```
2. 加载 env文件
```sh
%dotenv
```
或者指定一个env文件
```sh
%dotenv relative/or/absolute/path/to/.env
```
3. 其他参数

  - -o：即override 覆盖原有变量
  ```sh
  %dotenv -o
  ```
  - -v：输出提示信息
  ```sh
  %dotenv -v
  ```

### [配置远程服务器](https://github.com/theskumar/python-dotenv#setting-config-on-remote-servers)

与 [Fabric](http://www.fabfile.org) 配合使用
