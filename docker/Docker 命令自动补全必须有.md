> 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yFR6IGCFv2vf9C64S6m_lw)

前言
--

不知道这个小伙伴有多久没用过 Docker 了， 突然对我说 Docker 命令怎么发生变化了

```sh
docker run ...
#变成了
docker container run ...
```

他说，本来对 Docker 命令就不熟悉，这下感觉更加混乱了。其实个人看来，这么变化还使得命令看着更加规整

当在命令行直接输入 `docker` 然后回车：

![](https://mmbiz.qpic.cn/mmbiz_png/N1knSK6wthoavL1f0oZLAn3IhgcRqE1ibSQPGc9qwGkUXmhGtiabR7jjTqia6fokLUiaydGUYn7zOuljnYdEibyryFA/640?wx_fmt=png)

从图中可以看出，Docker 将命令结构化的划分了两大类，Management Commands 和 Commands，其实前者就是一级命令，后者就是子命令 （这是自 Docker 1.13 开始的改动），所以以后使用命令就是这样滴：

```shell
docker <Management Command> <Sub-Command <Opts/Args>>
```

这样以后我们使用命令只需要先关注 Management Commands 就可以了，那后续的子命令还是不知道怎么用，还要一点点查询嘛？

Docker 命令自动补全 [1]
-----------------

为了解决这个问题，Docker 也提供了非常完善的命令自动补全功能，也就是把一切交给 Tab 键

### Mac 安装 Docker 命令自动补全

逐条键入下面命令：

```sh
brew install bash-completion

sudo curl -L https://raw.githubusercontent.com/docker/compose/1.27.4/contrib/completion/bash/docker-compose -o /usr/local/etc/bash_completion.d/docker-compose
```

打开 `~/.bash_profile` 文件，将下面内容粘贴进去：

```bash
if [ -f $(brew --prefix)/etc/bash_completion ]; then
 . $(brew --prefix)/etc/bash_completion
 fi
```

然后刷新使之生效

```sh
source ~/.bash_profile
```

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640.gif)

我觉得 Zsh 更好，为什么？答案请看这篇：这篇 iTerm2 + Oh My Zsh 教程手把手让你成为这条街最靓的仔

### Zsh 安装 Docker 命令自动补全

如果没有安装 Oh-My-Zsh shell，第一步则是要先安装它，逐条键入下面命令：

```sh
mkdir -p ~/.zsh/completion

curl -L https://raw.githubusercontent.com/docker/compose/1.27.4/contrib/completion/zsh/_docker-compose > ~/.zsh/completion/_docker-compose
```

打开 `~/.zshrc` 文件，将下面内容粘贴进去：

```sh
fpath=(~/.zsh/completion $fpath)
autoload -Uz compinit && compinit -i
```

比如我的 `~/.zshrc` 文件内容：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201206103638041.png)

搜索该文件插件位置，更新插件内容：

```sh
plugins=(... docker docker-compose
)
```

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640.png)

顺便说一下，强烈建议使用 git 插件

最后刷新一下使之生效：

```sh
source ~/.zshrc
```

总结
--

自动补全功能就可以疯狂利用你的 Tab 键，这比查阅文档要更加快捷，来看看效果：

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/640-20201206103646098.gif)

### 参考

[1]Docker Command Completion: https://docs.docker.com/compose/completion/#install-command-completion