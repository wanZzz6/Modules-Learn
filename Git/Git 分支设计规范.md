# 概述

> 前言：
>
> 规定 Git 分支设计规范，目的是提供给研发人员做参考。
> 规范是死的，人是活的。



在说 Git 分支规范之前，先说下在系统开发过程中常用的**环境**。

|简称	|全称| 作用
|:---|:----|:-----|
|DEV |Development environment| 用于开发者调试使用
|FAT |Feature Acceptance Test environment|功能验收测试环境，用于测试环境下的软件测试者测试使用
|UAT |User Acceptance Test environment|用户验收测试环境，用于生产环境下的软件测试者测试使用
|PRO |Production environment|就是生产环境

比如，项目域名为：`http://www.abc.com`，那么相关环境的域名可这样配置：

- DEV 环境：本地配置虚拟域名即可
- FAT 环境：`http://fat.abc.com`
- UAT 环境：`http://uat.abc.com`
- PRO 环境：`http://www.abc.com`

接下来，针对不同的环境来设计**分支**。






# 分支

|分支	  |名称 |	环境	|可访问
|:----|:------|:-----|:-----|
|master	 |主分支	|PRO	|是
|release	|预上线分支	|UAT |	是
|hotfix	 |紧急修复分支	|DEV|	否
|develop	|测试分支	|FAT	|是
|feature	|需求开发分支|	DEV|	否

## master 分支

`master` 为主分支，用于部署到正式环境（PRO），一般由 `release` 或 `hotfix`  分支合并

- **任何情况下不允许直接在 master 分支上修改代码。**
- 分支上锁，只允许核心人员操作，不可随意推送。
- 永远只存可以发布到生产环境的代码。


## release 分支

`release` 为预上线分支，用于部署到预上线环境（UAT），始终保持与 `master` 分支一致，一般由 `develop` 或 `hotfix` 分支合并，

- 不建议直接在 `release` 分支上直接修改代码。
- 该分支通过版本号命名。
- 一次只能出现一个版本。
- 如果在 `release `分支测试出问题，需要回归验证 `develop` 分支看否存在此问题。

```sh
// 从 dev 分支创建一个预发布分支
$git checkout -b release-1.0
// 合并到 master 主分支
$git checkout master
$git merge –no-ff release-1.0
// 对合并生成的新节点,做一个标签.
$git tag -a 1.0
$git branch -d release-1.0
```

## hotfix 分支

`hotfix` 为紧急修复分支，命名规则为 `hotfix-` 开头，当线上出现紧急问题需要马上修复时，需要基于 `release` 或 `master` 分支创建 `hotfix` 分支

- 修复完成后，再合并到 `release` 或 `develop` 分支，一旦修复上线，便将其删除
- 该分支根据需要修复的 BUG 命名
- 允许同时出现多个 BUG 修复分支


## develop 分支

`develop` 为测试分支，用于部署到测试环境（FAT），始终保持最新完成以及 bug 修复后的代码，可根据需求大小程度确定是由 `feature` 分支合并，还是直接在上面开发。

**一定是满足测试的代码才能往上面合并或提交。**

## feature 分支

`feature` 为需求开发分支，命名规则为 `feature-` 开头，**一旦该需求上线，便将其删除。**

- 该分支根据需要做的功能命名。
- 允许同时出现多个功能分支。
- 功能开发结束并合并到`master`后，删除该分支。

```sh
// 从 dev 分支创建一个名为 feature-addNumber 的功能分支
$git checkout -b feature-addNumber
// 开发完成后合并到 dev 分支
$git checkout dev
$git merge --no-ff feature-addNumber
// 删除功能分支
$git branch -d feature-addNumber
```

<br>
这么说可能有点不容易理解，接下来举几个开发场景。

# 开发场景

## 新需求加入

有一个订单管理的新需求需要开发，首先要创建一个 `feature-order` 分支，问题来了，该分支是基于哪个分支创建？

如果 存在 未测试完毕的需求，就基于 `master` 创建。

如果 不存在 未测试完毕的需求，就基于 `develop` 创建。

1. 需求在 `feature-order` 分支开发完毕，准备提测时，要先确定 `develop` 不存在未测试完毕的需求，这时研发人员才能将将代码合并到 `develop` （测试环境）供测试人员测试。

2. 测试人员在 `develop` （测试环境） 测试通过后，研发人员再将代码发布到 `release` （预上线环境）供测试人员测试。

3. 测试人员在 `release` （预上线环境）测试通过后，研发人员再将代码发布到 `master` （正式环境）供测试人员测试。

4. 测试人员在 `master` (正式环境) 测试通过后，研发人员需要删除 `feature-order` 分支。

## 普通迭代

有一个订单管理的迭代需求，如果开发工时 < 1d，直接在 `develop` 开发，如果开发工时 > 1d，那就需要创建分支，在分支上开发。

开发后的提测上线流程 与 新需求加入的流程一致。

## 修复测试环境 Bug

在 `develop` 测试出现了Bug，如果修复工时 < 2h，直接在 `develop` 修复，如果修复工时 > 2h，需要在分支上修复。

修复后的提测上线流程 与 新需求加入的流程一致。

```sh
// 从 dev 分支创建一个名为 fixbug-001 的 bug 分支
$git checkout -b fixbug-001
// bug 修复完成后合并到 dev 分支
$git checkout dev
$git merge --no-ff fixbug-001
// 删除 bug 分支
$git branch -d fixbug-001
```

## 修改预上线环境 Bug

在 `release` 测试出现了Bug，首先要回归下 `develop` 分支是否同样存在这个问题。

如果存在，修复流程 与 修复测试环境 Bug流程一致。

如果不存在，这种可能性比较少，大部分是数据兼容问题，环境配置问题等。

## 修改正式环境 Bug

在 master 测试出现了Bug，首先要回归下 release 和 develop 分支是否同样存在这个问题。

如果存在，修复流程 与 修复测试环境 Bug流程一致。

如果不存在，这种可能性也比较少，大部分是数据兼容问题，环境配置问题等。

## 紧急修复正式环境 Bug

需求在测试环节未测试出 Bug，上线运行一段时候后出现了 Bug，需要紧急修复的。

我个人理解紧急修复的意思是没时间验证测试环境了，但还是建议验证下预上线环境。

- 如果 `release` 分支存在未测试完毕的需求，就基于` master` 创建 `hotfix-xxx` 分支，修复完毕后发布到 master 验证，验证完毕后，将 master 代码合并到 `release` 和 `develop` 分支，同时删掉 `hotfix-xxx` 分支。

- 如果 `release` 分支不存在未测试完毕的需求，但 `develop` 分支存在未测试完毕的需求，就基于 `release` 创建 `hotfix-xxx` 分支，修复完毕后发布到 `release` 验证，后面流程与上线流程一致，验证完毕后，将 `master` 代码合并到 `develop` 分支，同时删掉 `hotfix-xxx` 分支。

- 如果 `release` 和 `develop` 分支都不存在未测试完毕的需求， 就直接在 `develop` 分支上修复完毕后，发布到 `release` 验证，后面流程与上线流程一致。

## 并行提测

在一个项目中并行开发了两个需求，并行提测，但是上线日期不同。

我能想到的两种方案：

- 再部署一套可供测试人员测试的分支
- 使用 git cherry-pick “挑拣”提交

对于并行提测，你有好的方案吗？欢迎留言。


# Commit 日志规范

提交信息一定要认真填写！

建议参考规范：`<type>(scope)：<subject>`

比如：<U>fix(首页模块)：修复弹窗 JS Bug</U>。

`type` 表示 动作类型，可分为：

- fix：修复 xxx Bug
- feat：新增 xxx 功能
- test：调试 xxx 功能
- style：变更 xxx 代码格式或注释
- docs：变更 xxx 文档
- refactor：重构 xxx 功能或方法
- scope 表示 影响范围，可分为：模块、类库、方法等。

`subject` 表示 简短描述，最好不要超过 60 个字，如果有相关 Bug 的 Jira 号，建议在描述中加上。


# 示例操作流程

```sh
// 从远程仓库克隆项目 dev 分支 
$git clone -b dev http://git.ts-it.cn/BornToRain/testGit.git
// 进入项目目录
$cd testGit
// 从 dev 分支创建功能分支
$git checkout -b feature-helloworld
// 创建一个${姓名}.java
$vim xxx.java
// 加入 Git
$git add xxx.java
// 提交到本地仓库 
$git commit -m "新增(xxx) 功能已完成"
// 切换回 dev 分支
$git checkout dev
// 将功能分支实现的功能合并到 dev 分支上
$git merge --no-ff feature-helloworld
// 推送本地 dev 分支内容到远程仓库
$git push origin dev
// 测试无误后删除本地功能分支
$git branch -d feature-helloworld
```
