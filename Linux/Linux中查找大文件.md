## 使用`find`命令查找大文件

`find`命令是 Linux 系统管理员工具库中最强大的工具之一。它允许你根据不同的标准（包括文件大小）搜索文件和目录。
 例如，如果在当前工作目录中要搜索大小超过 100MB 的文件，请使用以下命令：

```sh
sudo find . -xdev -type f -size +100M
```

`.` 代表当前目录。如要搜索其它目录替换`.`为要搜索目录的路径。

输出将显示的文件列表，不会包含其它信息。

```
/var/lib/libvirt/images/centos-7-desktop_default.img
/var/lib/libvirt/images/bionic64_default.img
/var/lib/libvirt/images/winqcow2
/var/lib/libvirt/images/debian-9_default.img
/var/lib/libvirt/images/ubuntu-18-04-desktop_default.img
/var/lib/libvirt/images/centos-7_default.img
```

`find`命令还可以与其他命令结合使用，例如`ls`或`sort`对这些文件执行操作。

在下面的示例中，我们传递`find`命令的输出到`ls` ，`ls`将打印已找到的每个文件的大小，然后将将输出传递给`sort`命令，以根据文件大小的第 5 列对其进行排序。

```sh
find . -xdev -type f -size +100M -print | xargs ls -lh | sort -k5,5 -h -r
```

输出像这样：

```
-rw-------  1 root   root 40967M Jan  5 14:12 /var/lib/libvirt/images/winqcow2
-rw-------  1 root   root  3725M Jan  7 22:12 /var/lib/libvirt/images/debian-9_default.img
-rw-------  1 root   root  1524M Dec 30 07:46 /var/lib/libvirt/images/centos-7-desktop_default.img
-rw-------  1 root   root   999M Jan  5 14:43 /var/lib/libvirt/images/ubuntu-18-04-desktop_default.img
-rw-------  1 root   root   562M Dec 31 07:38 /var/lib/libvirt/images/centos-7_default.img
-rw-------  1 root   root   378M Jan  7 22:26 /var/lib/libvirt/images/bionic64_default.img
```

如果输出包含大量信息，你可以使用该`head`命令仅打印前 10 行：

```sh
find . -xdev -type f -size +100M -print | xargs ls -lh | sort -k5,5 -h -r | head
```

分解命令：`find . -xdev -type f -size +100M -print`

*   仅搜索当前工作目录（`.`）中的 文件 (`-type f`)，大于 100MB（`-size +100M`），不要查找其他文件系统上的目录（`-xdev`）并在标准输出上打印完整文件名，然后是新的一行（`-print`） 。
*   `xargs ls -lh`- `find`命令的输出通过管道`xargs`执行，`ls -lh`命令将以长列表可读格式打印输出。
*   `sort -k5,5 -h -r`- 基于第 5 列（`-k5,5`）对行进行排序，以可读格式（`-h`）的值并反转结果（`-r`）。
*   `head` ：仅打印管道输出的前 10 行。

> `find`命令带有许多强大的选项。例如，你可以搜索超过多少天的大文件，具有特定扩展名的大文件或属于特定用户的大文件。

### 使用`du`命令查找大文件和目录

`du`命令用于估计文件空间使用情况，对于查找占用大量磁盘空间的目录和文件特别有用。

以下命令将打印最大的文件和目录：

```sh
du -ahx . | sort -rh | head -5
```

第一列包含文件大小，第二列包含文件名：

```
55G    .
24G    ./.vagrant.d/boxes
24G    ./.vagrant.d
13G    ./Projects
2G    ./.minikube
```

命令说明：

*   `du -ahx .`：估算当前工作目录（`.`）中的磁盘空间使用情况，包括文件和目录（`a`），以比较接近人的常见可读格式打印大小（`h`）并跳过不同文件系统上的目录（`x`）。
*   `sort -rh`：通过可读格式（`-h`）的值并反转结果（`-r`）来对输出行进行排序。
*   `head -5` ：仅打印管道输出的前 5 行。



---

[Linux上查找最大文件的3种方法_无忧杂货铺的博客-CSDN博客_](https://blog.csdn.net/qq_41816540/article/details/103046568)

