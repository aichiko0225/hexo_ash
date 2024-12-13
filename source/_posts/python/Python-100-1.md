---
title: Python-100天(一)
date: 2020-03-05 23:54:55
categories: IT技术
tags: Python
---

之前`Python`就已经学过了，`Flask`也玩的一溜一溜的。
但是间隔时间有些长，所以就找个一个项目重新温习一下，顺便记录一下。
这个系列文章会根据 `Python - 100天` 的流程走下去，当然其中有一些重复性的我就不介绍了，`Django`这个就不介绍了，因为跟`Flask`重复了，而且`Django`体量太大，不适合拿来用于学习。
<!-- more -->
### Python简介

#### Python的历史

1. 1989年圣诞节：Guido von Rossum开始写`Python`语言的编译器。
2. 1991年2月：第一个`Python`编译器（同时也是解释器）诞生，它是用C语言实现的（后面），可以调用C语言的库函数。在最早的版本中，`Python`已经提供了对“类”，“函数”，“异常处理”等构造块的支持，还有对列表、字典等核心数据类型，同时支持以模块为基础来构造应用程序。
3. 1994年1月：`Python 1.0`正式发布。
4. 2000年10月16日：`Python 2.0`发布，增加了完整的[垃圾回收](https://zh.wikipedia.org/wiki/%E5%9E%83%E5%9C%BE%E5%9B%9E%E6%94%B6_(%E8%A8%88%E7%AE%97%E6%A9%9F%E7%A7%91%E5%AD%B8))，提供了对[Unicode](https://zh.wikipedia.org/wiki/Unicode)的支持。与此同时，`Python`的整个开发过程更加透明，社区对开发进度的影响逐渐扩大，生态圈开始慢慢形成。
5. 2008年12月3日：`Python 3.0`发布，它并不完全兼容之前的`Python`代码，不过因为目前还有不少公司在项目和运维中使用`Python 2.x`版本，所以`Python 3.x`的很多新特性后来也被移植到`Python 2.6/2.7`版本中。

目前我们使用的`Python 3.7.x`的版本是在2018年发布的，`Python`的版本号分为三段，形如A.B.C。其中A表示大版本号，一般当整体重写，或出现不向后兼容的改变时，增加A；B表示功能更新，出现新功能时增加B；C表示小的改动（例如：修复了某个Bug），只要有修改就增加C。如果对`Python`的历史感兴趣，可以阅读名为[《Python简史》](http://www.cnblogs.com/vamei/archive/2013/02/06/2892628.html)的博文。

#### Python的优缺点

`Python`的优点很多，简单的可以总结为以下几点。

1. 简单和明确，做一件事只有一种方法。
2. 学习曲线低，跟其他很多语言相比，`Python`更容易上手。
3. 开放源代码，拥有强大的社区和生态圈。
4. 解释型语言，天生具有平台可移植性。
5. 对两种主流的编程范式（面向对象编程和函数式编程）都提供了支持。
6. 可扩展性和可嵌入性，例如在`Python`中可以调用`C/C++`代码。
7. 代码规范程度高，可读性强，适合有代码洁癖和强迫症的人群。

`Python`的缺点主要集中在以下几点。

1. 执行效率稍低，因此计算密集型任务可以由`C/C++`编写。
2. 代码无法加密，但是现在很多公司都不销售卖软件而是销售服务，这个问题会被弱化。
3. 在开发时可以选择的框架太多（如Web框架就有100多个），有选择的地方就有错误。

#### Python的应用领域

目前`Python`在`Web`应用开发、云基础设施、`DevOps`、网络数据采集（爬虫）、数据分析挖掘、机器学习等领域都有着广泛的应用，因此也产生了`Web`后端开发、数据接口开发、自动化运维、自动化测试、科学计算和可视化、数据分析、量化交易、机器人开发、自然语言处理、图像识别等一系列相关的职位。

### 100天计划 - Day01~15

基础知识就不详细介绍了，这个可以在下面这个网站上学习。
[Python教程](https://www.liaoxuefeng.com/wiki/1016959663602400)

**Day01~15** - **Python语言基础**

当然也可以查看已经整理好的简要文档

#### Day01 - [初识Python](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/01.%E5%88%9D%E8%AF%86Python.md)

- Python简介 - Python的历史 / Python的优缺点 / Python的应用领域
- 搭建编程环境 - Windows环境 / Linux环境 / MacOS环境
- 从终端运行Python程序 - Hello, world / print函数 / 运行程序
- 使用IDLE - 交互式环境(REPL) / 编写多行代码 / 运行程序 / 退出IDLE
- 注释 - 注释的作用 / 单行注释 / 多行注释

#### Day02 - [语言元素](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/02.%E8%AF%AD%E8%A8%80%E5%85%83%E7%B4%A0.md)

- 程序和进制 - 指令和程序 / 冯诺依曼机 / 二进制和十进制 / 八进制和十六进制
- 变量和类型 - 变量的命名 / 变量的使用 / input函数 / 检查变量类型 / 类型转换
- 数字和字符串 - 整数 / 浮点数 / 复数 / 字符串 / 字符串基本操作 / 字符编码
- 运算符 - 数学运算符 / 赋值运算符 / 比较运算符 / 逻辑运算符 / 身份运算符 / 运算符的优先级
- 应用案例 - 华氏温度转换成摄氏温度 / 输入圆的半径计算周长和面积 / 输入年份判断是否是闰年

#### Day03 - [分支结构](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/03.%E5%88%86%E6%94%AF%E7%BB%93%E6%9E%84.md)

- 分支结构的应用场景 - 条件 / 缩进 / 代码块 / 流程图
- if语句 - 简单的if / if-else结构 / if-elif-else结构 / 嵌套的if
- 应用案例 - 用户身份验证 / 英制单位与公制单位互换 / 掷骰子决定做什么 / 百分制成绩转等级制 / 分段函数求值 / 输入三条边的长度如果能构成三角形就计算周长和面积

#### Day04 - [循环结构](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/04.%E5%BE%AA%E7%8E%AF%E7%BB%93%E6%9E%84.md)

- 循环结构的应用场景 - 条件 / 缩进 / 代码块 / 流程图
- while循环 - 基本结构 / break语句 / continue语句
- for循环 - 基本结构 / range类型 / 循环中的分支结构 / 嵌套的循环 / 提前结束程序 
- 应用案例 - 1~100求和 / 判断素数 / 猜数字游戏 / 打印九九表 / 打印三角形图案 / 猴子吃桃 / 百钱百鸡

#### Day05 - [05.构造程序逻辑](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/05.%E6%9E%84%E9%80%A0%E7%A8%8B%E5%BA%8F%E9%80%BB%E8%BE%91.md)

- 经典案例：水仙花数 / 百钱百鸡 / Craps赌博游戏
- 练习题目：斐波那契数列 / 完美数 / 素数

#### Day06 - [函数和模块的使用](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/06.%E5%87%BD%E6%95%B0%E5%92%8C%E6%A8%A1%E5%9D%97%E7%9A%84%E4%BD%BF%E7%94%A8.md)

- 函数的作用 - 代码的坏味道 / 用函数封装功能模块
- 定义函数 - def语句 / 函数名 / 参数列表 / return语句 / 调用自定义函数
- 调用函数 - Python内置函数 /  导入模块和函数
- 函数的参数 - 默认参数 / 可变参数 / 关键字参数 / 命名关键字参数
- 函数的返回值 - 没有返回值  / 返回单个值 / 返回多个值
- 作用域问题 - 局部作用域 / 嵌套作用域 / 全局作用域 / 内置作用域 / 和作用域相关的关键字
- 用模块管理函数 - 模块的概念 / 用自定义模块管理函数 / 命名冲突的时候会怎样（同一个模块和不同的模块）

#### Day07 - [字符串和常用数据结构](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/07.%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%92%8C%E5%B8%B8%E7%94%A8%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84.md)

- 字符串的使用 - 计算长度 / 下标运算 / 切片 / 常用方法
- 列表基本用法 - 定义列表 / 用下表访问元素 / 下标越界 / 添加元素 / 删除元素 / 修改元素 / 切片 / 循环遍历
- 列表常用操作 - 连接 / 复制(复制元素和复制数组) / 长度 / 排序 / 倒转 / 查找
- 生成列表 - 使用range创建数字列表 / 生成表达式 / 生成器
- 元组的使用 - 定义元组 / 使用元组中的值 / 修改元组变量 / 元组和列表转换
- 集合基本用法 - 集合和列表的区别 /  创建集合 / 添加元素 / 删除元素 /  清空
- 集合常用操作 - 交集 / 并集 / 差集 / 对称差 / 子集 / 超集
- 字典的基本用法 - 字典的特点 / 创建字典 / 添加元素 / 删除元素 / 取值 / 清空
- 字典常用操作 - keys()方法 / values()方法 / items()方法 / setdefault()方法
- 基础练习 - 跑马灯效果 / 列表找最大元素 / 统计考试成绩的平均分 / Fibonacci数列 / 杨辉三角
- 综合案例 - 双色球选号 / 井字棋

#### Day08 - [面向对象编程基础](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/08.%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%BC%96%E7%A8%8B%E5%9F%BA%E7%A1%80.md)

- 类和对象 - 什么是类 / 什么是对象 / 面向对象其他相关概念
- 定义类 - 基本结构 / 属性和方法 / 构造器 / 析构器 / \_\_str\_\_方法
- 使用对象 - 创建对象 / 给对象发消息
- 面向对象的四大支柱 - 抽象 / 封装 / 继承 / 多态
- 基础练习 - 定义学生类 / 定义时钟类 / 定义图形类 / 定义汽车类

#### Day09 - [面向对象进阶](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/09.%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E8%BF%9B%E9%98%B6.md)

- 属性 - 类属性 / 实例属性 / 属性访问器 / 属性修改器 / 属性删除器 / 使用\_\_slots\_\_
- 类中的方法 - 实例方法 / 类方法 / 静态方法
- 运算符重载 - \_\_add\_\_ / \_\_sub\_\_ / \_\_or\_\_ /\_\_getitem\_\_ / \_\_setitem\_\_ / \_\_len\_\_ / \_\_repr\_\_ / \_\_gt\_\_ / \_\_lt\_\_ / \_\_le\_\_ / \_\_ge\_\_ / \_\_eq\_\_ / \_\_ne\_\_ / \_\_contains\_\_ 
- 类(的对象)之间的关系 - 关联 / 继承 / 依赖
- 继承和多态 - 什么是继承 / 继承的语法 / 调用父类方法 / 方法重写 / 类型判定 / 多重继承 / 菱形继承(钻石继承)和C3算法
- 综合案例 - 工资结算系统 / 图书自动折扣系统 / 自定义分数类

#### Day10 - [图形用户界面和游戏开发](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/10.%E5%9B%BE%E5%BD%A2%E7%94%A8%E6%88%B7%E7%95%8C%E9%9D%A2%E5%92%8C%E6%B8%B8%E6%88%8F%E5%BC%80%E5%8F%91.md)

- 使用tkinter开发GUI程序
- 使用pygame三方库开发游戏应用
- “大球吃小球”游戏

#### Day11 - [文件和异常](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/11.%E6%96%87%E4%BB%B6%E5%92%8C%E5%BC%82%E5%B8%B8.md)

- 读文件 - 读取整个文件 / 逐行读取 / 文件路径
- 写文件 - 覆盖写入 / 追加写入 / 文本文件 / 二进制文件
- 异常处理 - 异常机制的重要性 / try-except代码块 / else代码块 / finally代码块 / 内置异常类型 / 异常栈 / raise语句
- 数据持久化 - CSV文件概述 / csv模块的应用 / JSON数据格式 / json模块的应用

#### Day12 - [字符串和正则表达式](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/12.%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%92%8C%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F.md)

- 字符串高级操作 - 转义字符 / 原始字符串 / 多行字符串 / in和 not in运算符 / is开头的方法 / join和split方法 / strip相关方法 / pyperclip模块 / 不变字符串和可变字符串 / StringIO的使用
- 正则表达式入门 - 正则表达式的作用 / 元字符 / 转义 / 量词 / 分组 / 零宽断言 /贪婪匹配与惰性匹配懒惰 / 使用re模块实现正则表达式操作（匹配、搜索、替换、捕获）
- 使用正则表达式 - re模块 / compile函数 / group和groups方法 / match方法 / search方法 / findall和finditer方法 / sub和subn方法 / split方法
- 应用案例 - 使用正则表达式验证输入的字符串

#### Day13 - [进程和线程](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/13.%E8%BF%9B%E7%A8%8B%E5%92%8C%E7%BA%BF%E7%A8%8B.md)

- 进程和线程的概念 - 什么是进程 / 什么是线程 / 多线程的应用场景
- 使用进程 - fork函数 / multiprocessing模块 / 进程池 / 进程间通信
- 使用线程 - thread模块 / threading模块 / Thread类 / Lock类 / Condition类 / 线程池

#### Day14 - [网络编程入门和网络应用开发](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/14.%E7%BD%91%E7%BB%9C%E7%BC%96%E7%A8%8B%E5%85%A5%E9%97%A8%E5%92%8C%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91.md)

- 计算机网络基础 - 计算机网络发展史 / “TCP-IP”模型 / IP地址 / 端口 / 协议 / 其他相关概念
- 网络应用模式 - “客户端-服务器”模式 / “浏览器-服务器”模式
- 基于HTTP协议访问网络资源 - 网络API概述 / 访问URL / requests模块 / 解析JSON格式数据
- Python网络编程 - 套接字的概念 / socket模块 /  socket函数 / 创建TCP服务器 / 创建TCP客户端 / 创建UDP服务器 / 创建UDP客户端 / SocketServer模块
- 电子邮件 - SMTP协议 / POP3协议 / IMAP协议 / smtplib模块 / poplib模块 / imaplib模块
- 短信服务 - 调用短信服务网关

#### Day15 - [图像和办公文档处理](https://github.com/aichiko0225/Python-100-Days/blob/master/Day01-15/15.%E5%9B%BE%E5%83%8F%E5%92%8C%E5%8A%9E%E5%85%AC%E6%96%87%E6%A1%A3%E5%A4%84%E7%90%86.md)

- 用Pillow处理图片 - 图片读写 / 图片合成 / 几何变换 / 色彩转换 / 滤镜效果
- 读写Word文档 - 文本内容的处理 / 段落 / 页眉和页脚 / 样式的处理
- 读写Excel文件 - xlrd模块 / xlwt模块
- 生成PDF文件 - pypdf2模块 / reportlab模块

第一篇我们就扯一些稀奇古怪的东西

### Python参考书籍

先列出一些`Python`学习的参考书籍

#### 入门读物

1. 《Python基础教程》（*Beginning Python From Novice to Professional*）
2. 《Python学习手册》（*Learning Python*）
3. 《Python编程》（*Programming Python*）
4. 《Python Cookbook》
5. 《Python程序设计》（*Python Programming: An Introduction to Computer Science*）
6. 《Modern Python Cookbook》

#### 进阶读物

1. 《Python核心编程》（*Core Python Applications Programming*）
2. 《流畅的Python》（*Fluent Python*）
3. 《Effective Python：编写高质量Python代码的59个有效方法》（*Effective Python 59 Specific Ways to Write Better Python*）
4. 《Python设计模式》（*Learning Python Design Patterns*）
5. 《Python高级编程》（*Expert Python Programming*）
6. 《Python性能分析与优化》（*Mastering Python High Performance*）

#### Web框架

1. 《Django基础教程》（*Tango with Django*）
2. 《轻量级Django》（*Lightweight Django*）
3. 《Python Web开发：测试驱动方法》（*Test-Driven Development with Python*）
4. 《Web Development with Django Cookbook》
5. 《Test-Driven Development with Django》
6. 《Django Project Blueprints 》
7. 《Flask Web开发：基于Python的Web应用开发实战》（*Flask Web Development: Developing Web Applications with Python*）
8. 《深入理解Flask》（*Mastering Flask*）

#### 爬虫开发

1. 《用Python写网络爬虫》（*Web Scraping with Python*）
2. 《精通Python爬虫框架Scrapy》（*Learning Scrapy*）
3. 《Python网络数据采集》（*Web Scraping with Python*）
4. 《Python爬虫开发与项目实战》
5. 《Python 3网络爬虫开发实战》

#### 数据分析

1. 《利用Python进行数据分析》（*Python for Data Analysis*）
2. 《Python数据科学手册》（*Python Data Science Handbook*）
3. 《Python金融大数据分析》（*Python for Finance*）
4. 《Python数据可视化编程实战》（*Python Data Visualization Cookbook*）
5. 《Python数据处理》（*Data Wrangling with Python*）

#### 机器学习

1. 《Python机器学习基础教程》（*Introduction to Machine Learning with Python*）
2. 《Python机器学习实践指南》（*Python Machine Learning Blueprints*）
3. 《Python Machine Learning Case Studies》
4. 《Python机器学习实践：测试驱动的开发方法》（*Thoughtful Machine Learning with Python A Test Driven Approach*）
5. 《Python机器学习经典实例》（*Python Machine Learning Cookbook*）
6. 《TensorFlow：实战Google深度学习框架》

### Python编程惯例

“惯例”这个词指的是“习惯的做法，常规的办法，一贯的做法”，与这个词对应的英文单词叫“idiom”。由于`Python`跟其他很多编程语言在语法和使用上还是有比较显著的差别，因此作为一个`Python`开发者如果不能掌握这些惯例，就无法写出“Pythonic”的代码。下面我们总结了一些在`Python`开发中的惯用的代码。

1. 让代码既可以被导入又可以被执行。

   ```Python
   if __name__ == '__main__':
   ```

2. 用下面的方式判断逻辑“真”或“假”。

   ```Python
   if x:
   if not x:
   ```

   **好**的代码：

   ```Python
   name = 'jackfrued'
   fruits = ['apple', 'orange', 'grape']
   owners = {'1001': '骆昊', '1002': '王大锤'}
   if name and fruits and owners:
       print('I love fruits!')
   ```

   **不好**的代码：

   ```Python
   name = 'jackfrued'
   fruits = ['apple', 'orange', 'grape']
   owners = {'1001': '骆昊', '1002': '王大锤'}
   if name != '' and len(fruits) > 0 and owners != {}:
       print('I love fruits!')
   ```

3. 善于使用in运算符。

   ```Python
   if x in items: # 包含
   for x in items: # 迭代
   ```

   **好**的代码：

   ```Python
   name = 'Hao LUO'
   if 'L' in name:
       print('The name has an L in it.')
   ```

   **不好**的代码：

   ```Python
   name = 'Hao LUO'
   if name.find('L') != -1:
       print('This name has an L in it!')
   ```

4. 不使用临时变量交换两个值。

   ```Python
   a, b = b, a
   ```

5. 用序列构建字符串。

   **好**的代码：

   ```Python
   chars = ['j', 'a', 'c', 'k', 'f', 'r', 'u', 'e', 'd']
   name = ''.join(chars)
   print(name)  # jackfrued
   ```

   **不好**的代码：

   ```Python
   chars = ['j', 'a', 'c', 'k', 'f', 'r', 'u', 'e', 'd']
   name = ''
   for char in chars:
       name += char
   print(name)  # jackfrued
   ```

6. EAFP优于LBYL。

   EAFP - **E**asier to **A**sk **F**orgiveness than **P**ermission.

   LBYL - **L**ook **B**efore **Y**ou **L**eap.

   **好**的代码：

   ```Python
   d = {'x': '5'}
   try:
       value = int(d['x'])
       print(value)
   except (KeyError, TypeError, ValueError):
       value = None
   ```

   **不好**的代码：

   ```Python
   d = {'x': '5'}
   if 'x' in d and isinstance(d['x'], str) \
   and d['x'].isdigit():
       value = int(d['x'])
       print(value)
   else:
       value = None
   ```

7. 使用enumerate进行迭代。

   **好**的代码：

   ```Python
    fruits = ['orange', 'grape', 'pitaya', 'blueberry']
    for index, fruit in enumerate(fruits):
    print(index, ':', fruit)
   ```

   **不好**的代码：

   ```Python
   fruits = ['orange', 'grape', 'pitaya', 'blueberry']
   index = 0
   for fruit in fruits:
       print(index, ':', fruit)
       index += 1
   ```

8. 用生成式生成列表。

   **好**的代码：

   ```Python
   data = [7, 20, 3, 15, 11]
   result = [num * 3 for num in data if num > 10]
   print(result)  # [60, 45, 33]
   ```

   **不好**的代码：

   ```Python
   data = [7, 20, 3, 15, 11]
   result = []
   for i in data:
       if i > 10:
           result.append(i * 3)
   print(result)  # [60, 45, 33]
   ```

9. 用zip组合键和值来创建字典。

   **好**的代码：

   ```Python
   keys = ['1001', '1002', '1003']
   values = ['骆昊', '王大锤', '白元芳']
   d = dict(zip(keys, values))
   print(d)
   ```

   **不好**的代码：

   ```Python
   keys = ['1001', '1002', '1003']
   values = ['骆昊', '王大锤', '白元芳']
   d = {}
   for i, key in enumerate(keys):
       d[key] = values[i]
   print(d)
   ```

> **说明**：这篇文章的内容来自于网络，有兴趣的读者可以阅读[原文](http://safehammad.com/downloads/python-idioms-2014-01-16.pdf)。

### PEP8风格指南

`PEP`是`Python Enhancement Proposal`的缩写，通常翻译为“Python增强提案”。每个`PEP`都是一份为`Python`社区提供的指导`Python`往更好的方向发展的技术文档，其中的第8号增强提案（`PEP 8`）是针对`Python`语言编订的代码风格指南。尽管我们可以在保证语法没有问题的前提下随意书写`Python`代码，但是在实际开发中，采用一致的风格书写出可读性强的代码是每个专业的程序员应该做到的事情，也是每个公司的编程规范中会提出的要求，这些在多人协作开发一个项目（团队开发）的时候显得尤为重要。我们可以从`Python`官方网站的PEP 8链接中找到该文档，下面我们对该文档的关键部分做一个简单的总结。

#### 空格的使用

1. 使用空格来表示缩进而不要用制表符（`Tab`）。这一点对习惯了其他编程语言的人来说简直觉得不可理喻，因为绝大多数的程序员都会用Tab来表示缩进，但是要知道`Python`并没有像`C/C++`或`Java`那样的用花括号来构造一个代码块的语法，在Python中分支和循环结构都使用缩进来表示哪些代码属于同一个级别，鉴于此`Python`代码对缩进以及缩进宽度的依赖比其他很多语言都强得多。在不同的编辑器中，`Tab`的宽度可能是2、4或8个字符，甚至是其他更离谱的值，用`Tab`来表示缩进对`Python`代码来说可能是一场灾难。
2. 和语法相关的每一层缩进都用4个空格来表示。
3. 每行的字符数不要超过79个字符，如果表达式因太长而占据了多行，除了首行之外的其余各行都应该在正常的缩进宽度上再加上4个空格。
4. 函数和类的定义，代码前后都要用两个空行进行分隔。
5. 同一个类中，各个方法之间应该用一个空行进行分隔。
6. 二元运算符的左右两侧应该保留一个空格，而且只要一个空格就好。

#### 标识符命名

`PEP 8`倡导用不同的命名风格来命名`Python`中不同的标识符，以便在阅读代码时能够通过标识符的名称来确定该标识符在`Python`中扮演了怎样的角色（在这一点上，`Python`自己的内置模块以及某些第三方模块都做得并不是很好）。

1. 变量、函数和属性应该使用小写字母来拼写，如果有多个单词就使用下划线进行连接。
2. 类中受保护的实例属性，应该以一个下划线开头。
3. 类中私有的实例属性，应该以两个下划线开头。
4. 类和异常的命名，应该每个单词首字母大写。
5. 模块级别的常量，应该采用全大写字母，如果有多个单词就用下划线进行连接。
6. 类的实例方法，应该把第一个参数命名为`self`以表示对象自身。
7. 类的类方法，应该把第一个参数命名为`cls`以表示该类自身。

#### 表达式和语句

在`Python`之禅（可以使用`import this`查看）中有这么一句名言：**"There should be one-- and preferably only one --obvious way to do it."**，翻译成中文是“做一件事应该有而且最好只有一种确切的做法”，这句话传达的思想在`PEP 8`中也是无处不在的。

1. 采用内联形式的否定词，而不要把否定词放在整个表达式的前面。例如`if a is not b`就比`if not a is b`更容易让人理解。
2. 不要用检查长度的方式来判断字符串、列表等是否为`None`或者没有元素，应该用`if not x`这样的写法来检查它。
3. 就算`if`分支、`for`循环、`except`异常捕获等中只有一行代码，也不要将代码和`if`、`for`、`except`等写在一起，分开写才会让代码更清晰。
4. `import`语句总是放在文件开头的地方。
5. 引入模块的时候，`from math import sqrt`比`import math`更好。
6. 如果有多个`import`语句，应该将其分为三部分，从上到下分别是`Python`**标准模块**、**第三方模块**和**自定义模块**，每个部分内部应该按照模块名称的字母表顺序来排列。

### Zen of Python（Python之禅）

> Beautiful is better than ugly. （优美比丑陋好）  
> Explicit is better than implicit.（清晰比晦涩好）  
> Simple is better than complex.（简单比复杂好）  
> Complex is better than complicated.（复杂比错综复杂好）  
> Flat is better than nested.（扁平比嵌套好）  
> Sparse is better than dense.（稀疏比密集好）  
> Readability counts.（可读性很重要）  
> Special cases aren't special enough to break the rules.（特殊情况也不应该违反这些规则）  
> Although practicality beats purity.（但现实往往并不那么完美）  
> Errors should never pass silently.（异常不应该被静默处理）  
> Unless explicitly silenced.（除非你希望如此）  
> In the face of ambiguity, refuse the temptation to guess.（遇到模棱两可的地方，不要胡乱猜测）  
> There should be one-- and preferably only one --obvious way to do it.（肯定有一种通常也是唯一一种最佳的解决方案）  
> Although that way may not be obvious at first unless you're Dutch.（虽然这种方案并不是显而易见的，因为你不是那个荷兰人^这里指的是Python之父Guido^）  
> Now is better than never.（现在开始做比不做好）  
> Although never is often better than \*right\* now.（不做比盲目去做好^极限编程中的YAGNI原则^）  
> If the implementation is hard to explain, it's a bad idea.（如果一个实现方案难于理解，它就不是一个好的方案）  
> If the implementation is easy to explain, it may be a good idea.（如果一个实现方案易于理解，它很有可能是一个好的方案）  
> Namespaces are one honking great idea -- let's do more of those!（命名空间非常有用，我们应当多加利用）  
