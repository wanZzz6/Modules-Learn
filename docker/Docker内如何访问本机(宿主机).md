Docker内需要访问本机的数据库，如何访问。使用`127.0.0.1`肯定是不行的，因为这个在Docker容器里面指的是容器本身。所以，需要走别动渠道进行解决。



## 方法

下面几种办法，根据操作系统的类型，选取其一即可。

 ### 1. DockerFile

```dockerfile
RUN /sbin/ip route|awk '/default/ { print  $3,"\tdockerhost" }' >> /etc/hosts
```

### 2. Runtime

(may not use) 

```sh
docker run --add-host dockerhost:`/sbin/ip route|awk '/default/ { print  $3}'` [my container]
```

(useful) 

```sh
docker run --add-host=dockerhost:`docker network inspect  --format='{{range .IPAM.Config}}{{.Gateway}}{{end}}' bridge` [IMAGE]
```

### 🎈3. MAC

win/linux : `docker.for.win.localhost` 、 `host.docker.internal`
mac : `docker.for.mac.localhost`

示例：

在容器内

```sh
ping docker.for.win.localhost
```



```dockerfile
docker.for.mac.host.internal
MONGO_SERVER=docker.for.mac.host.internal

# docker-compose.yml
version: '3'

services:
  api:
    build: ./api
    volumes:
      - ./api:/usr/src/app:ro
    ports:
      - "8000"
    environment:
      - MONGO_SERVER
    command: /usr/local/bin/gunicorn -c /usr/src/app/gunicorn_config.py -w 1 -b :8000 wsgi
```

### 4. Linux

-  Solution 1

```sh
/sbin/ip route|awk '/default/ { print $3 }'
docker run --add-host dockerhost:`/sbin/ip route|awk '/default/ { print  $3}'` [my container]
```

-  Solution 2

```sh
-e "DOCKER_HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')"
```

### 5. 宿主机 ip地址

使用宿主机的局域网地址，如: 192.168.100.100

## 原理

想知道原理，需要了解计算机网络的模型和docker实现的模型。docker内部实际上实现了一个虚拟网桥docker0，需要通过网桥找到外部宿主机的在网桥的虚拟地址，也就是docker.for.mac.host.internal，就可以实现容器内访问外部宿主机。感兴趣的话可以了解下Docker的网络原理、计算机网络原理和docker compose等内容。

Reference
[1]. [(stackoverflow)insert-docker-parent-host-ip-into-containers-hosts-file](https://stackoverflow.com/questions/26864180/insert-docker-parent-host-ip-into-containers-hosts-file/26864854#26864854)

[2]. [(stackoverflow)how-to-get-the-ip-address-of-the-docker-host-from-inside-a-docker-container](https://stackoverflow.com/questions/22944631/how-to-get-the-ip-address-of-the-docker-host-from-inside-a-docker-container)

