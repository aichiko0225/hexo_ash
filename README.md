# ash 的 Hexo 博客（Stellar 主题）

这是我的个人博客仓库，技术栈是 **Hexo + Stellar**。

- 博客框架：Hexo
- 主题：Stellar（以 git submodule 方式放在 `themes/stellar`）
- 包管理与脚本：`yarn`
- 部署：`hexo-deployer-git`，发布到 `memoirs` 仓库

线上地址（当前配置）：`https://aichiko0225.github.com/memoirs`

---

## 仓库当前情况

核心目录（重点看这些）：

- `source/`：博客内容（文章、页面、图片、笔记入口）
- `_config.yml`：Hexo 主配置（站点信息、URL、部署、主题选择）
- `_config.stellar.yml`：Stellar 主题配置（菜单、页脚、组件等）
- `source/_data/wiki/notes.yml`：当前笔记系统（wiki 模式）的配置
- `themes/stellar/`：Stellar 主题子模块

另外：

- `public/` 是构建产物目录（每次 `yarn build` 会重建）
- `.deploy_git/` 是 Hexo deploy 的工作目录，可删除，部署时会自动重建

---

## 本地运行（快速开始）

> 本仓库统一使用 `yarn`，不使用 npm。

```bash
yarn install
yarn clean
yarn build
yarn server
```

访问本地预览地址（默认）：`http://localhost:4000`

### 常用命令

```bash
yarn clean      # 清理 public/.cache 等
yarn build      # 生成静态文件到 public/
yarn server     # 本地预览
yarn deploy     # 按 _config.yml 的 deploy 配置发布
```

---

## Hexo 你要记住的几件事

### 1) 新建文章

```bash
yarn hexo new post "文章标题"
```

默认会生成到 `source/_posts/`。

### 2) 新建独立页面

```bash
yarn hexo new page about/test
```

会生成 `source/about/test/index.md`（或同等页面结构）。

### 3) Front-matter 最常用字段

```yaml
---
title: 文章标题
date: 2026-03-15 10:00:00
tags:
  - React
categories:
  - IT技术
---
```

---

## Stellar 重点（这部分最常用）

Stellar 的优势是：不仅能写博客，还能做 wiki、专栏、笔记系统，且标签组件很多。

### 配置分层（在这个仓库里）

- `_config.yml`：Hexo 全局配置（例如 `theme: stellar`、`deploy`）
- `_config.stellar.yml`：主题行为配置（例如底部菜单 `menubar`）
- `source/_data/**/*.yml`：内容系统配置（例如 `wiki/notes.yml`）

### 你现在启用的笔记入口

在 `_config.stellar.yml` 里已经有：

- `menubar.items.notes`
- URL 指向 `/notes/`

并且页面入口文件已存在：

- `source/notes/index.md`

当前 front-matter：

```yaml
---
title: 我的笔记本
wiki: notes
menu_id: notes
comments: false
---
```

这表示：你现在的“笔记”是基于 Stellar 的 **wiki 文档系统模式**。

---

## 我还没写过笔记：从 0 到 1（按你仓库现状）

你现在最适合先用「简易笔记模式」（wiki）。步骤如下。

### 第一步：确认笔记配置文件

文件：`source/_data/wiki/notes.yml`

你现在已经有基础配置：

```yaml
name: 笔记本
title: 我的笔记本
base_dir: /notes/
```

可以逐步加 `tree`（目录树），例如：

```yaml
tree:
  前端:
    - react-hooks
  iOS:
    - runtime
```

### 第二步：创建第一篇笔记页面

示例新建文件：`source/notes/react-hooks.md`

```markdown
---
title: React Hooks 速记
date: 2026-03-15 10:00:00
---

# React Hooks 速记

- useState: 管理组件局部状态
- useEffect: 处理副作用
- useMemo: 缓存计算结果
```

然后在 `notes.yml` 的 `tree` 中加上 `react-hooks`，即可在笔记入口组织展示。

### 第三步：本地预览

```bash
yarn clean && yarn build
yarn server
```

访问：`/notes/`

---

## Stellar 的 note 用法（你问的“note 笔记”）

这里有两层意思，容易混淆：

1. **笔记系统（notes/notebook）**：内容组织方式（一个页面系统）
2. **`{% note %}` 标签插件**：文章里的提示框样式

你问“note 用法”时，很多时候其实是第 2 种。先给你最实用示例：

### 1) 单行 note 提示框

```md
{% note 这是一个默认提示 %}
{% note color:green 这是一个成功提示 %}
{% note color:yellow 注意 这个接口有速率限制 %}
{% note color:error 警告 请勿提交密钥到仓库 %}
```

语法（Stellar）：

```md
{% note [color:color] [title] content %}
```

可用颜色通常包括：
`red`, `orange`, `yellow`, `green`, `cyan`, `blue`, `purple`, `light`, `dark`, `warning`, `error`

### 2) 多段内容建议用 box/folding

`note` 适合短提示；如果你要放多段 Markdown、代码块，建议用：

````md
{% box 实战建议 color:blue %}
先本地跑通，再部署。

```bash
yarn clean && yarn build
```
{% endbox %}
````

或者可折叠：

```md
{% folding 排查步骤 open:false color:yellow %}
1. 检查 front-matter
2. 检查标签拼写
3. 检查 base_dir
{% endfolding %}
```

---

## 如何把“简易笔记”升级成“完整笔记体系”

Stellar 还有更完整的 notebook 系统（`/notebooks/` 体系），特点是：

- 以 `updated` 为主排序（更贴近笔记维护习惯）
- 支持标签树（tagtree）
- 支持多个 notebook

这套在你当前仓库还没启用。建议先把 `/notes/` 跑顺，再决定是否升级。

---

## 参考文档（建议收藏）

- Hexo 文档：`https://hexo.io/zh-cn/docs/`
- Stellar 文档首页：`https://xaoxuu.com/wiki/stellar/`
- Stellar 标签组件：`https://xaoxuu.com/wiki/stellar/tag-plugins/`
- Stellar 容器类标签（含 box/folding）：`https://xaoxuu.com/wiki/stellar/tag-plugins/container/`
- Stellar 简易笔记（wiki 方案）：`https://xaoxuu.com/wiki/stellar/wiki-settings/notes/`
- Stellar 完整笔记体系：`https://xaoxuu.com/wiki/stellar/notebooks/`

---

## 维护建议（给未来的我）

- 每次改配置后先执行：`yarn clean && yarn build`
- 发布前先本地看一眼 `/`、`/notes/`、`/about/`
- 升级 Stellar 子模块后，先看 release notes，再构建
- 不要手改 `public/` 和 `.deploy_git/`

如果你愿意，我下一步可以直接帮你：

1. 按你现在的内容方向，生成一个可直接用的 `source/_data/wiki/notes.yml` 目录树模板。
2. 一次性创建 3 篇“示例笔记”Markdown（React、iOS、工具链），你改内容就能发布。
