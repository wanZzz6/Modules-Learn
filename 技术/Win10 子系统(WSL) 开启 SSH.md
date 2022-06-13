---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region -->

wsl 是微软对 Windows Linux Subsystem 的官方叫法。安装 wsl 后，通过 bash 来启动这个子系统，然后可以安装 ssh。在我的 windows 发行版上，启用了 wsl 以后，ssh 就默认存在了。但要真正使用起来，还要注意以下几点。  

最重要的配置是这两项：  

```sh
UsePrivilegeSeparation no #因为wsl没有实现chroot

PasswordAuthentication yes

ListenAddress 0.0.0.0         #这一项在我的发行版里缺省为注释行。
```

为安全起见，我将 listen address 由 0.0.0.0 改成了 127.0.0.1。

较新的 windows 版本自带了一个 ssh server，也监听在 22 端口。你可以通过 power shell 来查看这项服务：  

```sh
PS C:\Users\yangy> Get-Service -Name ssh*

Status   Name               DisplayName

------   ----               -----------

Stopped  SshBroker          SSH Server Broker

Stopped  SshProxy           SSH Server Proxy
```

这是显示关闭以后的状态。这个服务必须关掉，不然 wsl 的 ssh service 是无法启动起来的。在 windows 服务里找到这两个服务：  
[![](https://hbaaron.github.io/blog_2017/%E5%9C%A8wsl%E4%B8%8B%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8sshd%E5%85%A8%E6%94%BB%E7%95%A5/2be1cbce554bcc9bea1a8346d52e6d70.png)](https://hbaaron.github.io/blog_2017/%E5%9C%A8wsl%E4%B8%8B%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8sshd%E5%85%A8%E6%94%BB%E7%95%A5/2be1cbce554bcc9bea1a8346d52e6d70.png)

1.  首先以 / usr/sbin/sshd -d 的方式启动服务。-d 表明是以调试方式启动的服务，这种情况下，错误会显示在控制台上。在我的电脑上，不存在 / var/log/secure 日志文件，所以无法以传统 linux 的方式来做 troubleshooting。
2.  在另一个 bash 窗口中输入 ssh username@localhost -v。可以使用 - v -vv, -vvv 来加重输出日志的详细程度。在我的电脑上出现过 connection closed 的错误，查看 sshd -d 窗口的输出，提示 No supported key exchange algorithms。这是因为在 sshd_config 中这一段中指定的 key 文件不存在：

```sh
# HostKeys for protocol version 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
```


这种情况下需要用 ssh-keygen 来生成这些文件：  

```sh
ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```

1.  如果以上步骤通过，那么现在可以使用下述方法启动：
    
```sh
sudo service ssh --full-restart
```


要注意即使以这种方法启动 ssh server，它仍然只是在存在 bash 窗口时的一个子服务。一旦最后一个 bash 窗口关闭，这个 ssh server 也就关闭了，显然这不是我们想要的。接下来看看怎么将 ssh server 以 windows 服务或者后台进程来运行。

当前 WSL 并不支持 ssh server 作为服务运行。我们需要借助 windows 计划任务和脚本，使得在 windows 启动时自动运行这一服务。  

```vbs
set ws=wscript.createobject("wscript.shell")
ws.run "C:\Windows\System32\bash.exe -c 'sudo /usr/sbin/sshd -D'",0
```

将这个文件存为 vbs，并在计划任务中添加一个启动任务，触发器设置为系统启动时。  
上述脚本存在一个问题，就是执行 sudo 时，会提示输入密码，而这时又无法拿到用户的输入。要解决这一问题，需要允许 sudo 在没有密码的情况下执行命令。

在 bash 窗口中运行 `sudo visudo`：  

```sh
#includedir /etc/sudoers.d
$username ALL=(ALL) NOPASSWD: /usr/sbin/sshd -D
```

这里的 $username 即 wsl 子系统中的一个用户名。我使用了安装 wsl 时给出的一个用户名。
<!-- #endregion -->
