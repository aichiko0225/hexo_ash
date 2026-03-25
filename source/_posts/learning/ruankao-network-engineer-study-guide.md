---
title: 软考网络工程师备考全攻略：8 周计划、速记表与端口协议清单
date: 2026-03-25
categories: 技术
tags:
- Networking
- Certification
- Study
- Ruankao
- Exam
---

如果你和我一样，白天上班，真正能拿出来备考的时间只有工作日晚间 `2-3 小时`，同时又不是网络科班出身，而是有开发经验、懂一些网络但没有系统梳理过，那么软考 `Network Engineer` 的难点通常不是“完全看不懂”，而是：知识点很散、真题节奏不熟、下午案例题写不出关键词。

这篇文章把三份资料合成了一篇可以直接照着执行的长文：

- `8 周备考计划`
- `高频知识速记表`
- `端口 + 协议 + 易混点清单`

目标不是追求高分，而是尽量在本次考试通过；即使这次没过，也把下一次复习的框架一次搭好。我会保留 `English concepts` 的组织方式，因为对很多有工程背景的人来说，这种方式更容易形成检索路径。

<!-- more -->

> 如果你不是按 `3/25 -> 5/23` 这个时间窗备考，也没关系，直接把下面的 `Week 0 - Week 8` 整体平移即可。

---

## 一、先讲策略：这场考试怎么准备更像“冲刺”而不是“啃书”

### 1）目标分数

- `Morning paper`：稳住基础分，目标 `52-58`
- `Afternoon paper`：不崩盘，目标 `48-55`
- 最终目标：`两科都过线`

### 2）学习原则

- 不走“从头到尾啃厚书”的路线
- 采用 `concept -> real questions -> notes -> revisit` 的闭环
- 优先抓 `high-frequency topics`
- 从第 `2` 周开始，必须接触 `afternoon case`

### 3）时间预算

按照工作日晚间 `2-3h` 计算，`8` 周大约可投入：

- `2h/night`：约 `86h`
- `2.5h/night`：约 `107h`
- `3h/night`：约 `129h`

这个投入量，对于“有多年开发经验、但网络知识没有系统梳理”的人来说，足够完成一次质量不错的冲刺。

### 4）Morning 和 Afternoon 分别怎么打

#### Morning

- 覆盖面广
- 小知识点很多
- 很容易在端口、术语、协议差异上丢分
- 做题速度很重要

#### Afternoon

- 题量少，但更偏场景题
- 高频题型喜欢考：`address planning`、`VLAN`、`routing`、`ACL/NAT`、`fault analysis`、`design`
- `partial credit` 很重要
- 关键词比长篇大论更重要

下午题一个很实用的答题原则是：

1. 要解决什么问题
2. 采用什么技术或协议
3. 为什么这个方案适合当前场景
4. 最终能达到什么效果

### 5）如果时间很紧，优先锁定这些内容

- `IPv4`, `subnetting`, `CIDR`, `VLSM`, `route summarization`
- `VLAN`, `Trunk`, `STP`
- `static routing`, `RIP`, `OSPF`, `BGP basics`
- `ACL`, `NAT`, `PAT`, `firewall`, `VPN basics`
- `DNS`, `DHCP`, `HTTP/HTTPS`, `SMTP`, `POP3`, `IMAP`, `FTP`
- `network design`, `redundancy`, `troubleshooting`, `cabling/media`

如果时间特别紧，不要过度投入这些内容：

- 很深的 `BGP policy`
- 很细的 `IPv6 details`
- `SDN / 5G / cloud overview` 这类只需要认知级理解的内容

---

## 二、资料怎么选：尽量少而有效

### 1）官方信息

- 官方网站：`https://www.ruankao.org.cn/`
- 考试计划：`https://www.ruankao.org.cn/exam/plan.html`
- 官方教材入口：`https://www.ruankao.org.cn/book/main.html`
- 报名入口：`https://bm.ruankao.org.cn/sign/welcome`
- 机考模拟/下载入口：`https://bm.ruankao.org.cn/sign/in?type=query&s=vexam/download/main`

### 2）教材

- 推荐主教材：`网络工程师教程（第6版）`
- 清华大学出版社页面：`https://www.tup.com.cn/booksCenter/book_10453401.html`

使用方式不要搞反：

- 把它当 `reference book`
- 不要从第一页一路硬读到最后一页
- 哪些真题章节反复出错，再回书里补对应章节

### 3）免费视频

晚间时间有限，更适合按专题看，所以优先用 `Bilibili`。

- 考试介绍 / 报考指南：`https://www.bilibili.com/video/BV1ZAivYsEt3/`
- 搜索关键词 1：`希赛软考 网络工程师 第6版`
- 搜索关键词 2：`网络工程师 下午真题 解析`
- 搜索关键词 3：`软考 网络工程师 机考`
- 搜索关键词 4：`子网划分 VLAN STP OSPF ACL NAT 网络工程师`

建议只看三类视频：

- `high-frequency concept videos`
- `afternoon case analysis`
- `机考/答题节奏` 视频

### 4）高频知识点与真题

- 高频知识点参考：`https://www.educity.cn/rk/5374342.html`
- 真题优先做近 `5 年`
- 如果纸质真题不全，优先补 `2023-2025` 的线上真题和解析

---

## 三、每晚怎么学：把时间切成可执行模板

### Option A：只有 `2 hours`

1. `15 min`：回顾昨天错题 / notes
2. `45 min`：学习当天主题的核心概念
3. `40 min`：做 `15-20` 道 morning 选择题
4. `20 min`：订正 + 记 `3-5` 条 notes

### Option B：有 `2.5-3 hours`

在上面的基础上再增加：

- `30-60 min`：做 `1` 道 `afternoon case`，或者看 `1` 道详细解析

### Weekly Output Target

每周至少完成：

- `80-100` 道 morning questions
- `1-2` 道 afternoon case
- `1` 页自己的 topic notes

### 我额外建议你固定做的 4 张纸

这些不是“可选项”，而是复习越到后面越关键：

- `protocol comparison`
- `common ports`
- `subnetting cheat sheet`
- `afternoon keywords`

---

## 四、考点优先级：先打通主线，再补边缘

### A-Level：必须拿下

- `IPv4 addressing`
- `subnetting / VLSM / CIDR`
- `route summarization`
- `VLAN / Trunk`
- `STP`
- `static routing / default route`
- `RIP / OSPF / BGP basics`
- `ACL`
- `NAT / PAT`
- `firewall / VPN basics`
- `DNS / DHCP / HTTP / SMTP`
- `network design / redundancy / troubleshooting`

### B-Level：必须会做题

- `SNMP / Syslog`
- `proxy`
- `FTP / POP3 / IMAP`
- `RAID`
- `server basics`
- `wireless LAN`
- `IPv6 basics`
- `cabling / media selection`

### C-Level：知道就行

- `SDN`
- `cloud networking overview`
- `5G / new-outline overview topics`
- 其他明显偏概念、偏新大纲的边缘内容

---

## 五、8 周冲刺计划：按周推进，不要每天重新想“今天学什么”

## Week 0：`3/25 Wed - 3/27 Fri`

### Goal

- 建立考试框架
- 知道 morning / afternoon 分别怎么考
- 完成一次 baseline test

### Plan

- `3/25 Wed`
  - 了解考试结构、题型、时间分配
  - 建立笔记文档：`wrong questions`、`topic notes`、`formula sheet`
  - 做一套 `morning` 的前 `20-30` 题，感受题型
- `3/26 Thu`
  - 学 `OSI / TCP-IP / encapsulation / decapsulation`
  - 学 `Ethernet / MAC / ARP`
  - 做 `15-20` 道对应选择题
- `3/27 Fri`
  - 学 `IPv4 addressing`、`subnet mask`、`CIDR`
  - 做 `15-20` 道地址基础题
  - 记录第一次暴露出的薄弱点

### Optional Weekend Catch-up

- 用 `60-90 min` 回顾本周错题
- 看 `1` 道 `afternoon case` 解析，先理解答题风格，不求会做

---

## Week 1：`3/30 Mon - 4/3 Fri`

### Goal

- 拿下 `subnetting` 这个高频送分点
- 对 `VLAN / Trunk` 建立基本理解

### Plan

- `3/30 Mon`
  - `subnetting`：网络地址、广播地址、可用主机数
  - 做 `15` 道子网题
- `3/31 Tue`
  - `VLSM` 和 `CIDR`
  - 做 `15-20` 道地址规划题
- `4/1 Wed`
  - `route summarization`
  - 建一张地址计算速记表
  - 做 `15` 道题
- `4/2 Thu`
  - `VLAN`、`access port`、`Trunk`
  - 做 `15-20` 道交换基础题
- `4/3 Fri`
  - 做一个小复盘
  - `1` 道 `afternoon case`：address planning 或 VLAN 基础题

### End-of-Week Check

- 能快速计算网段 / 广播地址 / 主机范围
- 知道 `VLAN` 和 `Trunk` 的作用
- 能看懂基本地址规划题

---

## Week 2：`4/6 Mon - 4/10 Fri`

### Goal

- 建立 `switching + routing basics`
- 开始接触 `STP` 和动态路由

### Plan

- `4/6 Mon`
  - `STP`：why it exists、loop avoidance、root bridge
  - 做 `15` 道题
- `4/7 Tue`
  - `link aggregation`、switch basics
  - 做 `15` 道题
- `4/8 Wed`
  - `static route`、`default route`
  - 做 `15-20` 道题
- `4/9 Thu`
  - `RIP`：hop count、convergence、suitable scenarios
  - 做 `15` 道题
- `4/10 Fri`
  - `OSPF basics`：link-state、metric、area
  - 做 `1` 道 afternoon case：switch / routing basics

### End-of-Week Check

- 能说明 `STP` 解决什么问题
- 能区分 `static route`、`RIP`、`OSPF`
- 能做基础的交换 / 路由题

---

## Week 3：`4/13 Mon - 4/17 Fri`

### Goal

- 进入网络工程师核心区：`OSPF / BGP / ACL / NAT`
- afternoon 开始真正练习表达

### Plan

- `4/13 Mon`
  - `OSPF`：neighbor、metric、convergence、area basics
  - 做 `15-20` 道题
- `4/14 Tue`
  - `BGP basics`：path selection basic ideas、inter-domain scenarios
  - 做 `10-15` 道题
- `4/15 Wed`
  - `ACL`：standard vs extended、matching logic
  - 做 `15-20` 道题
- `4/16 Thu`
  - `NAT / PAT`、`firewall basics`
  - 做 `15-20` 道题
- `4/17 Fri`
  - `VPN basics`
  - 做 `1-2` 道 afternoon case：ACL / NAT / routing

### End-of-Week Check

- 能说清 `OSPF` 和 `BGP` 的最核心差别
- 知道 `ACL` 一般按什么匹配
- 知道 `NAT / PAT` 的常见题型

---

## Week 4：`4/20 Mon - 4/24 Fri`

### Goal

- 补齐服务类高频考点
- 建立“服务 + 端口 + 故障”的联动记忆

### Plan

- `4/20 Mon`
  - `DNS`：recursion、authoritative、cache、typical issues
  - 做 `15-20` 道题
- `4/21 Tue`
  - `DHCP`：lease、relay、address assignment flow
  - 做 `15-20` 道题
- `4/22 Wed`
  - `HTTP / HTTPS`、`proxy`、basic web service concepts
  - 做 `15` 道题
- `4/23 Thu`
  - `SMTP / POP3 / IMAP / FTP`
  - 整理一张 `common ports` 速记表
  - 做 `15-20` 道题
- `4/24 Fri`
  - `SNMP`、`Syslog`、`server basics`、`RAID`
  - 做 `1` 道 afternoon case：service / operation / fault diagnosis

### End-of-Week Check

- 常见服务端口能认出来
- 知道 `DNS / DHCP / Mail` 常见故障模式
- afternoon 答题开始能写出关键词

---

## Week 5：`4/27 Mon - 5/1 Fri`

### Goal

- 切入 `design / topology / availability / troubleshooting`
- 让 afternoon 更像“写方案”而不是“猜答案”

### Plan

- `4/27 Mon`
  - `network topology`、core / distribution / access
  - 做 `15` 道题
- `4/28 Tue`
  - `redundancy`、`high availability`、backup links
  - 做 `15` 道题
- `4/29 Wed`
  - `troubleshooting`：fault isolation、layered diagnosis mindset
  - 做 `15-20` 道题
- `4/30 Thu`
  - `cabling / media selection`、`wireless LAN basics`
  - 做 `15` 道题
- `5/1 Fri`
  - `IPv6 basics` + 新大纲轻量内容扫一遍
  - 做 `1-2` 道 afternoon case：design / troubleshooting

### End-of-Week Check

- 知道典型企业网络分层结构
- 能解释冗余设计的目的
- 遇到故障题不会完全没思路

---

## Week 6：`5/4 Mon - 5/8 Fri`

### Goal

- 从“学知识”切换到“拿分”
- 真题优先级高于新视频

### Plan

- `5/4 Mon`
  - 做 `1` 套完整 `morning` 真题
  - 统计错题分布
- `5/5 Tue`
  - 复盘错题最多的两个专题
  - 补对应概念或视频
- `5/6 Wed`
  - 做 `1` 道 `afternoon case`
  - 按标准答案整理关键词
- `5/7 Thu`
  - 再做 `20-25` 道 morning 高频专题题
  - 重点盯 `subnetting / routing / services`
- `5/8 Fri`
  - 做 `1` 道 afternoon case
  - 输出一页 `high-frequency notes`

### End-of-Week Check

- 知道自己最弱的 `3` 个专题
- 开始形成自己的速记表

---

## Week 7：`5/11 Mon - 5/15 Fri`

### Goal

- 稳定做题节奏
- 压缩知识点到考场可调用状态

### Plan

- `5/11 Mon`
  - 做第 `2` 套完整 `morning` 真题
- `5/12 Tue`
  - 做 `1` 道 afternoon case，限时作答
- `5/13 Wed`
  - 回顾 `ACL / NAT / OSPF / DNS / DHCP`
  - 做 `20` 道专题题
- `5/14 Thu`
  - 做 `1` 套 `mini mock`：morning `30-40` 题 + `1` 道 afternoon
- `5/15 Fri`
  - 复盘整周错题
  - 完成最终版 `common ports + protocol comparison` 速记表

### End-of-Week Check

- morning 做题速度明显提升
- afternoon 不再只会看答案
- 高频知识点开始成体系

---

## Week 8：`5/18 Mon - 5/22 Fri`

### Goal

- 只收口，不扩张
- 把已学内容压成可复述、可作答、可拿分的状态

### Plan

- `5/18 Mon`
  - 做最后 `1` 套完整 `morning` 真题
  - 只记高频错点
- `5/19 Tue`
  - 做 `1` 道 afternoon case
  - 复盘答案模板
- `5/20 Wed`
  - 重点回顾：`subnetting / VLAN / STP / OSPF / ACL / NAT`
- `5/21 Thu`
  - 重点回顾：`DNS / DHCP / HTTP / Mail / troubleshooting / design`
- `5/22 Fri`
  - 只看自己的 `wrong questions + notes + formulas + ports`
  - 不再开新专题
  - 提前调整作息

### Exam-Eve Rules

- 不熬夜
- 不刷偏题、怪题
- 不再看大段新视频
- 相信你已经完成的复习闭环

---

## 六、把知识串起来：一张紧凑的知识地图

### Layer 2 / Layer 3

- `Ethernet`
- `MAC / ARP`
- `VLAN / Trunk`
- `STP`
- `routing / forwarding`

### Addressing

- `IPv4`
- `subnetting`
- `VLSM`
- `CIDR`
- `route summarization`
- `IPv6 basics`

### Routing

- `static route`
- `default route`
- `RIP`
- `OSPF`
- `BGP basics`

### Security

- `ACL`
- `NAT / PAT`
- `firewall`
- `VPN`
- 常见攻击与基础防护思路

### Services

- `DNS`
- `DHCP`
- `HTTP / HTTPS`
- `SMTP / POP3 / IMAP`
- `FTP`
- `proxy`
- `SNMP / Syslog`

### Design / Ops

- `topology`
- `core / distribution / access`
- `redundancy / HA`
- `load balancing`
- `troubleshooting`
- `RAID`
- `cabling / media`

### 这些东西要明确背，不要只靠“理解过”

- 常见服务端口
- `RIP / OSPF / BGP` 对比
- `ACL` 分类和匹配逻辑
- `NAT / PAT` 区别
- `VLAN / Trunk / STP` 关键词
- 子网划分计算套路
- `RAID` 级别特点
- 常见设备 / 介质适用场景

---

## 七、高频知识速记表：把最常考的地方先压缩到脑子里

## 1. IPv4 和 Subnetting

### Core Formulas

- 子网总地址数：`2^(32-prefix)`
- 常规可用主机数：`2^(32-prefix) - 2`
- 子网步长：找 `interesting octet`，计算 `256 - mask`

### Fast Memory Table

| Prefix | Mask | Total IPs | Usable Hosts |
|---|---|---:|---:|
| `/24` | `255.255.255.0` | 256 | 254 |
| `/25` | `255.255.255.128` | 128 | 126 |
| `/26` | `255.255.255.192` | 64 | 62 |
| `/27` | `255.255.255.224` | 32 | 30 |
| `/28` | `255.255.255.240` | 16 | 14 |
| `/29` | `255.255.255.248` | 8 | 6 |
| `/30` | `255.255.255.252` | 4 | 2 |

### Workflow for Subnetting Questions

1. 先看每个子网需要多少主机
2. 选能满足需求的最小前缀
3. `VLSM` 题先分配大网段，再分配小网段
4. 写清楚 `network address`、`usable range`、`broadcast address`
5. 最后检查是否发生 overlap

### High-Frequency Traps

- 把 `network address` 和 `first usable host` 搞混
- 忘了 `broadcast address`
- `VLSM` 没有先分配最大的子网
- `route summarization` 既要覆盖所有路由，又要尽量避免多余覆盖

## 2. VLAN、Trunk、STP

### VLAN

- 逻辑上分割广播域
- 提升隔离性、可管理性和安全性
- 不同 VLAN 的主机通信需要 `Layer 3` 转发

### Trunk

- 用来承载多个 VLAN 的流量
- 一般依赖 tagging
- 常见场景是交换机与交换机之间的链路

### STP

- 作用：防止二层环路
- 核心思路：阻塞冗余路径，但保留备份链路
- 必记术语：`root bridge`、`root port`、`designated port`、`blocking`

### Common Traps

- `VLAN` 解决的是分段，不会自动解决跨 VLAN 通信
- `Trunk` 不等于 `access port`
- 冗余链路如果没有 `STP`，可能造成广播风暴和 MAC 表震荡

## 3. Routing Cheat Sheet

### Static Route

- 简单
- 可预测
- 开销低
- 在大网络里可扩展性差

### RIP

- `distance-vector`
- 度量：`hop count`
- 收敛慢
- 只适合小型、简单网络

### OSPF

- `link-state`
- 比 `RIP` 收敛更快
- 支持 `areas` 的分层设计
- 适合中大型内部网络

### BGP

- `inter-domain routing`
- 偏 `policy-oriented`
- 常见于 `ISP / multi-AS scenarios`
- 不是普通企业内部路由的默认答案

### Fast Comparison Table

| Protocol | Type | Metric / Key Idea | Typical Use |
|---|---|---|---|
| `Static` | manual | admin control | small/stable networks |
| `RIP` | distance-vector | hop count | small LAN/WAN |
| `OSPF` | link-state | cost | enterprise internal routing |
| `BGP` | path-vector | policy/path attributes | inter-AS / ISP |

### High-Frequency Traps

- `RIP` 简单，但不适合大规模网络
- `OSPF` 通常用于内部，`BGP` 通常用于域间
- 不要脱离场景写出“`BGP` 比 `OSPF` 更好”这种答案

## 4. ACL、NAT、Firewall、VPN

### ACL

- 做流量过滤和访问控制
- 标准 ACL：主要按源地址匹配
- 扩展 ACL：可按源、目的、协议、端口匹配

### NAT / PAT

- `NAT`：私网地址和公网地址之间转换
- `PAT`：多个内网主机共用一个公网 IP，通过不同端口复用

### Firewall

- 执行安全策略
- 按规则允许或拒绝流量
- 常部署在网络边界或不同安全域之间

### VPN

- 在公共网络之上建立安全隧道
- 可用于 site-to-site 或 remote access

### High-Frequency Traps

- `ACL` 过滤流量，不等于 `NAT`
- 多个私网主机共享少量公网 IP 时，`PAT` 往往才是题目的实际答案
- 远程管理里 `telnet` 不安全，`SSH` 更安全

## 5. Services and Servers

### DNS

- 域名解析
- 必记：`UDP/TCP 53`
- 高频考法：cache、recursion、authoritative answer、DNS 故障症状

### DHCP

- 自动分配 IP
- 必记：`UDP 67/68`
- 关键概念：lease、pool、gateway、DNS server options、relay

### HTTP / HTTPS

- Web 服务
- 必记：`80 / 443`
- `HTTPS` 在 `HTTP` 基础上增加了 TLS 加密和身份校验

### Mail

- `SMTP`：发信
- `POP3`：收信，偏简单下载模型
- `IMAP`：收信，偏服务器端邮箱同步

### SNMP / Syslog

- `SNMP`：监控和管理
- `Syslog`：集中日志传输

### RAID Basics

| RAID | Key Feature |
|---|---|
| `RAID 0` | striping，性能好，但无冗余 |
| `RAID 1` | mirroring，有冗余 |
| `RAID 5` | striping + parity，容量和容错平衡 |
| `RAID 10` | 性能和冗余兼顾，但成本更高 |

## 6. Design and Troubleshooting

### Design Keywords

- `availability`
- `redundancy`
- `scalability`
- `security`
- `manageability`
- `performance`

### Typical Topology Terms

- `core layer`
- `distribution layer`
- `access layer`

### Troubleshooting Method

1. 先定义清楚症状
2. 判断影响范围：单主机、单 VLAN、单子网、单服务还是全网
3. 必要时先看物理连通性
4. 按顺序排查：addressing、gateway、VLAN、ACL、routing、DNS
5. 验证修复前后状态

### Common Fault Paths

- 域名访问不了，但 IP 能访问：大概率是 `DNS`
- 本地子网正常，跨子网失败：优先查 gateway / routing / ACL
- 间歇性环路或广播风暴：优先怀疑二层冗余没有正确跑 `STP`
- 内网用户无法出网：优先查 `NAT`、default route、firewall policy

## 7. Cabling and Media

不用深挖到物理层细枝末节，但方向要清楚：

- 双绞线：常见于接入层 LAN
- 光纤：距离更长、抗干扰更强，常用于骨干或上联
- 介质选型看：`distance`、`bandwidth`、`cost`、`environment`、`anti-interference`

---

## 八、端口与协议清单：这一块最适合考前反复默写

## 1. Must-Memorize Ports

| Service | Port / Protocol | Notes |
|---|---|---|
| `FTP data` | `20/TCP` | active mode data channel |
| `FTP control` | `21/TCP` | control channel |
| `SSH` | `22/TCP` | secure remote login |
| `Telnet` | `23/TCP` | insecure remote login |
| `SMTP` | `25/TCP` | mail sending |
| `DNS` | `53/UDP,TCP` | UDP 用于常规查询，TCP 常见于 zone transfer 或大响应 |
| `DHCP server` | `67/UDP` | server side |
| `DHCP client` | `68/UDP` | client side |
| `TFTP` | `69/UDP` | simple file transfer |
| `HTTP` | `80/TCP` | web |
| `POP3` | `110/TCP` | receive mail |
| `NTP` | `123/UDP` | time sync |
| `IMAP` | `143/TCP` | receive mail, synchronized mailbox |
| `SNMP` | `161/UDP` | management/query |
| `SNMP Trap` | `162/UDP` | unsolicited event/alert |
| `BGP` | `179/TCP` | routing between ASes |
| `LDAP` | `389/TCP,UDP` | directory service |
| `HTTPS` | `443/TCP` | encrypted web |
| `SMTPS` | `465/TCP` | secure SMTP，部分题目或资料中会出现 |
| `Syslog` | `514/UDP` | centralized logs |
| `RIP` | `520/UDP` | routing update protocol |
| `RIPng` | `521/UDP` | RIP for IPv6 |
| `DHCPv6 client` | `546/UDP` | IPv6 DHCP client |
| `DHCPv6 server` | `547/UDP` | IPv6 DHCP server |

## 2. Very Common Exam Traps

### DNS

- 不要只背 `53/UDP`
- `DNS` 也会用 `TCP 53`
- 典型考法包括 `zone transfer` 和大响应场景

### FTP

- `21` 是控制连接
- `20` 是主动模式下的数据连接
- 如果题目问得比较宽，不要只写一个端口而不加上下文

### Mail

- `SMTP` 负责发送
- `POP3` 和 `IMAP` 负责接收
- `IMAP` 更适合多设备同步邮箱

### Remote Management

- `Telnet` 是明文，不安全
- `SSH` 才是更安全的管理方案

## 3. Protocols Without a Classic Port Number

有些协议不是靠 TCP/UDP 端口来识别，而是靠 `IP protocol number`。

| Protocol | Identifier | Notes |
|---|---|---|
| `ICMP` | `IP protocol 1` | error reporting, diagnostics |
| `TCP` | `IP protocol 6` | connection-oriented transport |
| `UDP` | `IP protocol 17` | connectionless transport |
| `GRE` | `IP protocol 47` | tunneling |
| `ESP` | `IP protocol 50` | IPsec encryption |
| `AH` | `IP protocol 51` | IPsec authentication |
| `OSPF` | `IP protocol 89` | link-state routing |

这一点很重要，因为题目很喜欢把“端口号”和“IP 协议号”混着考。

## 4. Transport and Core Internet Protocols

| Protocol | Layer / Type | Key Feature | Common Exam Angle |
|---|---|---|---|
| `ARP` | Layer 2/3 boundary | map IP to MAC | local network resolution |
| `ICMP` | network | control and diagnostics | `ping`、error report |
| `TCP` | transport | reliable, ordered, connection-oriented | web、mail、SSH |
| `UDP` | transport | fast, no connection, lower overhead | DNS、DHCP、SNMP、RIP |

### TCP vs UDP

| Item | `TCP` | `UDP` |
|---|---|---|
| connection | yes | no |
| reliability | yes | no built-in reliability |
| ordering | yes | no |
| overhead | higher | lower |
| typical services | HTTP, HTTPS, SSH, SMTP, POP3, IMAP, BGP | DNS, DHCP, SNMP, RIP, TFTP, NTP |

高频判断题思路：

- 当可靠性、顺序性重要时，优先想到 `TCP`
- 当低开销、速度更重要，且应用层能容忍或处理丢包时，优先想到 `UDP`

## 5. Layer 2 and Switching Protocols

| Protocol / Tech | Main Role | What To Say In Answers |
|---|---|---|
| `Ethernet` | LAN framing and access | basic LAN data transmission |
| `VLAN` | logical segmentation | reduce broadcast domain, improve isolation |
| `Trunk` | carry multiple VLANs | inter-switch multi-VLAN transport |
| `STP` | loop prevention | avoid Layer 2 loop, keep redundancy |
| `LACP` / link aggregation | bundle links | increase bandwidth and/or redundancy |

Common trap：

- `VLAN` 本身不提供跨 VLAN 通信，跨 VLAN 仍然需要 `Layer 3 forwarding`

## 6. Routing Protocol Comparison

| Protocol | Category | Transport / Identifier | Key Metric / Idea | Typical Scenario |
|---|---|---|---|---|
| `RIP` | distance-vector | `UDP 520` | hop count | small/simple network |
| `OSPF` | link-state | `IP protocol 89` | cost, SPF | enterprise internal routing |
| `BGP` | path-vector | `TCP 179` | policy/path attributes | inter-AS / ISP |

### Quick Notes

- `RIP`：简单，但收敛慢、规模受限
- `OSPF`：收敛更快，支持 area 分层
- `BGP`：强调 route policy 和域间控制，不是企业内部路由的默认答案

## 7. Security Protocols and Concepts

| Item | Identifier / Port | Key Point |
|---|---|---|
| `SSH` | `22/TCP` | secure remote management |
| `Telnet` | `23/TCP` | insecure plaintext management |
| `HTTPS` | `443/TCP` | encrypted web access |
| `AH` | `IP protocol 51` | IPsec authentication/integrity |
| `ESP` | `IP protocol 50` | IPsec encryption + protection |
| `VPN` | varies | secure tunnel over public network |
| `ACL` | no fixed port | traffic filtering policy |
| `NAT/PAT` | no fixed port | address translation |
| `Firewall` | no fixed port | policy enforcement and traffic control |

High-frequency trap：

- `ACL` 和 `firewall` 都能控流，但两者不是同一个概念
- `NAT` 不是安全策略本身，它更多是地址转换，最多只是“隐藏内部地址”

## 8. Network Services

| Service | Protocol / Port | What Questions Often Test |
|---|---|---|
| `DNS` | `53/UDP,TCP` | name resolution, cache, zone transfer, DNS faults |
| `DHCP` | `67/68 UDP` | automatic addressing, lease, relay |
| `HTTP` | `80/TCP` | web access |
| `HTTPS` | `443/TCP` | encrypted web access |
| `SMTP` | `25/TCP` | send mail |
| `POP3` | `110/TCP` | receive mail |
| `IMAP` | `143/TCP` | synchronized mailbox access |
| `SNMP` | `161/162 UDP` | monitoring and management |
| `Syslog` | `514/UDP` | centralized logging |
| `NTP` | `123/UDP` | time synchronization |
| `TFTP` | `69/UDP` | simple file transfer, device configs/images in some contexts |

## 9. Easy Confusion Pairs

### `HTTP` vs `HTTPS`

- `HTTP`：明文 Web 传输
- `HTTPS`：基于 TLS 的加密 Web 传输

### `POP3` vs `IMAP`

- `POP3`：更偏简单下载模型
- `IMAP`：更适合多设备同步邮箱

### `RIP` vs `OSPF`

- `RIP`：hop count，简单，小型网络
- `OSPF`：link-state，收敛更快，适合更大的内部网络

### `OSPF` vs `BGP`

- `OSPF`：组织内部 / 网络域内部路由
- `BGP`：自治系统之间路由

### `ACL` vs `NAT`

- `ACL`：filter / control
- `NAT`：translate addresses

### `Telnet` vs `SSH`

- `Telnet`：明文，不安全
- `SSH`：加密，优先选择

## 10. What To Recite Before Exam Day

如果考前只剩 `10` 分钟，把这些快速背一遍：

- `20/21 FTP`、`22 SSH`、`23 Telnet`、`25 SMTP`
- `53 DNS`、`67/68 DHCP`、`69 TFTP`、`80 HTTP`
- `110 POP3`、`123 NTP`、`143 IMAP`
- `161/162 SNMP`、`179 BGP`、`443 HTTPS`、`514 Syslog`、`520 RIP`
- `OSPF = IP protocol 89`
- `AH = 51`、`ESP = 50`、`GRE = 47`

---

## 九、下午题怎么写：不要写成“我觉得大概是这样”

下午题尽量固定成这个结构：

1. `What is the problem / goal?`
2. `Which protocol / technology should be used?`
3. `Why is it suitable here?`
4. `What result / effect does it achieve?`

### Example Skeleton

```text
该问题需要解决的是 ______。
可采用 ______ 技术/协议。
原因是：它能够 ______，并且适用于 ______ 场景。
实施后可实现 ______，从而提高 ______。
```

这个模板可以反复套进这些高频题：

- `VLAN / Trunk`
- `OSPF`
- `ACL`
- `NAT`
- `DNS / DHCP`
- `redundancy / backup design`

### Afternoon Keywords You Should Reuse

答题时能复用就复用这些词：

- `reduce broadcast domain`
- `improve security isolation`
- `provide redundancy`
- `improve availability`
- `speed up convergence`
- `support scalable network design`
- `centralized management`
- `automatic address assignment`
- `secure remote access`
- `control traffic by policy`

我的补充建议是：不要追求句子华丽，先保证关键词到位。很多下午题你写不出完整论文没关系，但一定要让阅卷人看到“你知道问题、知道技术、知道原因、知道结果”。

---

## 十、最后两三周怎么复习：把知识压到“可调用”状态

这部分最适合搭配上面的速记表使用。

### Last-Week Review Checklist

考前一周，确认自己能快速回答这些问题：

- 你能不能不慌地做 `subnetting`？
- 你能不能用自己的话解释 `VLAN`、`Trunk`、`STP`？
- 你能不能比较 `RIP`、`OSPF`、`BGP`？
- 你能不能说清 `ACL`、`NAT`、`PAT`、`firewall`、`VPN` 的区别？
- 你能不能快速回忆常见端口和服务职责？
- 你能不能按 `problem -> solution -> reason -> result` 写出一段简短下午题答案？

如果这些你都能做到，说明核心过线能力已经基本具备。

### If You Fall Behind

如果某一周被工作打乱，不要慌，按照这个优先级保底。

#### Never Drop

- `subnetting`
- `VLAN / STP`
- `static / RIP / OSPF / BGP basics`
- `ACL / NAT`
- `DNS / DHCP`
- `afternoon case practice`

#### Can Be Simplified

- `wireless`
- `IPv6 details`
- `SDN / 5G / cloud overview`
- 比较偏的管理类或边缘新概念

#### Recovery Strategy

- 工作日只保留 `1h` 也没关系，但不要断线
- 真断线时，至少完成：`10` 道题 + `10` 分钟复盘
- 追赶进度时优先补 `real questions`，不要先补长视频

### Exam-Eve Rules

- 不熬夜
- 不刷偏题、怪题
- 不再看大段新视频
- 只看自己的 `wrong questions + notes + formulas + ports`
- 相信你已经完成的复习闭环

---

## 十一、临门一脚：6 个自测问题

如果你不看笔记就能快速答出下面这些，这份清单就算发挥作用了：

1. `BGP` 用什么端口？
2. 为什么 `DNS` 既可能用 `UDP`，也可能用 `TCP`？
3. 设备远程管理更安全的是 `Telnet` 还是 `SSH`？
4. `POP3` 和 `IMAP` 的核心区别是什么？
5. `OSPF` 是靠 TCP/UDP 端口识别，还是靠 IP 协议号识别？
6. `ACL` 和 `NAT` 的核心区别是什么？

---

## 十二、最后的建议

- 如果你本身就有多年开发经验，理解力通常不是问题，真正的问题往往是考试表达和体系化记忆
- 不要用“我懂一点网络”替代“我会做真题”
- 只要把 `subnetting + switching + routing + ACL/NAT + DNS/DHCP + afternoon case` 这条主线打通，过线概率就不低
- 即使这次没过，下次也不是从零开始，因为你的复习框架已经搭好了

我再补一句最现实的话：这门考试对在职备考的人来说，最怕的不是难，而是断。哪怕某几天只能学 `1` 小时，也尽量别让链条断掉。稳定、小步、真题驱动，通常比“周末爆肝一次然后一周不碰”有效得多。

如果你真准备开始动手，今天晚上就做三件事：

1. 建好 `wrong questions`、`topic notes`、`formula sheet` 三份笔记。
2. 先做 `20-30` 道 morning 题，摸清自己弱点。
3. 开始做第一张 `common ports` 速记表。
