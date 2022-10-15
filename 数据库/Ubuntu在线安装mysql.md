

### 添加 APT 仓库

1.  访问 https://dev.mysql.com/downloads/repo/apt/。
    
2.  选择下载适合自己平台的 deb 包。
    
3.  执行下面的命令，安装下载的软件包。
    

```sh
sudo dpkg -i /PATH/version-specific-package-name.deb
```

用下载的包的名称替换掉 version-specific-package-name.deb。

6.  在安装期间，需要选择 mysql server 和组件的版本。不能确定版本，就不要改变默认版本。如果不想安装某一个组件，就选择 none。选择完毕后，选择 ok 就可以完成安装。
    

安装完成以后也可以通过选择发行版本，修改 mysql 版本。

8.  可以用下边的命令更新包。
    

```sh
apt-get update
```

除了利用发行的 deb 包，还可以人工自己添加 APT 仓库。详见 https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/index.html#repo-qg-apt-repo-manual-setup

注意：MYSQL APT 仓库一旦生效，就不可以从系统自带的软件库安装 MYSQL 的任何包。

### APT 安装 MYSQL

利用下面的命令安装 mysql：

```sh
apt-get install mysql-server
```

安装 mysql 客户端和数据库普通文件的命令与上面的命令类似。

在安装过程中，需要提供一个 root 用户的密码（需要记住）。

提示：如果想以后再设置密码，则可以不提供密码，选择 ok，继续安装。在这种情况下，root 可以通过 Unix socket file 连接 mysql，通过 Socket Peer-Credential Pluggable Authentication 的授权。以后可以通过 mysql_secure_installation 再设置 root 的密码。

### 启动停止 mysql server

Mysql server 安装完成后，自动启动，可以用下边的命令查看 Mysql server 的状态：

```sh
service mysql status
```

使用下边的命令，停止 Mysql server 的运行:

```sh
service mysql stop
```

使用下边的命令启动 Mysql server

```sh
service mysql start
```

使用下边的命令重启 Mysql server

```sh
service mysql restart
```

注意：一些依赖于本机 MySQL 包的第三方本机存储库包可能无法与 MySQL APT 存储库包一起使用。例如：konadi-backend-mysql, handlersocket-mysql-5.5, 和 zoneminder。

### 选择发行版本

Mysql server 和所有的组件的安装和升级的默认版本，都是来自添加 APT 仓库选择的版本。可以在任何时候利用以下命令修改原来的选择。

```sh
dpkg-reconfigure mysql-apt-config
```

修改完毕后，用以下命令更新 mysql 仓库：

```sh
apt-get update
```

再次运行 apt-get install 命令，就会安装你选择的版本。

Mysql 的组件版本选择与此类似。

### 安装附加的 MYSQL 产品和组件

在添加了 Mysql 的 APT 仓库后。首先，用下面的命令从 APT 仓库获取最新的包信息。

```sh
apt-get update
```

用下面的命令安装你选择的组件或附加产品，用包名字替换 package-name。

```sh
apt-get install package-name
```

例如：安装共享客户端库：

```sh
apt-get install libmysqlclient18
```

### APT 删除 mysql

删除用 MySQL APT 仓库安装的 mysql server 和他的组件，首先用下面的命令删除 mysql server：

```sh
apt-get remove mysql-server
```

接着删除和 mysql server 一起自动安装的软件：

```bash
apt-get autoremove
```

用下面的命令删除附属产品和组件，用你想删除的包名称替换 package-name：

```sh
apt-get remove package-name
```

查看你利用 MySQL APT repository 安装的包，用下面的命令：

```sh
dpkg -l | grep mysql | grep ii
```

上述就是小编为大家分享的怎么利用 APT 库安装 MySQL 了，如果刚好有类似的疑惑，不妨参照上述分析进行理解。如果想知道更多相关知识，欢迎关注亿速云行业资讯频道。