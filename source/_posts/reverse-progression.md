---
title: 逆向工程进阶
date: 2020-02-17 15:16:48
categories: 逆向
tags:
- 逆向
- iOS
---

## 前言

如果您是iOS开发，具备相应的开发储备，除了需要了解逆向的基础，同样需要
知道程序的运行原理。

下面会介绍逆向工程相关的进阶知识，理论知识比较枯燥，但是确实必须要掌握的。

## 程序加载

在编写一个应用程序时，我们看到的入口函数是`main.m`里面的`main`函数，因此我们一般会以为程序是从这里开始执行的。其实不然，程序在执行`main`函数之前已经执行了`+load`和`constructor`构造函数。接下来，让我们一起看看在`main`函数执行之前都发生了什么。

### dyld简介

程序在运行时会依赖很多系统动态库。系统动态库会通过动态库加载器（默认是`/usr/lib/dyld`）加载到内存中，系统内核在做好启动程序的准备工作之后就会将工作交给`dyld`。由于很多程序都需要使用系统动态库，不可能每个程序加载时都去加载所有的系统动态库，为了优化程序启动速度和利用动态库缓存，`iOS`系统采用了共享缓存技术。`dyld`缓存在`iOS`系统中，位于`/System/Library/Caches/com.apple.dyld/`目录下，按照不同架构保存不同的文件。

### dyld加载流程

要想知道`+load`和`constructor`是在什么时候调用的，就需要分析`dyld`加载`Mach-O`文件的流程。`dyld`的代码可以从苹果开源网站下载。从`dyldStartup.s`文件开始执行，其中用汇编实现的`__dyld_start`方法里面调用了`dyldbootstrap::start()`方法，然后调用了`dyld`的`main`函数。

`dyld`的加载流程主要包括9个步骤

1. 设置上下文信息，配置进程是否受限
2. 配置环境变量，获取当前运行架构
3. 加载可执行文件，生成一个`ImageLoader`实例对象
4. 检查共享缓存是否映射到了共享区域
5. 加载所有插入的库
6. 链接主程序
7. 链接所有插入的库，执行符号替换
8. 执行初始化方法
9. 寻找主程序入口

`initializeMainExecutable`执行初始化方法，`+load`和`constructor`方法就是在这里执行的。

## Mach-O文件格式

`Mach-O` 文件比较重要，了解`Mach-O`文件结构后可以更好地进行逆向工程。

### Mach-O文件的基础格式

`Mach-O`的文件结构包括：Mach-O头部、Load Command、Section、Other Data。

![Math-O文件的基础结构](/images/Math-O_1.png)

### Mach-O头部

Header部分由以下部分组成

* magic: Mach-O 文件的魔数。FAT为`0xcafebabe`，ARMv7为`0xfeedface`，ARM64为`0xfeedfacf`（Mac是小端模式）
* cputype、cpusubtype: `CPU`架构和子版本
* filetype: 文件类型。
* ncmds: 加载命令的数量
* sizeofcmds: 所有加载命令的大小
* flags: `dyld`加载需要的一些标记。其中，`MH_PIE`表示启用地址空间布局随机化。
* reserved: 64位的保留字段。

### Load Command

**********

未完待续