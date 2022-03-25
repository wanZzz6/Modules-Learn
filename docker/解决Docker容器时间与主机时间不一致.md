### 问题

通过 date 命令查看时间

- 查看主机时间

```sh
[root@localhost ~]# date
2016年 07月 27日 星期三 22:42:44 CST
```

- 查看容器时间

```sh
root@b43340ecf5ef:/#date                     
Wed Jul 27 14:43:31 UTC 2016
```

可以发现，他们相隔了 8 小时。

- CST 应该是指（China Shanghai Time，东八区时间）   
- UTC 应该是指（Coordinated Universal Time，标准时间） 

所以，这 2 个时间实际上应该相差 8 个小时。(bluer: 所以没有设置过的容器, 一般跟宿主机时间相差 8h)

所以，必须统一两者的时区。

### 共享主机的 localtime  (方法一)

创建容器的时候指定启动参数，挂载 localtime 文件到容器内  ，保证两者所采用的时区是一致的。

```sh
docker run -d -v /usr/share/zoneinfo/Asia/Shanghai:/etc/localtime --rm -p 8888:8080 tomcat:latest
```

### 复制主机的 localtime  (方法二)

```sh
docker cp /usr/share/zoneinfo/Asia/Shanghai 【容器ID或者NAME】:/etc/localtime
```

在完成后，再通过 date 命令进行查看当前时间。 

但是，在容器中运行的程序的时间不一定能更新过来，比如在容器运行的 MySQL 服务，在更新时间后，通过 sql 查看 MySQL 的时间

```sql
select now() from dual;
```

可以发现，时间并没有更改过来。 

这时候必须要重启 mysql 服务或者重启 Docker 容器，mysql 才能读取到更改过后的时间。

### 创建自定义的 dockerfile  (方法三)

创建 dockerfile 文件，其实没有什么内容，就是自定义了该镜像的时间格式及时区。

```sh
...

#定义时区参数
ENV TZ=Asia/Shanghai

#设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone

...
```

保存后，利用 docker build 命令生成镜像使用即可。


**在 docker 容器和系统时间不一致是因为 docker 容器的原生时区为 0 时区，而国内系统为东八区，当然，我们不深究其原因。**

1）进入容器

```
docker exec -t -i c360cc412528 /bin/bash    // c360cc412528 为容器i
```

2）在 /usr/share/zoneinfo 目录下找上海时区

```
cd  /usr/share/zoneinfo/Asia
```

3）复制上海时区到 /etc 重命名 localtime 文件

```
cp -i Shanghai /etc/localtime
```
