---
title: Spring 数据库实战：用 Spring Boot + JPA + H2 把最小项目真正落库
date: 2026-06-13 14:00:00
updated: 2026-06-13 14:00:00
categories: 技术
tags:
- Java
- Spring Boot
- Practice
- JPA
- Database
---

到这一步，前面的最小 Spring Boot 项目已经有了接口、有了基础分层，也开始有了校验和异常处理的意识。接下来最值得做的一件事，就是把“内存里的假数据”换成真正可读写的数据库。

这篇文章是这组系列的第 4 篇，也是第一轮完整实战的收口。重点不是一下学会所有 ORM 细节，而是把 `Entity -> Repository -> Service -> Controller -> Database` 这条链亲手跑通。

为了把主线压到最清晰，这里优先选择 `Spring Data JPA + H2`：依赖少、配置轻、反馈快，适合第一次把数据库整合走完。

系列顺序如下：

1. Spring 入门认知
2. 最小 REST 项目实战
3. 把最小项目升级成更像真实项目的版本
4. 这篇：用 JPA + H2 把项目真正落库

<!-- more -->

这篇文章接在前面三篇后面：

- Spring 入门教程：给会 Python 后端、准备转 Java 全栈的人
- Spring 第一个项目实战：从 0 搭一个最小 REST 服务
- Spring 项目下一步：把最小 REST 项目升级成更像真实项目的版本

如果前面三篇解决的是：

- Spring 核心认知
- 第一个最小 REST 项目
- 参数校验、异常处理、分层和事务意识

那这一篇解决的是：

- 怎么把“内存假数据”真正换成数据库
- 怎么用 `Spring Data JPA` 接数据库
- 怎么定义 Entity
- 怎么写 Repository
- 怎么完成最小 CRUD
- 怎么配 H2 内存数据库
- 怎么把事务放到正确位置

这篇会优先用：

- `Spring Boot`
- `Spring Data JPA`
- `H2 Database`

原因很简单：

- 上手快
- 配置最轻
- 不需要你先安装本地 MySQL
- 很适合把数据库主线先走通

你可以把这一篇理解成：

> 从“接口返回假数据”，升级到“接口真的读写数据库”。

## 1. 为什么这一步先选 H2，而不是直接上 MySQL

很多人一学数据库整合就急着上 MySQL。

这当然没问题，但入门阶段有个现实问题：

- 你会同时面对数据库安装
- 连接配置
- SQL 方言
- 权限
- IDE 数据源
- Spring 配置
- JPA 逻辑

学习点太多了。

所以更合理的方式是：

1. 先用 H2 跑通 Spring Data JPA 主线
2. 确认你理解了 Entity / Repository / Service / Controller 的关系
3. 再把 H2 换成 MySQL

这样你会轻松很多。

## 2. 这次要完成什么目标

这篇完成后，你应该能做到：

- 能配置 JPA 和 H2
- 能定义一个最小 `User` 实体
- 能写 `UserRepository`
- 能通过接口查询、创建用户
- 能理解数据从数据库表到接口响应的流转
- 能把 `@Transactional` 放在合理位置

我们最终会得到这些能力：

- `GET /users/{id}`：按 id 查询用户
- `GET /users`：查询用户列表
- `POST /users`：创建用户
- 数据真实存进数据库

## 3. 先给项目加依赖

如果你当前项目已经有：

- `Spring Web`

那现在需要再补两个依赖：

- `Spring Data JPA`
- `H2 Database`

`pom.xml` 里一般会新增：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```

### 3.1 这两个依赖分别负责什么

#### `spring-boot-starter-data-jpa`

它提供：

- JPA 相关能力
- Spring Data JPA
- ORM 相关自动配置

#### `h2`

它提供：

- 一个轻量关系型数据库
- 可以以内存模式运行
- 非常适合学习和测试

## 4. 先把配置文件补好

接数据库后，`application.yml` 会比之前重要得多。

你可以先配置成这样：

```yaml
server:
  port: 8080

spring:
  application:
    name: demo

  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:

  h2:
    console:
      enabled: true
      path: /h2-console

  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true
```

## 5. 逐项理解这份配置

这一步不要跳过去。

### 5.1 `spring.datasource`

这部分是数据库连接配置。

#### `url: jdbc:h2:mem:testdb`

表示：

- 用 H2 数据库
- 使用内存模式
- 数据库名是 `testdb`

你可以先把它理解成：

- 应用启动时，数据库在内存里准备好
- 应用停掉，数据也会消失

这非常适合学习和练手。

#### `driver-class-name`

指定数据库驱动。

#### `username` / `password`

数据库连接账号信息。

### 5.2 `spring.h2.console`

这部分是启用 H2 Web 控制台。

```yaml
spring:
  h2:
    console:
      enabled: true
      path: /h2-console
```

它的作用是：

- 让你可以通过网页直接查看数据库
- 这对学习非常有帮助

后面你可以访问：

```text
http://localhost:8080/h2-console
```

### 5.3 `spring.jpa.hibernate.ddl-auto: update`

这是一个很常见的配置。

入门阶段你先这样理解：

- 根据实体类变化自动更新表结构

### 5.4 `show-sql` 和 `format_sql`

这两个配置可以让你在日志里更容易看到 SQL。

对学习阶段很有帮助，因为你能看到：

- 你写的是 Repository 调用
- 底层实际上还是 SQL 在执行

## 6. 先定义 Entity

数据库接入后，和之前最大不同之一就是：你不再只是返回 DTO，而是要有和表结构对应的实体对象。

例如：

```java
package com.example.demo.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

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

### 6.1 这里几个核心注解先怎么记

- `@Entity`：告诉 JPA 这是一个实体
- `@Table(name = "users")`：映射到数据库表 `users`
- `@Id`：主键
- `@GeneratedValue`：主键生成策略

### 6.2 Entity 不等于 DTO

这是很重要的一点。

- `Entity` 更偏数据库映射
- `DTO` 更偏接口输入输出

入门阶段你可以先简单用，但最好从一开始就知道这两者不是一个概念。

## 7. 再定义 Repository

下一步是数据访问层。

例如：

```java
package com.example.demo.repository;

import com.example.demo.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
}
```

### 7.1 为什么这个接口这么短

因为 `JpaRepository` 已经帮你提供了很多常见能力：

- `findById`
- `findAll`
- `save`
- `deleteById`

这就是 Spring Data JPA 的一个核心体验：

- 很多基础 CRUD 不需要你自己先手写一堆实现

### 7.2 这一步会带来什么认知变化

你会开始发现：

- 以前内存里的假数据逻辑
- 现在要通过 Repository 和数据库交互

这就是真正的“数据访问层”开始出现的时刻。

## 8. 让 Service 真正开始连接业务和数据库

接下来把之前的 `UserService` 改造成真正调 Repository 的版本。

例如：

```java
package com.example.demo.service;

import com.example.demo.dto.UserDTO;
import com.example.demo.entity.User;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Transactional(readOnly = true)
    public UserDTO getUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        return toDTO(user);
    }

    @Transactional(readOnly = true)
    public List<UserDTO> listUsers() {
        return userRepository.findAll().stream()
                .map(this::toDTO)
                .toList();
    }

    @Transactional
    public UserDTO createUser(String name) {
        User user = new User();
        user.setName(name);
        User savedUser = userRepository.save(user);
        return toDTO(savedUser);
    }

    private UserDTO toDTO(User user) {
        return new UserDTO(user.getId(), user.getName());
    }
}
```

### 8.1 为什么事务通常放在 Service 层

因为 Service 更适合表达业务流程边界。

例如创建用户时：

- 准备实体
- 调用保存
- 转成返回对象

这一整段更像一个业务动作。

### 8.2 `readOnly = true` 是什么感觉

它表达的是：

- 这是只读事务场景

你先不用深究所有优化细节，但可以先建立这个意识。

## 9. Controller 基本不用大改，但语义会完全不同

Controller 层看起来可能变化不大，例如：

```java
@GetMapping("/{id}")
public UserDTO getUser(@PathVariable Long id) {
    return userService.getUser(id);
}
```

但这时它和前面的区别非常大：

- 以前返回的是内存假数据
- 现在返回的是数据库真实数据

这一点你要有感觉，因为这意味着整条链真的通了。

## 10. 现在数据到底是怎么流动的

这是这篇最重要的一步之一。

创建用户时，数据流大致是：

1. 客户端发 JSON
2. Controller 用 `@RequestBody` 接收
3. Service 组装 Entity
4. Repository 调用 `save`
5. JPA 把数据写入数据库
6. Service 把 Entity 转成 DTO
7. Controller 返回 JSON

你现在应该开始能把这条链说顺。

## 11. H2 控制台为什么值得你亲手点开

很多初学者写完代码后，只看接口返回对不对。

但如果你想真正理解“数据真的落库了”，最好自己去 H2 控制台看一下。

### 11.1 可以看什么

- 表是不是自动建出来了
- 新创建的用户有没有写进去
- 数据长什么样

这会帮你把“代码世界”和“数据库世界”真正连起来。

## 12. `ddl-auto: update` 入门阶段为什么够用

因为现在你的目标不是数据库迁移治理，而是先把主线跑通。

入门阶段它能让你更专注在：

- 实体怎么定义
- Repository 怎么写
- 接口怎么打通

后面进入更真实项目时，再去学习 Flyway、Liquibase 或更严格的表结构管理方式更合适。

## 13. 这一步最容易犯的几个错误

### 13.1 把 Entity 直接当所有场景通用对象

短期能跑，但长期会让接口层和数据库层耦合太紧。

### 13.2 Controller 直接访问 Repository

这会让层次重新变乱。

### 13.3 不区分读写事务意识

刚开始不一定出问题，但最好尽早养成习惯。

### 13.4 一开始就纠结复杂 ORM 细节

这会打断主线。

你现在最重要的是：

- 先跑通
- 再理解
- 再优化

## 14. 这一篇真正想让你建立的认知

不是“我会几个 JPA 注解了”。

而是你要开始真正理解：

- 数据库配置为什么写在 `application.yml`
- JPA 的 Entity 是什么
- Repository 为什么这么重要
- 为什么 Service 层通常承担事务边界
- 为什么 Controller 不应该直接碰数据库细节
- DTO 和 Entity 为什么应该有意识地区分
- Spring Data JPA 为什么能让入门变快

## 15. 为什么这一步会让你对 Spring 更有手感

因为从这里开始，Spring 不再只是：

- 写几个注解
- 返回几个 JSON

而是开始真的连接：

- Web 层
- 业务层
- 数据访问层
- 配置
- 事务
- 数据库

这就是“工程感”真正起来的地方。

## 16. 如果你要继续增强这个项目，可以先怎么做

做完最小落库后，你就有了一个很好的练习底座。

接下来可以继续补：

- 更新用户接口
- 删除用户接口
- 分页查询
- 更完整的异常返回格式
- MySQL 切换
- 测试

## 17. 做完这篇后，你应该能说清什么

如果你把这篇真正做完，你应该已经能比较扎实地理解下面这些事：

1. 数据库配置为什么写在 `application.yml`
2. JPA 的 Entity 是什么
3. Repository 为什么这么重要
4. 为什么 Service 层通常承担事务边界
5. 为什么 Controller 不应该直接碰数据库细节
6. DTO 和 Entity 为什么应该有意识地区分
7. Spring Data JPA 为什么能让入门变快

## 18. 下一步最自然的增强方向

做完这一篇以后，你可以继续往下增强这个项目。

推荐顺序：

1. 加更新用户接口
2. 加删除用户接口
3. 给查询列表加分页意识
4. 给异常处理补校验错误格式
5. 把 H2 切换到 MySQL
6. 再补测试

## 19. 最后的建议

这一篇最值得你体验的，不是“我学会了几个 JPA 注解”，而是：

- 我第一次把 Spring Web、Spring Data、配置文件、事务、数据库连成了一条线

只要这条线通了，你后面无论走 JPA 还是 MyBatis，都会快很多。

如果你准备继续往真实项目推进，最好的方式不是再找十篇教程，而是直接基于这个小项目继续补 CRUD、分页、异常格式、数据库切换和测试。

一句话总结：

> Spring 数据库入门最关键的不是先学复杂 ORM，而是先把“Entity -> Repository -> Service -> Controller -> Database”这条链真正跑通。
