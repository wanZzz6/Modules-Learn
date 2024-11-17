`Linux`在程序员中属于高逼格的存在，当然安装了图形界面的程序员要减分，毕竟你需要用鼠标了！程序员的桌面不能比谁的更酷更炫，要比谁的屏幕多，桌面颜色少！

Windows 向来是没有这种光圈的，因为它的目标是白痴用户。当然它的 cmd 命令从始至终充满了科技的味道，一直都是黑白两色。

微软最近几年终于要照顾一下苦逼的开发者了。两个拿得出手的产品，一个是`vscode`，另外一个就是`Windows Terminal`。

为什么终端这么重要呢？对于一个程序员来说，没有了命令行相当于少了半条手臂。这条手臂到底美不美，壮不壮，要看命令行终端好不好用。

以至于微软的员工，很长一段时间在公司都抱着一台 Mac，这多打脸啊。

现在，终于不用这么纠结了。Windows 和 Linux 终于合体了。在同一个系统下，你既可以玩游戏，又可以开开心心的写命令行了，而且有了海量的 Linux 工具支持。

安装 Windows Terminal
-------------------

在远程连接其他 Linux 的时候，我通常使用`Xshell`，就因为它长得比较漂亮耐看。

在 Windows 上，就可以安装`Windows Terminal`。有点类似于 MacOS 上的`iTerm`，可以说是 Windows 下最舒适的终端。

安装`Windows Terminal`需要从应用商店去获取，就是下面这个按钮。  

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYuwHmnBPzu5MgXckINQTaEmKTMibo6mdAKNwHPuYs5dLI9KY7oy01Vjnw/640?wx_fmt=png)

在搜索框里搜索`Windows Terminal`，即可找到这个软件。比较人性化的一点是，它不像 Mac 的应用商店一样，需要你先准备一个账号。WT 不需要登录即可获取。  

如果你的页面一直打转也不要紧，关闭重新打开几次就好了。由于众所周知的原因，国外网站就没有几个不转圈的。  

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYurBJiaY3UKxw8zpTDE74Pibw7PQTw0ib4XeImWRzwlZia6AdXeicq7ACOWow/640?wx_fmt=png)

安装 Ubuntu 子系统
-------------

此时，我们仅仅安装了一个命令行终端而已，离我们扔掉 Linux 的目标还差上一小节。别担心，下面就介绍怎么在`Windows`上安装`Ubuntu`。

方案一、通过虚拟机安装 Linux，然后终端去访问？。这种方案太低级，是我过去一直用的方式，充满了坎坷。

方案二、划分一个分区安装 Linux，然后重启的时候进行切换。开个玩笑，这种方式更加落后，属于古董级别玩家的产物。

我们只需要在系统上开启子系统功能，然后在应用商店安装 Linux 就可以了。

有多简单？简单到你操作的时间可能都没看我唠叨的时间花费多。

如下图，在控制面板，找到程序选项，点击  “启用或关闭 Windows 功能”。  

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYuLibuiaibnibHOWN7lZ7l49UYfWSxV25oAhqPicXDuMf6Evm4dVadQuibF71w/640?wx_fmt=png)

从弹出的对话框里，划到最下边，然后给 “适用于 Linux 的 Windows 子系统 “，打勾，完事！  

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYuTsSVicRicGf1EFLGT2k3U4uKAmzxdIuNZXlJDaRszX8aiaDMwngj0wldg/640?wx_fmt=png)

从应用商店安装 Ubuntu 系统，这个系统将会以软件的形式存在。我这里选择的是 LTS 版本，可以看到给它打分的人并不多，可能大多数都是像我一样没有微软账号的游客。  

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYu3Zzh2BzFviaVILNqDMqvmsGBn63nwogiaI4jebq2R74dvzU7llEGBwkg/640?wx_fmt=png)

事后配置
----

此时，神奇的事情发生了。在我们的`Windows Terminal`右上角，有一个向下的箭头，点击它，就可以看到刚刚安装的 Ubuntu。

在 Windows 上离着 Linux，只差一次点击而已。  

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYuOMXMpRuIpOjslUJHL4MCh3Mxw62iaNiaReciahYrnLuXs1aCvr0zY2N9w/640?wx_fmt=png)

进入 Linux 系统之后，我们就可以像配置一个普通 Linux 一样配置这台机器。

首先把 ubuntu 的软件源给换掉。编辑`/etc/apt/sources.list`文件，把它的内容换成下面的源。

```
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse


```

然后，安装最好用的`oh-my-zsh`。先用`sudo apt install zsh`安装 shell 终端，然后运行下面的命令。

```
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"


```

等待一小段时间，我们的终端颜值就更上一层楼了。

如果你想要你的终端更加漂亮，可以参考下面的主题页面。毕竟命令终端是你每天都要面对的，比你面对自己女朋友的时间还要长，长得丑是影响心情的。

```
https://terminalsplash.com/


```

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYurTtjXfAl4vZcrxib8qoxwAeR1uhmjQ0Hy5dgHXGxHGxlW5U8HsulAyA/640?wx_fmt=png)

还有最后一个问题。我们 Linux 系统中的文件，在 Windows 中如何访问呢？

这个就有点魔幻了。在 Linux 下执行下面的命令。

```
cd /home
explorer.exe .


```

上面的命令，即可打开 Linux 目录对应的 Windows 目录，从文件管理器中我们就可以访问到。

为了操作方便，我把这个长长的目录，映射到了 Z 盘上。如图，下次在访问 Linux 的时候，直接访问 Z 盘就可以了。  

![](https://mmbiz.qpic.cn/mmbiz_png/cvQbJDZsKLo08E6fxsGqkb19ibKiamSjYu5xTxNzzkwEIY7h90MAOLpiayTq0YLORxkvhIiadibhU72OucabnI9N8dA/640?wx_fmt=png)

End
---

可以看到我们在介绍前面一些名词的时候，乱了阵脚。有时候说是 Ubuntu，一会儿说是 Linux，一会儿说是子系统。

这有两个原因。一个原因是我第一次用这个东西，比较激动，以至于语无伦次。另一个原因，就是我的系统现在已经变的四不像，`Windows`和`Linux`已经深度融合，不分你我，甚至网络也不分什么 NAT 桥接，直接是共享的。

再比如，我在 Linux 上，直接执行`cmd.exe`，竟然进入了 Windows 的命令行终端，以至于我现在的脑子都是蒙圈的。

想当年扔掉`Windows`、扔掉`Linux`，选择了`MacBook`，就是因为上面即有漂亮的图形终端，又有好用的命令行，现如今`Windows`也有了。

我还有什么理由坚持我的`MackBook`呢？可能是因为它比较贵，咖啡厅里拿出去比较有面子吧。

