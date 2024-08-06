## 使用场景

假设我从github 上git clone了一个开源项目 ffmpeg，然后我基于这个项目进行二次开发，新建了一个 my-feature 分支进行我个人的定制化开发，新增的功能不想然别人看到，所以我将整个仓库上传到私有github 仓库上 my-ffmpeg，但是我想让 my-ffmpeg 这个项目的 master 分支与开源项目ffmpeg的 master 分支保持一致，就是开源项目 ffmpeg 的 master分支发布了新内容，我的 my-ffmpeg 项目也能同步过来

## 具体操作

以下内容来自 chatgpt4-turbo

1. **添加开源项目作为一个新的远程仓库：**
   
   首先，在您的本地 `my-ffmpeg` 仓库中，添加原始的 `ffmpeg` 开源项目作为一个新的远程（通常称为 `upstream`）。

   ```bash
   git remote add upstream https://github.com/ffmpeg/ffmpeg.git
   ```

   这样做之后，您会有两个远程仓库：`origin` 指向您个人的私有仓库，`upstream` 指向公共的开源项目仓库。

2. **同步开源项目的 `master` 分支：**

   当开源项目的 `master` 分支有更新时，您可以通过以下命令来获取最新的更改：

   ```bash
   git fetch upstream
   ```

   然后，您可以将这些更改合并到您的本地 `master` 分支：

   ```bash
   git checkout master
   git merge upstream/master
   ```

3. **将同步后的更改推送到您的私有仓库：**

   同步并合并了最新的更改后，您可以将它们推送到您的私有仓库的 `master` 分支：

   ```bash
   git push origin master
   ```

4. **定期同步更新：**

   您可以手动执行这些步骤来同步更改，也可以设置一个定时任务（如使用 `cron`）来定期执行同步脚本。

5. **保持你的个人特性分支更新：**

   如果您希望您的个人特性分支也包含最新的 `master` 分支更改，您可能需要经常地将 `master` 分支的更新合并到您的 `my-feature` 分支：

   ```bash
   git checkout my-feature
   git merge master
   # 解决可能出现的合并冲突
   git push origin my-feature
   ```

记得在合并和推送更改之前，始终检查是否有任何合并冲突，并确保它们被妥善解决，以保持代码库的稳定性。

通过这种方式，您可以保持私有仓库的 `master` 分支与开源项目的 `master` 分支同步，同时在 `my-feature` 分支上进行私人定制化开发。

