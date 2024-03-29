如何停止 Win11 更新？
--------------

那么我们该如何彻底关闭 Windows 更新呢？我们为您准备了四种效果不错的关闭 Win11 更新方法，您可以根据自身实际情况选择合适的方法！

### 方案一：使用注册表编辑器关闭 Win11 更新

Windows 注册表实质上是一个庞大的数据库，存储着各种各样的计算机数据与配置，我们可以通过编辑注册表来解决一些很难搞定的计算机问题，比如彻底关闭 Win11 更新。

**1.** 按 **Win+R** 输入 **regedit** 并按 **Enter** 键打开注册表编辑器。

**2.** 导航到此路径：**HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows**。

**3.** 右键单击 Windows 文件夹，选择 **“新建”>“项”**，然后将其命名为 **“WindowsUpdate”**。

 [![](https://www.disktool.cn/0/666/1/193.png)](https://www.disktool.cn/0/666/1/193.png) 

**4.** 右键单击新建的 WindowsUpdate 文件夹，选择 **“新建”>“项”**，然后将其命名为 **“AU”**。

**5.** 在新建的 AU 文件夹右侧空白页面中右键单击并选择 **“新建”>“DWORD（32 位）值”**，然后将其命名为 **“NoAutoUpdate”**。

 [![](https://www.disktool.cn/0/666/1/194.png)](https://www.disktool.cn/0/666/1/194.png) 

**6.** 双击新建的 NoAutoUpdate，在弹出窗口中将其数值数据从 **0** 更改为 **1**，然后单击 **“确定”**。

 [![](https://www.disktool.cn/0/666/1/195.png)](https://www.disktool.cn/0/666/1/195.png) 

**7.** 关闭注册表编辑器，重启计算机即可彻底关闭 Windows 更新。

### 方案二：使用组策略编辑器关闭 Win11 更新

组策略是管理员为计算机和用户定义的，用来控制应用程序、系统设置和管理模板的一种机制，通俗一点说，即为介于控制面板和注册表之间的一种修改系统、设置程序的工具。当然，我们也可以通过本地组策略编辑器来关闭 Win11 更新。

**1.** 按 **Win+R** 输入 **gpedit.msc** 并按 **Enter** 键打开本地组策略编辑器。

**2.** 转到此路径：**本地计算机策略 > 计算机配置 > 管理模板 > Windows 组件 > Windows 更新 > 适用于企业的 Windows 更新**。

 [![](https://www.disktool.cn/0/666/1/196.png)](https://www.disktool.cn/0/666/1/196.png) 

**3.** 双击此文件夹下的 **“选择目标功能更新版本”** 设置。

**4.** 在弹出窗口中将其配置为 **“已启用”**，在左下方长条框中填入 **“20H1”**（或者其他您想停留的 Windows10 版本），然后单击 **“应用”>“确定”** 即可。

 [![](https://www.disktool.cn/0/666/1/197.png)](https://www.disktool.cn/0/666/1/197.png) 

**5.** 关闭本地组策略编辑器，重启计算机即可彻底停止 Win11 更新。

### 方案三：使用 Windows 设置关闭 Win11 更新

在 Windows 系统设置中，也有一个设置可以暂时关闭 Win11 更新，让我们一起来看看吧！

**1.** 按 **Win+I** 打开 Windows 设置页面。

**2.** 单击 **“更新和安全”>“Windows 更新”**，然后在右侧详情页中选择 **“暂停更新 7 天”** 选项即可在此后 7 天内关闭 Windows 更新。

 [![](https://www.disktool.cn/0/666/1/198.png)](https://www.disktool.cn/0/666/1/198.png) 

### 方案四：使用本地服务关闭 Win11 更新

本地服务是汇集整个计算机上全部服务的一个集合，我们可以在这里对指定的 Windows 服务项进行启用、停止或禁用配置，关闭 Win11 更新也不例外。

**1.** 按 **Win+R** 输入 **services.msc** 并按 **Enter** 键打开服务页面。

**2.** 在右侧列表中找到 **“Windows Update”** 选项，双击进入详细属性页面，将其启动类型配置为 **“禁用”**，然后单击 **“应用”>“确定”** 即可关闭 Windows 自动更新。

 [![](https://www.disktool.cn/0/666/1/199.png)](https://www.disktool.cn/0/666/1/199.png) 

结论
--

Windows 自动更新是一件非常烦人的事情，为了彻底关闭 Win11 更新，我们分别为您介绍了注册表编辑器、组策略编辑器、系统设置和服务这四种关闭 Windows 更新的有效解决方案，您可以根据自身实际情况酌情选择合适的方法。