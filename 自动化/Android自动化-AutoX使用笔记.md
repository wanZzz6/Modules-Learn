# AutoX.js 使用笔记

未完待续。。。。

>[autoxjs](http://doc.autoxjs.com/#/)
>
>[webpack-autojs](https://github.com/kkevsekk1/webpack-autojs)
>
>[auto.pro](https://github.com/molysama/auto.pro)

## 一、前言

随着 AutoJS Pro 9 的塌房，我也第一次体验到什么叫做“正版软件受害者”，只怪自己经验不足，图一时爽快，被 Pro 版看似强大的功能所吸引，其实免费版本的就够用了。

以后选择框架时有开源版本绝不用闭源，前期开发阶段还好说，等代码写的差不多了，你告诉我突然不能用了，我真是···*～● 凸(艹皿艹 ) 

![](https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/%E9%80%80%E9%92%B1.gif)



AutoX 是基于 AutoJs 4.1 的社区开发版，基本兼容AutoJs，虽不能像 Pro 版那样及时修复bug，但是如果你能找到bug所在，可以提Pr解决，无后顾之忧，还可以自己丰富 AutoX 的功能，从而成为该项目的贡献者。

因本人之前详细阅读过 AutoJs Pro 版的文档，也做了一篇博客笔记 [Android自动化-AutoJs Pro v9使用教程（一）.md](./Android自动化-AutoJs Pro v9使用教程（一）.md)（第二篇已删除，彻底放弃Pro），网上也有不少其Autojs的教程博客可参考，所以不会对模块的基本用法再详细介绍，本文仅作为自己的学习笔记，查漏补缺使用。



我按照功能类别和重要程度重新划分了目录结构，仅供参考。



## 二、环境搭建

我在日常前端开发和 Auto js Pro9 中习惯了使用 ES6语法，转到 AutoX 的原生js开发有点不习惯，好在官方给了工程化开发模板：[webpack-autojs](https://github.com/kkevsekk1/webpack-autojs)，参考该项目 README 文档，初始化一个支持ts、es6、vue等特性的项目还是很简单的，再配合插件可以做到开发环境热部署，非常方便。

- 手机上安装 Autox：[Releases · kkevsekk1/AutoX ](https://github.com/kkevsekk1/AutoX/releases)

- 安装VScode 插件：[Auto.js-Autox.js-VSCodeExt ](https://marketplace.visualstudio.com/items?itemName=aaroncheng.auto-js-vsce-fixed)

- 克隆项目

  ```shell
  npm i -g webpack webpack-cli --registry=https://registry.npm.taobao.org
  git clone https://github.com/kkevsekk1/webpack-autojs.git --depth 1
  cd webpack-autojs
  npm install --registry=https://registry.npm.taobao.org
  
  # 用vscode 打开该文件夹
  code .
  ```

- vscode 中按下 `Ctrl+Shift+P`，输入 `autoxjs`，找到”开启服务。。。。“

- 手机端打开Autox，并在左侧菜单中点击连接电脑，输入电脑的IP地址

- 开发环境下运行 `npm run start`，会在目录下生成一个 dist 文件夹，里面存放 webpack 打包编译过的文件（项目初始化时里面有几个示例项目，打包哪个项目需要在`scriptConfig.js` 中配置，具体看注释），在dist目中录找一个打包过的js主程序，右键选择 `重新运行`，手机端便会运行该示例项目，`./work` 目录存放的就是项目源码，你可以尝试修改项目文件，点击保存后会自动打包并重新运行（热部署）。

- 完整过程：[优酷视频讲解](https://v.youku.com/v_show/id_XNDg2NjA3NTYyMA==.html)  

<img src="https://md-picture-1254350681.cos.ap-beijing.myqcloud.com/autox-init.png" alt="image-20230319234843453" style="zoom:50%;" />

👍[autoX-webpack-template](https://github.com/wanZzz6/autoX-webpack-template)：我在用 webpack-autojs 时遇到点bug，总是不能自动上传运行，暂时不知道哪的问题，所以自己稍加修改定制了一个项目模板，欢迎大家测试使用。

[使用 vue 作为 UI ](http://auto.moly.host/index.html#/example/vue)  

## 三、基础模块

### 1. 全局变量与函数

#### sleep()

本质是 `java.lang.Thread.sleep(millis);`

会阻塞**当前线程**，**当前线程**，**当前线程**！

如不想阻塞，可以启用[协程](#async) 或`Promise`特性。


#### getClip() 

Android 10以上限制了应用的后台剪贴板内容获取行为, 只有当前界面获得焦点后（onResume）才能获取到剪切板内容

我们创造一个有焦点的悬浮窗, 就可以获取剪贴板内容了：
~~并且要开启前台服务~~

```js
if (!floaty.checkPermission()) {
  toast('本脚本需要悬浮窗权限来显示悬浮窗');
  floaty.requestPermission();
  exit();
}

events.on('exit', function () {
  floaty.closeAll(); // 关闭所有本脚本的悬浮窗。
  console.log('onExit');
});

const _window = floaty.window(<frame visibility="invisible"></frame>);

function myGetClip() {
  const result = threads.disposable();
  ui.run(function () {
    _window.requestFocus();
    setTimeout(() => {
      result.setAndNotify(getClip());
      _window.disableFocus();
    }, 1);
  });
  return result.blockedGet();
}

console.log(myGetClip());
sleep(5000);
console.log(myGetClip());
```



#### toast(message)

需要提前打开AutoX 的**后台弹窗权限**或者通知权限，否则在AutoX后台运行时看不到弹框。

以气泡显示信息message几秒，具体时间取决于安卓系统，一般都是2秒。

注意，**信息的显示是"异步"执行的**，并且，不会等待信息消失程序才继续执行。如果在循环中执行该命令，可能出现脚本停止运行后仍然有不断的气泡信息出现的情况。



#### context

`android.content.Context`对象。

注意该对象为`ApplicationContext`，不能用于界面、对话框等的创建。



### 2. App

- 获取应用版本
- 启动、卸载应用
- 打开应用设置
- 获取 packageName
- 快速预览、编辑文件
- 用浏览器打开网站url
- 发送邮件
- 意图Intent

  可以与其他应用传递消息，快速打开页面
  属于比较高级的内容，先得了解[安卓Intent](https://www.baidu.com/s?wd=android Intent)，按需阅读，或者直接搜索所需的相关代码，`CTRL+C，CTRL+V`

  - `startActivity(options)`：构造一个Intent，并启动该Activity
  - `sendBroadcast(options)`：发送广播
  - `startService(options)`：构造一个Intent，并启动该服务。

### 3. 设备-Device

基本上能获取到手机的 设置->关于手机 页面显示的所有信息。

- 屏幕宽、高，导航栏高度、设备品牌、型号等
- Android 版本、Mac地址、IMEI（从Android 10开始，应用不再有权限获取IMEI）
- 屏幕亮度、音量、电量、充电状态、内存状态、震动等

```js
console.show();

var str = '';
str += '屏幕宽度:' + device.width;
str += '\n屏幕高度:' + device.height;
str += '\nbuildId:' + device.buildId;
str += '\n主板:' + device.board;
str += '\n制造商:' + device.brand;
str += '\n型号:' + device.model;
str += '\n产品名称:' + device.product;
str += '\nbootloader版本:' + device.bootloader;
str += '\n硬件名称:' + device.hardware;
str += '\n唯一标识码:' + device.fingerprint;
try {
  str += '\nIMEI: ' + device.getIMEI();
} catch (error) {
  str += '\nIMEI: 无权限获取';
}
str += '\nAndroidId: ' + device.getAndroidId();
str += '\nMac: ' + device.getMacAddress();
str += '\nAPI: ' + device.sdkInt;
str += '\n电量: ' + device.getBattery();
str += '\n是否有虚拟导航: ' + device.checkDeviceHasNavigationBar();
str += '\n虚拟导航高度: ' + device.getVirtualBarHeigh();
log(str);
```



#### 唤醒设备

- `device.wakeUp()`：唤醒设备，可以用来点亮屏幕。
- `device.wakeUpIfNeeded()`：如果屏幕没有点亮，则唤醒设备。

#### 屏幕常亮

- `device.keepScreenOn([timeout])`：屏幕保持常亮的时间, 单位毫秒。如果不加此参数，则一直保持屏幕常亮。
- `device.keepScreenDim([timeout])`：保持屏幕常亮，但允许屏幕变暗来节省电量。此函数可以用于定时脚本唤醒屏幕操作，不需要用户观看屏幕，可以让屏幕变暗来节省电量。
- `device.cancelKeepingAwake()`：取消设备保持唤醒状态。

使设备在**无人操作的情况下**保持屏幕常亮；同时，**如果此函数调用时屏幕没有点亮，则会唤醒屏幕**。

最好设置timeout参数（毫秒）

```js
//一直保持屏幕常亮
device.keepScreenOn(365 * 24 * 3600 * 1000)
```

### 4. 文件系统

文件、路径的操作。  

一次性的文件读写可以直接使用`files.read()`, `files.write()`, `files.append()`等方便的函数，但如果需要频繁读写或随机读写，则使用`open()`函数打开一个文件对象来操作文件，并在操作完毕后调用`close()`函数关闭文件。

- 路径拼接：`join()`
- 获取当前工作路径：`cwd()`
- 列出文件，支持过滤函数：`listDir(path[, filter])`
- 打开一个文件：`open()`，类似于 python 的 `open()` 函数，返回一个可读(写)的文件流对象，退出前记得调用 `close()` 关闭对象

### 5. 本地存储-Storage

可用于保存用户配置、运行缓存等数据。  

保存的数据除非应用被卸载或者被主动删除，否则会一直保留。  

可存放任何可以用 `JSON.stringify` 序列化的数据类型，`undefined` 除外。



storages保存的数据在脚本之间是共享的，任何脚本只要知道storage名称便可以获取到相应的数据，可作为跨进程通信的方式。

**不要用常见的单词做Storage名字，避免脚本之间的数据存取发生冲突**。



当然，此特性也可作为脚本间**跨进程通信**的方式。

### 6. 控制台输出

能按日志等级区分出不同颜色输出调试信息、中间结果等。  

能使用部分与浏览器中相同功能的API方法：`assert()`、`time()`、`trace()`、`input()`



**使用建议：**

- 在基于坐标的操作中不建议展示控制台，会干扰截图区域，或者通过调整位置和大小将其放置于合理位置。

- 当程序发生异常时可使其主动弹出展示错误栈。
- 若脚本需长期运行或运行中会打印大量日志，请务必配置:`setMaxLines()`最大行数、`setGlobalLogConfig()`: 日志文件位置、大小、日志级别、备份数量，甚至日志格式[PatternLayout](http://logging.apache.org/log4j/1.2/apidocs/org/apache/log4j/PatternLayout.html)，见下文[日志文件](#logger)

### 7. 定时器

用法与浏览器中的API一致，只是内部实现方式不同，这个我们无需关心。

包括：`setInterval`、`setTimeout`、`setImmediate`， 以及对应的取消函数 `clearInterval`、`clearTimeout`、`clearImmediate`



需要注意的是，这些定时器仍然是单线程的。如果脚本**主体有耗时操作或死循环，则设定的定时器不能被及时执行**，例如：

```js
setTimeout(function(){
    //这里的语句会在10秒后执行而不是5秒后
    toast("hello")
}, 5000);
//暂停10秒
sleep(10000);
```



`setInterval(func, delay)`在autoX中的表现与 nodejs 中不一致，autoX中相当于在每次执行完func函数后再额外等待 delay 毫秒执行下一次循环，不能像 nodejs 那样保证func函数每次开始执行的时间点与上次开始执行的时间点间隔等于 delay，但这样的好处是当func执行耗时大于 delay 时，cpu不会过于频繁执行func导致占用率较高。



如果有必要，请开启多线程`thread`执行定时器。



### 8、多线程-Threads

由于 JavaScript 自身没有多线程的支持，因此您可能会遇到意料之外的问题。



脚本主线程会等待所有子线程执行完成后才停止执行，因此如果子线程中有死循环，请在必要的时候调用`exit()`来直接停止脚本或`threads.shutDownAll()`来停止所有子线程。

通过`threads.start()`启动的所有线程会在脚本被强制停止时自动停止。



线程安全和线程通信时开发中常遇到的问题，这里提供的API也很简单，做过开发的小伙伴肯定熟悉。

线程安全：

- 数组 Array 不是线程安全的，如果有这种复杂的需求，请用 Android 和 Java 相关 API 来实现
- 锁：`threads.lock()、threads.unlock()`，加锁是最通用方式。
- 函数同步锁：`sync()`，如果使用，请尽量保证被装饰的方法简洁，将需要保证线程安全的代码
-  整数原子变量：`threads.atomic()`，仅用于整数操作。

**线程通信**：

- `threads.disposable()`：用于简单的线程结果等待
- `Lock.newCondition()`: 用法较麻烦
- `events.emitter()`：通用、易扩展、灵活，使代码结构更清晰，推荐。



### 9. 事件监听

可用于辅助控制脚本的运行、停止。

- 事件的处理是单线程的，并且仍然在原线程执行，如果脚本主体或者其他事件处理中有耗时操作，则事件将会进入事件队列等待脚本主体或其他事件处理完成才执行。
- 5个可监听的按键事件：`volume_up`、`volume_down`、`home`、`back`、`menu`
- 通知监听：需要提前开启权限，可快速删除或者点击进入通知
- 支持链式调用
- **脚本间广播**：[events.broadcast](http://doc.autoxjs.com/#/events?id=eventsbroadcast)

基础示例：

```js
auto.waitFor();

// ================= 按键监听 =================
events.observeKey();
// 屏蔽按键原有功能
events.setKeyInterceptionEnabled('volume_up', true);
events.setKeyInterceptionEnabled('volume_down', true);

events.on('key_down', function (keyCode, event) {
  console.log('按下: ' + KeyEvent.keyCodeToString(event.keyCode));
});
events.on('key_up', function (keyCode, event) {
  console.log('弹起: ' + KeyEvent.keyCodeToString(event.keyCode));
});

// ================= 退出事件 =================
events.on('exit', function () {
  console.log('onExit');
});

// ================= 通知监听 =================
events.observeNotification();
events.on('notification', function (n) {
  log('收到新通知:\n 标题: %s, 内容: %s, \n包名: %s', n.getTitle(), n.getText(), n.getPackageName());
});

// ================= Toast监听 =================
// 当有应用发出 toast(气泡消息)时会触发该事件, 但 Auto.js 软件本身的 toast 除外。
events.observeToast();
events.onToast(function (toast) {
  log('Toast内容: ' + toast.getText() + ' 包名: ' + toast.getPackageName());
});

// ================= EventEmitter基本用法 =================
//新建一个emitter, 并指定回调执行的线程为当前线程
const myEE = events.emitter(threads.currentThread());
myEE
  .on('foo', (name) => console.log('first', name))
  .prependListener('foo', (name) => console.log('second', name))
  .emit('foo', 'AutoX');
// 打印:
// second AutoX
// first AutoX
```



### 10. 简单交互-对话框

包含：确认框、输入框、多选框、单选框、菜单、进度条等样式的简单交互界面。

只能用于跟用户完成一次性交互，若想要长时间展示信息并能与用户交互，还得用 `ui` 模块

具体可参考：[示例代码](https://github.com/kkevsekk1/AutoX/tree/dev-test/app/src/main/assets/sample/%E5%AF%B9%E8%AF%9D%E6%A1%86)



## 四、❤自动化核心功能

以下操需要开启无障碍服务，部分操作需要root权限，建议首行都加上：`auto.waitFor()`

- `auto.waitFor()`：检查无障碍服务是否已经启用，如果没有启用则跳转到无障碍服务启用界面，并等待无障碍服务启动；当无障碍服务启动后脚本会继续运行。



### 1. 基于控件的操作

- `click(text[, i])`、`longClick(text[, i]))`: 点击文本，当不指定参数 i 时则会尝试点击屏幕上出现的所有文字 text 并返回**是否全部点击成功**。尽量指定第二个参数 `i`，提高执行效率。
- `setText()`、`input()`：文本输入



- 选择器 `UiSelector`：

  常用属性选择器：`text()、desc()、id()、depth()、className()、drawingOrder()` 以及其扩展方法 `xxxContains()`、`xxxStartsWith()`、`xxxEndsWith()`、`xxxMatches()` 。这些是`UiSelector`类的实例方法，作为全局变量可直接使用，但是从代码设计角度来讲，这样并不可取，既污染了全局变量又不符合面向对象设计规范，在开发中尽量先用 `selector()` 方法获取到`UiSelector()` 实例，然后再添加筛选条件，例如：

  ```js
  selector().text('文本').depth(11).className('xxx').findOnce()?.click()
  ```

  **id属性**并不代表在页面中的唯一性。  

  `bounds()` 属性一般不用于查询条件（因为不同手机的屏幕尺寸不一样，导致代码兼容性差），当控件的`click()`方法返回 false 时可用来获取控件中心坐标.

  `drawingOrder`属性在 Android 7.0 以上才能使用.  

  如果使用**正则表达式**，请使用javaScript的双反斜杠语法，例如`textMatches(/\d+/)`  

  

  有时候只靠一个属性并不能唯一确定一个控件，这时需要通过属性的组合来完成定位，例如`className("ImageView").depth(10).findOne().click()`，通过链式调用来组合条件。  

  如果不加`findOne()`而直接进行操作，则选择器会找出**所有**符合条件的控件并操作。

  

  文档中列出的方法不全，全部可用的筛选方法可参考源码：[UiGlobalSelector.kt](https://github.com/kkevsekk1/AutoX/blob/84a1f59135433f40747d18ac0805f1b4682bd032/automator/src/main/java/com/stardust/automator/UiGlobalSelector.kt) 与其子类 [UiSelector.java](https://github.com/kkevsekk1/AutoX/blob/8b3c57b06b7323d2b656f331c8ae31d834f69388/autojs/src/main/java/com/stardust/autojs/core/accessibility/UiSelector.java)

  

- 搜索：

  - `findOne()`：对屏幕上的控件进行**深度优先搜索**(DFS)，直到屏幕上出现满足条件的一个控件为止，并返回该控件。如果找不到控件，当屏幕内容发生变化时会重新寻找，直至找到。需要注意的是，**如果屏幕上一直没有出现所描述的控件，则该函数会阻塞**，直至所描述的控件出现为止。因此此函数不会返回`null`。

  - `findOne(timeout)`：如果在 timeout 毫秒的时间内没有找到符合条件的控件，则终止搜索并返回`null`。

  - `findOnce(i)`：只在屏幕上**深度优先搜索(DSF)一次而不是一直搜索**，并返回第 i + 1 个符合条件的控件；如果没有找到符合条件的控件，或者符合条件的控件个数 < i, 则返回`null`。

  - `find()`: 找到所有满足条件的控件集合并返回。这个搜索只进行一次，返回 `UiCollection` 控件集合

  - `exits()`： 判断控件是否存在

  - `filter(f)`：过滤

  - `waitFor()`： 等待控件出现

  - `algorithm(type)`: 设置搜索算法，只能传字符串 `”BFS“` 或 `”DFS“`，分别代表广度优先（默认）和深度优先。具体代码实现：[DFS](https://github.com/kkevsekk1/AutoX/blob/84a1f59135433f40747d18ac0805f1b4682bd032/automator/src/main/java/com/stardust/automator/search/DFS.kt)、

  

- UiObject控件操作：

  - `click()`: 点击。点击一个控件，**前提是这个控件的 clickable 属性为 true**
  - `longClick()`： 长按。长按一个控件，前提是这个控件的 longClickable 属性为 true
  - `setText()`：设置文本，只对可编辑的输入框(editable 为 true)有效
  - `scrollForward()`, `scrollBackward()`：滑动。滑动一个控件(列表等), 前提是这个控件的 `scrollable` 属性为 true
  - 输入框的文字选择、粘贴、复制、剪切
  - 二次查找：
    - `findByText(str)`: 在当前控件的子控件，孙控件，曾孙控件...中搜索 text 或 desc 包含 str 的控件，并返回它们组合的集合。
    - `find(selector)`、`findOne(selector)`: 根据选择器 selector 在该控件的子控件、孙控件...中搜索符合该选择器条件的控件



- UiObject控件属性：
  - 层级关系：`children()`、`child(i)`、`parent()`
  - 节点属性：`bounds()`、`drawingOrder()`、`id()`、`text()`

> 不建议使用 `findOne()`、`untilFind()` 和 `waitFor()`，而是自己用 `find()`、`findOnce`() 和 `sleep()` 封装一个更灵活的等待方法，一直阻塞线程而不给用户任何提示，会误以为程序卡死。



### 2. 基于坐标的操作

- 仅限**安卓7.0**以上
- `click()` 的默认点击持续时间为150ms，如果需要更快或者更慢的点击动作，需要用 `press()` 代替
- 多点触摸操作需开启root权限用RootAutomator来实现


- 双指捏合

  ```js
  gestures([500, [800, 300], [500, 1000]],
           [500, [300, 1500], [500, 1000]]);
  ```


### 3. 按键模拟

按键模拟部分提供了一些模拟物理按键的全局函数，包括Home、音量键、锁屏键等。

一般来说，**以大写字母开头的函数**都依赖于root权限。


### 4. 颜色-colors

颜色和图片这两部分的API设计的很不优雅，都是模块的静态方法调用，不如用面向对象思想设计成一个 `Color` 类型。



颜色用一个字符串`"#AARRGGBB"`或`"#RRGGBB"`表示，AA（Alpha)通道基本用不到，也不建议加，否则可能会发生java整形溢出错误。

```js
log(colors.isSimilar(0xff112233, 0xff223344));
```

常用方法：

- `colors.parseColor()`：把颜色字符串解析为颜色整数（有符号整型）
- `colors.isSimilar(color2, color2[, threshold, algorithm])`：比较两个颜色是否相似，threshold误差默认为4，颜色默认匹配算法 'diff'



### 5. 图片-Images

images模块提供了一些手机设备中常见的图片处理函数，包括截图、读写图片、图片剪裁、旋转、二值化、找色找图等。

> 需要注意的是，image对象创建后尽量在不使用时进行回收，同时避免循环创建大量图片.
>
> 即：`img.recycle()`;
>
> 例外的是，`caputerScreen()`返回的图片不需要回收。

**图片创建、保存**：

- 读取本地图片：`images.read(path)`
- 加载网络图片：`images.load(url)`
- 截屏：`requestScreenCapture([landscape])`、`captureScreen()`，如果需要临时缓存截图，需要调用 `images.copy(img)`，否则下次截图会自动回收上一次截图结果。
- 保存：`images.save(image, path)`，如果文件不存在会被创建；文件存在会被覆盖。

```js
//把图片压缩为原来的一半质量并保存
var img = images.read("/sdcard/1.png");
images.save(img, "/sdcard/1.jpg", "jpg", 50);
app.viewFile("/sdcard/1.jpg");
```

关于Image图片对象的属性和方法，官方文档里描述的不是很全，可以通过 `Object.keys(img)` 自行查看。

**图片处理：**

- Base64转换、裁剪、resize()、比例缩放、旋转、灰度化

- 二值化：`image.threshold(img, threshold, maxVal, type)`，`images.inRange(img, lowerBound, upperBound)`、`images.interval(img, color, interval)`，

  可以参考有关博客（比如[threshold函数的使用](https://blog.csdn.net/u012566751/article/details/77046445)）或者OpenCV文档[threshold](https://docs.opencv.org/3.4.4/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57)。

- 平滑处理：`images.blur(img, size)`、中值滤波`images.medianBlur(img, size)`、高斯滤波`images.gaussianBlur(img, size)`

详细示例：[图片处理](https://github.com/kkevsekk1/AutoX/blob/dev-test/app/src/main/assets/sample/图片与图色处理/图片处理.js)



**找图找色：**

- 取色：`images.pixel(image, x, y)`
- 找色：`images.findColor(image, color, options)`、`images.findAllPointsForColor(img, color, options)`，可限制regon查找区域
- 多点找色：`images.findAllPointsForColor(img, color, options)`
- 取色并比较：`images.detectsColor(image, color, x, y)`，用于检测图片中某个位置是否是特定颜色。
- 找图：`images.findImage(img, template)`、`images.matchTemplate(img, template)`，在大图片img中查找小图片template的位置（模块匹配）
- 找圆：`images.findCircles(gray)`，需要提前转为灰度图

找图、多点找色操作时尽量限定 regon 查找范围参数，提高准确度和查找效率。

### 6. OCR 文字识别

- 内置模型
  - 百度飞桨OCR，总体感觉还凑合，如果识别不准确可以先进行图片预处理。可设置模型精度和cpu数量，建议使用 AutoX 6.2.5 以后的版本
  - 6.3.4 新增Google MLkITOCR，速度比飞桨快，准确度方面我觉得可以跟飞桨搭配使用，前者识别不准时，后者可能就很准，反之亦然😂。附[简略API文档](https://github.com/kkevsekk1/AutoX/blob/de7a9a07661d0466fe3ab9296191607a127f1a84/app/src/main/assets/sample/GoogleMLKit/API.md)，当然你可以从[示例代码](https://github.com/kkevsekk1/AutoX/blob/de7a9a07661d0466fe3ab9296191607a127f1a84/app/src/main/assets/sample/GoogleMLKit/OCR截图识别.js)中学习到更多东西
  - 6.2.9 新增 Tessract OCR。(emmmm.........暂不做评价）

个人感觉这两个模型用起来都没有 Autojs Pro9 中的准确度高，只可惜。。。当然，你可以用自己训练的OCR模型重新编译打包autoX。  

其次要吐槽的一点是，这几种ocr方式返回的结构都不一样，结果中只要包含文字（text)、位置（rect)、置信度（confidence)这三个属性就够了，且按从上到下、从左往右的出现顺序排列，也就是飞桨OCR返回的结果最简洁、实用。如果项目中要混合使用多种OCR方式（不限于以上官方提供的3种），自己有必要再对OCR识别结果类型进行统一封装。



基础用例：

```js
auto.waitFor();

// 默认true使用v2的slim版(速度更快)，false使用v2的普通版(准确率更高）
let useSlim = true

if (!requestScreenCapture()) {
  toast('请求截图失败');
  exit();
}
sleep(1000);

var img = captureScreen();
let res = paddle.ocr(img, 4, useSlim);
console.log(res);

// 回收图片
img.recycle()
// 释放native内存，非必要，供万一出现内存泄露时使用
// paddle.release()
```

[PaddleOCR(自定义模型路径)](https://github.com/kkevsekk1/AutoX/blob/dev-test/app/src/main/assets/sample/PaddleOCR/PaddleOCR(CustomModel)/PaddleOCR(自定义模型路径).js)



## 五、编写 UI 界面

Auto.js的UI系统来自于Android，所有属性和方法都能在Android源码中找到。如果某些代码或属性没有出现在Auto.js的文档中，可以参考Android的文档。

- [android.view.Viewopen in new window](https://developer.android.google.cn/reference/android/view/View?hl=cn)
- [android.widget](https://developer.android.google.cn/reference/android/widget/package-summary?hl=cn)

这部分的文档还AutoX不完善，是看Autojs吧：[ui入门介绍 ](https://pro.autojs.org/docs/zh/v8/ui/) 

> 这部分对于不熟悉Android开发的小伙伴有些不太友好，尤其是写复杂页面，可以先参考示例文件，加以改造使用。
>
> 如果熟悉前端开发，可以使用 vue 框架来写，详见：[auto.pro](https://github.com/molysama/auto.pro)



### 1. 控件-Widget

- 文本：`<text text="文本内容" textColor="red" textSize="14sp" textStyle="bold|italic" maxLines="5" ellipsize="end"/>`
- 按钮：`<button style="Widget.AppCompat.Button.Colored" text="一个按钮"/>`
- 输入框: `<input id="name" hint="请输入姓名"/>`
- 图片: `<img w="40" h="40" radius="2" tint="red" borderWidth="2" borderColor="gray" src="file:///sdcard/Download/1.png" scaleType="fitCenter"/>`
- 复选框：`<checkbox checked="true" text="被禁用的复选框" enabled="false"/>`
- 单选框: 一般与radiogroup搭配使用，`<radio id="radio3" text="已勾选的单选框3" checked="true"/>`
- 开关：`<Switch id="sw" text="单选框1" />`
- 拖动条: `<seekbar id="seekbar" max="200"/>`
- 下拉菜单: `<spinner id="sp1" entries="选项1|选项2|选项3" />`
- 日期选择: `<datepicker />`
- 时间选择: `<timePicker />`
- 浮动按钮: `<fab w="auto" h="auto" src="@drawable/ic_add_black_48dp" margin="16" layout_gravity="bottom|right" tint="#ffffff" />`
- 标题栏:`<toolbar id="toolbar" title="Todo" />`

### 2. 布局-Layout

- 水平布局：`<horizontal>...</horizontal>`
- 垂直布局：`<vertical> ... </vertical>`
- 帧布局：`<frame> ... </frame>` 帧布局是最简单的布局，它默认从容器的左上角(0,0)坐标开始布局，多个子控件层叠排序，后面的控件会覆盖前面的控件
- 相对布局: `<relative>...</relative>` 相对布局会把在它里面的控件以父容器和兄弟控件作为参照来确定控件的位置
- 抽屉布局: `<drawer>...</drawer>`

### 3. 控件和布局通用属性

属性值为数字时，默认单位为 dp，其他单位包括 px(像素), mm(毫米), in(英寸)。有关尺寸单位的更多内容，参见[尺寸的单位: Dimension](http://doc.autoxjs.com/#/ui?id=尺寸的单位-dimension)。



- `attr(name)`: 获取属性值
- `attr(name, value)`：设置属性值
- `w`:宽度
  - `*` 表示宽度**尽量**填满父布局；
  - `auto`表示根据 View 的**内容**自适应。如果不设置该属性，则不同的控件和布局有不同的默认宽度，大多数为`auto`
  - 具体数值
- `h`:高度，取值与`w`相同
- `id`：一个界面的 id 在同一个界面下通常是唯一的，id 属性也是连接 xml 布局和 JavaScript 代码的桥梁。不建议使用控件的同名属性作为 id，比如`id="bg"`，会产生误会，不清楚到底是获取属性值还是根据 id 获取视图对象。
- `gravity`：决定 View 中的内容的位置。取值为：`left、right、top、bottom、center、center_vertical、center_horizontal`中的一种或者组合，例如`gravity="right|bottom"`内容会在右下角。
- `layout_gravity`：决定 View 在他的**父布局**中的位置，取值与 `gravity` 相似，注意区分两者的作用对象。
- `margin、padding`：与 css 中的外、内边距作用相似，但是取值的顺序不一样，左、上、右、下。
- `bg`：
  - 颜色，`bg="#00ff00"`
  - 效果链接，`bg="?attr/selectableItemBackground"`
  - 图片文件路径，`bg="file:///sdcard/1.png"`
- `alpha`、`minHeight`、`minWidth`、`visibility`、`rotation`、`style`

```js
'ui';

ui.layout(
  <vertical w="auto" h="auto" bg="#FF444444">
    <img id="pic"/>
  </vertical>
);

// 动态设置图片
// 方式1
ui.pic.setSource('file:///sdcard/Download/11.png');

// 方式2
const pic = images.read('/sdcard/Download/11.png');
ui.pic.setSource(pic);

// 方式3
const pic = images.read(imgPath);
ui.pic.setImageBitmap(pic.bitmap);
events.on("exit", function () {
  pic.recycle();
});

// 方式4
ui.pic.attr('src', 'data:image/png;base64,' + images.toBase64(pic));
```







### 4. 事件

- `click`：点击事件
- `long_click`: 长按事件。
- `check`: 当用户勾选/取消勾选选项框时会触发该事件，`Switch`, `checkbox`, `radio`等控件才有该事件

```js
"ui";
ui.layout(
    <vertical padding="16">
        <button id="click_me" text="点我" w="auto"/>
    </vertical>
);

ui.click_me.on("long_click", (event) => {
    toast("我被长按啦");
    // 消费事件
    event.consumed = true;
});
```



### 4. ui常用方法

- `ui.layout(xml)`：将布局XML渲染为视图（View）对象，用于创建新视图并切换为当前主视图。
- `ui.inflate(xml[, parent = null, attachToParent = false])`：此函数用于动态创建、显示View。容易出问题，不建议使用。
- `ui.findView(id)`：在当前视图中根据ID查找相应的视图对象并返回
- `ui.setContentView(view)`：将视图对象设置为当前视图。
- `ui.finish()`：结束当前活动并销毁界面。
- `ui.run()、ui.post()`：用于UI线程中执行动作，`sleep()`不能在UI线程中使用

基础示例：

```js
"ui";
ui.layout(
    <vertical padding="16">
        <text textSize="16sp" textColor="black" text="请输入姓名"/>
        <input id="name" text="小明" lines="1"/>
        <button id="ok" text="确定"/>
    </vertical>
);
//指定确定按钮点击时要执行的动作
ui.ok.click(function(){
    var name = ui.name.text();
    toast(name + "您好!");
});
```

### 5. 悬浮窗

floaty模块提供了悬浮窗的相关函数，可以在屏幕上显示自定义悬浮窗，控制悬浮窗大小、位置等。



- 首行不要加 `'ui';`
- `floaty`
  - `window(layout)`：创建悬浮窗对象并立即显示，返回一个`FloatyWindow`对象，`layout`参数可以是xml布局或者一个View，所以要先了解前面的 `ui` 模块。此类型悬浮窗自带关闭、调整大小、调整位置按键，可根据需要调用`setAdjustEnabled(enable)`函数来显示或隐藏。
  - `rawWindow(layout)`：创建悬浮窗对象并立即显示，返回一个`FloatyRawWindow`对象。与`floaty.window()`函数不同的是，该悬浮窗不会增加任何额外设施（例如调整大小、位置按钮）。而且，该悬浮窗**支持完全全屏**，可以覆盖状态栏，因此**可以做护眼模式之类**的应用。

- 悬浮窗大小：悬浮窗控件可以看作创建此悬浮窗的xml根节点的父级View，xml控件内容默认填满悬浮窗，可通过 `setSize(width, height)` 设置悬浮窗大小，单位像素。`FloatyWindow`对象也可以开启 `setAdjustEnabled(true)` 手动调节

- 悬浮窗在脚本停止运行时会自动关闭，可以用一个 Timer 保持。

```js
const w = floaty.window(
    <frame gravity="center">
        <text id="text">长按调整</text>
    </frame>
);

w.exitOnClose();
w.setPosition(100, device.height / 2);
w.text.on('long_click', () => {
  w.setAdjustEnabled(!w.isAdjustEnabled());
});
setInterval(() => {}, 1000);
```

- 因为脚本运行的线程不是UI线程，而所有对控件的修改操作需要在UI线程执行，此时需要用`ui.run`

```js
ui.run(function(){
  w.text.setText("文本");
});
```

  

## 六、高级功能

### 1. 脚本引擎

可用来运行其他js脚本，关闭脚本等。本质上是开启新线程执行js文件，但不共享变量空间。



个人认为用处不大。

如果要执行的另一个 js 文件跟当前项目是独立的，或者是录制好的 `.auto` 文件，可用此方式执行。

否则，为了更好维护和管理，尽量将其他脚本代码集成到当前项目，在主线程和新线程中执行皆可，能共享变量，又能借助 `events` 模型通信。



### <span id='async'>2. 协程</span>

用过 Nodejs 或者 python 的开发者都知道协程能提高单线程代码的执行效率，Autojs Pro 9 可使用Node作为脚本引擎，再配合 `async/await` 语法可降低协程开发难度。

最近几个版本 AutoX 更新了 `Promise` 特性的实现，比之前好用了些，如需使用 `async/await` 语法还是得用借助 webpack



### 2. 调用 Java

- [`runtime.loadJar(path)`](http://doc.autoxjs.com/#/globals?id=runtimeloadjarpath)
- [Rhino 官方文档](https://p-bakker.github.io/rhino/tutorials/scripting_java/)

## 七、示例

### 1. 终端模拟器

将弹出的 console 控制台作为交互界面，读取用户输入并输出shell执行结果，每次输入完需手动点击确定，回车作为换行符，输入`'exit'`退出程序。  

部分机型可能会有控制台不显示输入框的情况，属于bug。

```js
console.show(true);

threads.start(() => {
  console.setSize(device.width, device.height / 2);

  var sh = new Shell();
  sh.setCallback({
    onOutput: function (str) {
      print(str);
    }
  });

  do {
    var cmd = console.rawInput();
    sh.exec(cmd);
  } while (cmd != 'exit');
  sh.exit();
});
```



### 2. 多线程按键监听

```js
auto.waitFor();

threads.start(function () {
  //在子线程中调用observeKey()从而使按键事件处理在子线程执行
  events.observeKey();
  events.setKeyInterceptionEnabled('volume_up', true);
  //音量键关闭脚本
  events.on('key_up', function (keyCode, events) {
    exit();
  });
});

toast('音量上键关闭脚本');

events.on('exit', function () {
  toastLog('脚本已结束');
});

while (true) {
  log('脚本运行中...');
  sleep(2000);
}
```

### 3. 护眼模式

```js
var w = floaty.rawWindow(
    <frame gravity="center" bg="#44ffcc00"/>
);

w.setSize(-1, -1); // 占满全屏
w.setTouchable(false);

setTimeout(()=>{
    w.close();
}, 4000);
```




## 五、发布&打包

### 1. 兼容性

对运行环境版本进行检测和处理，从而使脚本适用于更多平台。



屏幕分辨率兼容性处理：

当脚本是基于坐标进行定位时，为了能在其他分辨率的机型上运行，需要获取当前开发环境的屏幕分辨率，然后在程序启动阶段调用 `setScreenMetrics(width, height)`，AutoX会将代码中的坐标自动缩放，从而适应当前屏幕。



另外，安卓端的自动化工具有很多，[hamibot](https://hamibot.com/)、[Aibote](http://www.aibote.net/index.html)、[冰狐智能辅助](https://aznfz.com/)等，他们的API用法也差不多，如果你想从AutoX 迁移到其他框架上（万一开发者跑路了），就不要过度依赖框架提供的API，而是尽量自己封装成自己的API方法，屏蔽掉框架之间的差异，使自己更专注于自动化流程实现。



AutoX与此相关的API：

- `app.autojs.versionCode`：获取当前的Auto.js版本号
- `app.autojs.versionName`：获取当前的Auto.js版本
- [requiresApi(api)](http://doc.autoxjs.com/#/globals?id=requiresapiapi)：表示此脚本需要Android API版本达到指定版本才能运行。详见：[Build.VERSION_CODES  | Android Developers (google.cn)](https://developer.android.google.cn/reference/kotlin/android/os/Build.VERSION_CODES#m)
- [requiresAutojsVersion(version)](http://doc.autoxjs.com/#/globals?id=requiresautojsversionversion): 表示此脚本需要Auto.js版本达到指定版本才能运行。
- `device.sdkInt`：安卓系统API版本。例如安卓4.4的sdkInt为19。
- `setScreenMetrics(width, height)`：设置脚本坐标点击所适合的屏幕宽高。



### <span id='logger'>2. 日志文件</span>

AutoX提供的配置参数有限，参考配置：

```js
console.setGlobalLogConfig({
  file: '/sdcard/Download/log.txt', // 文件位置
  maxFileSize: 10 * 1024 * 1024, // 10M
  rootLevel: 'INFO',
  maxBackupSize: 5, // 备份文件最大数量
  filePattern: '%-d{yyyy-MM-dd HH:mm:ss} [%t]-[%p] %m%n' // 日志格式
});

console.log(1);
console.info(2);
console.warn(3);
app.viewFile('/sdcard/Download/log.txt');
```

- `%m`:  输出代码中指定的消息
- `%p`:  输出优先级，即DEBUG，INFO，WARN，ERROR，FATAL 
- `%r`:  输出自应用启动到输出该log信息耗费的毫秒数 
- `%c`:  输出所属的类目，通常就是所在类的全名 
- `%t`:  输出产生该日志事件的线程名 
- `%n`:  输出一个回车换行符，Windows平台为“\r\n”，Unix平台为“\n” 
- `%d`:  输出日志时间点的日期或时间，默认格式为ISO8601，也可以在其后指定格式，比如：%d{yyy MMM dd HH:mm:ss , SSS}，输出类似：2002年10月18日 22 ： 10 ： 28 ， 921 
- `%l`:  输出日志事件的发生位置，包括类目名、发生的线程，以及在代码中的行数。举例：Testlog4.main(TestLog4.java: 10 ) 