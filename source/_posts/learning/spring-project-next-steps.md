---
title: Spring 项目下一步：把最小 REST 项目升级成更像真实项目的版本
date: 2026-06-13 16:00:00
updated: 2026-06-13 16:00:00
categories: 技术
tags:
- Java
- Spring Boot
- Practice
- Architecture
- MyBatis
---

最小 Spring Boot 项目跑起来之后，很多人会误以为自己已经“会 Spring 了”。但真正进入开发后，你会很快遇到另外一层问题：参数不能随便收、错误不能随便返回、数据不能一直写死在内存里，业务写入也不能不考虑事务。

这篇文章是这组系列的第 3 篇，目标不是继续堆功能，而是把“能跑”的项目往“像项目”的方向推进。你会开始接触校验、统一异常处理、分层边界、数据库接入选择以及事务意识。

它承接前两篇，又为最后一篇数据库实战做准备。

系列顺序如下：

1. Spring 入门认知
2. 最小 REST 项目实战
3. 这篇：把最小项目升级成更像真实项目的版本
4. 下一篇：用 JPA + H2 把项目真正落库

<!-- more -->

这篇文章接在前两篇后面：

- Spring 入门教程：给会 Python 后端、准备转 Java 全栈的人
- Spring 第一个项目实战：从 0 搭一个最小 REST 服务

如果前两篇解决的是：

- Spring 核心概念是什么
- 第一个最小 Spring Boot 项目怎么搭
- 怎么写最基本的 Controller / Service / DTO

那这一篇解决的是：

- 怎么让这个最小项目更像真实项目
- 参数怎么校验
- 错误怎么统一处理
- 数据库怎么接进来
- 事务该放哪里
- JPA 和 MyBatis 应该怎么理解

这篇依然不追求“大而全”，而是追求：

> 让你的第一个项目从“能跑”升级到“像项目”。

## 1. 先看真实项目和最小项目的差别

在上一份文档里，你已经有了一个最小的用户接口项目。

它已经具备：

- Boot 启动
- 基本路由
- 请求参数接收
- DTO
- Service 分层
- JSON 返回

但真实项目通常还会多出这些要求：

1. 输入参数要校验
2. 错误响应要统一
3. 数据不能一直写死在内存里
4. 写操作要考虑事务
5. 项目结构要更清晰

所以接下来的升级顺序应该是：

1. 先补参数校验
2. 再补统一异常处理
3. 再接数据库
4. 再补事务
5. 最后明确选 JPA 还是 MyBatis

## 2. 第一步升级：参数校验

最小项目里，你的创建用户请求大概是这样的：

```java
public class CreateUserRequest {
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

这个类现在有个问题：

- 用户传空字符串也行
- 用户不传也行
- 用户传特别长的名字也行

真实项目里通常不会放任接口输入这么松。

### 2.1 参数校验为什么重要

因为接口层是数据进入系统的入口。

如果入口不做基本约束，后面问题会越来越多：

- 业务代码要到处判空
- 数据库里可能落脏数据
- 错误信息不一致
- bug 更难定位

### 2.2 Spring 里最常见的参数校验思路

Spring 常和 Bean Validation 一起使用。

你可以先把它理解成：

- 给字段打约束注解
- 在 Controller 参数上触发校验

例如把请求类改成：

```java
package com.example.demo.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class CreateUserRequest {

    @NotBlank(message = "name 不能为空")
    @Size(max = 20, message = "name 长度不能超过 20")
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

### 2.3 Controller 里怎么触发校验

```java
@PostMapping
public UserDTO createUser(@Valid @RequestBody CreateUserRequest request) {
    return userService.createUser(request.getName());
}
```

这里最关键的是：

- `@RequestBody`：把 JSON 请求体绑定到对象
- `@Valid`：触发参数校验

### 2.4 这里需要补什么依赖

如果项目没有带校验能力，通常要加：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

### 2.5 你现在先记住什么

这一节先记住这条主线：

```text
字段约束注解 + @Valid + @RequestBody = 基本请求参数校验
```

## 3. 第二步升级：统一异常处理

现在思考一个问题。

如果：

- 用户不存在
- 参数不合法
- 业务失败

你的接口应该怎么返回？

如果没有统一异常处理，常见后果是：

- 每个 Controller 自己处理一套
- 错误格式不一致
- 前端拿到的错误很难统一消费

### 3.1 为什么要统一异常处理

真实项目里，错误响应一般也需要“像接口”。

也就是说，不只是成功响应要有结构，失败响应也应该有结构。

例如你可能希望统一返回：

```json
{
  "code": "USER_NOT_FOUND",
  "message": "用户不存在"
}
```

### 3.2 先定义一个统一错误响应对象

例如新建 `ApiError.java`：

```java
package com.example.demo.dto;

public class ApiError {
    private final String code;
    private final String message;

    public ApiError(String code, String message) {
        this.code = code;
        this.message = message;
    }

    public String getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }
}
```

### 3.3 定义一个业务异常

例如：

```java
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id) {
        super("用户不存在，id=" + id);
    }
}
```

### 3.4 再用 `@RestControllerAdvice` 统一处理

例如：

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ApiError handleUserNotFound(UserNotFoundException ex) {
        return new ApiError("USER_NOT_FOUND", ex.getMessage());
    }
}
```

### 3.5 这一步最重要的价值是什么

它不是“多写了一个类”。

它的核心价值是：

- 错误返回结构统一
- Controller 更干净
- 异常处理逻辑可集中维护

这是 Spring 项目里很常见的做法。

## 4. 第三步升级：重新看分层边界

很多最小项目一开始虽然有 Controller / Service，但边界还不够清晰。

### 4.1 Controller 不应该做什么

Controller 不应该承担：

- 过多业务判断
- 大量对象组装
- 数据访问细节
- 重复错误处理

它更适合做的是：

- 接请求
- 做参数绑定
- 调用 Service
- 返回结果

### 4.2 Service 更像什么

Service 更像业务流程层。

它适合：

- 编排业务逻辑
- 决定事务边界
- 调用 Repository / DAO
- 抛业务异常

### 4.3 Repository / DAO 层为什么要独立

因为数据库访问终究会变复杂。

如果一开始就把 SQL 或持久化细节塞进 Controller 或 Service，后面维护会很痛苦。

## 5. 第四步升级：先理解 JPA 路线是什么

如果你以后走 Spring Boot 主流路线，JPA 会非常常见。

它通常和这些词一起出现：

- JPA
- Hibernate
- Spring Data JPA

### 5.1 JPA 可以先怎么理解

你可以先把 JPA 理解成：

- 一套 Java 持久化规范
- 一种更偏对象映射的数据库访问方式

在 Spring Boot 里，常见搭配是：

- `Spring Data JPA`

它会帮你把很多常见数据库操作抽象得更顺。

### 5.2 JPA 适合入门的原因

- Spring 生态整合很成熟
- 上手主线比较快
- 很适合先理解 Entity / Repository / Service 的关系

### 5.3 但它也不是万能的

你也要知道：

- 复杂查询时不一定总是最顺手
- ORM 思维需要一点适应成本

## 6. 第五步升级：再理解 MyBatis 路线是什么

如果你以后接触国内常见业务项目，MyBatis 很大概率会出现。

### 6.1 MyBatis 可以先怎么理解

它和 JPA 的感觉不太一样。

大致上：

- JPA 更偏对象映射和框架接管
- MyBatis 更偏你自己明确控制 SQL

如果你更喜欢“SQL 写在自己手里”，会更容易对 MyBatis 有感觉。

### 6.2 MyBatis 的典型优点

- SQL 可控
- 对复杂查询表达更直接
- 在很多传统业务系统里使用广泛

## 7. JPA 和 MyBatis 先怎么做一版很粗的比较

你现在不用追求精确到所有细节。

先建立一个够用的比较框架：

- JPA：框架感更强
- MyBatis：SQL 可控感更强
- JPA：上手主线更顺
- MyBatis：复杂查询时常更直接

入门阶段最重要的不是“马上站队”，而是知道它们在解决什么问题、风格差别在哪。

## 8. 第六步升级：事务意识必须建立起来

最小项目时，很多写操作看起来都很简单。

但下一步你必须知道，真实项目不会一直这样。

只要一个业务动作里包含多步数据修改，就要开始思考事务。

### 8.1 事务最常放在哪里

Spring 项目里，事务通常更适合放在 Service 层。

因为事务本质上是业务流程边界问题，而不是路由问题。

### 8.2 Spring 里常见事务写法

```java
@Transactional
public UserDTO createUser(String name) {
    ...
}
```

### 8.3 这里最重要的不是注解本身

而是你要开始形成意识：

- 事务是“这一组操作要不要一起成功失败”
- 它应该跟业务过程绑定

## 9. 目录结构也该更像项目

随着功能增加，目录最好开始更清晰。

例如：

```text
com/example/demo
├── controller
├── service
├── repository
├── dto
├── entity
├── exception
└── config
```

### 9.1 为什么现在就该整理

因为项目还小的时候调整最轻松。

等代码多了再重整目录，成本会高很多。

## 10. 真实项目和最小项目的差别，本质上差在哪

很多人会觉得“真实项目”和“练习项目”的区别在于技术栈多少。

其实更本质的差别通常在这里：

1. 输入是否被约束
2. 错误是否被统一处理
3. 数据访问是否有独立层
4. 事务是否有边界意识
5. 配置是否清晰
6. 项目结构是否可维护

所以你会发现：

一个最小项目和一个真实项目，区别主要在工程化细节。

## 11. 如果你现在只做一轮最小增强，优先做什么

如果你不想一次改很多，最推荐的顺序还是这几个：

1. 请求参数加校验
2. 增加统一错误响应
3. 增加业务异常类
4. 把异常处理集中化
5. 给项目目录做一次最小整理

这几步做完，项目气质就会明显不一样。

## 12. 这一篇真正想让你建立的是什么

不是让你背更多注解。

而是让你开始有下面这些意识：

- 接口输入不能太松
- 错误返回要统一
- Controller 不能承担所有逻辑
- 数据访问要有独立层
- 事务是业务流程边界问题
- 配置文件会越来越重要
- 一个最小项目和一个真实项目，区别主要在工程化细节

## 13. 最后给你一个最实用的落地建议

不要把这篇当“阅读材料”结束掉。

如果你已经把这一篇理解清楚，下一篇建议直接接着看这组系列的第 4 篇：**Spring 数据库实战：用 Spring Boot + JPA + H2 把最小项目真正落库**。

它会带你把前面的最小项目真正接上数据库，走一遍 `Spring Data JPA + H2` 的完整最小闭环。

最好的方式是按下面顺序，真的去改你上一个最小项目：

1. 给 `CreateUserRequest` 加校验注解
2. 在 Controller 上加 `@Valid`
3. 增加 `ApiError`
4. 增加 `UserNotFoundException`
5. 增加 `GlobalExceptionHandler`
6. 重新整理目录结构
7. 再决定下一步是先接 JPA 还是 MyBatis

只要你亲手把这几步做一遍，你对 Spring 项目的理解会比“只看教程”扎实很多。

一句话总结：

> 从最小项目走向真实项目，关键不是突然引入很多技术，而是按顺序补上校验、异常处理、数据访问、事务和配置这几层工程化能力。
