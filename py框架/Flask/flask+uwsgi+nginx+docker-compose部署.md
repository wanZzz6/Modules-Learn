## 简单介绍

Flask 这里就不多阐述了，已经是很流行的一个轻量级 python 框架了，对于小、中型项目特别适合。这里用 docker 的 compose 编排部署.  
uwsgi 简单的说明下，uWSGI 是一个 Web 服务器，它实现了 WSGI 协议、uwsgi、http 等协议。
Nginx 中 HttpUwsgiModule 的作用是与 uWSGI 服务器进行交换。
WSGI 是一种 Web 服务器网关接口。它是一个 Web 服务器（如 nginx，uWSGI 等服务器）与 web 应用（如用 Flask 框架写的程序）通信的一种规范。
这是官方说法，大概还是看具体例子能够说明一切，https://www.runoob.com/python3/python-uwsgi.html（这里是 http 方式），另外一种是 socket 方式，
下面附一张图来说明
![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/665135-20190729103746625-1213586825.png)
现在大部分 web 服务器（如 nginx）支持 uwsgi， socket 是最高效的一种网络通信方式，socket 通信速度会比 http 快
uwsgi.ini 的配置说明：

```ini
http-socket=:5000//配置uwsgi监听的socket(ip+端口）
callable=app//uwsgi调用的python应用实例名称,Flask里默认是app,根据具体项目代码实例命名来设置
wsgi-file=server.py//调用的主程序文件，绝对路径或相对于该ini文件位置的相对路径均可
master=true//以独立守护进程运行
processes=8//配置进程数量
threads=4//配置线程数量
enable-threads=true//允许在请求中开启新线程
stats=127.0.0.1:9191//返回一个json串，显示各进程和worker的状态
pidfile=uwsgi.pid//存放uwsgi进程的pid，便于重启和关闭操作
listen=1024//监听队列长度，默认100，设置大于100的值时，需要先调整系统参数
chdir = /project  //指定项目目录为主目录
daemonize=uwsgi.daemonize.log//以守护进程运行，日志文件路径
memory-report=true//启用内存报告，报告占用的内存
buffer-size=65535//设置请求的最大大小 (排除request-body)，这一般映射到请求头的大小。默认情况下，它是4k，大cookies的情况下需要加大该配置
```

docker-compose 的一些常用操作

- docker-compose up -d nginx                     构建建启动nignx容器
- docker-compose exec nginx bash            登录到nginx容器中
- docker-compose down                              删除所有nginx容器,镜像
- docker-compose ps                                   显示所有容器
- docker-compose restart nginx                   重新启动nginx容器
- docker-compose run --no-deps --rm php-fpm php -v  在php-fpm中不启动关联容器，并容器执行php -v 执行完成后删除容器
- docker-compose build nginx                     构建镜像 。        
- docker-compose build --no-cache nginx   不带缓存的构建。
- docker-compose logs  nginx                     查看nginx的日志 
- docker-compose logs -f nginx                   查看nginx的实时日志
- docker-compose config  -q                        验证（docker-compose.yml）文件配置，当配置正确时，不输出任何内容，当文件配置错误，输出错误信息。 
- docker-compose events --json nginx       以json的形式输出nginx的docker日志
- docker-compose pause nginx                 暂停nignx容器
- docker-compose unpause nginx             恢复ningx容器
- docker-compose rm nginx                       删除容器（删除前必须关闭容器）
- docker-compose stop nginx                    停止nignx容器
- docker-compose start nginx                    启动nignx容器

## 正式部署

先看下目录

	创建文件夹 mkdir docker-flask  
	创建文件 docker-compose.yml nginx.conf  文件夹webapp  
	cd webapp 里面创建文件 Dockerfile app.py requirements.txt uwsgi.ini

文件内容依次如下：

- docker-compose.yml　

```yaml
version: "2"
services:
    webapp:
        build: ./webapp  #webapp目录地址，当前文件夹
        container_name: webapp  #容器名称
    nginx:
        image: nginx  #需要nginx镜像，所以最好在本地事先生成一个nginx镜像
        volumes:
            - ./nginx.conf:/etc/nginx/conf.d/default.conf  #做配置映射
        depends_on:
            - webapp   #依赖webapp
        ports:
            - "8888:80"
```

编排服务的其实就是将多个分别的服务关联到一起启动，可以事先对每个服务先做下单独的运行，都成功的话，在配置的 docker-compose 里面。

- nginx.conf

```
server {
    listen 80;
    server_name 0.0.0.0; 
    location / {
        include uwsgi_params;
        uwsgi_pass webapp:8002; 
    }
}
```

webapp 文件夹里的文件内容
- Dockerfile

```dockerfile
1 FROM python:3.5
2 ENV TZ=Asia/Shanghai
3 RUN mkdir /webapp
4 WORKDIR /webapp  #指定工作目录
5 COPY . /webapp
6 
7 RUN pip install -i https://pypi.doubanio.com/simple/  --trusted-host pypi.doubanio.com -r requirements.txt #这里用国内信任的豆瓣源，速度比较快
8 
9 CMD ["uwsgi", "--ini", "/webapp/uwsgi.ini"] #初始化的启动操作
```

- app.py

```python
 1 #!/usr/bin/env python
 2 #coding=utf-8
 3 
 4 from flask import Flask,render_template_string
 5 
 6 app = Flask(__name__)
 7 
 8 @app.route("/")
 9 def index():
10         return render_template_string('<h1>Hello Flask</h1>')
11 
12 if __name__ == "__main__":
13     app.run(debug=True,host='127.0.0.1',port=5000) #这里是用python app.py启动的设置，如果用uwsgi这种，可以无需关注 
```

- requirements.txt

```
1 Flask
2 uwsgi
```

- uwsgi.ini　　

```ini
 1 [uwsgi]
 2 module = app:app #目录.文件:app对象
 3 #callable = app #或者这么设置
 4 master = true
 5 processes = 4
 6 chdir = /webapp #指定运行目录
 7 socket = :8002  #监听端口
 8 chmod-socket = 666
 9 logto = /webapp/app.log
10 vacuum = true
```


都配置完成后，在 docker-flask 目录下执行

```sh
docker-compose up  
或者后台运行
docker-compose up -d 
```

```sh
// 查看运行的容器
docker ps
// 查看运行的服务
docker-compose ps
```

如果没什么问题的话在浏览器直接输入 127.0.0.1:8888 就会看到

　　Hello Flask

完毕！