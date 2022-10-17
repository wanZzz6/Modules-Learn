什么是正则表达式？
---------

正则表达式（Regular Expression）通常被用来检索、替换那些符合某个模式 (规则) 的文本。

此处的 Regular 即是规则、规律的意思，Regular Expression 即 “描述某种规则的表达式” 之意。

本文收集了一些常见的正则表达式用法，方便大家查询取用，并在最后附了详细的正则表达式语法手册。

案例包括：**「邮箱、身份证号、手机号码、固定电话、域名、IP 地址、日期、邮编、密码、中文字符、数字、字符串」**

Python 如何支持正则？
--------------

我用的是 python 来实现正则，并使用 Jupyter Notebook 编写代码。

Python 通过 re 模块支持正则表达式，re 模块使 Python 语言拥有全部的正则表达式功能。

这里要注意两个函数的使用：

`re.compile`用于编译正则表达式，生成一个正则表达式（ Pattern ）对象;

`.findall`用于在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。

```python
# 导入re模块
import re
```

1. 邮箱
-----

包含大小写字母，下划线，阿拉伯数字，点号，中划线  

表达式：

`[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)`

案例：

```python
pattern = re.compile(r"[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)")

strs = '我的私人邮箱是zhuwjwh@outlook.com，公司邮箱是123456@qq.org，麻烦登记一下？'
result = pattern.findall(strs)

print(result)
```

```
['zhuwjwh@outlook.com', '123456@qq.org']
```

2. 身份证号
-------

xxxxxx yyyy MM dd 375 0     十八位

*   地区：[1-9]\d{5}  
    
*   年的前两位：(18|19|([23]\d))       1800-2399  
    
*   年的后两位：\d{2}  
    
*   月份：((0[1-9])|(10|11|12))  
    
*   天数：(([0-2][1-9])|10|20|30|31)          闰年不能禁止 29+  
    
*   三位顺序码：\d{3}  
    
*   两位顺序码：\d{2}  
    
*   校验码：[0-9Xx]  
    

表达式：

`[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]`

案例：

```python
pattern = re.compile(r"[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]")

strs = '小明的身份证号码是342623198910235163，手机号是13987692110'
result = pattern.findall(strs)

print(result)
```

```
['342623198910235163']
```

3. 国内手机号码
---------

手机号都为 11 位，且以 1 开头，第二位一般为 3、5、6、7、8、9 ，剩下八位任意数字  
例如：13987692110、15610098778  

表达式：

`1(3|4|5|6|7|8|9)\d{9}`

案例：

```python
pattern = re.compile(r"1[356789]\d{9}")

strs = '小明的手机号是13987692110，你明天打给他'
result = pattern.findall(strs)

print(result)
```

```
['13987692110']
```

4. 国内固定电话
---------

区号 3~4 位，号码 7~8 位  

例如：0511-1234567、021-87654321  

表达式：

`\d{3}-\d{8}|\d{4}-\d{7}`

案例：

```python
pattern = re.compile(r"\d{3}-\d{8}|\d{4}-\d{7}")

strs = '0511-1234567是小明家的电话，他的办公室电话是021-87654321'
result = pattern.findall(strs)

print(result)
```

```
['0511-1234567', '021-87654321']
```

5. 域名
-----

包含 http:\\ 或 https:\\

表达式：

`(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)`

案例：

```python
pattern = re.compile(r"(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)")

strs = 'Python官网的网址是https://www.python.org/'
result = pattern.findall(strs)

print(result)
```

```
['https://www.python.org/']
```

6. IP 地址
--------

IP 地址的长度为 32 位 (共有 2^32 个 IP 地址)，分为 4 段，每段 8 位，用十进制数字表示  
每段数字范围为 0～255，段与段之间用句点隔开　  

表达式：

`((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))`

案例：

```python
pattern = re.compile(r"((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))")

strs = '''请输入合法IP地址，非法IP地址和其他字符将被过滤！
增、删、改IP地址后，请保存、关闭记事本！
192.168.8.84
192.168.8.85
192.168.8.86
0.0.0.1
256.1.1.1
192.256.256.256
192.255.255.255
aa.bb.cc.dd'''

result = pattern.findall(strs)

print(result)
```

```
['192.168.8.84', '192.168.8.85', '192.168.8.86', '0.0.0.1', '56.1.1.1', '192.255.255.255']
```

7. 日期
-----

常见日期格式：yyyyMMdd、yyyy-MM-dd、yyyy/MM/dd、yyyy.MM.dd

表达式：

`\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}`

案例：

```python
pattern = re.compile(r"\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}")

strs = '今天是2020/12/20，去年的今天是2019.12.20，明年的今天是2021-12-20'
result = pattern.findall(strs)

print(result)
```

```python
['2020/12/20', '2019.12.20', '2021-12-20']
```

8. 国内邮政编码
---------

我国的邮政编码采用四级六位数编码结构  
前两位数字表示省（直辖市、自治区）  
第三位数字表示邮区；第四位数字表示县（市）  
最后两位数字表示投递局（所）  

表达式：

`[1-9]\d{5}(?!\d)`

案例：

```python
pattern = re.compile(r"[1-9]\d{5}(?!\d)")

strs = '上海静安区邮编是200040'
result = pattern.findall(strs)

print(result)
```

```python
['200040']
```

9. 密码
-----

密码 (以字母开头，长度在 6~18 之间，只能包含字母、数字和下划线)

表达式：

`[a-zA-Z]\w{5,17}`

强密码 (以字母开头，必须包含大小写字母和数字的组合，不能使用特殊字符，长度在 8-10 之间)

表达式：

`[a-zA-Z](?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}`

```python
pattern = re.compile(r"[a-zA-Z]\w{5,17}")

strs = '密码：q123456_abc'
result = pattern.findall(strs)

print(result)
```

```
['q123456_abc']
```

```python
pattern = re.compile(r"[a-zA-Z](?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}")

strs = '强密码：q123456ABc，弱密码：q123456abc'
result = pattern.findall(strs)
p
print(result)
```

```
['q123456ABc，']
```

10. 中文字符
--------

表达式：

`[\u4e00-\u9fa5]`

案例：

```python
pattern = re.compile(r"[\u4e00-\u9fa5]")

strs = 'apple：苹果'
result = pattern.findall(strs)

print(result)
```

```
['苹', '果']
```

11. 数字
------

*   验证数字：`^[0-9]*$`
    
*   验证 n 位的数字：`^\d{n}$`
    
*   验证至少 n 位数字：`^\d{n,}$`
    
*   验证 m-n 位的数字：`^\d{m,n}$`
    
*   验证零和非零开头的数字：`^(0|[1-9][0-9]*)$`
    
*   验证有两位小数的正实数：`^[0-9]+(.[0-9]{2})?$`
    
*   验证有 1-3 位小数的正实数：`^[0-9]+(.[0-9]{1,3})?$`
    
*   验证非零的正整数：`^\+?[1-9][0-9]*$`
    
*   验证非零的负整数：`^\-[1-9][0-9]*$`
    
*   验证非负整数（正整数 + 0） `^\d+$`
    
*   验证非正整数（负整数 + 0） `^((-\d+)|(0+))$`
    
*   整数：`^-?\d+$`
    
*   非负浮点数（正浮点数 + 0）：`^\d+(\.\d+)?$`
    
*   正浮点数 `^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$`
    
*   非正浮点数（负浮点数 + 0） `^((-\d+(\.\d+)?)|(0+(\.0+)?))$`
    
*   负浮点数 `^(-(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*)))$`
    
*   浮点数 `^(-?\d+)(\.\d+)?$`
    

12. 字符串
-------

*   英文和数字：`^[A-Za-z0-9]+$ 或 ^[A-Za-z0-9]{4,40}$`
    
*   长度为 3-20 的所有字符：`^.{3,20}$`
    
*   由 26 个英文字母组成的字符串：`^[A-Za-z]+$`
    
*   由 26 个大写英文字母组成的字符串：`^[A-Z]+$`
    
*   由 26 个小写英文字母组成的字符串：`^[a-z]+$`
    
*   由数字和 26 个英文字母组成的字符串：`^[A-Za-z0-9]+$`
    
*   由数字、26 个英文字母或者下划线组成的字符串：`^\w+$ 或 ^\w{3,20}$`
    
*   中文、英文、数字包括下划线：`^[\u4E00-\u9FA5A-Za-z0-9_]+$`
    
*   中文、英文、数字但不包括下划线等符号：`^[\u4E00-\u9FA5A-Za-z0-9]+$ 或 ^[\u4E00-\u9FA5A-Za-z0-9]{2,20}$`
    
*   可以输入含有 ^%&',;=?$\” 等字符：`[^%&',;=?$\x22]+`
    
*   禁止输入含有~ 的字符：`[^~\x22]+`
    

附：正则表达式语法详解
-----------

<table><thead><tr><th>字符</th><th>描述</th></tr></thead><tbody><tr><td><code>\</code></td><td>将下一个字符标记为一个特殊字符（File Format Escape，清单见本表）、或一个原义字符（Identity Escape，有 ^$()*+?.[{| 共计 12 个)、或一个向后引用（backreferences）、或一个八进制转义符。例如，“<code>n</code>” 匹配字符 “<code>n</code>”。“<code>\n</code>” 匹配一个换行符。序列 “<code>\\</code>” 匹配 “<code>\</code>” 而 “<code>\(</code>” 则匹配 “<code>(</code>”。</td></tr><tr><td><code>^</code></td><td>匹配输入字符串的开始位置</td></tr><tr><td><code>$</code></td><td>匹配输入字符串的结束位置</td></tr><tr><td><code>*</code></td><td>匹配前面的子表达式零次或多次。例如，zo * 能匹配 “<code>z</code>”、“<code>zo</code>” 以及 “<code>zoo</code>”。* 等价于 {0,}。</td></tr><tr><td><code>+</code></td><td>匹配前面的子表达式一次或多次。例如，“<code>zo+</code>” 能匹配 “<code>zo</code>” 以及 “<code>zoo</code>”，但不能匹配 “<code>z</code>”。+ 等价于 {1,}。</td></tr><tr><td><code>?</code></td><td>匹配前面的子表达式零次或一次。例如，“<code>do(es)?</code>” 可以匹配 “<code>does</code>” 中的 “<code>do</code>” 和 “<code>does</code>”。? 等价于 {0,1}。</td></tr><tr><td><code>{n}</code></td><td>n 是一个非负整数。匹配确定的 n 次。例如，“<code>o{2}</code>” 不能匹配 “<code>Bob</code>” 中的 “<code>o</code>”，但是能匹配 “<code>food</code>” 中的两个 o。</td></tr><tr><td><code>{n,}</code></td><td>n 是一个非负整数。至少匹配 n 次。例如，“<code>o{2,}</code>” 不能匹配 “<code>Bob</code>” 中的 “<code>o</code>”，但能匹配 “<code>foooood</code>” 中的所有 o。“<code>o{1,}</code>” 等价于 “<code>o+</code>”。“<code>o{0,}</code>” 则等价于 “<code>o*</code>”。</td></tr><tr><td><code>{n,m}</code></td><td>m 和 n 均为非负整数，其中 n&lt;=m。最少匹配 n 次且最多匹配 m 次。例如，“<code>o{1,3}</code>” 将匹配 “<code>fooooood</code>” 中的前三个 o。“<code>o{0,1}</code>” 等价于 “<code>o?</code>”。请注意在逗号和两个数之间不能有空格。</td></tr><tr><td><code>?</code></td><td>非贪心量化（Non-greedy quantifiers）：当该字符紧跟在任何一个其他重复修饰符（*,+,?，{n}，{n,}，{n,m}）后面时，匹配模式是<strong>「非」</strong>贪婪的。非贪婪模式尽可能少的匹配所搜索的字符串，而默认的贪婪模式则尽可能多的匹配所搜索的字符串。例如，对于字符串 “<code>oooo</code>”，“<code>o+?</code>” 将匹配单个 “<code>o</code>”，而 “<code>o+</code>” 将匹配所有 “<code>o</code>”。</td></tr><tr><td><code>.</code></td><td>匹配除 “<code>\r</code>”“<code>\n</code>” 之外的任何单个字符。要匹配包括 “<code>\r</code>”“<code>\n</code>” 在内的任何字符，请使用像 “<code>(.\|\r\|\n)</code>” 的模式。</td></tr><tr><td><code>(pattern)</code></td><td>匹配 pattern 并获取这一匹配的子字符串。该子字符串用于向后引用。所获取的匹配可以从产生的 Matches 集合得到，在 VBScript 中使用 SubMatches 集合，在 JScript 中则使用 $0…$9 属性。要匹配圆括号字符，请使用 “<code>\(</code>” 或 “<code>\)</code>”。可带数量后缀。</td></tr><tr><td><code>(?:pattern)</code></td><td>匹配 pattern 但不获取匹配的子字符串（shy groups），也就是说这是一个非获取匹配，不存储匹配的子字符串用于向后引用。这在使用或字符 “<code>(\|)</code>” 来组合一个模式的各个部分是很有用。例如 “<code>industr(?:y\|ies)</code>” 就是一个比 “<code>industry\|industries</code>” 更简略的表达式。</td></tr><tr><td><code>(?=pattern)</code></td><td>正向肯定预查（look ahead positive assert），在任何匹配 pattern 的字符串开始处匹配查找字符串。这是一个非获取匹配，也就是说，该匹配不需要获取供以后使用。例如，“<code>Windows(?=95\|98\|NT\|2000)</code>” 能匹配 “<code>Windows2000</code>” 中的 “<code>Windows</code>”，但不能匹配 “<code>Windows3.1</code>” 中的 “<code>Windows</code>”。预查不消耗字符，也就是说，在一个匹配发生后，在最后一次匹配之后立即开始下一次匹配的搜索，而不是从包含预查的字符之后开始。</td></tr><tr><td><code>(?!pattern)</code></td><td>正向否定预查（negative assert），在任何不匹配 pattern 的字符串开始处匹配查找字符串。这是一个非获取匹配，也就是说，该匹配不需要获取供以后使用。例如 “<code>Windows(?!95\|98\|NT\|2000)</code>” 能匹配 “<code>Windows3.1</code>” 中的 “<code>Windows</code>”，但不能匹配 “<code>Windows2000</code>” 中的 “<code>Windows</code>”。预查不消耗字符，也就是说，在一个匹配发生后，在最后一次匹配之后立即开始下一次匹配的搜索，而不是从包含预查的字符之后开始</td></tr><tr><td><code>(?&lt;=pattern)</code></td><td>反向（look behind）肯定预查，与正向肯定预查类似，只是方向相反。例如，“<code>(?&lt;=95\|98\|NT\|2000)Windows</code>” 能匹配 “<code>2000Windows</code>” 中的 “<code>Windows</code>”，但不能匹配 “<code>3.1Windows</code>” 中的 “<code>Windows</code>”。</td></tr><tr><td><code>(?&lt;!pattern)</code></td><td>反向否定预查，与正向否定预查类似，只是方向相反。例如 “<code>(?&lt;!95\|98\|NT\|2000)Windows</code>” 能匹配 “<code>3.1Windows</code>” 中的 “<code>Windows</code>”，但不能匹配 “<code>2000Windows</code>” 中的 “<code>Windows</code>”。</td></tr><tr><td><code>x\|y</code></td><td>没有包围在 () 里，其范围是整个正则表达式。例如，“<code>z\|food</code>” 能匹配 “<code>z</code>” 或 “<code>food</code>”。“<code>(?:z\|f)ood</code>” 则匹配 “<code>zood</code>” 或 “<code>food</code>”。</td></tr><tr><td><code>[xyz]</code></td><td>字符集合（character class）。匹配所包含的任意一个字符。例如，“<code>[abc]</code>” 可以匹配 “<code>plain</code>” 中的 “<code>a</code>”。特殊字符仅有反斜线 \ 保持特殊含义，用于转义字符。其它特殊字符如星号、加号、各种括号等均作为普通字符。脱字符 ^ 如果出现在首位则表示负值字符集合；如果出现在字符串中间就仅作为普通字符。连字符 - 如果出现在字符串中间表示字符范围描述；如果如果出现在首位（或末尾）则仅作为普通字符。右方括号应转义出现，也可以作为首位字符出现。</td></tr><tr><td><code>[^xyz]</code></td><td>排除型字符集合（negated character classes）。匹配未列出的任意字符。例如，“<code>[^abc]</code>” 可以匹配 “<code>plain</code>” 中的 “<code>plin</code>”。</td></tr><tr><td><code>[a-z]</code></td><td>字符范围。匹配指定范围内的任意字符。例如，“<code>[a-z]</code>” 可以匹配 “<code>a</code>” 到 “<code>z</code>” 范围内的任意小写字母字符。</td></tr><tr><td><code>[^a-z]</code></td><td>排除型的字符范围。匹配任何不在指定范围内的任意字符。例如，“<code>[^a-z]</code>” 可以匹配任何不在 “<code>a</code>” 到 “<code>z</code>” 范围内的任意字符。</td></tr><tr><td><code>[:name:]</code></td><td>增加命名字符类（named character class）中的字符到表达式。只能用于<strong>「方括号表达式」</strong>。</td></tr><tr><td><code>[=elt=]</code></td><td>增加当前 locale 下排序（collate）等价于字符 “elt” 的元素。例如，[=a=]可能会增加 ä、á、à、ă、ắ、ằ、ẵ、ẳ、â、ấ、ầ、ẫ、ẩ、ǎ、å、ǻ、ä、ǟ、ã、ȧ、ǡ、ą、ā、ả、ȁ、ȃ、ạ、ặ、ậ、ḁ、ⱥ、ᶏ、ɐ、ɑ 。只能用于方括号表达式。</td></tr><tr><td><code>[.elt.]</code></td><td>增加排序元素 elt 到表达式中。这是因为某些排序元素由多个字符组成。例如，29 个字母表的西班牙语， "CH" 作为单个字母排在字母 C 之后，因此会产生如此排序 “cinco, credo, chispa”。只能用于方括号表达式。</td></tr><tr><td><code>\b</code></td><td>匹配一个单词边界，也就是指单词和空格间的位置。例如，“<code>er\b</code>” 可以匹配 “<code>never</code>” 中的 “<code>er</code>”，但不能匹配 “<code>verb</code>” 中的 “<code>er</code>”。</td></tr><tr><td><code>\B</code></td><td>匹配非单词边界。“<code>er\B</code>” 能匹配 “<code>verb</code>” 中的 “<code>er</code>”，但不能匹配 “<code>never</code>” 中的 “<code>er</code>”。</td></tr><tr><td><code>\cx</code></td><td>匹配由 x 指明的控制字符。x 的值必须为<code>A-Z</code>或<code>a-z</code>之一。否则，将 c 视为一个原义的 “<code>c</code>” 字符。控制字符的值等于 x 的值最低 5 比特（即对 32<sub>10 进制</sub>的余数）。例如，\cM 匹配一个 Control-M 或回车符。\ca 等效于 \ u0001, \cb 等效于 \ u0002, 等等…</td></tr><tr><td><code>\d</code></td><td>匹配一个数字字符。等价于 [0-9]。注意 Unicode 正则表达式会匹配全角数字字符。</td></tr><tr><td><code>\D</code></td><td>匹配一个非数字字符。等价于 [^0-9]。</td></tr><tr><td><code>\f</code></td><td>匹配一个换页符。等价于 \ x0c 和 \ cL。</td></tr><tr><td><code>\n</code></td><td>匹配一个换行符。等价于 \ x0a 和 \ cJ。</td></tr><tr><td><code>\r</code></td><td>匹配一个回车符。等价于 \ x0d 和 \ cM。</td></tr><tr><td><code>\s</code></td><td>匹配任何空白字符，包括空格、制表符、换页符等等。等价于 [\f\n\r\t\v]。注意 Unicode 正则表达式会匹配全角空格符。</td></tr><tr><td><code>\S</code></td><td>匹配任何非空白字符。等价于 [^ \f\n\r\t\v]。</td></tr><tr><td><code>\t</code></td><td>匹配一个制表符。等价于 \ x09 和 \ cI。</td></tr><tr><td><code>\v</code></td><td>匹配一个垂直制表符。等价于 \ x0b 和 \ cK。</td></tr><tr><td><code>\w</code></td><td>匹配包括下划线的任何单词字符。等价于 “<code>[A-Za-z0-9_]</code>”。注意 Unicode 正则表达式会匹配中文字符。</td></tr><tr><td><code>\W</code></td><td>匹配任何非单词字符。等价于 “<code>[^A-Za-z0-9_]</code>”。</td></tr><tr><td><code>\xnn</code></td><td>十六进制转义字符序列。匹配两个十六进制数字 nn 表示的字符。例如，“<code>\x41</code>” 匹配 “<code>A</code>”。“<code>\x041</code>” 则等价于 “<code>\x04&amp;1</code>”。正则表达式中可以使用 ASCII 编码。.</td></tr><tr><td><code>\num</code></td><td>向后引用（back-reference）一个子字符串（substring），该子字符串与正则表达式的第 num 个用括号围起来的捕捉群（capture group）子表达式（subexpression）匹配。其中 num 是从 1 开始的十进制正整数，其上限可能是 9、31、99，甚至无限。例如：“<code>(.)\1</code>” 匹配两个连续的相同字符。</td></tr><tr><td><code>\n</code></td><td>标识一个八进制转义值或一个向后引用。如果 \ n 之前至少 n 个获取的子表达式，则 n 为向后引用。否则，如果 n 为八进制数字（0-7），则 n 为一个八进制转义值。</td></tr><tr><td><code>\nm</code></td><td>3 位八进制数字，标识一个八进制转义值或一个向后引用。如果 \ nm 之前至少有 nm 个获得子表达式，则 nm 为向后引用。如果 \ nm 之前至少有 n 个获取，则 n 为一个后跟文字 m 的向后引用。如果前面的条件都不满足，若 n 和 m 均为八进制数字（0-7），则 \ nm 将匹配八进制转义值 nm。</td></tr><tr><td><code>\nml</code></td><td>如果 n 为八进制数字（0-3），且 m 和 l 均为八进制数字（0-7），则匹配八进制转义值 nml。</td></tr><tr><td><code>\un</code></td><td>Unicode 转义字符序列。其中 n 是一个用四个十六进制数字表示的 Unicode 字符。例如，\u00A9 匹配著作权符号（©）。</td></tr></tbody></table>

优先权
---

<table><thead><tr><th>优先权</th><th>符号</th></tr></thead><tbody><tr><td>最高</td><td><code>\</code></td></tr><tr><td>高</td><td><code>()</code>、<code>(?:)</code>、<code>(?=)</code>、<code>[]</code></td></tr><tr><td>中</td><td><code>*</code>、<code>+</code>、<code>?</code>、<code>{n}</code>、<code>{n,}</code>、<code>{n,m}</code></td></tr><tr><td>低</td><td><code>^</code>、<code>$</code>、中介字符</td></tr><tr><td>次最低</td><td>串接，即相邻字符连接在一起</td></tr><tr><td>最低</td><td><code>\|</code></td></tr></tbody></table>
