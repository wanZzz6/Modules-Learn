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
**环境：Win10，Mysql8.0**

## 1. [下载路径](https://dev.mysql.com/downloads/mysql/)

## 2. [安装教程](https://blog.csdn.net/qq_34531925/article/details/78022905) 

为方便起见，建议将 C:\Program Files\MySQL\MySQL Server 8.0\bin 目录添加到 path 环境变量下。      

---

接下来有一个问题，data 默认安装到了 C 盘。随着数据库越来越大，这会导致 C 盘非常卡。**本文接下来，示例将数据库 data 移到 D 盘：**

## 3. 创建文件夹

  在D:\下新建 MysqlData 文件夹

## 4. 查看现在的data文件存放位置

从开始菜单打开`Mysql8.0 Command Line Client` 或者 从cmd输入以下命令进入mysql命令行

```sh
mysql -u root -p
然后输入密码，进入 mysql
```

进入 mysql 之后，通过如下命令查看 data 默认存储路径：

```sql
show variables like '%dir%';
```

如下所示：
可以看到我现在的数据存储路径是 `C:\ProgramData\MySQL\MySQL Server 8.0\Data`

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/20201202102559.png)


## 5. 停止Mysql 服务

通过管理员身份进入cmd控制台，输入: 

```sh
net stop mysql80
```

或者通过其他方式关闭服务都行

## 6. 迁移Data目录

将上面的`C:\ProgramData\MySQL\MySQL Server 8.0\Data` 路径下的所有文件**移动**到你刚创建的新的目录下


## 7. 修改 data 路径

 关闭 mysql 服务之后，修改 my.ini 文件。这个文件属于隐藏文件，需要去打开隐藏文件名。一般，my.ini 在这个路径下（`C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`）。你可以直接复制该路径，`Win + R，粘贴、回车`一气呵成,即可打开该文件

将 my.ini 文件的一个配置 改为：`datadir=D:/MysqlData`（`datadir=D:/MysqlData` 为上面创建的新存储路径， 注意斜杠不要反了）

## 7. 开启 mysql 服务

```
net start mysql80
```

大功告成
<!-- #endregion -->
