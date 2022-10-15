使用 git 的开发者都知道提交代码的最简单命令： `git commit -m '此次提交的内容说明'`。  
我们在 github 发现了这样一张视图：

<img src="C:\Users\wzz\AppData\Roaming\Typora\typora-user-images\image-20220613120416799.png" alt="image-20220613120416799" style="zoom: 67%;" />

这是在 commit 时，添加了 emoji 表情说明，我们来看看其命令语法：

在 commit 时添加一个 emoji 表情图标
-------------------------

```
git commit -m ':emoji: 此次提交的内容说明'
```

添加多个 emoji 表情图标
---------------

```
git commit -m ':emoji1: :emoji2: :emoji3: 此次提交的内容说明'
```

在提交内容的前面增加了 emoji 标签： **:emoji:**，其中 emoji 是表情图标的标签，列表见下面的附录表格。

<table><thead><tr><th>emoji</th><th>emoji 代码</th><th>commit 说明</th></tr></thead><tbody><tr><td>🎨 (调色板)</td><td><code>:art:</code></td><td>改进代码结构 / 代码格式</td></tr><tr><td>⚡️ (闪电)🐎 (赛马)</td><td><code>:zap:“:racehorse:</code></td><td>提升性能</td></tr><tr><td>🔥 (火焰)</td><td><code>:fire:</code></td><td>移除代码或文件</td></tr><tr><td>🐛 (bug)</td><td><code>:bug:</code></td><td>修复 bug</td></tr><tr><td>🚑 (急救车)</td><td><code>:ambulance:</code></td><td>重要补丁</td></tr><tr><td>✨ (火花)</td><td><code>:sparkles:</code></td><td>引入新功能</td></tr><tr><td>📝 (备忘录)</td><td><code>:memo:</code></td><td>撰写文档</td></tr><tr><td>🚀 (火箭)</td><td><code>:rocket:</code></td><td>部署功能</td></tr><tr><td>💄 (口红)</td><td><code>:lipstick:</code></td><td>更新 UI 和样式文件</td></tr><tr><td>🎉 (庆祝)</td><td><code>:tada:</code></td><td>初次提交</td></tr><tr><td>✅ (白色复选框)</td><td><code>:white_check_mark:</code></td><td>增加测试</td></tr><tr><td>🔒 (锁)</td><td><code>:lock:</code></td><td>修复安全问题</td></tr><tr><td>🍎 (苹果)</td><td><code>:apple:</code></td><td>修复 macOS 下的问题</td></tr><tr><td>🐧 (企鹅)</td><td><code>:penguin:</code></td><td>修复 Linux 下的问题</td></tr><tr><td>🏁 (旗帜)</td><td><code>:checked_flag:</code></td><td>修复 Windows 下的问题</td></tr><tr><td>🔖 (书签)</td><td><code>:bookmark:</code></td><td>发行 / 版本标签</td></tr><tr><td>🚨 (警车灯)</td><td><code>:rotating_light:</code></td><td>移除 linter 警告</td></tr><tr><td>🚧 (施工)</td><td><code>:construction:</code></td><td>工作进行中</td></tr><tr><td>💚 (绿心)</td><td><code>:green_heart:</code></td><td>修复 CI 构建问题</td></tr><tr><td>⬇️ (下降箭头)</td><td><code>:arrow_down:</code></td><td>降级依赖</td></tr><tr><td>⬆️ (上升箭头)</td><td><code>:arrow_up:</code></td><td>升级依赖</td></tr><tr><td>👷 (工人)</td><td><code>:construction_worker:</code></td><td>添加 CI 构建系统</td></tr><tr><td>📈 (上升趋势图)</td><td><code>:chart_with_upwards_trend:</code></td><td>添加分析或跟踪代码</td></tr><tr><td>🔨 (锤子)</td><td><code>:hammer:</code></td><td>重大重构</td></tr><tr><td>➖ (减号)</td><td><code>:heavy_minus_sign:</code></td><td>减少一个依赖</td></tr><tr><td>🐳 (鲸鱼)</td><td><code>:whale:</code></td><td>Docker 相关工作</td></tr><tr><td>➕ (加号)</td><td><code>:heavy_plug_sign:</code></td><td>增加一个依赖</td></tr><tr><td>🔧 (扳手)</td><td><code>:wrench:</code></td><td>修改配置文件</td></tr><tr><td>🌐 (地球)</td><td><code>:globe_with_meridians:</code></td><td>国际化与本地化</td></tr><tr><td>✏️ (铅笔)</td><td><code>:pencil2:</code></td><td>修复 typo</td></tr></tbody></table>

参考资料 :

*   [https://gitmoji.carloscuesta.me/](https://gitmoji.carloscuesta.me/)
