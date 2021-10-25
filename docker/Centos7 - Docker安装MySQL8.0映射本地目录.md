<!-- #region -->
---
参考：

[Docker部署MySQL](https://www.jianshu.com/p/c5bc91868d07)

# 安装启动 Docker

## 1. 安装依赖
```sh
yum -y update
yum install https://download.docker.com/linux/fedora/30/x86_64/stable/Packages/containerd.io-1.2.6-3.3.fc30.x86_64.rpm
yum install -y yum-utils device-mapper-persistent-data lvm2
# 可能需要的选项
# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# yum makecache
yum install docker-ce docker-ce-cli containerd.io
```
## 2. 启动 Dokcer
```sh
systemctl start docker
systemctl enable docker
systemctl status docker
```
## 3. 验证安装是否成功 (有 client 和 service 两部分表示 docker 安装启动都成功了)
```sh
docker version
```
正常显示上下两部分如下内容
![image-20210913135616658](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/image-20210913135616658.png)
# 安装数据库
## 1. 拉取镜像
```sh
docker pull mysql:8.0
docker images   #查看一下镜像拉取是否成功
```
## 2. 测试运行
此次运行镜像只做测试用，一会再删除
```sh
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 --name t_mysql mysql:8.0
docker ps   #查看容器是否正常运行，没有的话可以用 docker ps -a 查看是否创建容器然后用 docker logs 容器ID来查看日志
```
## 3. 查看各个文件所在的位置
```sh
docker exec -it t_mysql /bin/bash    #进入容器
cd /etc/mysql
ls
```
显示如下：
```sh
conf.d/	my.cnf	my.cnf.fallback
```
查看各个文件的位置
```sh
cat my.cnf
```
显示如下：
```sh
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL
```
**解释：**
```
pid-file       #设置包含运行的named守护进程的进程id的文件位置。
socket        #MySQL的通讯协议的载体
datadir        #MySQL的数据库文件所在目录
secure-file-priv= NULL
log-error	   #MySQL的错误日志
```
# 映射本地目录
通过映射让容器内的配置文件、日志文件、数据文件与本地相对应
## 1. 在本地创建对应文件及目录
```
docker stop t_mysql
docker rm -f t_mysql
```
```sh
# 用于存放mysql配置文件
mkdir -p /docker/mysql/conf/
# 用于存放mysql数据文件
mkdir -p /docker/mysql/data/
```
### MySQL 配置文件
```ini
[client]
port            = 3306
socket          = /tmp/mysql.sock
[mysqld]
datadir=/var/lib/mysql       # mysql默认数据存储目录
socket=/tmp/mysql.sock       # mysql服务器连接方式
port=3306                    # mysql服务端口
sql_mode="NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"      # 定义了mysql应该支持的sql语法，数据校验等!  NO_AUTO_CREATE_USER：禁止GRANT创建密码为空的用户。 NO_ENGINE_SUBSTITUTION 如果需要的存储引擎被禁用或未编译，可以防止自动替换存储引擎
long_query_time = 5         # 超过的时间为1s；MySQL能够记录执行时间超过参数 long_query_time 设置值的SQL语句，默认是不记录的。
slow_query_log = 1          # 开启慢查询
slow_query_log_file = slow.log  # 指定慢查询日志保存路径及文件名
max_connections=3000       # mysql的最大连接数，MySQL的实际最大可连接数为max_connections+1；MySQL无论如何都会保留一个用于管理员（SUPER）登陆的连接，用于管理员连接数据库进行维护操作，即使当前连接数已经达到了
skip-name-resolve          # 跳过客户端域名解析
back_log=384               # 在MySQL暂时停止响应新请求之前的短时间内多少个请求可以被存在堆栈中
log-bin=mysql-bin          # 开启二进制日志功能，binlog数据位置
binlog_format=mixed        # mysql 复制方式：混合模式复制
expire_logs_days = 7       # 控制binlog日志文件保留时间，expire_logs_days=7           # 表示保留最近7天的binlog日志，7天以前的binlog日志会被自动删除
server-id = 123          # mysql的同步数据中是包含server-id的，用于标识该语句最初从哪个server写入
```
## 2. 创建容器
-v :/etc/my.cnf -v /docker/mysql/data:/var/lib/mysql  
```sh
docker run -d -p 3306:3306 --privileged=true \
:\
-v /docker/mysql/conf/my.cnf:/etc/mysql/my.cnf \
-v /opt/data/mysql:/var/lib/mysql \
-v /opt/logs/mysql/error.log:/var/log/mysql/error.log \
--character-set-server=utf8mb4 --collation-server=utf8mb4_general_ci \
--name mysql mysql:8.0
```
**说明：**
- `run`: run 是运行一个容器
- `-d`: 表示后台运行
- `-p`: 表示容器内部端口和服务器端口映射关联
- `--privileged=true`: 设值MySQL 的root用户权限, 否则外部不能使用root用户登陆
- `--name mysql`: 设值容器名称为mysql
- `mysql:8.0`  表示从docker镜像mysql:8.0 中启动一个容器
- `--character-set-server=utf8mb4 --collation-server=utf8mb4_general_ci`:   设值数据库默认编码
- `-v /docker/mysql/conf/my.cnf:/etc/my.cnf`   将服务器中的my.cnf配置映射到docker中的/docker/mysql/conf/my.cnf配置
- `-v /docker/mysql/data:/var/lib/mysql`　　　　同上,映射数据库的数据目录, 避免以后docker删除重新运行MySQL容器时数据丢失
- `-e MYSQL_ROOT_PASSWORD=123456`　:设置MySQL数据库root用户的密码
## 测试
1. 创建容器成功后查看一下/opt/data/mysql 下是否有文件
```sh
docker exec -it test_mysql /bin/bash  #进入容器查看配置文件是否同步
cat /etc/mysql/my.cnf
```
执行MySQL命令, 输入root密码, 连接MySQL
```sh
mysql -u root -p
123456
show databases;
```
2. 测试数据库文件是否映射正确
# 其他
## 解决Docker中mysql修改配置导致无法启动的docker容器
宿主机中查找my.cnf文件
```sh
find / -name my.cnf |grep '/etc/mysql/my.cnf'
```
找到：
```
/data/docker/overlay2/dfc2ddbed53a1237fa120f7b9a79eb4488bd3d2ff2ae7f4ce6052ba5b52b480a/diff/etc/mysql/my.cnf
```
#vi 修改如上找到的文件即可
或到目录
/data/docker/overlay2/dfc2ddbed53a1237fa120f7b9a79eb4488bd3d2ff2ae7f4ce6052ba5b52b480a/diff/etc/mysql/下，如果有my.cnf.fallback
可以执行

```sh
mv my.cnf.fallback my.cnf
```
## 优化 mysql内存占用
1. 进入docker bash
```sh
$ docker exec -it mysql bash
```
2. 进入 /etc/mysql/conf.d  
3. 安装 Vim
```sh
$ apt-get update
$ apt-get install vim 
```
4. vim docker.cnf，追加以下内容
```ini
[mysqld]
performance_schema = off  # 加入这一行即可
performance_schema_max_table_instances=400  
table_definition_cache=400  
table_open_cache=256
```
按Esc :wq! 退出vim
退出bash， 重启mysql
```sh
docker restart mysql 
```
```sh
mkdir -p /docker/mysql/data
mkdir -p /docker/mysql/conf


# ......

docker run -d -p 3306:3306 --privileged=true \
-e MYSQL_ROOT_PASSWORD=123456 \
-v /docker/mysql/data:/var/lib/mysql \
-v /docker/mysql/logs/error.log:/var/log/mysql/error.log \
--name mysql mysql:8.0 \
--character-set-server=utf8mb4 --collation-server=utf8mb4_general_ci

#创建挂载目录
mkdir -p /docker/gogs

docker run -d -p 9022:22 -p 9080:3000 \
--link mysql:mysql \
-v /docker/gogs:/data \
--name=tjkj-gogs2 \
gogs/gogs
```
---
<!-- #endregion -->