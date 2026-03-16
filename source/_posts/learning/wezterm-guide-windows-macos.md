---
title: WezTerm Guide：Windows 和 macOS 的入门、配置与日常工作流
date: 2026-03-17
categories: AI与工具
tags:
- WezTerm
- Terminal
- Tooling
- Productivity
---

WezTerm 这两年基本成了我最愿意推荐给开发者的终端之一：配置文件化、标签页和分屏能力强、跨平台一致性也不错。

但很多教程有两个问题：要么只讲“怎么装”，要么一上来就把配置堆得很满。对大多数人来说，真正需要的不是一份炫技配置，而是一套稳定可落地的起步方案。

这篇文章把 Windows 和 macOS 放在一起写，目标很直接：先让你用起来，再决定要不要继续折腾。

<!-- more -->

## 一、先讲清楚：WezTerm 是什么，不是什么

WezTerm 是终端模拟器，不是 shell。

你可以把它理解成两层：

- `WezTerm`：窗口、标签页、分屏、渲染、快捷键、主题
- `Shell`：真正执行命令的环境，比如 Windows 上的 `PowerShell`，macOS 上的 `zsh`

所以“我想把 WezTerm 配成 PowerShell / zsh”这句话，更准确地说是：

- 用 WezTerm 作为终端界面
- 用 PowerShell 或 zsh 作为默认 shell

这个区分很重要，因为后面很多配置项其实都是围绕这两层展开的。

## 二、为什么我会推荐 WezTerm

和系统自带终端相比，WezTerm 最实用的优势有 4 个：

1. 配置文件就是 `~/.wezterm.lua`，适合版本管理和渐进调整。
2. 默认就有很强的标签页、分屏、搜索和复制粘贴能力。
3. Windows / macOS / Linux 的整体体验比较统一，换机器成本低。
4. 改完配置可以直接重载，不需要每次去找图形设置界面。

如果你是开发者，尤其经常需要同时跑服务、看日志、连远程机器，它会比“能用就行”的终端更顺手。

## 三、先用最稳的思路，不要一开始就过度定制

我更建议按这个顺序上手：

- 第一步：先确定默认 shell
- 第二步：先选一个稳定深色主题
- 第三步：先用官方默认快捷键
- 第四步：一周后再决定要不要改键位、字体和状态栏

原因很简单：

- shell 是工作流核心，先稳定
- 主题影响阅读舒适度，先解决
- 快捷键属于肌肉记忆，改太早容易把自己弄乱

如果你当前目标只是“日常开发能稳定用”，那这套路径比一上来抄一份 200 行配置更有效。

## 四、Windows：最适合大多数人的起步方案

### 1）安装与配置文件位置

Windows 上装好 WezTerm 后，默认配置文件通常放在：

`%USERPROFILE%\.wezterm.lua`

例如：

`C:\Users\<你的用户名>\.wezterm.lua`

改完配置后，推荐用 `Ctrl+Shift+R` 重载；不行再完全重启 WezTerm。

### 2）Windows 推荐默认组合

如果你不想折腾，最稳的默认组合是：

- 终端：`WezTerm`
- 默认 shell：`powershell.exe -NoLogo`
- 主题：`Tokyo Night Storm`
- 快捷键：官方默认

之所以先推荐 `powershell.exe`，不是因为它最强，而是因为它通常最稳定。`pwsh.exe` 当然更现代，但 profile、模块、环境变量一旦有历史包袱，排错成本会更高。

### 3）一份够用的 Windows 配置

```lua
local wezterm = require("wezterm")

return {
  color_scheme = "Tokyo Night Storm",
  window_background_opacity = 0.92,
  text_background_opacity = 1.0,

  enable_tab_bar = true,
  hide_tab_bar_if_only_one_tab = true,
  use_fancy_tab_bar = false,
  tab_max_width = 32,
  window_padding = { left = 8, right = 8, top = 6, bottom = 6 },

  default_prog = { "powershell.exe", "-NoLogo" },
  exit_behavior = "Close",
  scrollback_lines = 8000,
  adjust_window_size_when_changing_font_size = false,

  launch_menu = {
    { label = "Windows PowerShell", args = { "powershell.exe", "-NoLogo" } },
    { label = "PowerShell 7", args = { "pwsh.exe", "-NoLogo", "-NoProfile" } },
    { label = "Command Prompt", args = { "cmd.exe" } },
  },
}
```

这份配置的重点不是“炫”，而是稳：

- 深色主题，提升长期阅读舒适度
- 轻微透明和边距，界面更松弛
- 默认用 `powershell.exe`
- 保留 `launch_menu`，需要时再手动切到 `pwsh` 或 `cmd`

### 4）Windows 日常最常用快捷键

- 新建标签页：`Ctrl+Shift+T`
- 关闭当前标签页：`Ctrl+Shift+W`
- 新建窗口：`Ctrl+Shift+N`
- 复制：`Ctrl+Shift+C`
- 粘贴：`Ctrl+Shift+V`
- 搜索输出：`Ctrl+Shift+F`
- 重载配置：`Ctrl+Shift+R`

分屏常见默认键位：

- 水平分屏：`Ctrl+Shift+Alt+"`
- 垂直分屏：`Ctrl+Shift+Alt+%`

如果你的键盘布局和这两个符号位置不一致，不用慌，这在 Windows 上很常见。

### 5）Windows 常见坑

最典型的三个问题：

- 配了系统里没有的字体，导致启动时报字体错误
- 把 `pwsh.exe` 设成默认后，profile 报错直接退出
- 改了配置但没重载，误以为配置没生效

我的建议是：

- 刚开始先不要配字体
- 默认 shell 先用 `powershell.exe`
- 任何修改先按 `Ctrl+Shift+R` 再判断

## 五、macOS：更自然的组合是 WezTerm + zsh

### 1）安装与配置文件位置

macOS 最省事的安装方式是 Homebrew：

```bash
brew install --cask wezterm
```

配置文件位置是：

`~/.wezterm.lua`

例如：

`/Users/<你的用户名>/.wezterm.lua`

改完配置后，推荐按 `Command+Shift+R` 重载。

### 2）macOS 推荐默认组合

Mac 上最自然的起步方案通常是：

- 终端：`WezTerm`
- 默认 shell：`/bin/zsh -l`
- 主题：`Tokyo Night Storm`
- 快捷键：官方默认

之所以推荐 `zsh -l`，是因为它更贴近 macOS 的默认行为。很多用户的 PATH、Homebrew 初始化、代理配置、别名和提示符，都是在 shell login 过程里建立起来的。

### 3）一份够用的 macOS 配置

```lua
local wezterm = require("wezterm")

return {
  color_scheme = "Tokyo Night Storm",
  window_background_opacity = 0.95,
  text_background_opacity = 1.0,

  enable_tab_bar = true,
  hide_tab_bar_if_only_one_tab = true,
  use_fancy_tab_bar = false,
  tab_max_width = 32,
  window_padding = { left = 8, right = 8, top = 6, bottom = 6 },

  default_prog = { "/bin/zsh", "-l" },
  exit_behavior = "Close",
  scrollback_lines = 10000,
  adjust_window_size_when_changing_font_size = false,

  launch_menu = {
    { label = "zsh", args = { "/bin/zsh", "-l" } },
    { label = "bash", args = { "/bin/bash", "-l" } },
  },
}
```

如果你还装了 `fish`、`pwsh` 之类的 shell，再把它们补进 `launch_menu` 就行。需要注意的是，Homebrew 在 Apple Silicon 和 Intel Mac 上的安装路径不同：

- Apple Silicon 常见是 `/opt/homebrew/bin`
- Intel Mac 常见是 `/usr/local/bin`

### 4）macOS 日常最常用快捷键

macOS 下很多高频操作优先用 `Command`，也就是 WezTerm 文档里的 `SUPER`：

- 新建标签页：`Command+T`
- 关闭当前标签页：`Command+W`
- 新建窗口：`Command+N`
- 复制：`Command+C`
- 粘贴：`Command+V`
- 搜索输出：`Command+F`
- 放大字体：`Command+=`
- 缩小字体：`Command+-`
- 重置字体：`Command+0`
- 重载配置：`Command+Shift+R`

要特别注意：

- `Ctrl+C` 在终端里通常还是中断当前进程，不是复制
- 分屏默认键位通常仍是 `Ctrl+Shift+Alt+"` 和 `Ctrl+Shift+Alt+%`

### 5）macOS 常见坑

最常见的不是 WezTerm 本身出问题，而是 shell 路径没配对：

- `default_prog` 指向了不存在的可执行文件
- Homebrew shell 的路径写成了另一种架构的目录
- 你以为在跟随系统默认 shell，其实手动写死了 `default_prog`

遇到这类问题时，先用下面几个命令确认路径：

```bash
echo $SHELL
which zsh
which bash
which fish
which pwsh
```

## 六、跨平台都适用的配置理解

不管是 Windows 还是 macOS，真正最值得理解的是这几类配置项：

### 1）外观相关

- `color_scheme`：主题名称
- `window_background_opacity`：窗口背景透明度
- `text_background_opacity`：文本背景透明度
- `window_padding`：内容和边缘的留白

建议：

- 先固定一个深色主题，不要频繁切换
- 透明度轻一点就够了，过高会影响阅读

### 2）标签页相关

- `enable_tab_bar`
- `hide_tab_bar_if_only_one_tab`
- `use_fancy_tab_bar`
- `tab_max_width`

起步阶段我更推荐：

- 开启标签栏
- 单标签时自动隐藏
- 关闭 fancy tab bar，保持简洁

### 3）启动相关

- `default_prog`：默认启动哪个 shell
- `default_cwd`：默认目录（Windows 更常用）
- `launch_menu`：新建标签或窗口时可选启动项
- `exit_behavior`：最后进程退出时窗口怎么处理

如果你希望配置长期稳定，`launch_menu` 很值得加。它能让“主力 shell 稳定”和“保留其他入口”同时成立。

### 4）体验相关

- `scrollback_lines`：历史输出回滚行数
- `adjust_window_size_when_changing_font_size`：调字号时是否改变窗口尺寸

一般来说：

- `8000-20000` 行足够大多数开发场景
- 关闭字号联动改窗体尺寸，体验更稳定

## 七、我建议的上手路径：三阶段就够了

### 阶段 A：先稳定用起来

- 只保留默认 shell、深色主题、官方快捷键
- 熟悉标签页、复制粘贴、搜索、分屏

### 阶段 B：只加少量增强

- 增加 2-4 个高频键位
- 增加 `launch_menu`
- 根据阅读习惯微调透明度、边距、滚动回溯行数

### 阶段 C：最后再做重度定制

- 字体与 fallback
- 状态栏与 workspace
- leader key
- 启动时自动布局

这一阶段当然很爽，但并不是“好用”的前提。

## 八、两套我更推荐的模板

如果你只想抄一份能用的配置，可以直接从下面两套开始。

### Windows 模板

```lua
local wezterm = require("wezterm")

return {
  color_scheme = "Tokyo Night Storm",
  window_background_opacity = 0.92,
  text_background_opacity = 1.0,
  enable_tab_bar = true,
  hide_tab_bar_if_only_one_tab = true,
  use_fancy_tab_bar = false,
  tab_max_width = 32,
  window_padding = { left = 8, right = 8, top = 6, bottom = 6 },
  default_prog = { "powershell.exe", "-NoLogo" },
  exit_behavior = "Close",
  scrollback_lines = 8000,
  adjust_window_size_when_changing_font_size = false,
}
```

### macOS 模板

```lua
local wezterm = require("wezterm")

return {
  color_scheme = "Tokyo Night Storm",
  window_background_opacity = 0.95,
  text_background_opacity = 1.0,
  enable_tab_bar = true,
  hide_tab_bar_if_only_one_tab = true,
  use_fancy_tab_bar = false,
  tab_max_width = 32,
  window_padding = { left = 8, right = 8, top = 6, bottom = 6 },
  default_prog = { "/bin/zsh", "-l" },
  exit_behavior = "Close",
  scrollback_lines = 10000,
  adjust_window_size_when_changing_font_size = false,
}
```

## 九、最后给一个很实际的建议

很多人喜欢问：“WezTerm 最强配置是什么？”

我现在更认同另一种问法：你每天最常做的 3 件终端操作是什么？

如果你的答案是：

- 开项目
- 跑服务
- 看日志

那你真正需要的往往只有这些：

- 稳定的默认 shell
- 好读的主题
- 够用的标签页和分屏
- 不打架的快捷键

先把这 4 件事配好，WezTerm 就已经足够成为主力终端了。剩下的高级玩法，等你真的需要时再加，完全不晚。
