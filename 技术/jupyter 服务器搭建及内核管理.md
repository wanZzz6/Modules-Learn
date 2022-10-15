# 远程访问服务搭建

## 环境准备
```bash
sudo apt-get install update
sudo apt-get install python3 python-pip
sudo pip3 install jupyter
```


## 修改pip源

Linux编辑 ~/.pip/pip.conf ，在最上方加入如下内容：
```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

## 虚拟环境（可选）

```bash
sudo pip install -U virtualenv
virtualenv venv -p python3
source venv/bin/activate
```

## 创建登陆密码

```python
from notebook.auth import passwd
print(passwd("jupyter"))
```
Out[2]: 'sha1:*******************'


## 创建ssl证书（https连接需要，http可跳过）

>openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem

## 编辑配置文件

**jupyter notebook --generate-config**

root用户加上--allow-root

在当前用户根目录下生成.**.jupyter/jupyter_notebook_config.py**文件
修改以下内容：
```python
c.NotebookApp.notebook_dir = '/home/demo'  # 默认启动目录
c.NotebookApp.allow_remote_access = True  # jupyter 4.5版本以上需要配
c.NotebookApp.allow_root = True     #允许root用户运行
c.NotebookApp.ip = '*'   # 允许远程访问（备用参数0.0.0.0）
c.NotebookApp.notebook_dir = r'/root/jupyter'  # 启动目录
c.NotebookApp.open_browser = False    # 默认不启动浏览器
c.NotebookApp.password = 'sha1:xxxxxxxxxx' # 上面生成的密钥
c.NotebookApp.certfile = u'c:/jpyb/mycert.pem'  # 指定文件路径
c.NotebookApp.keyfile = u'c:/jpyb/mykey.key'  # 指定文件路径
c.IPKernelApp.pylab = 'inline'    # 所有matplotlib的图像都通过iline的方式显示
c.NotebookApp.port = 8888     # 运行的端口

```

 - 查看端口是否占用脚本
>netstat -anp|grep 8888

## 启动jupyter

```bash
nohup jupyter notebook &
```
注：可以写入 sh 脚本，然后设置开机自启

## 设置阿里云安全组（非阿里云用户无需这一步）
在`控制台`-`云服务器ESC`-`实例` 选择自己的主机点击`本实例安全组`-`安全组列表`-`配置规则`-`入方向`-`手动添加`添加如下图所示配置
注：其中端口号填写自己设置的端口
![](https://img-blog.csdnimg.cn/2020073110064542.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dhbnpoZW5nXzk2,size_16,color_FFFFFF,t_70#pic_center)


## ✨更换Logo

图片地址：

>/usr/local/lib/python3.5/dist-packages/notebook/static/base/images/logo.png

## 👍安装扩展插件

[github地址](https://github.com/ipython-contrib/jupyter_contrib_nbextensions)

>pip3 install jupyter_contrib_nbextensions

>pip3 install -U six

>jupyter contrib nbextension install --user

# 打开Markdown为ipynb

## 安装

直接安装jupytext即可

```sh
pip install jupytext

# ipynb 转 md 命令
jupytext --to markdown *.ipynb
```

## 其他方案

插件主页：https://github.com/aaren/notedown

`notedown` 插件可以使 ipynb 和 .md  文件进行互相转换，还可以配置在浏览器界面直接编辑和预览 markdown文件，还能将 md文件中的python代码块渲染成ipynb中可编辑可执行的 cell单元，总之很强大。

```
pip install notedown
```

或者安装开发版

```sh
pip install https://github.com/aaren/notedown/tarball/master
```

修改配置文件，（配置文件位置见上文[#1.6]部分）

```py
c.NotebookApp.contents_manager_class = 'notedown.NotedownContentsManager'
```

### 用法

#### md 转 ipynb

```sh
notedown input.md > output.ipynb
```

####  ipynb 转 md

**清空所有输出内容**

```sh
notedown input.ipynb --to markdown --strip > output.md
```

**保留所有输出，渲染成原始的json**

```sh
notedown input.ipynb --to markdown > output_with_outputs.md
```

**保留所有输出，渲染成原div 元素（不好使）**

```sh
notedown input.ipynb --to markdown  --render > output_with_outputs.md 
```

# 📢内核管理

## 常用操作

### 查看已安装内核的信息

```sh
jupyter kernelspec list
```

### 卸载

卸载指定名称的内核，比如： java

```sh
jupyter kernelspec remove java
```

### 删除

```sh
jupyter kernelspec uninstall java   #java  
```

## 安装多版本python内核

安装多个py内核后就能像虚拟环境一样运行不同版本的代码了，在jupyter 新建文件时可以选择不同的内核版本，也可以在上方菜单栏点击<kbd>Kernel</kbd> - > <kbd>Change kernel</kbd> 切换当前内核。

当前场景：以在python3 中安装了jupyter，需要安装 python2 的内核

1. 在python2（虚拟环境也可）下安装 ipykernel 
```sh
python2 -m pip install ipykernel
```

2. 安装内核到jupyter 中
```sh
python2 -m ipykernel install --user --name py2 
# --user安装到当前用户，可查看帮助选择不同安装位置，也可不加该参数，安装到默认位置。--name为内核命名为py2
```
3. 查看
```sh
jupyter kernelspec list
```

4. 重启jupyter

## 🚀支持C++内核( 需要minicanda或者新建虚拟环境）


### 利用windows子系统（WSL）或者Linux中

（利用Win10子系统可视化开发环境搭建可参考鄙人文章）

1. 从windows应用商店里安装Ubuntu子系统

2. 安装 Miniconda

这里使用 xeus-cling，安装说明指出需要 Miniconda，因为 Anaconda 会有冲突，因此我使用 Miniconda，已经装过 Anaconda 的可以尝试一下用 Anaconda 安装。

在这里找到需要的 Miniconda 版本，然后复制链接：
https://docs.conda.io/en/latest/miniconda.html

通过命令行或者开始菜单打开上一步中安装的 Ubuntu，输入下列命令。
```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
出现 License 之后按 q，输入 yes 允许许可，然后 Enter，如果要改路径就自行修改。然后输入 yes 完成初始化

输入`which python` 发现python路径与Windows里的python路径是隔离的，并不冲突。终于发现子系统的好处了😂。

<https://github.com/QuantStack/xeus-cling>

安装：

>conda install xeus-cling -c conda-forge

安装完之后再次打开 Jupyter notebook，可以在 New 按钮下看到多了 C++11，C++14 和 C++17，新建一个 C++14 notebook，输入一些 C++ 代码，Shift + Enter 可以得到运行结果，没有报错就大功告成了！

## ☕支持Java

![](assets/display-img.png)

### 环境准备：

1. Java JDK >= 9，注意不是jre

 i. 检查java环境
```
> java -version
java version "9"
Java(TM) SE Runtime Environment (build 9+181)
Java HotSpot(TM) 64-Bit Server VM (build 9+181, mixed mode)
```

ii. 接下来，确保Java位于jdk的安装位置，而不仅仅是jre, 使用`java --list-modules` .输出列表应当包含`jdk.jshell`.

  - On *nix `java --list-modules | grep "jdk.jshell"`
  
  - 在 windows上: `java --list-modules | findstr "jdk.jshell"`

应当输出`jdk.jshell@`

如果没有，请输入`java -verbose`检查第一行或者最后一行的java路径信息，确认java在JDK路径下，而不是JRE中。

2. 不限类似jupyter的环境
  - Jupyter
  - JupyterLab
  - nteract

### 安装

1. 下载地址：<https://github.com/SpencerPark/IJava/releases>

可选择下载压缩包：ijava-$version.zip

2. 解压，看到文件install.py 和 一个java文件夹

查看安装帮助：

```sh
python3 install.py -h
```

安装：

```sh
python3 install.py --sys-prefix
```

其他安装选项：`--default`, `--user`, `--sys-prefix`, `--prefix`, `--path`, or `--legacy`,不同选项对应不同安装位置。

查看已经安装的内核，应当包含java，如图：

```
jupyter kernelspec list
```

![untitled.png](assets/untitled.png)

### 使用

导包：
直接导入
```
%jars import org.slf4j.Logger;
%jars import org.slf4j.LoggerFactory;
```
maven 导入
```
%%loadFromPOM
<dependency>
  <groupId>ch.qos.logback</groupId>
  <artifactId>logback-core</artifactId>
  <version>1.2.3</version>
</dependency>
```
>import ch.qos.logback.core.Layout;

或者
```
%maven org.slf4j:slf4j-api:1.7.25 ch.qos.logback:logback-core:1.2.3 ch.qos.logback:logback-classic:1.2.3

import org.slf4j.logger;
```
## 支持javascript

项目地址： https://github.com/n-riesco/ijavascript

- 依赖：Node.js、npm
  
    > sudo apt-get install nodejs npm

### 安装

```sh
npm install -g ijavascript
ijsinstall
```
## 支持Node JS - jupyter-nodejs

项目地址：https://github.com/notablemind/jupyter-nodejs

使用效果：[Example](http://nbviewer.jupyter.org/gist/jaredly/404a36306fdee6a1737a)

### 安装依赖

- IPython 3.x
- pkg-config

    >sudo apt install pkg-config
    
- 安装Node
    >sudo apt-get install nodejs  
    >sudo apt-get install npm
    
- 检查node-gyp 是否安装

    >node-gyp list
    
    未安装的请执行：`npm install -g node-gyp`
    
- ubuntu下安装ZeroMQ：

    >apt-get install libzmq3-dev
    
    其他系统安装方式： https://zeromq.org/download/

### 安装

```sh
git clone https://github.com/notablemind/jupyter-nodejs.git --depth=1
cd jupyter-nodejs
mkdir -p ~/.ipython/kernels/nodejs/
npm install && node install.js
npm run build
npm run build-ext
```

### 尝试

```sh
jupyter console --kernel nodejs
```
## 👍其他内核支持

<https://github.com/jupyter/jupyter/wiki/Jupyter-kernels>
