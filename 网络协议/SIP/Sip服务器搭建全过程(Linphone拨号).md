> 原文地址 [blog.csdn.net](https://blog.csdn.net/qq_38631503/article/details/80005454)

**Sip 服务器搭建全过程**

参考文档：[http://blog.csdn.net/jhope/article/details/53129122](http://blog.csdn.net/jhope/article/details/53129122)  
参考文档：[https://www.cnblogs.com/xlwm/p/4414207.html](https://www.cnblogs.com/xlwm/p/4414207.html)  
参考文档：[http://blog.csdn.net/Richar1/article/details/50949506](http://blog.csdn.net/Richar1/article/details/50949506)  
参考文档：[http://blog.csdn.net/lhh1002/article/details/6131733](http://blog.csdn.net/lhh1002/article/details/6131733)  

参考文档：[http://blog.csdn.net/canglonghacker/article/details/30537709](http://blog.csdn.net/canglonghacker/article/details/30537709)

环境：ubuntu14.04

虚拟机网络适配器改为桥接模式 (自动)

桥黑板，重点提醒：

***** 安装过程中及时使用虚拟机快照功能 *****

快照使用：[https://jingyan.baidu.com/article/1709ad806e1ebb4635c4f048.html](https://jingyan.baidu.com/article/1709ad806e1ebb4635c4f048.html)

极度郁闷：安装过程中提示错误，网上查找都说在目录 / var/log 目录下有对应的日志文件，但我实际安装过程中虽然有生成这些文件，但是不会更新记录错误信息，很是郁闷。下面所说的问题解决方法，都是自己查找资料，实验得出来的，按照这个操作步骤，及时使用虚拟快照功能 (防止误操作从头来过)，将 sip 服务器搭建起来是没有问题的。

有知道日志是什么回事的请告知！！！

**1. 关于 mysql 数据库**

a)  安装 mysql

sudo apt-get install mysql-server

sudo apt-get install mysql-client

sudo apt-get install libmysqlclient-dev

这里输入的密码是 root 数据库的密码

b)  卸载 mysql

删除 mysql 的数据文件

sudo rm /var/lib/mysql/ -R

删除 mysql 的配置文件

sudo rm /etc/mysql/ -R

自动卸载 mysql(包括 server 和 client)

sudo apt-get autoremove mysql* --purge

sudo apt-get remove apparmor

检查是否卸载干净

dpkg -l | grep mysql # 若没有返回，说明已完成卸载

**2. 关于 opensips 安装**

过程中可能涉及到权限问题，为了方便在 root 操作

a)  下载 opensips

官网下载地址：[http://www.opensips.org/Resources/Downloads](http://www.opensips.org/Resources/Downloads)

我这里使用的是在虚拟机下 git 直接下载

git clone https://github.com/OpenSIPS/opensips.git -b2.2 opensips-2.2

b)  编译 opensips

最最重要的就是把 db_mysql 模块编译进去

make menuconfig 执行此命令直接退出，会在源码根目录下生成 Makefile.conf 文件（使用左右键进入 / 返回菜单；opensis 中默认是不支持 mysql 的，需要手动修改 Makefile.conf 文件）

![](https://img-blog.csdn.net/20180419153225946?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

修改 Makefile.conf 文件：

在 exclude_modules 中删掉 db_mysql,

在 include_modules 中添加 db_mysql，

修改安装目录为 PREFIX=/usr/local/opensips/

![](https://img-blog.csdn.net/20180419153240647?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

make all

make install

c)  配置 opensips

cd /usr/local/opensips/

目录结构如下

![](https://img-blog.csdn.net/20180419153254884?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

这里有两个文件需要修改，opensipsctlrc 和 oepnsips.cfg

修改 opensipsctlrc 文件

![](https://img-blog.csdn.net/20180419153305850?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

将对应字段的注释打开，部分需要手动修改

ip 为自己主机 ip

修改 opensips.cfg 文件 (这个地方是个天坑)

使用 make menuconfig 菜单工具生成一个 opensips.cfg 文件

![](https://img-blog.csdn.net/20180419153328410?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

![](https://img-blog.csdn.net/20180419153339694?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

![](https://img-blog.csdn.net/20180419153353246?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

![](https://img-blog.csdn.net/20180419153402662?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

![](https://img-blog.csdn.net/20180419153411875?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

这一步记住自己菜单中生成的 .cfg 文件名

退出菜单后

cd etc/

mv opensips_residential_2018-2-7_3\:59\:1.cfgopensips.cfg

cp opensips.cfg /usr/local/opensips/etc/opensips/opensips.cfg

这里之后开始真正地修改 opensips.cfg 文件

![](https://img-blog.csdn.net/20180419153441839?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

d)  创建 opensips 数据库

cd /usr/local/opensips/sbin

检测配置文件语法

./opensips -C

创建数据库

./opensipsdbctl create

![](https://img-blog.csdn.net/20180419153459285?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

MySQL password for root: 输入安装 mysql 时的 (root) 密码

报错 1：

![](https://img-blog.csdn.net/20180419153538158?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)  

解决方法：

修改 my.cnf 文件

vi /etc/mysql/my.cnf

![](https://img-blog.csdn.net/20180419153554435?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)  

重新启动 mysql

![](https://img-blog.csdn.net/20180419153605780?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

报错 2：

![](https://img-blog.csdn.net/20180419153618894?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

解决方法：

![](https://img-blog.csdn.net/20180419153628363?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

mysql 安装的 root 数据库密码为 1

% 使所有外部 ip 地址都能访问使用 mysql

e)  开启 opensips 服务

./opensipsctl start      #开启 opensips 服务

./opensipsctl stop       #关闭 opensips 服务

./opensipsctl restart    #重启 opensips 服务 

![](https://img-blog.csdn.net/20180419153654710?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)  

报错 1：

![](https://img-blog.csdn.net/20180419153703173?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)  

解决方法：

vi/usr/local/opensips/etc/opensips/opensips.cfg

![](https://img-blog.csdn.net/20180419153717402?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)  

修改为 modules 实际路径

f)  添加 sip 用户

./opensipsctl add username password       #添加用户

./opensipsctl rm username                 #删除用户

![](https://img-blog.csdn.net/20180419153738738?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

g)  查看 sip 用户

可以使用 mysql -u opensips -p 而后输入你的密码，就能够通过 show databases; 查看数据库，再使用 use opensips; 并且 show tables; 就可以查看 opensips 数据库里的表格，最后使用 select * from subscriber; 便能够查看添加的 sip 用户情况

默认的 opensips 的数据库密码为 opensipsrw

![](https://img-blog.csdn.net/20180419153804954?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

h)  查看在线用户

./opensipsctl ul show

./opensipsctl online

这个时候查询还没有效果，先进行下一步使用 Linphone 注册 sip 账户，注册之后再查看就会显示在线

**3. 关于 Linphone 安装**

a)  PC 机安装 Linphone

百度软件中心 (普通下载)：[http://rj.baidu.com/soft/detail/35293.html?ald](http://rj.baidu.com/soft/detail/35293.html?ald)  

b)  手机安装 Linphone

绿色资源网 (其他下载地址)：[http://www.downcc.com/soft/342710.html](http://www.downcc.com/soft/342710.html)

c)  设置 PC 机 Linphone

Options->SIP 账户管理

![](https://img-blog.csdn.net/20180419154356743?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

1. 填写自己的显示名称，随便填，不重要；

2. 填写自己 sip 服务器上已经注册的账户；

3. 添加 sip 代理账户；

4. 按格式填写，IP 为 PC 机 IP 地址，5060 默认端口；

5. 按格式填写，IP 为 SIP 服务器地址，5060 默认端口；

添加联系人

![](https://img-blog.csdn.net/20180419154418580?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

1. 点击添加 Linphone 联系人；

2. 填写联系人名称；

3. 按格式填写，IP 为 SIP 服务器地址，5060 默认端口；

4. 自动识别，不用改；

d)  设置手机端 Linphone

注册 sip 用户

![](https://img-blog.csdn.net/20180419154439537?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

 ![](https://img-blog.csdn.net/20180419154450884?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

 **![](https://img-blog.csdn.net/20180419154502335?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)** 

 **![](https://img-blog.csdn.net/20180419154514194?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)** 

    4.sip 服务器注册用户的 usrname;
    
      5.sip 服务器注册用户的 password;
    
      6.sip 服务器的 IP 地址；
    
      7. 选择 UDP；
    
      9. 直接选择 Maybe later，其他不用管；

 ![](https://img-blog.csdn.net/20180419154534400?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

      10. 圆点变绿表示自己在线，才能和其他客户端通信；
    
      11. 自动填充的格式，IP 为 sip 服务器地址；
    
      添加联系人
    
     ![](https://img-blog.csdn.net/20180419154556971?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NjMxNTAz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
    
      2. 拨打用户的名称，不重要；
    
      3. 按格式填写，联系人的 sip 地址，ip 为 sip 服务器地址，5060 为默认端口；
    
      4.sip 服务器注册好的 sip 用户名称；
    
      按手机添加联系人理解

**4. 互相拨打电话测试**