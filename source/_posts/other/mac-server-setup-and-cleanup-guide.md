---
title: 把一台 Mac 整理成可远程管理的小服务器：搭建、清理与实操清单
date: 2026-05-26
categories: 技术
tags:
- macOS
- SSH
- Docker
- Tooling
---

这篇文档不是泛泛而谈的教程，而是基于我对这台 Mac 的实际检查结果整理出来的实操手册。目标很明确：

- 保留日常使用能力
- 支持外网 SSH 登录
- 支持后续运行 Docker 和 Web 服务
- 明确哪些软件该保留，哪些该停用，哪些可以卸载
- 明确哪些目录值得清理，哪些不要乱删

这台机器不是要改造成一台纯 Linux 服务器，而是整理成一台“可以远程管理、可以长期开机、可以运行服务”的 macOS 工作机。

<!-- more -->

---

## 1. 这台 Mac 当前的实际情况

先把当前状态说清楚，这样后面的操作才不会空泛。

### 1.1 系统与空间

- 系统版本：`macOS 13.7.7`
- 系统盘总容量：约 `233Gi`
- 当前已用：约 `8.7Gi`
- 当前可用：约 `63Gi`

结论：

- 这台机器当前不是“系统盘爆了”
- 真正的问题是本地内容、缓存、聊天软件容器数据、后台网络工具偏多
- 所以整理重点不是重装系统，而是收敛后台、自启和大目录

### 1.2 当前登录用户和 SSH 用户

我已经确认过这台机器当前的本地用户信息：

- 登录用户名：`ash`
- 主目录：`/Users/ash`
- Shell：`/bin/zsh`
- 真实姓名：`赵光飞`
- 用户 UID：`501`

这一点很重要：

**SSH 用户名就是 `ash`，不是“赵光飞”这个显示名。**

也就是说，未来无论你在局域网还是在公网登录，命令格式都应该是：

```bash
ssh ash@192.168.0.108
```

或者：

```bash
ssh -p 你的外网端口 ash@你的花生壳域名
```

### 1.3 当前 SSH 权限状态

我已经确认：

- 用户 `ash` 已经在 `com.apple.access_ssh` 组里
- 也就是说，**系统权限上 `ash` 是允许 SSH 登录的**
- 但 `sshd` 当前没有在运行，说明 `Remote Login` 还没有真正启用

检查结果对应的命令如下：

```bash
dseditgroup -o checkmember -m ash com.apple.access_ssh
launchctl print system/com.openssh.sshd
```

其中返回结果已经确认：

- `yes ash is a member of com.apple.access_ssh`
- `sshd` 当前 `state = not running`

所以后续的关键操作不是“新建 SSH 用户”，而是：

1. 打开 `Remote Login`
2. 用 `ash` 这个账号登录
3. 用花生壳把外网流量转发到本机 `22` 端口

### 1.4 当前内网地址

当前内网 IP 已确认是：

```text
192.168.0.108
```

这意味着你后面做花生壳时，内网映射目标可以先按这个地址配置。但从长期稳定角度，还是建议你到路由器里把这台 Mac 的 DHCP 地址固定住，避免后面 IP 变掉。

---

## 2. 你真正要保留的远程方案

你现在提到的几个东西，需要先分工明确。

### 2.1 UU Remote 的定位

你本机装了：

- `UURemote.app`
- `/Library/LaunchAgents/com.netease.uuremote.agent.plist`
- `/Library/LaunchDaemons/com.netease.uuremote.daemon.plist`

这说明 UU Remote 已经不只是一个普通 App，而是带后台常驻组件。

它适合做：

- 远程桌面
- 临时远控
- 你已经熟悉的组网访问方式

它**不适合**代替标准 SSH 服务。

原因很简单：

- 它不是标准 OpenSSH 服务端
- 你以后如果要跑脚本、部署 Docker、端口转发、SFTP、Git 拉代码，还是标准 SSH 最稳
- 博客、自动化脚本、开发工具都默认围绕 SSH 工作

结论：

- **UU Remote 保留**
- **但它只作为远控备用，不作为主远程入口**

### 2.2 花生壳的定位

你本机已经有：

- `PhDDNS.app`
- 相关后台进程 `application.com.oray.phddns.clientmac...`

花生壳的正确定位是：

- 外网入口
- 内网穿透
- 公网域名和端口映射

它应该做的事只有两类：

1. 把公网 TCP 端口映射到这台 Mac 的 `22`
2. 后续把公网 Web 端口映射到 Docker 服务端口

它不负责：

- 替代 SSH
- 管理本机用户
- 管理本机密码

### 2.3 正确的远程结构

最终结构应该是：

```text
外网电脑
  -> 花生壳公网域名:外网端口
  -> 映射到 Mac 内网 IP 192.168.0.108:22
  -> macOS 自带 OpenSSH (Remote Login)
  -> 登录用户 ash
```

如果以后要对外暴露 Web 服务，则是：

```text
外网浏览器
  -> 花生壳公网域名:80/443/8080...
  -> 映射到 Mac 内网 IP 192.168.0.108:容器端口
  -> Docker 容器里的 Web 服务
```

---

## 3. SSH 用户名和密码到底是什么，在哪里看

这是你特别关心的一块，我单独写清楚。

### 3.1 SSH 用户名是什么

SSH 用户名就是本地 macOS 用户名：

```text
ash
```

查看方法：

```bash
whoami
id
dscl . -read /Users/ash
```

### 3.2 SSH 密码是什么

SSH 密码就是这个 macOS 本地用户 `ash` 的登录密码。

也就是说：

- 你平时登录这台 Mac 的账户密码
- 就是以后 SSH 用的密码

### 3.3 能不能“查看”当前 SSH 密码

**不能。**

macOS 和绝大多数现代系统一样，不允许你把本地用户密码明文读出来。

系统里存的是哈希，不是明文。  
我已经看到这个账户的认证方式是：

```text
ShadowHash
SALTED-SHA512-PBKDF2
```

这表示：

- 系统知道这个密码是否正确
- 但系统不会告诉你原密码是什么

所以 CLI 能做的是：

- 验证你输入的密码对不对
- 修改密码
- 重置密码

CLI 不能做的是：

- 读取当前密码明文

### 3.4 如果忘了密码怎么办

如果你还记得当前密码，可以直接改：

```bash
passwd
```

或者：

```bash
sysadminctl -newPassword -oldPassword
```

但更直观的是用管理员权限重置：

```bash
sudo sysadminctl -resetPasswordFor ash -newPassword -
```

这条命令的意思是：

- 以管理员身份
- 把用户 `ash` 的密码重置
- 新密码交互输入，不直接写在命令行里

如果你想用旧密码直接改自己的密码，也可以：

```bash
passwd ash
```

### 3.5 CLI 是否可以管理 SSH 用户和密码

可以管理很多，但不是无限制。

CLI 可以管理的内容：

- 开启或关闭 SSH 服务
- 允许哪些本地用户通过 SSH 登录
- 检查某个用户是否被允许 SSH 登录
- 修改某个本地用户密码
- 重置某个本地用户密码
- 配置公钥登录
- 配置 SSH 只允许某些用户
- 配置是否允许密码登录

CLI 不可以做的内容：

- 查看现有密码明文
- 直接“读取出”谁的密码是什么

### 3.6 实际常用命令

查看某个用户是否允许 SSH：

```bash
dseditgroup -o checkmember -m ash com.apple.access_ssh
```

把某个用户加入 SSH 允许列表：

```bash
sudo dseditgroup -o edit -a ash -t user com.apple.access_ssh
```

从 SSH 允许列表移除某个用户：

```bash
sudo dseditgroup -o edit -d ash -t user com.apple.access_ssh
```

重置用户密码：

```bash
sudo sysadminctl -resetPasswordFor ash -newPassword -
```

---

## 4. 明天正确的操作顺序

你今天不准备动，明天远程慢慢搞，那最稳妥的顺序是：

1. 先打通本机 SSH
2. 再打通花生壳公网访问
3. 再补密钥登录
4. 再处理 Docker
5. 最后再慢慢清理应用和文件

这个顺序的原因很现实：

- 先保证远程入口可用
- 万一本地清理出问题，你还能远程修
- 避免先删东西再发现远程没打通

---

## 5. 明天第一阶段：先把 SSH 打通

### 5.1 图形界面打开 SSH

进入：

```text
System Settings > General > Sharing > Remote Login
```

把 `Remote Login` 打开。

如果系统让你选择：

- `All users`
- `Only these users`

建议选：

```text
Only these users
```

然后确保 `ash` 在里面。

### 5.2 用 CLI 打开 SSH

你也可以用命令行：

```bash
sudo systemsetup -setremotelogin on
```

检查状态：

```bash
sudo systemsetup -getremotelogin
```

检查 SSH 服务：

```bash
sudo launchctl print system/com.openssh.sshd
```

如果已经启用，应该能看到它被系统监听。

### 5.3 先本机测试 SSH

先在本机终端测试：

```bash
ssh ash@127.0.0.1
```

如果本机能连通，说明 SSH 服务本身是正常的。

### 5.4 再局域网测试 SSH

从同一局域网的另一台设备测试：

```bash
ssh ash@192.168.0.108
```

如果局域网能通，就说明：

- SSH 服务正常
- 用户名正常
- 密码正常
- 局域网访问正常

这一步成功之后，再做花生壳。

---

## 6. 明天第二阶段：花生壳映射 SSH

### 6.1 花生壳要映射什么

你先只映射一个服务：

- 类型：`TCP`
- 内网地址：`192.168.0.108`
- 内网端口：`22`

外网端口可以选择：

- `22`
- 或者更建议用一个高位端口，比如 `22222`

原因：

- 高位端口更不显眼
- 一些网络环境会限制默认 `22`

### 6.2 外网 SSH 测试方式

假设花生壳给你的外网域名是：

```text
example.oray.net
```

映射外网端口是：

```text
22222
```

那么外网登录命令就是：

```bash
ssh -p 22222 ash@example.oray.net
```

### 6.3 测试顺序

建议按这个顺序测：

1. `ssh ash@127.0.0.1`
2. `ssh ash@192.168.0.108`
3. `ssh -p 外网端口 ash@花生壳域名`

不要一步到位直接测公网。  
分层测试能快速定位问题到底在：

- 本机 SSH
- 局域网
- 花生壳
- 路由/NAT

---

## 7. 明天第三阶段：补 SSH 密钥登录

你当前本机 `~/.ssh` 里已经有这些文件：

```text
id_rsa
id_rsa.pub
known_hosts
known_hosts.old
```

但这不代表你的服务器端已经完成了公钥登录配置。这里最容易搞混。

### 7.1 本机现有密钥说明

我已经看到一把公钥指纹：

```text
2048 SHA256:M1FxvXA+he9Lc30/wOoHDt9tcfPyq1wRb6cqjUE8RfU ash66 (RSA)
```

这更像是你拿来连接别的机器的客户端密钥，不等于“当前 Mac 已经可用公钥登录”。

### 7.2 正确做法

如果你想让“别的电脑”免密登录这台 Mac，正确流程是：

1. 在“那台外部电脑”生成 SSH 密钥
2. 把那台电脑的公钥追加到这台 Mac 的：

```bash
~/.ssh/authorized_keys
```

### 7.3 在 Mac 上准备服务器端目录

先确保目录和权限正确：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 7.4 追加外部电脑公钥

把外部电脑上的公钥内容追加到：

```bash
~/.ssh/authorized_keys
```

例如：

```bash
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... your-laptop' >> ~/.ssh/authorized_keys
```

### 7.5 什么时候关闭密码登录

你明天先不急着关。

建议顺序：

1. 先确认密码登录能成功
2. 再确认公钥登录能成功
3. 最后再关密码登录

如果未来要关闭密码登录，可以在：

```text
/etc/ssh/sshd_config.d/99-server.conf
```

添加：

```text
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers ash
PermitRootLogin no
```

然后重启 SSH 服务或重新加载配置。

注意：

- 这一步一定要等公钥验证通过之后再做
- 否则你可能会把自己锁在门外

---

## 8. Docker 现在是什么状态，应该怎么处理

### 8.1 当前状态

我已经确认：

- Homebrew 里有 `docker` / `docker-desktop` 的安装记录
- `/Applications/Docker.app` 当前不存在
- `docker` 命令不可用

这表示：

- Docker 现在不是“能用状态”
- 大概率是历史安装残留，或者只留了 cask 记录

### 8.2 正确处理方式

明天直接重新安装 Docker Desktop，不要猜。

```bash
brew install --cask docker
open -a Docker
```

然后检查：

```bash
docker version
docker ps
docker context ls
```

### 8.3 为什么不用别的容器方案

因为你现在目标不是折腾容器生态，而是快速建立：

- 稳定远程入口
- 稳定的 Web 服务承载环境

`Docker Desktop` 在 macOS 上最省心，后面真要走极致轻量，再考虑别的方案。

### 8.4 后面如何对外暴露 Docker 服务

只暴露业务端口。

例如你的容器跑了一个 Web：

```bash
docker run -d --name myapp -p 8080:80 nginx
```

然后让花生壳映射：

```text
公网端口 -> 192.168.0.108:8080
```

不要做的事：

- 不要把 Docker daemon 公开到外网
- 不要暴露 `/var/run/docker.sock`
- 不要因为方便就把管理端口直接穿出去

---

## 9. 这台 Mac 上哪些软件该保留，哪些该停用，哪些可以卸载

这一节非常关键。你要的不是空泛建议，而是基于现在这台 Mac 的实际列表做整理。

### 9.1 应该保留的软件

这些是你明确还要保留，或者当前用途明确的软件：

- `UURemote.app`
- `PhDDNS.app`
- `Google Chrome.app`
- `Visual Studio Code.app`
- `Xcode.app`
- `iTerm.app`
- 系统 `Terminal`
- `Termius.app`
- `FileZilla.app`
- `WeChat.app`
- `QQ.app`
- `Foxmail.app`
- `Apifox.app`
- `Karabiner-Elements.app`
- `Alfred 5.app`

### 9.2 可以保留但不要常驻后台的软件

这些不是必须卸载，但不要让它们常驻和开机启动：

- `Clash Verge.app`
- `Proxyman.app`
- `Tunnelblick.app`
- `CleanMyMac X.app`

原因：

- 它们会改网络路径、代理、VPN、抓包、系统清理行为
- 会增加远程问题排查难度
- 不运行时它们不影响你做服务器

### 9.3 建议卸载的软件

你已经明确说了：

- `WezTerm` 不要了

所以它是本次最明确的卸载对象：

```text
/Applications/WezTerm.app
```

### 9.4 为什么我现在不建议乱卸载更多

因为你明确要求：

- 开发环境保留
- 聊天软件保留
- 数据保留
- 兼顾日常使用

在这个前提下，这台 Mac 的整理目标不是“删得越多越好”，而是：

- 删掉确定不用的工具
- 停掉不需要常驻的工具
- 迁移桌面大文件
- 清掉缓存和垃圾桶

---

## 10. 这台 Mac 具体该清理哪些目录

我已经实际检查过主要占用。

### 10.1 先看最值得动的目录

当前大的目录大致如下：

- `~/Desktop` 约 `48G`
- `~/Library/Containers` 约 `19G`
- `~/Library/Application Support` 约 `12G`
- `~/.Trash` 约 `1.8G`
- `~/Library/Caches` 约 `3.4G`

这说明你最值得处理的是：

1. 桌面项目目录
2. 垃圾桶
3. 缓存
4. 某些长期不用软件的残留目录

### 10.2 桌面上最值得整理的内容

我已经看到 `~/Desktop` 里这些大目录：

- `~/Desktop/ash` 约 `24G`
- `~/Desktop/APP UI` 约 `7.2G`
- `~/Desktop/oneapp-app_2` 约 `6.5G`
- `~/Desktop/GitHub` 约 `3.9G`
- `~/Desktop/t-systems` 约 `2.2G`
- `~/Desktop/web-docker` 约 `1.5G`

这些目录先不要上来直接删。

建议做法：

1. 先用 `du -sh` 再确认一遍
2. 归类成“工作长期保留 / 历史归档 / 可删除”
3. 能压缩归档的先归档到外置盘或 NAS
4. 再从桌面移走

桌面应该尽量恢复成“只有当前工作内容”，不要长期堆项目仓库和资源包。

### 10.3 当前垃圾桶可以直接清

已确认：

```text
~/.Trash 约 1.8G
```

如果垃圾桶里没有需要恢复的内容，可以直接清空：

```bash
rm -rf ~/.Trash/*
```

注意：

- 这是破坏性操作
- 执行前一定先看一眼垃圾桶内容

先查看：

```bash
ls -lah ~/.Trash
```

### 10.4 当前缓存可以清

已确认：

```text
~/Library/Caches 约 3.4G
```

可以做一轮缓存清理，但建议分步进行，不要一把梭。

先看大头：

```bash
du -sh ~/Library/Caches/* 2>/dev/null | sort -h | tail -n 30
```

如果只是做温和清理，可以删除明显的 App 缓存目录。  
如果你想一次性清大部分用户缓存：

```bash
rm -rf ~/Library/Caches/*
```

注意：

- 某些应用下次启动会自动重建缓存
- 第一次重新打开某些 App 可能会稍慢

### 10.5 聊天软件容器数据先不删

我已经确认：

- `~/Library/Containers/com.tencent.xinWeChat` 约 `10G`
- `~/Library/Containers/com.tencent.qq` 约 `5G`

但你已经明确要求：

- 微信保留
- QQ 保留
- 数据保留

所以这次**不要动这两个目录**。

只要在文档里知道它们很大就够了，后面如果你哪天愿意迁移历史数据，再单独处理。

### 10.6 当前可见的其他大目录

`~/Library/Application Support` 里的大目录包括：

- `Google` 约 `8.0G`
- `Steam` 约 `1.8G`
- `Code` 约 `347M`
- `io.github.clash-verge-rev.clash-verge-rev` 约 `186M`
- `com.netease.uuremote` 约 `92M`

这意味着：

- `Chrome` 数据是很大的
- `Steam` 如果以后不用，是一个可释放点
- 代理和远控工具占用本身不算大

---

## 11. 可以删掉哪些具体残留目录

这一节只列“你已经明确不要”或者“可以安全按需删”的内容。

### 11.1 WezTerm 残留

你明确不要 `WezTerm`，那可以删除：

- `/Applications/WezTerm.app`
- `~/Library/Saved Application State/com.github.wez.wezterm.savedState`

### 11.2 如果未来要彻底删 Clash Verge

当前我已看到这些相关目录：

- `~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev`
- `~/Library/Group Containers/io.github.clash-verge-rev.clash-verge-rev`
- `~/Library/WebKit/io.github.clash-verge-rev.clash-verge-rev`
- `~/Library/Caches/io.github.clash-verge-rev.clash-verge-rev`
- `/Library/LaunchDaemons/io.github.clash-verge-rev.clash-verge-rev.service.plist`

但你现在不是要卸载它，只是要停用它，所以现在先别删。

### 11.3 如果未来要彻底删 Proxyman

当前我已看到这些相关目录：

- `~/Library/Application Support/com.proxyman.NSProxy`
- `~/Library/WebKit/com.proxyman.NSProxy`
- `~/Library/Preferences/com.proxyman.NSProxy.plist`
- `/Library/LaunchDaemons/com.proxyman.NSProxy.HelperTool.plist`

同样地，你现在不是要卸载，只是要减少干扰，所以先保留。

### 11.4 如果未来要彻底删 Tunnelblick

相关目录包括：

- `~/Library/Application Support/Tunnelblick`
- `~/Library/Preferences/net.tunnelblick.tunnelblick.plist`
- `~/Library/LaunchAgents/net.tunnelblick.tunnelblick.LaunchAtLogin.plist`
- `/Library/LaunchDaemons/net.tunnelblick.tunnelblick.tunnelblickd.plist`

### 11.5 如果未来要彻底删 CleanMyMac

相关目录包括：

- `~/Library/Application Support/CleanMyMac X`
- `~/Library/Application Support/CleanMyMac X Menu`
- `~/Library/Application Support/CleanMyMac X HealthMonitor`
- `~/Library/Preferences/com.macpaw.CleanMyMac4.plist`
- `~/Library/Preferences/com.macpaw.CleanMyMac4.Menu.plist`
- `~/Library/Preferences/com.macpaw.CleanMyMac4.HealthMonitor.plist`
- `~/Library/Group Containers/com.macpaw.CleanMyMac4`
- `/Library/LaunchDaemons/com.macpaw.CleanMyMac4.Agent.plist`

但你当前要求是“保留软件本体，禁用后台”，所以先别删它本体。

---

## 12. 应该停掉哪些后台和自启

这台 Mac 当前已经检查到这些后台相关项：

### 12.1 当前 LaunchAgents / LaunchDaemons

- `/Library/LaunchAgents/com.netease.uuremote.agent.plist`
- `/Library/LaunchDaemons/com.netease.uuremote.daemon.plist`
- `/Library/LaunchDaemons/com.docker.socket.plist`
- `/Library/LaunchDaemons/io.github.clash-verge-rev.clash-verge-rev.service.plist`
- `/Library/LaunchDaemons/com.proxyman.NSProxy.HelperTool.plist`
- `/Library/LaunchDaemons/com.macpaw.CleanMyMac4.Agent.plist`
- `/Library/LaunchDaemons/net.tunnelblick.tunnelblick.tunnelblickd.plist`
- `~/Library/LaunchAgents/net.tunnelblick.tunnelblick.LaunchAtLogin.plist`
- `~/Library/LaunchAgents/com.google.GoogleUpdater.wake.plist`
- `~/Library/LaunchAgents/com.github.facebook.watchman.plist`
- `~/Library/LaunchAgents/com.valvesoftware.steamclean.plist`

### 12.2 当前登录项

我能看到的登录项里只有：

- `Alfred 5`

但这不代表别的工具没有后台，它们很多是通过 LaunchDaemon 方式驻留。

### 12.3 明天建议这样处理

保留运行：

- `UURemote`
- `PhDDNS`

默认停用或按需启用：

- `Clash Verge`
- `Proxyman`
- `Tunnelblick`
- `CleanMyMac X`

### 12.4 怎么停用

图形界面先看：

```text
System Settings > General > Login Items
```

CLI 或服务层面则看：

```bash
launchctl list
brew services list
```

如果某个工具你不想让它长期运行，最稳妥的方式通常是：

- 在 App 内关闭开机启动
- 在系统登录项里关掉
- 必要时卸载或移除对应的 LaunchAgent / LaunchDaemon

注意：

- 不要一上来就乱删 `/Library/LaunchDaemons`
- 先确认你是真的不再使用对应软件

---

## 13. 哪些 CLI 命令值得以后长期记住

### 13.1 用户和 SSH

查看当前用户：

```bash
whoami
id
```

查看用户详细信息：

```bash
dscl . -read /Users/ash
```

检查 SSH ACL：

```bash
dseditgroup -o read com.apple.access_ssh
dseditgroup -o checkmember -m ash com.apple.access_ssh
```

把用户加入 SSH：

```bash
sudo dseditgroup -o edit -a ash -t user com.apple.access_ssh
```

从 SSH 中移除：

```bash
sudo dseditgroup -o edit -d ash -t user com.apple.access_ssh
```

### 13.2 开关 SSH

打开：

```bash
sudo systemsetup -setremotelogin on
```

关闭：

```bash
sudo systemsetup -setremotelogin off
```

查看：

```bash
sudo systemsetup -getremotelogin
```

### 13.3 修改密码

改自己密码：

```bash
passwd
```

管理员重置：

```bash
sudo sysadminctl -resetPasswordFor ash -newPassword -
```

### 13.4 查看磁盘热点

查看一级大目录：

```bash
du -sh ~/* 2>/dev/null | sort -h
du -sh ~/Library/* 2>/dev/null | sort -h
```

查看桌面：

```bash
du -sh ~/Desktop/* 2>/dev/null | sort -h
```

查看容器目录：

```bash
du -sh ~/Library/Containers/* 2>/dev/null | sort -h | tail -n 30
```

查看缓存：

```bash
du -sh ~/Library/Caches/* 2>/dev/null | sort -h | tail -n 30
```

### 13.5 管理 Homebrew 服务

查看：

```bash
brew services list
```

启动：

```bash
brew services start nginx
```

停止：

```bash
brew services stop nginx
```

当前本机结果已经确认：

- `nginx` 未运行
- `privoxy` 未运行
- `unbound` 未运行

也就是说，当前没有 Homebrew 服务在偷跑。

---

## 14. 推荐的明天操作清单

如果你明天就准备开干，建议按下面一步一步做。

### 阶段 A：先打通远程

1. 打开 `Remote Login`
2. 本机测试 `ssh ash@127.0.0.1`
3. 局域网测试 `ssh ash@192.168.0.108`
4. 配花生壳映射 `TCP -> 192.168.0.108:22`
5. 外网测试 `ssh -p 外网端口 ash@花生壳域名`

### 阶段 B：补安全

1. 给外部管理电脑准备 SSH 公钥
2. 把公钥写进本机 `~/.ssh/authorized_keys`
3. 测试密钥登录
4. 成功后再考虑关闭密码登录

### 阶段 C：修 Docker

1. `brew install --cask docker`
2. `open -a Docker`
3. `docker version`
4. `docker ps`

### 阶段 D：整理本机

1. 检查并清空 `~/.Trash`
2. 清理 `~/Library/Caches`
3. 迁移桌面大目录
4. 卸载 `WezTerm`
5. 关闭 `Clash Verge`、`Proxyman`、`Tunnelblick`、`CleanMyMac` 的常驻和自启

---

## 15. 最后的结论

这台 Mac 现在最适合的定位不是“纯服务器”，而是：

**一台兼顾日常使用、可远程管理、可运行 Docker 服务的 macOS 主机。**

真正需要做的，不是盲目卸载一堆软件，而是：

- 用 `ash` 这个本地用户打通 SSH
- 用花生壳把公网流量映射到本机 SSH
- 保留 UU Remote 做备用远控
- 修复 Docker Desktop 的安装
- 处理桌面大文件、垃圾桶、缓存
- 让代理、抓包、VPN、系统清理工具不要常驻后台

你现在这台 Mac 的重点不是“系统太臃肿”，而是“角色不清晰”。  
把远程入口、容器、桌面工具、后台服务分工理顺之后，它就能稳定地承担远程开发和轻量服务的角色。

---

## 16. 官方参考

- Apple Remote Login 官方文档：<https://support.apple.com/guide/mac-help/allow-a-remote-computer-to-access-your-mac-mchlp1066/mac>
- 花生壳官网：<https://hsk.oray.com/>
