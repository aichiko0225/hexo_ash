---
title: Git CLI 命令操作手册与详细介绍
date: 2026-04-02 10:00:00
categories: 技术
tags:
- Git
- CLI
- Tooling
- Workflow
---

`Git` 是目前最主流的分布式版本控制系统。很多人会用 `git add`、`git commit`、`git push`，但一旦进入分支协作、历史整理、冲突处理、误操作恢复，就容易开始混乱。

这篇文章按“从日常到深入”的顺序，把 `Git CLI` 的核心命令系统化整理出来：先讲最常用的工作流，再讲协作、历史、恢复、排错和高级功能，最后给出一份尽量完整的命令索引。

如果你只想先建立一套稳定工作流，可以重点看这些命令：`git init`、`git clone`、`git status`、`git add`、`git commit`、`git log`、`git diff`、`git branch`、`git switch`、`git restore`、`git fetch`、`git pull`、`git push`、`git merge`、`git rebase`、`git stash`、`git tag`、`git reset`、`git revert`、`git reflog`。

<!-- more -->

## 目录

- 1. Git 到底在管理什么
- 2. Git 配置与帮助系统
- 3. 新建仓库与获取仓库
- 4. Git 的四个核心区域
- 5. 日常高频命令
- 6. 分支与切换
- 7. 查看历史与定位问题
- 8. 远程仓库协作
- 9. 合并、变基与历史整理
- 10. 撤销、回退与恢复
- 11. 标签、暂存、清理与归档
- 12. 高级协作与维护命令
- 13. 常见场景速查
- 14. Git 命令全景索引
- 15. 学习建议

## 1. Git 到底在管理什么

先别急着背命令。真正理解 `Git`，关键是先理解它在管理什么。

`Git` 管理的不是“文件夹快照”这么简单，而是：

- 工作区：你当前正在编辑的文件。
- 暂存区：下一次提交准备带走的内容。
- 本地仓库：已经提交到当前仓库历史中的内容。
- 远程仓库：例如 `GitHub`、`GitLab`、`Gitea` 上的仓库副本。

`Git` 的大部分命令，本质上都是在这几个区域之间移动内容，或者比较它们之间的差异。

你可以把它简单理解成：

```text
工作区 --git add--> 暂存区 --git commit--> 本地仓库 --git push--> 远程仓库
```

反过来也成立：

```text
远程仓库 --git fetch/pull--> 本地仓库/当前分支
本地仓库 --git restore/reset--> 暂存区/工作区
```

如果这个模型不清楚，后面很多命令都会越用越乱。

## 2. Git 配置与帮助系统

### 2.1 查看版本

```bash
git --version
```

确认当前机器安装的 `Git` 版本。

### 2.2 基础配置

第一次使用 Git，通常先配用户名和邮箱：

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

查看当前生效配置：

```bash
git config --list
git config --global --list
git config --local --list
```

常见配置项：

- `user.name`：提交记录显示的用户名。
- `user.email`：提交记录显示的邮箱。
- `core.editor`：默认编辑器。
- `init.defaultBranch`：默认初始分支名，例如 `main`。
- `pull.rebase`：`git pull` 时默认走 `rebase` 还是 `merge`。
- `merge.tool`：冲突时使用的合并工具。
- `alias.xxx`：给常用命令设置别名。

例如：

```bash
git config --global init.defaultBranch main
git config --global core.editor "vim"
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --decorate --all"
```

### 2.3 查看某个配置值

```bash
git config user.name
git config --global core.editor
```

### 2.4 删除配置

```bash
git config --global --unset alias.co
git config --unset user.name
```

### 2.5 Git 帮助系统

```bash
git help
git help status
git status -h
git help config
git help -a
```

含义：

- `git help`：查看帮助入口。
- `git help status`：查看 `status` 的完整手册。
- `git status -h`：查看简短帮助。
- `git help -a`：列出所有可用子命令。

如果你真的想看“全部命令”，最权威的入口不是某篇博客，而是 `git help -a` 和官方手册。

## 3. 新建仓库与获取仓库

### 3.1 初始化仓库：`git init`

```bash
git init
git init my-project
```

作用：

- 把当前目录初始化成 Git 仓库。
- 或直接创建一个新目录并初始化仓库。

常见场景：

- 本地新项目开始纳入版本控制。
- 把已有代码目录变成仓库。

### 3.2 克隆仓库：`git clone`

```bash
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git
git clone https://github.com/user/repo.git myrepo
```

作用：

- 从远程获取完整仓库历史。
- 自动创建远程别名 `origin`。
- 默认检出远程默认分支。

常见参数：

- `--depth 1`：浅克隆，只拉最近历史。
- `--branch <name>`：克隆后直接检出指定分支。
- `--recurse-submodules`：同时拉取子模块。

例如：

```bash
git clone --depth 1 --branch main https://github.com/user/repo.git
```

### 3.3 判断当前目录是不是 Git 仓库

```bash
git rev-parse --is-inside-work-tree
```

输出 `true` 代表当前路径在仓库内部。

## 4. Git 的四个核心区域

理解这四个区域后，很多命令就不难了。

### 4.1 工作区

就是你当前磁盘上的真实文件。

### 4.2 暂存区

也叫 `index`。`git add` 并不是“提交”，而是把改动放入“下一次提交候选区”。

### 4.3 本地仓库

`git commit` 之后，内容进入本地历史。

### 4.4 远程仓库

`git push` 才会把本地提交送到远程。

### 4.5 最容易混淆的三个对比

```text
git diff              比较工作区 和 暂存区
git diff --cached     比较暂存区 和 最近一次提交
git diff HEAD         比较工作区 和 最近一次提交
```

这是很多人学 Git 时最容易糊的地方。

## 5. 日常高频命令

这一节是实际工作中最常用的部分。

### 5.1 查看状态：`git status`

```bash
git status
git status -s
git status --short
git status -b
```

作用：

- 查看当前分支。
- 查看哪些文件已修改。
- 查看哪些内容已暂存。
- 查看哪些文件未跟踪。

常见输出含义：

- `M`：已修改。
- `A`：已添加。
- `D`：已删除。
- `R`：已重命名。
- `??`：未跟踪文件。

### 5.2 添加到暂存区：`git add`

```bash
git add file.txt
git add src/
git add .
git add -A
git add -p
```

高频用法说明：

- `git add file.txt`：只暂存一个文件。
- `git add src/`：暂存一个目录。
- `git add .`：暂存当前目录下变更。
- `git add -A`：更明确地把新增、修改、删除都纳入暂存。
- `git add -p`：按代码块交互式暂存，适合拆分提交。

`git add -p` 非常实用。比如你在一个文件里同时做了“修 bug”和“顺手重构”，这时可以按块选择，只暂存你想提交的那部分。

### 5.3 提交：`git commit`

```bash
git commit -m "fix: handle empty response"
git commit
git commit --amend
git commit -a -m "docs: update README"
```

高频说明：

- `git commit -m`：直接写提交说明。
- `git commit`：进入编辑器写更完整说明。
- `git commit --amend`：修改上一次提交。
- `git commit -a -m`：把已跟踪文件的修改直接提交，不包含新文件。

提交信息建议：

- 写清楚“为什么改”。
- 一次提交只做一类事情。
- 不要把大量无关改动揉成一个提交。

### 5.4 查看差异：`git diff`

```bash
git diff
git diff --cached
git diff HEAD
git diff branchA..branchB
git diff commit1 commit2
git diff --stat
git diff --name-only
```

高频场景：

- 提交前确认到底改了什么。
- 对比两个提交、两个分支的内容差异。
- 看哪些文件变了，不看具体行时可以配 `--stat` 或 `--name-only`。

### 5.5 查看文件内容来自哪个提交：`git blame`

```bash
git blame file.txt
git blame -L 10,30 file.txt
```

作用：

- 看某一行是谁在什么时候改的。
- 排查历史问题时非常有用。

但别把 `blame` 只理解成“追责”，它更多是为了找上下文。

### 5.6 查看对象详情：`git show`

```bash
git show
git show HEAD
git show HEAD~1
git show <commit>
git show v1.0.0
```

作用：

- 查看某个提交的详细变更。
- 查看标签、对象、提交说明。

## 6. 分支与切换

### 6.1 查看分支：`git branch`

```bash
git branch
git branch -a
git branch -r
git branch -vv
```

说明：

- `git branch`：本地分支。
- `git branch -a`：本地和远程分支。
- `git branch -r`：远程跟踪分支。
- `git branch -vv`：看本地分支跟踪关系和最近提交。

### 6.2 创建分支

```bash
git branch feature/login
git switch -c feature/login
```

更推荐 `git switch -c`，语义更清晰：创建并切换。

### 6.3 切换分支：`git switch`

```bash
git switch main
git switch feature/login
git switch -c hotfix/header
git switch -
```

说明：

- `git switch -`：切回上一个分支。

旧命令里很多人还在用：

```bash
git checkout main
git checkout -b feature/login
```

现在更推荐把“切分支”和“恢复文件”交给 `git switch` / `git restore`，比 `checkout` 更不容易误用。

### 6.4 重命名分支

```bash
git branch -m old-name new-name
```

当前分支重命名：

```bash
git branch -m new-name
```

### 6.5 删除分支

```bash
git branch -d feature/login
git branch -D feature/login
```

区别：

- `-d`：安全删除，只删已经合并过的分支。
- `-D`：强制删除，没合并也删。

### 6.6 跟踪远程分支

```bash
git switch --track origin/feature/login
git checkout --track origin/feature/login
```

## 7. 查看历史与定位问题

### 7.1 历史查看：`git log`

```bash
git log
git log --oneline
git log --oneline --graph --decorate --all
git log -p
git log --stat
git log --author="ash"
git log --since="2026-01-01"
git log -- file.txt
```

高频组合：

```bash
git log --oneline --graph --decorate --all
```

这个几乎可以作为默认日志视图。

### 7.2 精简历史：`git shortlog`

```bash
git shortlog
git shortlog -sn
```

作用：

- 汇总提交者和提交数量。
- 适合快速看项目贡献概览。

### 7.3 查找历史中的某段文本：`git grep`

```bash
git grep "useEffect"
git grep "TODO"
git grep -n "function render"
```

它和系统里的 `grep` 不同，它是面向 Git 仓库内容的检索工具。

### 7.4 二分定位引入 bug 的提交：`git bisect`

```bash
git bisect start
git bisect bad
git bisect good <commit>
git bisect reset
```

工作流程：

1. 告诉 Git 当前版本是坏的。
2. 告诉 Git 某个历史提交是好的。
3. Git 自动在中间挑提交让你验证。
4. 你反复标记 `good` / `bad`，最终定位问题提交。

这个命令在“某个 bug 是什么时候引入的”这种场景里非常强。

## 8. 远程仓库协作

### 8.1 查看远程：`git remote`

```bash
git remote
git remote -v
```

### 8.2 添加远程

```bash
git remote add origin https://github.com/user/repo.git
git remote add upstream git@github.com:org/repo.git
```

常见约定：

- `origin`：你自己的默认远程。
- `upstream`：上游仓库，例如 fork 场景里的原始仓库。

### 8.3 修改远程地址

```bash
git remote set-url origin git@github.com:user/repo.git
```

### 8.4 删除远程

```bash
git remote remove upstream
```

### 8.5 获取远程更新：`git fetch`

```bash
git fetch
git fetch origin
git fetch --all
git fetch --prune
```

作用：

- 只拉取远程最新提交和引用。
- 不自动合并到当前分支。

`git fetch` 很安全，因为它不会直接改你的工作内容。

### 8.6 拉取并合并：`git pull`

```bash
git pull
git pull origin main
git pull --rebase
```

它本质上等于：

```text
git fetch + git merge
```

或者使用 `--rebase` 时：

```text
git fetch + git rebase
```

什么时候用 `pull --rebase`：

- 希望本地提交接在远程最新提交后面。
- 想减少无意义的 merge commit。

### 8.7 推送：`git push`

```bash
git push
git push origin main
git push -u origin feature/login
git push --tags
```

说明：

- `-u`：建立上游跟踪关系，之后可以直接 `git push` / `git pull`。
- `--tags`：推送标签。

### 8.8 强制推送

```bash
git push --force-with-lease
```

尽量不要直接用：

```bash
git push --force
```

原因：

- `--force` 可能覆盖别人已经推上来的提交。
- `--force-with-lease` 更安全，会先检查远程是否还是你预期的状态。

## 9. 合并、变基与历史整理

### 9.1 合并分支：`git merge`

```bash
git switch main
git merge feature/login
```

作用：

- 把另一个分支的提交合入当前分支。

常见参数：

- `--no-ff`：即使能快进，也创建 merge commit。
- `--squash`：把对方分支压成一个未提交改动，再由你手动提交。

### 9.2 变基：`git rebase`

```bash
git switch feature/login
git rebase main
```

含义：

- 把当前分支的提交“重新播放”到 `main` 最新提交之后。

优点：

- 历史更线性。
- 阅读提交链更顺。

代价：

- 会改写提交历史。
- 已共享给别人的分支上要谨慎使用。

### 9.3 交互式变基：`git rebase -i`

```bash
git rebase -i HEAD~3
```

常见用途：

- 合并多个碎提交。
- 调整提交顺序。
- 修改提交信息。
- 删除不需要的提交。

常见动作：

- `pick`：保留提交。
- `reword`：保留提交，修改信息。
- `edit`：中途停下，修改提交内容。
- `squash`：压缩到前一个提交，并合并说明。
- `fixup`：压缩到前一个提交，丢弃当前说明。
- `drop`：移除提交。

### 9.4 挑选提交：`git cherry-pick`

```bash
git cherry-pick <commit>
git cherry-pick commit1 commit2
```

作用：

- 只拿某一个提交到当前分支。
- 非常适合 hotfix 回灌、跨分支补丁迁移。

### 9.5 合并中断与继续

```bash
git merge --abort
git rebase --abort
git rebase --continue
git cherry-pick --abort
git cherry-pick --continue
```

这类命令在冲突处理中非常常见。

## 10. 撤销、回退与恢复

这是 Git 最容易让人误操作的一部分，要区分清楚。

### 10.1 恢复工作区文件：`git restore`

```bash
git restore file.txt
git restore .
git restore --source=HEAD~1 file.txt
```

作用：

- 丢弃工作区未暂存修改。
- 或把文件恢复成某个提交中的版本。

### 10.2 取消暂存：`git restore --staged`

```bash
git restore --staged file.txt
git restore --staged .
```

作用：

- 把文件从暂存区拿回工作区。
- 文件内容还在，只是不参与下一次提交了。

### 10.3 老写法：`git checkout -- file`

```bash
git checkout -- file.txt
```

历史上常用，但语义不够清晰，现在更推荐 `git restore`。

### 10.4 重置分支：`git reset`

```bash
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
```

三种模式必须分清：

- `--soft`：回退提交，保留暂存区和工作区。
- `--mixed`：回退提交，清空暂存区，保留工作区。这是默认模式。
- `--hard`：回退提交，同时覆盖暂存区和工作区，危险最大。

高频用途：

- 刚提交错了，想撤回重新整理：`git reset --soft HEAD~1`
- 想把暂存全部撤掉：`git reset`
- 确认不再需要改动，强制回到某版本：`git reset --hard <commit>`

### 10.5 反向提交撤销：`git revert`

```bash
git revert <commit>
git revert HEAD
```

作用：

- 不改写历史。
- 新建一个“反向提交”来抵消旧提交。

在已经推送到远程、已经共享给团队的提交上，通常优先考虑 `git revert`，而不是 `git reset`。

### 10.6 查看引用移动历史：`git reflog`

```bash
git reflog
git reflog show HEAD
```

这是救命命令。

场景：

- 你 `reset --hard` 了。
- 你误删分支了。
- 你做了 `rebase` 后找不到原来的提交了。

只要引用移动过，很多情况下都能从 `reflog` 找回来。

例如：

```bash
git reflog
git reset --hard HEAD@{3}
```

### 10.7 删除未跟踪文件：`git clean`

```bash
git clean -n
git clean -f
git clean -fd
git clean -fdx
```

说明：

- `-n`：先预览，不真正删除。
- `-f`：真正删除文件。
- `-d`：连目录一起删。
- `-x`：连 `.gitignore` 忽略的文件也删。

这是非常危险的命令，最好总是先跑一次 `git clean -n`。

## 11. 标签、暂存、清理与归档

### 11.1 标签：`git tag`

```bash
git tag
git tag v1.0.0
git tag -a v1.0.0 -m "release v1.0.0"
git show v1.0.0
git push origin v1.0.0
git push --tags
git tag -d v1.0.0
```

标签分两类：

- 轻量标签：只是一个引用。
- 附注标签：带作者、时间、说明，更适合正式发布。

### 11.2 临时保存现场：`git stash`

```bash
git stash
git stash push -m "wip: header refactor"
git stash list
git stash show
git stash show -p stash@{0}
git stash pop
git stash apply
git stash drop stash@{0}
git stash clear
```

适用场景：

- 改到一半，需要先切分支修 bug。
- 当前改动还不想提交。

区别：

- `pop`：恢复后同时删除 stash。
- `apply`：恢复但保留 stash 记录。

### 11.3 归档导出：`git archive`

```bash
git archive --format=zip --output=release.zip HEAD
git archive --format=tar HEAD | gzip > release.tar.gz
```

适合导出某个提交的源代码快照，但不包含 `.git` 历史。

## 12. 高级协作与维护命令

### 12.1 多工作树：`git worktree`

```bash
git worktree list
git worktree add ../repo-hotfix hotfix/login
git worktree remove ../repo-hotfix
```

作用：

- 一个仓库同时检出多个分支到不同目录。
- 特别适合“主线开发中，临时开一个目录修线上 bug”。

### 12.2 子模块：`git submodule`

```bash
git submodule status
git submodule update --init --recursive
git submodule add <url> path/to/submodule
```

作用：

- 在一个仓库中引用另一个仓库的特定提交。

但子模块管理复杂度比较高，能不用就尽量别滥用。

### 12.3 仓库完整性检查：`git fsck`

```bash
git fsck
```

作用：

- 检查对象完整性和引用有效性。

### 12.4 垃圾回收与优化：`git gc`

```bash
git gc
git gc --prune=now
```

作用：

- 压缩对象。
- 清理不可达对象。
- 优化仓库存储。

### 12.5 打包传输对象：`git bundle`

```bash
git bundle create repo.bundle --all
git clone repo.bundle repo-copy
```

适合离线传输仓库。

### 12.6 查看引用：`git show-ref`

```bash
git show-ref
git show-ref --heads
git show-ref --tags
```

### 12.7 解析对象名：`git rev-parse`

```bash
git rev-parse HEAD
git rev-parse --short HEAD
git rev-parse --abbrev-ref HEAD
```

这类命令在脚本里非常常见。

## 13. 常见场景速查

### 13.1 新项目第一次提交

```bash
git init
git add -A
git commit -m "chore: initial commit"
```

### 13.2 从远程拉代码开始工作

```bash
git clone <repo-url>
git switch -c feature/xxx
```

### 13.3 提交前检查

```bash
git status
git diff
git diff --cached
```

### 13.4 提交到远程新分支

```bash
git push -u origin feature/xxx
```

### 13.5 暂时保存现场去修别的问题

```bash
git stash push -m "wip"
git switch main
```

修完后：

```bash
git switch feature/xxx
git stash pop
```

### 13.6 本地提交还没推送，想重新整理

```bash
git reset --soft HEAD~1
```

### 13.7 远程已经有别人提交，先同步再推送

```bash
git fetch origin
git rebase origin/main
git push
```

### 13.8 误删提交，想找回来

```bash
git reflog
git reset --hard HEAD@{n}
```

### 13.9 回退线上某次错误提交

```bash
git revert <bad-commit>
git push
```

### 13.10 清掉未跟踪垃圾文件

```bash
git clean -n
git clean -fd
```

## 14. Git 命令全景索引

这一节按类别列出常见和重要命令。严格来说，`Git` 还包含不少 plumbing 命令和内部维护命令，因此“覆盖所有命令”在实践里更适合理解为：覆盖你日常开发、排错、维护和脚本里最可能接触到的完整命令体系。

如果你想看当前版本 Git 提供的全部子命令，请执行：

```bash
git help -a
```

### 14.1 初始化与获取

- `git init`：初始化仓库。
- `git clone`：克隆仓库。

### 14.2 配置与帮助

- `git config`：查看和设置配置。
- `git help`：查看帮助。
- `git bugreport`：生成 bug 报告信息。

### 14.3 工作区与暂存区

- `git status`：查看状态。
- `git add`：加入暂存区。
- `git restore`：恢复工作区或暂存区。
- `git rm`：删除文件并记录到 Git。
- `git mv`：移动或重命名文件。
- `git clean`：删除未跟踪文件。

### 14.4 提交与历史

- `git commit`：提交。
- `git log`：查看历史。
- `git show`：查看对象详情。
- `git diff`：查看差异。
- `git blame`：查看行级作者信息。
- `git annotate`：`blame` 的相关形式。
- `git shortlog`：摘要式日志。
- `git describe`：根据最近标签描述提交。

### 14.5 分支与引用

- `git branch`：管理分支。
- `git switch`：切换分支。
- `git checkout`：旧式切换/恢复命令。
- `git tag`：管理标签。
- `git show-ref`：查看引用。
- `git update-ref`：底层更新引用。

### 14.6 远程协作

- `git remote`：管理远程。
- `git fetch`：获取远程更新。
- `git pull`：拉取并合并或变基。
- `git push`：推送提交。
- `git ls-remote`：查看远程引用。
- `git request-pull`：生成拉取请求摘要。

### 14.7 合并与历史整理

- `git merge`：合并分支。
- `git rebase`：变基。
- `git cherry-pick`：挑选提交。
- `git revert`：反向提交撤销。
- `git reset`：移动当前分支并可重置暂存区/工作区。
- `git range-diff`：比较两组提交序列。

### 14.8 暂存现场与补丁

- `git stash`：暂存现场。
- `git apply`：应用补丁。
- `git am`：应用邮件格式补丁。
- `git format-patch`：导出补丁。

### 14.9 搜索与排错

- `git grep`：搜索内容。
- `git bisect`：二分定位问题提交。
- `git reflog`：查看引用变动历史。
- `git fsck`：检查仓库完整性。

### 14.10 子模块、多工作区与归档

- `git submodule`：管理子模块。
- `git worktree`：多工作树。
- `git archive`：导出归档。
- `git bundle`：离线打包仓库。

### 14.11 对象库与维护

- `git gc`：垃圾回收。
- `git prune`：清理不可达对象。
- `git repack`：重新打包对象。
- `git pack-refs`：压缩引用存储。
- `git count-objects`：统计对象数量。
- `git maintenance`：仓库维护任务。

### 14.12 常见 plumbing 命令

这些命令平时不一定直接手敲，但在脚本、底层理解和高级排错里很重要：

- `git cat-file`：查看对象内容。
- `git hash-object`：计算对象哈希并可写入对象库。
- `git ls-files`：列出索引和工作树文件。
- `git ls-tree`：查看树对象。
- `git read-tree`：把树对象读入索引。
- `git write-tree`：把索引写成树对象。
- `git commit-tree`：直接基于树对象创建提交。
- `git mktree`：从文本描述创建树对象。
- `git mktag`：创建标签对象。
- `git rev-parse`：解析修订表达式。
- `git rev-list`：列出提交对象。
- `git name-rev`：用可读名称描述提交。
- `git merge-base`：查找分支共同祖先。
- `git symbolic-ref`：读取或修改符号引用。
- `git for-each-ref`：遍历引用。
- `git update-index`：直接操作索引。
- `git checkout-index`：从索引签出文件。
- `git diff-index`：比较树和工作区/索引。
- `git diff-tree`：比较两个树对象。
- `git diff-files`：比较工作区和索引。
- `git unpack-objects`：解包对象。
- `git pack-objects`：打包对象。
- `git verify-pack`：校验 pack 文件。
- `git unpack-file`：解出 blob 内容。
- `git replace`：用替代对象覆盖显示效果。
- `git notes`：附加注释对象。

### 14.13 邮件工作流相关命令

这类命令在内核社区或部分传统开源项目里比较常见：

- `git send-email`
- `git imap-send`
- `git mailinfo`
- `git mailsplit`
- `git mailmap`
- `git am`
- `git format-patch`
- `git request-pull`

## 15. 学习建议

如果你不是想研究 Git 内部实现，而是想把工作流先跑稳，建议按下面顺序掌握：

1. 先彻底搞懂 `status`、`add`、`commit`、`diff`、`log`。
2. 再掌握 `branch`、`switch`、`fetch`、`pull`、`push`。
3. 然后掌握 `merge`、`rebase`、`stash`、`tag`。
4. 最后重点掌握 `restore`、`reset`、`revert`、`reflog`，这组命令决定你出问题时能不能救回来。

我自己的建议是：

- 每次提交前都跑一次 `git status`。
- 每次提交前都看一次 `git diff --cached`。
- 已经推送到共享分支的历史，优先用 `git revert`，少用改写历史的方式。
- 强制推送优先用 `git push --force-with-lease`。
- 遇到 Git 混乱时，先停下来，看 `status`、`log`、`reflog`，不要盲目敲命令。

最后给一个非常实用的最小速查表：

```bash
git status
git add -A
git diff
git diff --cached
git commit -m "message"
git log --oneline --graph --decorate --all
git switch -c feature/xxx
git fetch --all --prune
git pull --rebase
git push -u origin feature/xxx
git restore --staged .
git restore .
git reset --soft HEAD~1
git revert <commit>
git stash push -m "wip"
git stash pop
git reflog
```

如果你把上面这一组命令吃透了，已经能覆盖绝大多数日常开发场景。
