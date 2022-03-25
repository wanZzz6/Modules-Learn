

# linux磁盘空间占满问题快速定位并解决

常使用如下几个命令进行排查：`df`, `lsof`，`du`。

通常的解决步骤如下：

### 1. df -h 查看全部磁盘空间

```
[root@localhost ~]# df -h
文件系统             容量  已用  可用 已用% 挂载点
tmpfs                 16G  530M   16G    4% /run
/dev/mapper/cl-root   50G   34G   17G   67% /
/dev/mapper/cl-home  492G  232G  261G   48% /home
/dev/sda1            976M  278M  632M   31% /boot
```

### 2. 快速定位一下应用日志大小情况 

进入使用率较高的挂载点，凭感觉定位可能过大的文件，比如 tomcat 日志，应用系统自己的日志等。

### 3. 使用 du 命令定位

如果不能直观地排除出是某个日志多大的原因，就需要看一下指定目录下的文件和子目录大小情况，

```sh
du -h --max-depth=1 path | sort -hr #查看目录大小并按照大小倒序展示
```

```
[root@test ~]# du -h --max-depth=1 /usr/local/ | sort -hr
2.6G    /usr/local/
1.1G    /usr/local/mysql
358M    /usr/local/jdk1.8.0_121
......
```

### 4. 删除或者清空文件

清空

清空而不删除用 > 符号，例如清空 debug.log 文件：

```sh
[root@localhost ~]# > logs/catalina.out
```

删除

删除文件时注意：

有时候用 `rm` 命令删除日志文件之后再 `df -h` 查看空间依然被占满，则该大文件可能在被某个进程占用而未释放。

```sh
lsof 文件名 # 查看文件占用进程情况
```

如果删除的日志正在被某个进程占用，则必须重启或者 kill 掉进程。

```
[root@test ~]# lsof /usr/local/apache-tomcat-7.0.54/logs/catalina.out
COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
java 7053 root 1w REG 202,1 958123 1180888 /usr/local/apache-tomcat-7.0.54/logs/catalina.out
java 7053 root 2w REG 202,1 958123 1180888 /usr/local/apache-tomcat-7.0.54/logs/catalina.out
```

【参考】

- [每天一个 linux 命令（34）：du 命令](http://www.cnblogs.com/peida/archive/2012/12/10/2810755.html)
- [Linux 中删除文件，磁盘空间未释放问题追踪](http://blog.csdn.net/cjf_iceking/article/details/37593963)  
- [linux 删除文件后，如何释放磁盘空间?](https://segmentfault.com/q/1010000003044027)

