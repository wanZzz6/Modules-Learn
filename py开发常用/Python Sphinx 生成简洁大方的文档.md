>  原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rCSZAxIhEYRXBIrRfV2haw)

*   安装 sphinx 库
    
*   简单示例（ Spninx 使用 ）
    
*   步骤一：Sphinx 创建出基础配置
    
*   步骤二：配置项目入口 index.rst
    
*   步骤三：生成项目文档
    
*   步骤四：展示出来
    
*   小小总结
    

Sphinx 简介
=========

Sphinx 是一种工具，是一个有趣 python 的第三方库，它允许程序员以纯文本格式编写文档，Spninx 可以轻松生成各种格式的输出，比如 html，pfd，等等。纯文本的文档方便使用版本管理工具进行跟踪。纯文本文档对不同系统之间的协作者也非常有用，纯文本是当前可以采用的最便捷的格式之一，不然 markdown 格式咋那么火呢，不是没有道理的。

程序员最讨厌的两件事：

1.  自己写代码文档
    
2.  别人的代码没文档
    

正经写文档确实麻烦，为啥麻烦呢？因为很长时间程序员写代码和写文档是完全独立分开的，这说起来就是两份工作量，最不能忍受的还是变化带来的负担，代码是可能经常变动的，代码变动之后，含义自然就可能不一样，或者新加了了功能，文档如果还要手动跟进的话，最喜欢偷懒的程序员自然就不愿了。

我们回归本源，程序员这讨厌的两件事说明了什么？

心有余而力不足。心里还是想写文档的，就是太累了。

所以，对此我们有解决方案吗？

**有，最核心的就是代码即文档，根据代码来生成文档**。

这个 golang 在语言工具包里就整合了 `go doc` 这样的工具，能够根据代码和代码里的注释生成一个漂亮的文档。

Python 也有自己的方案，解决文档就是 Sphinx ，Python3.x 官方的文档就是用这个生成的。所以，如果你的也是 Python 项目，那么可以生成一个和官方文档同款的文档项目，非常实用和拉风。

Sphinx 怎么用？
===========

先给大家看一张我本地生成文档项目的图，提提兴趣：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640)  


使用这个小工具，你就不用专门写文档项目了，只需要写好代码就好，代码即文档。

## 安装 sphinx 库

安装非常方便，就是一个简单的 Python 三方库，用 pip 安装就行了：

```
pip install Sphinx
```

安装完之后呢，应该有四个二进制文件：

*   `sphinx-apidoc`
    
*   `sphinx-autogen`
    
*   `sphinx-build`
    
*   `sphinx-quickstart`

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224222822.png)  


如果呢，你没有找到这四个二进制文件，那么可以直接去找对应的 python 文件：

*   `build.py`
    
*   `make_mode.py`
    
*   `quickstart.py`

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224222842.png)  

## 简单示例（ Spninx 使用 ）

搞了一个最简单的示例，项目根目录是 `~/qiya/python-tools/` ，下面都是以此目录为基础，下面的是我自己创建的目录，搞了几个简单的目录，`common`，`misc` 是项目的代码目录，`docs` 是我预定的专门放文档的目录。

```
root@ubuntu:~/qiya/python-tools# tree 
.
├── common
│   ├── demo.py
│   └── __init__.py
├── docs
│   └── __init__.py
├── misc
│   └── __init__.py
│   └── tools.py
└── README.md
```

我先准备好演示用的代码项目：

demo 类文件：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224222901.png)

tools 函数文件：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224222915.png)

### 步骤一：Sphinx 创建出基础配置

#### 执行 `sphinx-quickstart`

使用`sphinx-quickstart` 可以直接做初始化，能够完成最简单的配置，生成一些最基础的配置文件。

```
$ cd docs/
$ sphinx-quickstart
```

执行完这个命令，需要配置一些操作，信息如下：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224222937.png)  

`sphinx-quickstart` 命令执行完成之后，下面全都是自动生成的文件：

```sh
root@ubuntu:~/qiya/python-tools/docs# tree 
.
├── build
├── __init__.py
├── make.bat
├── Makefile
└── source
    ├── conf.py
    ├── index.rst
    ├── _static
    └── _templates
```

**特意说下，最重要的就是两个文件**：

1.  `source/conf.py`  ：这个是 Sphinx 的配置，包括主题的设置，文档的生成形式，都可以在这里配置；
2.  `source/index.rst` ：这个是项目的主页文件，rst 语法，类似于 markdown，都是一种标记类文档语言，具体的语法可以看这里: [reStructuredText Primer](http://www.sphinx-doc.org/en/stable/rest.html)。

`sphinx-quickstart` 执行完之后呢，基础的东西是给你准备好了，接下来就是要根据自身的情况来配置。首先要看的就是 `conf.py` 这个配置文件，我们的目录是：

```
root@ubuntu:~/qiya/python-tools# tree 
.
├── common
│   ├── demo.py
│   └── __init__.py
├── docs
│   ├── build
│   ├── __init__.py
│   ├── make.bat
│   ├── Makefile
│   └── source
│       ├── conf.py
│       ├── index.rst
│       ├── _static
│       └── _templates
├── misc
│   ├── __init__.py
│   └── tools.py
└── README.md
```

#### 配置 conf.py 文件

所以呢，我们要让 conf.py 找到代码，那么就要添加好路径，在最开头修改，如下：

```
import sys
from os.path import abspath, dirname
# 为什么是上三层目录呢？conf.py 这个文件和根目录不就隔着三层目录嘛
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
```

这样 Sphinx 就能找到你想要自动生成文档的代码了。下一步，添加 extensions ，说明咱们的文档可以自动生成：

```
# 指明用 autodoc 的形式生成
extensions = [
        'sphinx.ext.autodoc'
]
# 指明用 sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
```

`sphinx_rtd_theme`  这个主题不是默认的，这个是一个比较好看的主题，这个可以直接用 pip 安装即可：

```
$ pip install sphinx_rtd_theme
```

`conf.py` 修改的样子如下：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224223001.png)  

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224223017.png)

### 步骤二：配置项目入口 index.rst

这个 index.rst 文件是入口，项目文档怎么生成，生成什么格式，就是这个文件里配置的（这里的配置是要和 conf 对应着来）。

```rst
************
Welcome to demo's API Documentation
************

Introduction
============
This is the introduction of demo。

common 公共库
=================

.. automodule:: common.demo
   :members:
   
misc 库
=================
.. automodule:: misc.tools
   :members:

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

- toctree生成了一个节点，此节点必须。

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:
```

- automodule即自动生成模块，后面跟着py文件的文件名。（这里的 `common.demo` 和 `misc.tools` 模块对应了 py 文件。这个怎么才能找到这两个模块，这个就跟你配置 conf.py 里面的 path 配置有关。）

```rst
.. automodule:: common.demo
   :members:
```

解释下，

### 步骤三：生成项目文档

执行命令：

```sh
$ cd docs/
$ sphinx-build source/ build/
```

执行这个命令，就会自动去搜索代码，生成文档项目，默认生成的是 html 的文件。

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224223036.png)  

这里顺带提一下，如果你想生成其他格式的项目文档，比如纯文本格式，那么可以执行：

```
$ cd docs/
$ sphinx-build -b text source/ build/
```

纯文本格式如下：

### 步骤四：展示出来

怎么看到效果呢？演示的话，开一个静态服务器就行，给大家演示一个 python 3 一键起一个静态服务器的命令：

```
$ python3 -m http.server 9000
```

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224223056.png)  

显示效果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201224223116.png)

  

# 优化页面层次

在项目较大时，我们的py文件会不止一个，我们可以将py文件和html文档一一对应，这样就可以分散式管理文档。
实际上在rst文档中是可以以链接的形式引用其他rst文档的，就像vue组件一样，也就是说我们可以自由的对文档结构进行组织使其更易读

我们进入到sphinx/source中，创建common文件夹并添加文件demo.rst，写入以下内容：

```rst
common 公共库
=================

.. automodule:: common.demo
   :members:

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

下面我们在index.rst里修改，删除原来的链接，并改为demo.rst 的文件地址

```rst
Welcome to demo's API Documentation
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

    common/demo
    misc/tools

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

现在重新生成html，就会看到页面显示上的变化了。

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201225095545.png)

如果还有新的new.py文件加入的话，新建一个XXX.rst文件，添加automodule指令，并在index.rst文件内添加XXX即可。



# 小小总结

希望大家写好代码，名字易读，注释规范，这样就自然有好的文档了。还有就是，这个 Sphinx 工具其实不仅适用于 Python，其他语言也能适用，大家可以探索。**关键思考：代码即文档**。
