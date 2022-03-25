ADD 复制文件
--------

*   格式：
    *   ADD <src>...<dest>
    *   ADD ["<src>",..."<dest>"]

```dockerfile
ADD docker-test-demo-0.0.1-SNAPSHOT.jar app.jar
```

*   从 src 目录复制文件到容器的 dest，其中 src 可以是 Dockerfile 所在目录的相对路径，也可以是一个 URL，还可以是一个压缩包
*   **注意**：
    *   src 必须在构建的上下文内，不能使用例如：ADD ../somethine /something 这样的命令，因为 docker build 命令首先会将上下文路径和其子目录发送到 docker daemon
    *   如果 src 是一个 URL，同时 dest 不以斜杠结尾，则 dest 会被视为文件，src 对应内容文件会被下载到 dest
    *   如果 src 是一个 URL，同时 dest 以斜杠结尾，则 dest 会被视为目录，src 对应内容文件会被下载到 dest 目录
    *   如果 src 是一个目录，那么整个目录下的内容将会被复制，包括文件系统元数据
    *   如果文件是可是别的压缩包，则 docker 会自动解压

ARG 设置构建参数
----------

*   格式：
    *   ARG <name>[=<default value>]

```
ARG user1=someuser
```

*   ARG 指令用于设置构建参数，类似与 ENV，不同的是，ARG 设置的是构建时的环境变量，在容器运行时是不会存在这些变量的

CMD 容器启动命令
----------

*   格式：
    *   CMD ["executable","param1","param2"]（推荐）
    *   CMD ["param1","param2"]（为 ENTRYPOINT 指令提供预设参数）
    *   CMD command param1 param2 （在 shell 中执行）

```
CMD echo "This is a test." | wc -
```

*   CMD 指令用于为执行容器提供默认值，每个 Dockerfile 只有一个 CMD 命令，如果指定了多个 CMD 命令，那么只有最后一条被执行，如果启动容器时指定了运行的命令，则会被覆盖掉 CMD 指定的指令

COPY 复制文件
---------

*   格式：
    *   COPY <src>...<dest>
    *   COPY ["<src>",..."<dest>"]
*   复制本地端的 src 到容器的 dest，COPY 指令和 ADD 指令类似，COPY 不支持 URL 和压缩包

ENTRYPOINT 入口点
--------------

*   格式：
    *   ENTRYPOINT ["executable","param1","param2"]
    *   ENTRYPOINT command param1 param2
*   ENTRYPOINT 和 CMD 指令的目的一样，都是指定 Docker 容器启动时的执行命令，可以多次设置，但只有最后一个有效

ENV 设置环境变量
----------

*   格式：
    *   ENV <key> <value>
    *   ENV <key>=<value> ...

```
ENV JAVA_HOME /path/to/java
```

EXPOSE 声明暴露的端口
--------------

*   格式：
    *   EXPOSE <port> [<port>...]

```sh
# 声明暴露一个端口
EXPOSE port1
# 相应的运行容器使用的命令
docker run -p port1 image
# 也可以使用 -P 选项启动
docker run -P image

# 声明暴露多个端口
EXPOSE port1 port2 port3
# 相应的运行容器使用的命令
docker run -p port1 -p port2 -p port3 image
# 也可以指定需要映射到宿主机器上的端口号
docker run -p host_port1:port1 -p host_port2:port2 -p host_port3:port3 image
```

*   EXPOSE 指令用于声明在运行时容器提供的服务端口，该指令的作用主要是帮助镜像使用者理解该镜像服务的守护端口，其次是当运行时使用随机映射时，会自动映射 EXPOSE 的端口

FROM 指定基础镜像
-----------

*   格式：
    *   FROM <image>
    *   FROM <image>:<tag>
    *   FROM <image>@<digest>
*   使用 FROM 指令指定基础镜像，FROM 指令类似 Java 里的 extends 关键字，FROM 指令必须指定且必须在其它指令之前，FROM 指令之后的的所有指令都依赖于所指定的镜像

LABEL 为镜像添加元数据
--------------

*   格式：
    *   LABEL <key>=<value> <key>=<value> <key>=<value> ...
    *   使用 " 和 \ 转换命令行

```dockerfile
LABEL "com.example.vendor"="ACME Incorporated"
LABEL "com.example.label-with-value"="foo"
LABEL version="1.0"
LABEL description="This text illustrates \ 
that label-values can span multiple lines."
```

MAINTAINER 指定维护者信息
------------------

*   格式：
    *   MAINTAINER <name>

```
MAINTAINER xxx<xxxx@qq.com>
```

RUN 执行命令
--------

*   格式：
    *   RUN <command>
    *   RUN ["executable","param1","param2"]
*   RUN <command> 在 shell 终端中运行，在 Linux 中默认是 /bin/sh -c，在 Windows 中是 cmd /s /c

USER 设置用户
---------

*   格式：
    *   USER 用户名

```
USER daemon
```

*   该指令用于设置启动镜像时的用户或者 UID，写在该指令后的 RUN、CMD 以及 ENTRYPOINT 指令都将使用该用户执行命令

VOLUME 指定挂载点
------------

*   格式：
    *   VOLUME ["/data"]

```
VOLUME /data
```

*   该指令使容器中的一个目录具有持久化存储功能，该目录可被容器本身使用，也可以共享给其它容器
*   当容器中的应用有持久化数据的需求时可以在 Dockerfile 中使用该指令

WORKDIR 指定工作目录
--------------

*   格式：
    *   WORKDIR /path/to/workdir
*   切换目录指令，类似于 cd 命令，写在该指令后的 RUN、CMD 以及 ENTRYPOINT 都将该工作目录作为当前目录，并执行指令

其它
--

*   Dockerfile 还有一些其它指令，例如 STOPSINGAL、SHELL 等