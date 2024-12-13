---
title: 逆向工程进阶
date: 2020-02-17 15:16:48
categories: IT技术
tags:
- 逆向
- iOS
---

## 前言

如果您是iOS开发，具备相应的开发储备，除了需要了解逆向的基础，同样需要
知道程序的运行原理。

下面会介绍逆向工程相关的进阶知识，理论知识比较枯燥，但是确实必须要掌握的。
<!-- more -->
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

Header部分由以下部分组成:

* magic: Mach-O 文件的魔数。FAT为`0xcafebabe`，ARMv7为`0xfeedface`，ARM64为`0xfeedfacf`（Mac是小端模式）
* cputype、cpusubtype: `CPU`架构和子版本
* filetype: 文件类型。
* ncmds: 加载命令的数量
* sizeofcmds: 所有加载命令的大小
* flags: `dyld`加载需要的一些标记。其中，`MH_PIE`表示启用地址空间布局随机化。
* reserved: 64位的保留字段。

下面是微信的Header部分

![Wechat Mach-O Header](/images/mach-o/mach-wechat.png)

### Load Command

Load Command 告诉操作系统应当如何加载文件中的数据，对系统内核加载器和动态链接器起指导作用。
可以使用MachOView 查看 Load Command部分。

Load Command 包含以下部分:

* LC_SEGMENT_64: 定义一个段，加载后被映射到内存中，包括里面的节。
* LC_DYLD_INFO_ONLY: 记录了有关链接的重要信息，包括在__LINKEDIT中动态链接相关信息的具体偏移和大小。ONLY表示这个加载指令是程序运行所必需的，如果旧的链接器无法识别它，程序就会出错。
* LC_SYMTAB: 为文件定义符号表和字符串表，在链接文件时被链接器使用，同时也用于调试器映射符号到源文件。符号表定义的本地符号仅用于调试，而已定义和未定义的 `external` 符号被链接器使用。
* LC_DYSYMTAB: 将符号表中给出符号的额外符号信息提供给动态链接器。
* LC_LOAD_DYLINKER: 默认的加载器路径。
* LC_UUUID: 用于标识 Mach-O 文件的ID，也用于崩溃堆栈和符号文件的对应解析。
* LC_VERSION_MIN_IPHONES: 系统要求的最低版本。
* LC_SOURCE_VERSION: 构建二进制文件的源代码版本号。
* LC_MAIN: 程序的入口。`dyld`获取地址，然后跳转到该处执行。
* LC_ENCRYPTION_INFO_64: 文件是否加密的标志，加密内容的偏移和大小。
* LC_LOAD_DYLIB: 依赖的动态库，包括动态库名称、当前版本号、兼容版本号。可以使用 `otool -L xxx` 命令查看。
* LC_RPATH: Runpath Search Paths，@rpath 搜索的路径。
* LC_FUNCTION_STARTS: 函数起始地址表，是调试器和其他程序能很容易地看到一个地址是否在函数内。
* LC_DATA_IN_CODE: 定义在代码段内的非指令的表。
* LC_CODE_SIGNAURE: 代码签名信息。

![Mach-O Load Command](/images/mach-o/mach-wechat-1.png)

我们看到Load Command还包含以下4种段

* __PAGEZERO: 空指针陷阱段，映射到虚拟内存空间的第一页，用于捕捉对`NULL`指针的引用。
* __TEXT: 代码段/只读数据段。
* __DATA: 读取和写入数据的段。
* __LINKEDIT: 动态链接器需要使用的信息，包括重定位信息、绑定信息、懒加载信息等。

### 懒加载和非懒加载

iOS系统为了加快系统启动速度，将符号分成了懒加载符号和非懒加载符号。非懒加载符号在`dyld`加载时就会绑定真实的值；而懒加载符号不会，只有第1次去调用它时才会绑定真实的地址，在第2次调用时直接使用真实的地址。

这也是`fishhook`替换符号实现逆向功能的原理，原理会以后详细介绍。

后面还有 动态库，以及逆向原理会介绍。

*******

未完待续
