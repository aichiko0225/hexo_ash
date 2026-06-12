---
title: Spring 第一个项目实战：从 0 搭一个最小 REST 服务
date: 2026-06-13 18:00:00
updated: 2026-06-13 18:00:00
categories: 技术
tags:
- Java
- Spring Boot
- Practice
- REST API
---

如果你已经把 Spring Framework、Spring MVC、Spring Boot 这些概念大致理顺了，接下来最重要的事情不是继续看名词，而是亲手起一个真正能跑起来的项目。

这篇文章就是这组系列的第 2 篇。它不追求一步到位做成企业项目，而是专注把最小闭环真正跑通：启动应用、写接口、接参数、返回 JSON、做一层最基础的分层。

你可以把它当成“从认知进入代码”的第一步。先把主线走通，后面再在这个项目上逐步补校验、异常处理、数据库和事务。

系列顺序如下：

1. 已完成：Spring 入门认知
2. 这篇：从 0 搭一个最小 REST 服务
3. 下一篇：把最小项目升级成更像真实项目的版本
4. 最后：用 JPA + H2 把项目真正落库

<!-- more -->

如果前一篇解决的是：

- Spring 是什么
- Spring Boot 是什么
- Spring MVC 怎么理解
- 为什么要分 `Controller / Service / Repository`

那这一篇解决的是：

- 怎么真正起一个项目
- 怎么写第一个接口
- 怎么把理论里的注解和分层变成代码

目标非常明确：

> 做出一个最小可运行的 Spring Boot REST 项目。

这篇不会一上来就接数据库，也不会引入一堆复杂能力。

先把最小闭环打通：

- 启动项目
- 写接口
- 接参数
- 返回 JSON
- 做简单分层
- 用配置文件

## 1. 这个项目最终会长什么样

我们要做一个最小的用户接口项目，功能非常简单：

1. 查询用户详情
2. 查询用户列表
3. 创建用户

先不接数据库。

先用内存里的假数据把 Spring Boot 主线跑通。

最终你会得到这些接口：

- `GET /users/1`
- `GET /users?page=1`
- `POST /users`

这已经足够让你把下面这些关键点走一遍：

- `@SpringBootApplication`
- `@RestController`
- `@RequestMapping`
- `@GetMapping`
- `@PostMapping`
- `@PathVariable`
- `@RequestParam`
- `@RequestBody`
- `@Service`
- `application.yml`

## 2. 先准备环境

你至少需要这些：

- JDK 17 或更高
- Maven
- 一个顺手的 IDE

如果你后面要走现代 Spring Boot 3.x，推荐直接用：

- JDK 17+
- Spring Boot 3.x

这是因为：

- Spring 6 / Spring Boot 3 已经要求更现代的 Java 版本
- 现在新项目主流也基本是这套组合

## 3. 从 `start.spring.io` 创建项目

推荐直接用官方脚手架：<https://start.spring.io>

### 3.1 建议这样选

- Project: `Maven`
- Language: `Java`
- Spring Boot: 选当前稳定版本的 `3.x`
- Group: `com.example`
- Artifact: `demo`
- Packaging: `Jar`
- Java: `17`

### 3.2 依赖先只加一个

先只加：

- `Spring Web`

不要一开始就加：

- 数据库
- 安全
- Redis
- Kafka

因为我们现在只想把 Web 主线先走通。

### 3.3 为什么只加 `Spring Web`

因为它已经能给你一套最小 REST 项目所需的核心能力：

- Spring MVC
- JSON 序列化
- 内嵌 Tomcat
- Web 基础自动配置

你可以把它理解成：

> 一个依赖，先把 HTTP 接口项目最基本的地基铺好。

## 4. 先看生成出来的项目结构

项目生成后，你通常会看到类似结构：

```text
demo/
  .mvn/
  src/
    main/
      java/
        com/example/demo/
          DemoApplication.java
      resources/
        application.properties
    test/
      java/
        com/example/demo/
          DemoApplicationTests.java
  mvnw
  mvnw.cmd
  pom.xml
```

这里最关键的是几个位置：

### 4.1 `pom.xml`

项目依赖和构建配置。

### 4.2 `DemoApplication.java`

应用入口。

### 4.3 `src/main/java`

你的主要 Java 代码都放这里。

### 4.4 `src/main/resources`

配置文件、模板、静态资源等一般放这里。

### 4.5 `mvnw` / `mvnw.cmd`

这是 Maven Wrapper。

它的好处是：

- 项目可以自带 Maven 运行方式
- 团队环境更统一

在 Windows 上你后面更可能用：

```powershell
./mvnw.cmd spring-boot:run
```

## 5. 先理解入口类在干什么

脚手架生成的入口类通常长这样：

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

这段代码虽然短，但它是整个项目的起点。

### 5.1 `@SpringBootApplication`

你现在先记住它的实际作用：

- 告诉 Spring Boot 这是应用入口
- 开启组件扫描
- 开启自动配置

### 5.2 `SpringApplication.run(...)`

它会：

- 启动 Spring 容器
- 初始化自动配置
- 启动内嵌 Web 服务器

所以你可以把它理解成：

> 整个项目的启动总开关。

## 6. 先写第一个最简单的接口

现在不要急着分层，先把最小接口跑起来。

例如新建一个控制器：

```java
package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "hello spring";
    }
}
```

### 6.1 这里发生了什么

这段代码其实已经把几个核心概念串起来了：

- `@RestController` 告诉 Spring：这是一个 Web 控制器
- `@GetMapping("/hello")` 定义一个 GET 路由
- 返回值直接作为响应体返回

### 6.2 跑起来后你应该看到什么

启动项目后访问：

```text
http://localhost:8080/hello
```

如果能看到：

```text
hello spring
```

这说明最基础的 Spring Boot Web 链路已经通了：

- 应用启动成功
- Spring MVC 生效
- 路由能匹配
- 响应能返回

## 7. 把它升级成一个最小用户接口

接下来不要停在 `hello world`。

我们要把它升级成更像接口项目的样子。

例如我们准备做 `/users` 相关接口。

### 7.1 先定义返回对象

例如：

```java
package com.example.demo.dto;

public class UserDTO {
    private Long id;
    private String name;

    public UserDTO() {
    }

    public UserDTO(Long id, String name) {
        this.id = id;
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

### 7.2 为什么要先有 DTO

因为真实接口一般不会一直直接返回字符串。

你最终更常返回的是结构化 JSON。

例如：

```json
{
  "id": 1,
  "name": "ash"
}
```

返回对象时，Spring 会把它们转成 JSON。

## 8. 写第一个用户查询接口

控制器可以先写成：

```java
package com.example.demo.controller;

import com.example.demo.dto.UserDTO;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping("/{id}")
    public UserDTO getUser(@PathVariable Long id) {
        return new UserDTO(id, "user-" + id);
    }
}
```

### 8.1 这里最重要的三个点

- `@RequestMapping("/users")`：给控制器统一加路径前缀
- `@GetMapping("/{id}")`：处理具体 GET 路由
- `@PathVariable Long id`：接收路径参数

### 8.2 这一步你应该观察什么

访问：

```text
GET /users/1
```

你应该能得到类似：

```json
{
  "id": 1,
  "name": "user-1"
}
```

这会让你真正感受到：

- 你写的是 Java 对象
- Spring MVC 在帮你做 HTTP 参数绑定和 JSON 输出

## 9. 再补一个查询列表接口

例如：

```java
@GetMapping
public List<UserDTO> listUsers(@RequestParam(defaultValue = "1") int page) {
    List<UserDTO> users = new ArrayList<>();
    users.add(new UserDTO(1L, "ash"));
    users.add(new UserDTO(2L, "tom"));
    return users;
}
```

### 9.1 这里重点看什么

- `@GetMapping` 处理 `/users`
- `@RequestParam` 处理查询参数
- 默认值可以避免参数缺失时报错

访问：

```text
GET /users?page=1
```

你就能把“查询参数绑定”这条主线走一遍。

## 10. 再补一个创建用户接口

现在把 POST 也走通。

先定义请求对象：

```java
package com.example.demo.dto;

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

然后写 Controller：

```java
@PostMapping
public UserDTO createUser(@RequestBody CreateUserRequest request) {
    return new UserDTO(3L, request.getName());
}
```

### 10.1 为什么这里要有 getter / setter

因为 Spring 在接收 JSON 请求体并绑定到 Java 对象时，通常需要可访问的属性读写方式。

### 10.2 这一步打通的是什么

你现在走通的是：

- 客户端发 JSON
- Spring 把 JSON 绑定到 Java 对象
- Controller 拿到对象
- 返回新的 JSON 响应

这已经是最典型的 REST 接口开发主线之一了。

## 11. 现在开始做最基础分层

很多教程一开始就把所有代码堆在 Controller 里。

这样虽然能跑，但很快就会乱。

所以现在开始做最基础的分层。

### 11.1 先建一个 Service

例如：

```java
package com.example.demo.service;

import com.example.demo.dto.UserDTO;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class UserService {

    public UserDTO getUser(Long id) {
        return new UserDTO(id, "user-" + id);
    }

    public List<UserDTO> listUsers(int page) {
        List<UserDTO> users = new ArrayList<>();
        users.add(new UserDTO(1L, "ash"));
        users.add(new UserDTO(2L, "tom"));
        return users;
    }

    public UserDTO createUser(String name) {
        return new UserDTO(3L, name);
    }
}
```

### 11.2 Controller 改成调用 Service

```java
package com.example.demo.controller;

import com.example.demo.dto.CreateUserRequest;
import com.example.demo.dto.UserDTO;
import com.example.demo.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public UserDTO getUser(@PathVariable Long id) {
        return userService.getUser(id);
    }

    @GetMapping
    public List<UserDTO> listUsers(@RequestParam(defaultValue = "1") int page) {
        return userService.listUsers(page);
    }

    @PostMapping
    public UserDTO createUser(@RequestBody CreateUserRequest request) {
        return userService.createUser(request.getName());
    }
}
```

### 11.3 为什么要这么做

因为你要开始建立一个真实项目的基本习惯：

- Controller 负责接请求
- Service 负责业务逻辑

这在 Python 项目里其实也一样，只是 Spring 更强调这种分层组织方式。

## 12. 理解一下 Spring 为什么能把 `UserService` 注入进来

这里的关键在于：

- `UserService` 上有 `@Service`
- Spring 要管理它
- `UserController` 通过构造函数声明依赖

所以容器在启动时会把对象组装起来。

这就是依赖注入在项目里第一次变得“有手感”的地方。

## 13. 配置文件也顺手走一遍

现在不要只写代码，也顺手碰一下配置文件。

把 `application.properties` 改成 `application.yml` 也可以。

例如：

```yaml
server:
  port: 8080

spring:
  application:
    name: demo
```

### 13.1 这一节的重点不在配置量

重点在于你要知道：

- Spring Boot 很多基础行为是通过配置文件控制的
- 端口、环境、数据库、中间件几乎都会从这里继续扩展

## 14. 到这里你已经真正走通了什么

很多时候你以为只是“写了几个接口”，其实已经把 Spring 最关键的一批入门能力走过了一遍。

你已经实际碰到了：

- `@SpringBootApplication`
- `SpringApplication.run(...)`
- `@RestController`
- `@RequestMapping`
- `@GetMapping`
- `@PostMapping`
- `@PathVariable`
- `@RequestParam`
- `@RequestBody`
- `@Service`
- `application.yml`

这不是“演示代码”，而是一个真实最小项目的骨架。

## 15. 当前这个项目还故意没做什么

为了让主线足够清晰，这篇先故意没做下面这些：

- 参数校验
- 全局异常处理
- 数据库
- 事务
- JPA / MyBatis
- 安全认证
- 测试

不是它们不重要。

而是如果你一开始全塞进来，很容易只剩配置焦虑，反而抓不住主线。

## 16. 你现在可以自己检查哪些地方

做到这里，你可以反问自己：

1. 我能不能自己从头起一个 Spring Boot Web 项目
2. 我能不能解释 `@RestController` 是做什么的
3. 我能不能说清 `@PathVariable`、`@RequestParam`、`@RequestBody` 的区别
4. 我能不能把业务逻辑从 Controller 挪到 Service
5. 我知不知道为什么返回 Java 对象会变成 JSON

如果这些你都能回答，说明这篇已经达到目的了。

## 17. 一个建议：真的把它手敲一遍

不要只“看懂代码”。

最好真的：

- 自己创建一次项目
- 自己跑一次启动
- 自己发一次 GET / POST 请求
- 自己把 Controller 挪成 Controller + Service

只有手敲一遍，你对结构和注解的感觉才会稳定下来。

## 18. 如果你想再往前一步，可以先怎么增强

在还没接数据库之前，你也可以先做一些轻量增强：

- 给请求参数做基本校验
- 给用户不存在场景加异常
- 给错误响应统一格式
- 补一个更清晰的目录结构

这些会是下一篇的主题。

## 19. 这个最小项目之后，下一步应该怎么继续

最自然的下一步不是马上去碰微服务，而是把这个小项目逐步升级。

建议顺序如下。

### 19.1 第一步：补参数校验

让创建用户接口支持基本校验。

### 19.2 第二步：补统一异常处理

让错误响应更像真实项目。

### 19.3 第三步：接数据库

先选一条最简单路线：

- JPA
或
- MyBatis

### 19.4 第四步：补事务

让写操作具备事务边界。

### 19.5 第五步：补日志和测试

让项目更接近真实开发。

## 20. 你做完这个项目后，至少应该真正掌握什么

如果你真的把这篇从头做完，而不是只看代码，你应该已经掌握：

1. 怎么起一个 Spring Boot Web 项目
2. 怎么写最小 Controller
3. 怎么用 `@GetMapping` 和 `@PostMapping`
4. 怎么接路径参数、查询参数、请求体
5. 怎么返回 JSON
6. 怎么做基本分层
7. 怎么使用 Service
8. 怎么理解 Boot 启动入口
9. 怎么理解配置文件
10. 怎么从“只会看教程”过渡到“自己能起一个最小项目”

## 21. 最后的建议

做这个项目的时候，请不要追求一次写得像企业项目。

如果你已经把这篇走完，最适合接着读的是这组系列的第 3 篇：**Spring 项目下一步：把最小 REST 项目升级成更像真实项目的版本**。

它会继续带你把这个最小项目升级成“更像真实项目”的版本，重点补参数校验、统一异常处理、数据库接入和事务。

你现在真正要拿下的是：

- 我知道项目怎么起
- 我知道一个请求怎么走
- 我知道怎么分层
- 我知道 Spring Boot 和 Spring MVC 分别在干什么

只要这个最小闭环真的跑通了，你的入门就不是假的。

一句话总结：

> 第一个 Spring 项目不要追求复杂，而要追求把启动、路由、参数、分层、配置这条主线真正走通。
