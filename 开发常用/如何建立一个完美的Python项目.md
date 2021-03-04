- 原文地址：[How to set up a perfect Python project][1]

*   原文作者：Brendan Maginnis
    
*   译者：HelloGitHub - 丫丫
    
*   校对者：HelloGitHub - 削微寒
    

当开始一个新的 Python 项目时，大家很容易一头扎进去就开始编码。其实花一点时间选择优秀的库，将为以后的开发节省大量时间，并带来更快乐的编码体验。  

在理想世界中，所有开发人员的关系是相互依赖和关联的（协作开发），代码要有完美的格式、没有低级的错误、并且测试覆盖了所有代码。另外，所有这些将在每次提交时都可以得到保证。（代码风格统一、类型检测、测试覆盖率高、自动检测）

在本文中，我将介绍如何建立一个可以做到这些点的项目。您可以按照步骤操作，也可以直接跳到 使用 `cookiecutter` 生成项目 部分（老手）。

首先，让我们创建一个新的项目目录：

```sh
mkdir best_practices
cd best_practices
```

pipx 安装 Python 三方库的命令行工具
------------------------

[Pipx][2] 是一个可用于快速安装 Python 三方库的命令行工具。我们将使用它来安装 pipenv 和 cookiecutter。通过下面的命令安装 pipx：

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

使用 pipenv 进行依赖管理
----------------

> [Pipenv][3] 为您的项目自动创建和管理 virtualenv（虚拟环境），并在安装 / 卸载软件包时从 Pipfile 添加 / 删除软件包。它还会生成非常重要的 Pipfile.lock 用于保证依赖的可靠性。

当你知道，你和你的队友正在使用相同的库版本时，这将会极大地提高编程的信心和乐趣。Pipenv 很好地解决了使用相同的库，版本不同的这一问题，Pipenv 在过去的一段时间里获得了广泛的关注和认可，你可以放心使用。安装命令如下：

```sh
pipx install pipenv
```

使用 black 和 isort 进行代码格式化
------------------------

[black][4] 可以格式化我们的代码：

> Black 是毫不妥协的 Python 代码格式化库。通过使用它，你将放弃手动调整代码格式的细节。作为回报，Black 可以带来速度、确定性和避免调整 Python 代码风格的烦恼，从而有更多的精力和时间放在更重要的事情上。
>
> 无论你正在阅读什么样的项目，用 black 格式化过的代码看起来都差不多。一段时间后格式不再是问题，这样你就可以更专注于内容。
>
> black 通过减少代码的差异性，使代码检查更快。

而 [isort][5] 是对我们的 imports 部分进行排序：

> isort 为您导入的 Python 包部分（imports）进行排序，因此你不必再对 imports 进行手动排序。它可以按字母顺序对导入进行排序，并自动将其拆分成多个部分。

使用 pipenv 安装它，以便它们不会使部署混乱（可以指定只在开发环境安装）：

```sh
pipenv install black isort --dev
```

Black 和 isort 并不兼容的默认选项，因此我们将让 isort 遵循 black 的原则。创建一个 `setup.cfg` 文件并添加以下配置：

```ini
[isort]
multi_line_output=3
include_trailing_comma=True
force_grid_wrap=0
use_parentheses=True
line_length=88
```

我们可以使用以下命令运行这些工具：

```sh
pipenv run black
pipenv run isort
```

使用 flake8 保证代码风格
----------------

Flake8 确保代码遵循 PEP8 中定义的标准 Python 代码规范。使用 pipenv 安装：

```sh
pipenv install flake8 --dev
```

就像 isort 一样，它需要一些配置才能很好地与 black 配合使用。将这些配置添加到 `setup.cfg` ：

```ini
[flake8]
ignore = E203, E266, E501, W503
max-line-length = 88
max-complexity = 18
select = B,C,E,F,W,T4
```

现在我们可以运行 flake8 了，命令:

```sh
pipenv run flake8
```

使用 mypy 进行静态类型检查
----------------

> [Mypy][6] 是 Python 的非强制的静态类型检查器，旨在结合动态（或 “鸭子”）类型和静态类型的优点。Mypy 将 Python 的表达能力和便利性与功能强大的类型系统的编译时类型检查结合在一起，使用任何 Python VM 运行它们，基本上没有运行时开销。

在 Python 中使用类型需要一点时间来适应，但是好处却是巨大的。如下：

*   静态类型可以使程序更易于理解和维护
    
*   静态类型可以帮助您更早地发现错误，并减少测试和调试的时间
    
*   静态类型可以帮助您在代码投入生产之前发现难以发现的错误
    

```sh
pipenv install mypy --dev
```

默认情况下，Mypy 将递归检查所有导入包的类型注释，当库不包含这些注释时，就会报错。我们需要将 mypy 配置为仅在我们的代码上运行，并忽略没有类型注释的导入错误。我们假设我们的代码位于以下配置的 `best_practices` 包中。将此添加到 `setup.cfg` ：

```ini
[mypy]
files=best_practices,test
ignore_missing_imports=true
```

现在我们可以运行 mypy 了：

```sh
pipenv run mypy
```

这是一个有用的 [备忘单][7] 。

用 pytest 和 pytest-cov 进行测试
--------------------------

使用 [pytest][8] 编写测试非常容易，消除编写测试的阻力意味着可以快速的编写更多的测试！

```shell
pipenv install pytest pytest-cov --dev
```

这是 pytest 网站上的一个简单示例：

```python
# content of test_sample.py
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5
```

要执行它：

```sh
$ pipenv run pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert inc(3) == 5
E       assert 4 == 5
E        +  where 4 = inc(3)

test_sample.py:6: AssertionError
========================= 1 failed in 0.12 seconds =========================
```

我们所有的测试代码都放在 `test` 目录中，因此请将此目录添加到 `setup.cfg` ：

```ini
[tool:pytest]
testpaths=test
```

如果还想查看测试覆盖率。创建一个新文件 `.coveragerc`，指定只返回我们的项目代码的覆盖率统计信息。比如示例的 `best_practices` 项目，设置如下：

```ini
[run]
source = best_practices

[report]
exclude_lines =
    # Have to re-enable the standard pragma
    pragma: no cover

    # Don't complain about missing debug-only code:
    def __repr__
    if self\.debug

    # Don't complain if tests don't hit defensive assertion code:
    raise AssertionError
    raise NotImplementedError

    # Don't complain if non-runnable code isn't run:
    if 0:
    if __name__ == .__main__.:
```

现在，我们就可以运行测试并查看覆盖率了。

```sh
pipenv run pytest --cov --cov-fail-under=100
```

`--cov-fail-under=100` 是设定项目的测试覆盖率如果小于 100％ 那将认定为失败。

pre-commit 的 Git hooks
----------------------

Git hooks 可让您在想要提交或推送时随时运行脚本。这使我们能够在每次提交 / 推送时，自动运行所有检测和测试。[pre-commit][9] 可轻松配置这些 hooks。

> Git hook 脚本对于在提交代码审查之前，识别简单问题很有用。我们在每次提交时都将运行 hooks，以自动指出代码中的问题，例如缺少分号、尾随空白和调试语句。通过在 code review 之前指出这些问题，代码审查者可以专注于变更的代码内容，而不会浪费时间处理这些琐碎的样式问题。

在这里，我们将上述所有工具配置为在提交 Python 代码改动时执行（git commit），然后仅在推送时运行 pytest coverage（因为测试要在最后一步）。创建一个新文件 `.pre-commit-config.yaml`，配置如下：

```yaml
repos:
  - repo: local
    hooks:
      - id: isort
        name: isort
        stages: [commit]
        language: system
        entry: pipenv run isort
        types: [python]

      - id: black
        name: black
        stages: [commit]
        language: system
        entry: pipenv run black
        types: [python]

      - id: flake8
        name: flake8
        stages: [commit]
        language: system
        entry: pipenv run flake8
        types: [python]
        exclude: setup.py

      - id: mypy
        name: mypy
        stages: [commit]
        language: system
        entry: pipenv run mypy
        types: [python]
        pass_filenames: false

      - id: pytest
        name: pytest
        stages: [commit]
        language: system
        entry: pipenv run pytest
        types: [python]

      - id: pytest-cov
        name: pytest
        stages: [push]
        language: system
        entry: pipenv run pytest --cov --cov-fail-under=100
        types: [python]
        pass_filenames: false
```

如果需要跳过这些 hooks，可以运行 `git commit --no-verify` 或 `git push --no-verify`

使用 cookiecutter 生成项目
--------------------

现在，我们已经知道了理想项目中包含了什么，我们可以将其转换为 [模板][10] 从而可以使用单个命令生成一个包含这些库和配置的新项目：

```sh
pipx run cookiecutter gh:sourcery-ai/python-best-practices-cookiecutter
```

填写项目名称和仓库名称，将为您生成新的项目。

要完成设置，请执行下列步骤：

```sh
# Enter project directory
cd <repo_name>

# Initialise git repo
git init

# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```

模板项目包含一个非常简单的 Python 文件和测试，可以试用上面这些工具。在编写完代码觉得没问题后，就可以执行第一次 `git commit`，所有的 hooks 都将运行。

集成到编辑器
------

虽然在提交时知道项目的代码始终保持最高水准是件令人兴奋的事情。但如果在代码已全部修改完成之后（提交时），再发现有问题还是会让人很不爽。所以，实时暴露出问题要好得多。

在保存文件时，花一些时间确保代码编辑器运行这些命令。有及时的反馈，这意味着你可以在代码还有印象的时候能迅速解决引入的任何小问题。

我个人使用一些出色的 Vim 插件来完成此任务：

*   [ale][11] 实时运行 flake8 并在保存文件时运行 black、isort 和 mypy
    
*   与 [projectionist 集成][12]的  [vim-test][13] 在文件保存上运行 pytest
    

参考资料

[1]: https://sourcery.ai/blog/python-best-practices/
[2]: https://pipxproject.github.io/pipx/
[3]: https://github.com/pypa/pipenv
[4]: https://github.com/psf/black
[5]: https://github.com/timothycrosley/isort
[6]: http://mypy-lang.org/
[7]: https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html
[8]: https://docs.pytest.org/en/latest/
[9]: https://pre-commit.com/
[10]: https://github.com/sourcery-ai/python-best-practices-cookiecutter
[11]: https://github.com/dense-analysis/ale
[12]: https://github.com/janko/vim-test#projectionist-integration
[13]: https://github.com/janko/vim-test