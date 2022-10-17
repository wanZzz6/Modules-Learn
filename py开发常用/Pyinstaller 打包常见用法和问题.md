---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region -->
[toc]

# 安装

```sh
pip install --upgrade pyinstaller
```

安装最新开发版

```sh
pip install https://github.com/pyinstaller/pyinstaller/tarball/develop
```

验证安装

```sh
pyinstaller -v
```

结果应当输出类似与 3.x 或者 3.n.dev0-xxxxxx 的开发版本号

## 💊温馨提示

1. **在虚拟环境下打包**，只安装程序需要的依赖包，避免打包后文件过大
2. 在打包成单个 exe 文件之前，请先尝试打包成**一个文件夹**测试是否正常运行
3. 打包成单个文件启动较慢，原因是程序需要按原目录结构解压到临时目录下，在用户目录下生成临时文件，结束后会自动删除
4. 建议阅读本文全文，以免遗漏

# 用法

## 基本用法

### 1. 直接打包

将生成一个文件夹，里面包含可执行程序及其依赖，启动较单文件快

```sh
pyinstaller  myscript.py
```

### 2. 打包成单文件

```sh
pyinstaller -F myscript.py
```

### 3. 去掉控制台窗口，黑窗口

不显示控制台窗口(类似 cmd 的黑框框), 如果你写的是带 UI 的程序, 此选项基本必选.如果入口程序是 pyw 文件, 此选项默认生效.

```sh
pyinstaller -w myscript.py
```

### 4. 添加图标

```sh
pyinstaller -i icon.ico myscript.py
```

## 高级用法

打包一遍后，会生成一个`xxx.spec`文件, 是一个打包参数配置文件，该文件内容由上一次打包命令决定，可以通过添加打包参数重新生成，也可以可以直接修改其内容供下次使用。

😘 注1： spec 文件生成方法

将 `pyinstaller` 命令换成 `pyi-makespec`

例：

```sh
pyi-makespec -F filename
```

💊 注2：当你修改过 spec 文件并且想将其应用，你需要以下命令

```sh
pyinstaller ***.spec
```

### 1. 解决模块缺失

**使用场景：**  
有些模块在代码里是动态加载的，比如通过 `__import__(xxx)` 或者 `importlib` 模块加载的，在打包过程中是无法检测出来的，但是不打包进去这些模块，程序会抛出 `ModuleNotFoundError: No module named 'xxx'` 异常。这时候根据具体缺失的模块你有三种方法解决。

- 一是，在代码里显式地 import 这些模块，尽管你不去使用（pycharm 里显示灰色）
- 二是，在打包时添加打包参数，可以通过命令行参数，也可通过改 xxx.spec 配置文件，详见下文
- 三，以上两种方法解决可常见的模块缺失，但有些包就是不管用，该缺失还是缺失，这就需要一个额外的 hook 文件来解决，详见下文。

**测试文件**

我们写一个测试文件先：
里面就一行代码

- test.py

```py
print(__import__('flask', fromlist=['']).Flask)
```

这是 `from flask import Flask` 的动态导入写法，正常会输出一个类变量的描述字符串

```sh
<class 'flask.app.Flask'>
```

然后执行 `pyinstaller test.py`，你会发现5秒钟就打完包了😅😅，到打包好的dist/test 下运行可执行文件，就会发现报错：

```sh
Traceback (most recent call last):
  File "test.py", line 1, in <module>
ModuleNotFoundError: No module named 'flask'
[84851] Failed to execute script 'test' due to unhandled exception!
```

下面就解决这一类常见的打包模块缺失问题

#### 方法一：简单暴力，缺失补啥


提示缺失哪个模块就手动导入  
在程序入口处，或者根据个人喜好单独建个文件也好，将 `import xxx` 写进去，比如我上面的 test.py缺失 flask 模块，就 写 `import flask`。

#### 方法二：隐式导入

又分两种使用方式

1. 命令行模式：添加隐式导入参数

> --hidden-import MODULENAME1

例如：

```sh
pyinstaller test.py --hidden-import flask
```


如果缺失多个模块，可以多次使用


例如缺失 docx、pillow 两个模块：

```sh
--hidden-import docx --hidden-import Pillow
```

然后你可以将该打包命令成 脚本文件 比如 `build.sh` 或者 `build.bat`

2. 修改 spec 模式：

打开你上次执行完pyinstaller后生成的 xxx.spec 文件(我的test.spec)，修改以下字段，在列表里补充上缺失的模块

例：

```ini
hiddenimports=['flask'],
```

例：

```ini
hiddenimports=['docx', 'Pillow']
```

然后将可以将该spec 文件保存，提交到 git 😀

====================================

以上两种方法只能解决一小部分情况下包缺失的问题，还有问题，就得用第三种方法了。

假设有这种多层路径的模块动态导入（通常是你安装的第三方包里面的乱七八糟的运行时动态导入）

比如有个包叫 `paho-mqtt`（mqtt协议客户端），我在使用的时候需要，这样导入模块

```python
# 注意
# client 是个模块，模块就是单个 py 文件
# 而 Client 是个 class 类
from paho.mqtt.client import Client
```

改成动态导入语句就是

```python
Client = __import__('paho.mqtt.client', fromlist=['']).Client
```

打包后会提示如下信息

```sh
ModuleNotFoundError: No module named 'paho'
```

那你写个 `import paho` 能解决问题吗？写 `import paho.mqtt` 也不行啊，然后你写完发现还是不行，也许根据错误提示你最终会写上 `import paho.mqtt.client`，问题才得以解决，这就比较蛋疼了，况且如果缺失多个包呢？

#### 方法三：hook文件（待完善）

这时我们需要写个 hook 文件，将缺失的整个包全部包含进去就好了。

**步骤：**

在你执行打包命令的目录下新建一个py文件，比如 `hook-ctypes.macholib.py`

写入以下内容

```python
from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('flask') + copy_metadata('paho_mqtt') 
# 如果缺失多个就用加号继续追加
# 名称是你pip安装时的名称
```

然后执行命令时再加个 `--additional-hooks-dir`参数

```sh
pyinstaller test.py --additional-hooks-dir=.
```

应该就没问题了


如果还是不行。。。。欢迎评论区提问，我再好好研究研究

### 2. 打包静态文件

当你程序中需要读取一些静态文件比如 `setting.json` ,就需要你将他们一起打包进去，否则 pyinstaller 也会忽略他们。

#### 命令行模式

可以多次使用

```sh
--add-data <SRC;DEST or SRC:DEST>
```

👉 注意：格式为 一个原文件名和目**标文件夹**名！，中间用一个分号或者冒号分割。

👉 注意：路径中需要用 双反斜杠！！

例：  
将原路径（绝对路径或者相对路径都可）setting 目录下的 aaa.json 文件打包到目标的 setting 文件夹下

```sh
--add-data ".\\setting\\aaa.json;.\\setting"
```

例：  
将原路径（绝对路径或者相对路径都可）config 目录下的所有文件 文件打包到目标的 config 文件夹下

```sh
--add-data ".\\config\\*;.\\config"
```

#### 修改 spec 模式

```py
datas=[('.\\config\\*', '.\\config'),
('.\\setting\\aaa.json', '\\setting') ],
```

#### 💊 注意事项

将文件打包成单文件时（但文件夹除外），你在程序中访问这些静态文件时**切勿使用相对路径**，因为单文件在运行时先解压所有需要的文件到 用户临时文件夹下（ /temp 目录），并不在你当前运行路径下寻找这些静态文件。你需要将程序里访问这些静态文件的路径改为绝对路径，才能在其解压出的临时路径下找到他们：

```py
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)

#接上例，打包进去的 aaa.json，加到了这个绝对目录。
aaa = os.path.join(basedir, 'setting', 'aaa.json')
```

👉 效果参考：

https://blog.csdn.net/Iv_zzy/article/details/107407167

## 3. 打包二进制依赖文件

将程序中依赖的 dll 或者 so 文件 一起打包进去。（编译好的 python 可调用模块或者 ctypes 加载的 dll 文件都可）

> --add-binary <SRC;DEST or SRC:DEST>

可以多次使用；参数格式参考上一小标题（打包静态文件）

例：

```sh
--add-binary D:\\test\\pack\\HCNetSDK.dll;.\\lib
```

### 4. 加密字节码

详细介绍：https://pyinstaller.readthedocs.io/en/stable/usage.html#encrypting-python-bytecode

使用 --key 参数 指定一个长度为 16 的字符串，来加密 python 字节码文件，
你需要先执行以下命令

```sh
pip install pyinstaller[encryption]
```

然后

```sh
pyinstaller.exe --key=xxxx -F hellow.py
```

（🙏 过程可能不太顺利，过程慢长，打包完文件也较大）
<!-- #endregion -->
