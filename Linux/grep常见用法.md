grep [option] file

- -A -B -C 同时显示出匹配位置的n行上下文行内容 `-C 2` 等价于 `-A 2 -B 2`
- -c 只显示匹配的次数，不显示匹配的内容，等价于 `grep ‘xxx’ file |wc -l`
- -n 在输出的每行前面加上它所在的文件中它的行号
- -e 后跟基本正则表达式
- -r 递归地读每一目录下的所有文件。这样做和 `-d recurse` 选项等价
- -P 将模式 PATTERN 作为一个 Perl 正则表达式来解释
- -E 将模式 PATTERN 作为一个扩展的正则表达式来解释
- -i 忽略正则匹配的大小写
- -o 只显示匹配的行中与 PATTERN 相匹配的部分
- -z 在行尾禁用换行符，将其替换为空字符。也就是说，grep知道行尾是什么，但将输入视为一个大行
- -v 改变匹配的意义，只选择不匹配的行
- -m 最大匹配次数，在找到 NUM 个匹配的行之后，不再读这个文件
- -Pzo 使正则表达式适用于多行匹配



配合sed命令批量替换字符串

sed 用法

```sh
sed -i “s/oldstring/newstring/g” filename
sed -i “s/oldstring/newstring/g” grep oldstring -rl path
```

其中，oldstring是待被替换的字符串，newstring是待替换oldstring的新字符串，grep操作主要是按照所给的路径查找oldstring，path是所替换文件的路径；

-i 选项是直接在文件中替换，不在终端输出；

-r 选项是所给的path中的目录递归查找；

-l 选项是输出所有匹配到oldstring的文件；

```sh
# 将6替换为sk
sed -i “s/6/sk/g” grep 6 -rl /home/work/test/*.sh
```

### [linux 多行合并为一行](https://www.cnblogs.com/lishuaiqi/p/15102335.html)

1. xargs 

```sh
docker ps -a  | grep -v "CON" | awk '{print $1}' | xargs
```

2. sed

```sh
docker ps -a  | grep -v "CON" | awk '{print $1}' | sed ':a; N;s/\n/ /; ta'
```

N 代表两行合并一行,中间用\n替换, :a 做个标记, ta代表命令执行成功后会跳转到 :a, 所以这句话就是循环执行 N 并\n替换为空格来达到合并成一行的目的.

3. tr

```sh
docker ps -a  | grep -v "CON" | awk '{print $1}' | tr "\n" " "
```