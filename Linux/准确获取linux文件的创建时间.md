> 原文地址 [zhuanlan.zhihu.com](https://zhuanlan.zhihu.com/p/150235061)

**1. windows 与 linux 的文件创建时间**
------------------------------

在 windows 系统上，一个文件有 3 个时间属性，他们分别是

1.  创建时间
2.  修改时间
3.  访问时间

linux 上的文件也有三个时间属性，分别是

1.  访问时间（access time 简写为 atime）
2.  修改时间（modify time 简写为 mtime）
3.  状态修改时间 (change time 简写为 ctime)

很多人误将 linux 系统上文件的 ctime 对标成 windows 系统上的创建时间，这是不对的，ctime 里的字母 c 是 change 的缩写而非 create 的缩写。当文件的元数据发生变化时，ctime 就会发生改变，比如文件的权限，拥有者，所属的组，硬链接，当然也包括文件内容发生变化。

So，在 linux 系统上，无法获得文件的创建时间了么？这是一个复杂的问题，关于 linux 系统上为什么不记录文件的创建时间，有很多的讨论，有人认为文件的创建时间对于大多数人来说是无用的，可以用其他来代替：

*   如果文件没有修改过，就等于 mtime，即最后一次 write 时间
*   如果文件没有被修改权限过，就等于 ctime，即最后一次使用 chmod 的时间
*   如果文件没有被读取过，就等于 atime，即最后一个 read 的时间

这些理由我个人认为有些牵强，但现实的情况是，尽管 linux 没有提供创建时间，也没有影响大家使用，至少没有因为缺少创建时间导致谁的应用不可用，人们在程序设计上避开了文件的创建时间。

Linus 本人也对这个问题进行了深入的研究，windows 系统虽然提供了文件的创建时间，但是允许修改，Linus 认为这是 Unix ctime 概念的一种变体 ，因此建议修改 ctime 语义以适应 windows 情况，毕竟，很少有人使用 ctime。

但这种想法并未获得太多支持， 杰里米 · 艾里森（Jeremy Allison） 认为这将导致更可怕的混乱，宁愿意看到新增的表示创建时间的字段。

关于 linux 系统的文件创建时间的讨论，可以参考这篇文章 [File creation times](https://zhuanlan.zhihu.com/p/150235061/%20https://lwn.net/Articles/397442/%20)

**2. Ext4 的 crtime**
--------------------

一个令人惊喜的事实，如果文件系统的格式是 ext4， 那么会保存文件的创建时间，在 shell 里输入 df -T , 得到类似如下的结果

```
[root@pyhost ~]# df -T
Filesystem     Type     1K-blocks    Used Available Use% Mounted on
/dev/vda1      ext4      41151808 3078828  35959548   8% /
devtmpfs       devtmpfs    497108       0    497108   0% /dev
tmpfs          tmpfs       507704       0    507704   0% /dev/shm
tmpfs          tmpfs       507704     536    507168   1% /run
tmpfs          tmpfs       507704       0    507704   0% /sys/fs/cgroup
tmpfs          tmpfs       101544       0    101544   0% /run/user/0
```

想要得到文件的创建时间，只需要两个步骤

**步骤 1， 获得文件的 inode**

```
[root@pyhost ~]# ls -i 1.txt 
269710 1.txt
```

**步骤 2， 使用 debugfs**

```
[root@pyhost ~]# debugfs -R 'stat <269710>' /dev/vda1
debugfs 1.42.9 (28-Dec-2013)
Inode: 269710   Type: regular    Mode:  0777   Flags: 0x80000
Generation: 1404159711    Version: 0x00000000:00000001
User:     0   Group:     0   Size: 6
File ACL: 0    Directory ACL: 0
Links: 1   Blockcount: 8
Fragment:  Address: 0    Number: 0    Size: 0
 ctime: 0x5eec2951:296cbae4 -- Fri Jun 19 10:56:17 2020
 atime: 0x5eec2953:6ca8a4dc -- Fri Jun 19 10:56:19 2020
 mtime: 0x5eec2951:27fe84e4 -- Fri Jun 19 10:56:17 2020
crtime: 0x5eeb81e8:6361f8bc -- Thu Jun 18 23:02:00 2020
Size of extra inode fields: 28
EXTENTS:
(0):2171448
```

crtime 就是文件的创建时间，以上操作需要使用 sudo 权限。

以上实验过程，使用的是阿里云服务器，系统是 centos， 这里有一处怪异之处必须告诉各位读者，或许是由于阿里云服务器并非物理机，导致上述实验方法并不总是准确，如果新建一个文件，然后立即对其进行修改等操作，那么 crtime 也会随之发生变化，而非期望中的始终保存创建时间，因此在实验时，新建文件后，间隔一段时间后再对其进行修改操作来验证 crtime 是否准确，以我的经历来看，间隔一个小时足矣。

**3. python 获取 linux 文件创建时间**
-----------------------------

第二小节已经给出了获取文件创建时间的方法，这样，使用 python 来实现并不是什么难事，使用 subprocess.Popen 来执行命令即可，而且已经有开源库实现了这个功能，我们安装好以后直接使用就可以了, [crtime 的 Python 项目详细描述](https://zhuanlan.zhihu.com/p/150235061/%20https://www.cnpython.com/pypi/crtime%20) 是这个开源库的说明文档，包含了安装方法和使用示例，不过特别注意一点，他所提供的示例代码无法正常执行

```python
from crtime import get_crtimes_in_dir

for fname, date in get_crtimes_in_dir(".", raise_on_error=True, as_epoch=False):
    print(fname, date)
```

get_crtimes_in_dir 函数的第一个参数是文件目录，他给的示例代码用了相对路径，这导致无法获取文件的 crtime， 这里必须使用绝对路径。

作者的设计思路，是批量获取文件的 crtime， get_crtimes_in_dir 获取指定目录下的所有文件的 crtime， 如果你想获取单个文件的，使用 get_crtimes 方法，传入一个列表，列表里存放单个文件的绝对路径，切记，用绝对路径。