---
title: Python-Flask基础篇(二)
date: 2020-03-21 19:12:10
categories: Python
tags: Flask
---

## 前言

前面介绍了Flask和HTTP的基础知识，下面会介绍Flask的基础用法

## 第4章 表单

在`Web`程序中，表单是和用户交互最常见的方式之一。用户注册、登录、撰写文章、编辑设置，无一不用到表单。不过，表单的处理却并不简单。
你不仅要创建表单，验证用户输入的内容，向用户显示错误提示，还要获取并保存数据。幸运的是，强大的`WTForms`可以帮我们解决这些问题。
`WTForms`是一个使用`Python`编写的表单库，它使得表单的定 义、验证（服务器端）和处理变得非常轻松。这一章我们会介绍在Web 程序中处理表单的方法和技巧。

### 使用Flask-WTF处理表单

扩展`Flask-WTF`集成了`WTForms`，使用它可以在`Flask`中更方便地使用`WTForms`。`Flask-WTF`将表单数据解析、`CSRF`保护、文件上传等功能与`Flask`集成，另外还附加了`reCAPTCHA`支持。

Flask-WTF默认为每个表单启用CSRF保护，它会为我们自动生成和 验证CSRF令牌。默认情况下，Flask-WTF使用程序密钥来对CSRF令牌 进行签名，所以我们需要为程序设置密钥：

```Python
app.secret_key = 'secret string'
```

#### 定义WTForms表单类

当使用WTForms创建表单时，表单由Python类表示，这个类继承从 WTForms导入的Form基类。一个表单由若干个输入字段组成，这些字 段分别用表单类的类属性来表示（字段即Field，你可以简单理解为表单 内的输入框、按钮等部件）。下面定义了一个LoginForm类，最终会生 成我们在前面定义的HTML表单：

```Python
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


# 4.2.1 basic form example
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')
```

每个字段属性通过实例化WTForms提供的字段类表示。字段属性的名称将作为对应HTML`<input>`元素的name属性及id属性值。

![常用的WTForms字段](/images/flask/w1.png)

![实例化字段类常用参数](/images/flask/w2.png)

![常用的WTForms验证器](/images/flask/w3.png)

当使用`Flask-WTF`定义表单时，我们仍然使用`WTForms`提供的字段类和验证器，创建的方式也完全相同，只不过表单类要继承`Flask-WTF`提供的`FlaskForm`类。`FlaskForm`类继承自`Form`类，进行了一些设置，并附加了一些辅助方法，以便与`Flask`集成。

#### 输出HTML代码

以我们使用WTForms创建的LoginForm为例，实例化表单类，然后将实例属性转换成字符串或直接调用就可以获取表单字段对应的HTML代码：

```shell
>>> form = LoginForm() >>> form.username()
u'<input id="username" name="username" type="text" value="">'
>>> form.submit()
u'<input id="submit" name="submit" type="submit" value="Submit">'
```

在创建HTML表单时，我们经常会需要使用HTML`<input>`元素的其 他属性来对字段进行设置。比如，添加class属性设置对应的CSS类为字段添加样式；添加placeholder属性设置占位文本。默认情况下，WTForms输出的字段HTML代码只会包含id和name属性，属性值均为表单类中对应的字段属性名称。如果要添加额外的属性，通常有两种方法。

1. 使用render_kw属性

```Python
username = StringField('Username', render_kw={'placeholder': 'Your Username'})
```

```HTML
<input type="text" id="username" name="username" placeholder="Your Username">
```

2. 在调用字段时传入

```shell
>>> form.username(style='width: 200px;', class_='bar')
u'<i nput class="bar" id="username" name="username" style="width: 200px;" type="text">'
```

#### 在模板中渲染表单

为了能够在模板中渲染表单，我们需要把表单类实例传入模板。首 先在视图函数里实例化表单类LoginForm，然后在render_template()函 数中使用关键字参数form将表单实例传入模板。

```Python
from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm


@app.route('/basic')
def basic():
    form = LoginForm()
    return render_template('login.html', form=form)
```

```HTML
<form method="post"> {{ form.csrf_token }}
    <!-- 渲染CSRF令牌隐藏字段 -->
    {{ form.username.label }}{{ form.username }}<br>
    {{ form.password.label }}{{ form.password }}<br>
    {{ form.remember }}{{ form.remember.label }}<br>
    {{ form.submit }}<br>
</form>
```

需要注意的是，在上面的代码中，除了渲染各个字段的标签和字段本身，我们还调用了`form.csrf_token`属性渲染`Flask-WTF`为表单类自动创建的CSRF令牌字段。`form.csrf_token`字段包含了自动生成的CSRF令牌值，在提交表单后会自动被验证，为了确保表单通过验证，我们必须在表单中手动渲染这个字段。

### 处理表单数据

表单数据的处理涉及很多内容，除去表单提交不说，从获取数据到保存数据大致会经历以下步骤：

1. 解析请求，获取表单数据。
2. 对数据进行必要的转换，比如将勾选框的值转换成Python的布尔值。
3. 验证数据是否符合要求，同时验证CSRF令牌。
4. 如果验证未通过则需要生成错误消息，并在模板中显示错误消息。
5. 如果通过验证，就把数据保存到数据库或做进一步处理。

除非是简单的程序，否则手动处理不太现实，使用Flask-WTF和 WTForms可以极大地简化这些步骤。

#### 提交表单

在HTML中，当`<form>`标签声明的表单中类型为submit的提交字段被单击时，就会创建一个提交表单的HTTP请求，请求中包含表单各个字段的数据。
表单的提交行为主要由三个属性控制，如下图所示。

![HTML表单中控制提交行为的属性](/images/flask/w4.png)

form标签的action属性用来指定表单被提交的目标URL，默认为当前URL，也就是渲染该模板的路由所在的URL。如果你要把表单数据发送到其他URL，可以自定义这个属性值。

#### 验证表单数据

表单数据的验证是Web表单中最重要的主题之一，这一节我们会学习如何使用Flask-WTF验证并获取表单数据。

1. 客户端验证和服务器端验证
表单的验证通常分为以下两种形式：

    - 客户端验证
    客户端验证（client side validation）是指在客户端（比如Web浏览器）对用户的输入值进行验证。比如，使用HTML5内置的验证属性即可实现基本的客户端验证（type、required、min、max、accept等）。比如，下面的username字段添加了required标志：

    ```HTML
    <input type="text" name="username" required>
    ```

    - 服务器端验证

    服务器端验证（server side validation）是指用户把输入的数据提交到服务器端，在服务器端对数据进行验证。如果验证出错，就在返回的响应中加入错误信息。用户修改后再次提交表单，直到通过验证。我们在Flask程序中使用WTForms实现的就是服务器端验证。

2. WTForms验证机制
WTForms验证表单字段的方式是在实例化表单类时传入表单数据，然后对表单实例调用validate()方法。这会逐个对字段调用字段实例化时定义的验证器，返回表示验证结果的布尔值。如果验证失败，就把错误消息存储到表单实例的errors属性对应的字典中，验证的过程如下所示：

```shell
>>> from wtforms import Form, StringField, PasswordField, BooleanField
>>> from wtforms.validators import DataRequired, Length
>>> class LoginForm(Form):
... username = StringField('Username', validators=[DataRequired()])
... password = PasswordField('Password', validators=[DataRequired() , Length(8, 128)])
>>> form = LoginForm(username='', password='123')
>>> form.data
# 表单数据字典
{'username': '', 'password': '123'}
>>> form.validate()
False >>> form.errors
# 错误消息字典
{'username': [u'This field is required.'], 'password': [u'Field must be at least 6 characters long.']}
>>> form2 = LoginForm(username='greyli', password='123456')
>>> form2.data
{'username': 'greyli', 'password': '123456'}
>>> form2.validate()
True
>>> form2.errors {}
```

3. 在视图函数中验证表单
因为现在的basic_form视图同时接收两种类型的请求：GET请求和POST请求。所以我们要根据请求方法的不同执行不同的代码。具体来说：首先是实例化表单，如果是GET请求，那么就渲染模板；如果是 POST请求，就调用validate()方法验证表单数据。

```Python
@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
```

#### 在模板中渲染错误消息

如果form.validate_on_submit()返回False，那么说明验证没有通 过。对于验证未通过的字段，WTForms会把错误消息添加到表单类的 errors属性中，这是一个匹配作为表单字段的类属性到对应的错误消息 列表的字典。我们一般会直接通过字段名来获取对应字段的错误消息列表，即`"form.字段名.errors"`。比如，form.name.errors返回name字段的错 误消息列表。

```HTML
<form method="post">
    {{ form.csrf_token }}
    {{ form.username.label }}<br>
    {{ form.username() }}<br>
    {% for message in form.username.errors %}
    <small class="error">{{ message }}</small><br>
    {% endfor %} {{ form.password.label }}<br>
    {{ form.password }}<br>
    {% for message in form.password.errors %}
    <small class="error">{{ message }}</small><br>
    {% endfor %}
    {{ form.remember }}{{ form.remember.label }}<br>
    {{ form.submit }}<br>
</form>
```

## 第5章 数据库(重点)

数据库是大多数动态Web程序的基础设施，只要你想把数据存储下来，就离不开数据库。我们这里提及的数据库（Database）指的是由存储数据的单个或多个文件组成的集合，它是一种容器，可以类比为文件柜。而人们通常使用数据库来表示操作数据库的软件，这类管理数据库的软件被称为数据库管理系统（DBMS，Database Management System），常见的DBMS有MySQL、PostgreSQL、SQLite、MongoDB等。为了便于理解，我们可以把数据库看作一个大仓库，仓库里有一些负责搬运货物（数据）的机器人，而DBMS就是操控机器人搬运货物的程序。

### 数据库的分类

数据库一般分为两种，SQL（Structured Query Language，结构化查 询语言）数据库和NoSQL（Not Only SQL，泛指非关系型）数据库。

#### SQL

SQL数据库指关系型数据库，常用的SQL DBMS主要包括SQL Server、Oracle、MySQL、PostgreSQL、SQLite等。关系型数据库使用表来定义数据对象，不同的表之间使用关系连接。

在SQL数据库中，每一行代表一条记录（record），每条记录又由不同的列（column）组成。在存储数据前，需要预先定义表模式（schema），以定义表的结构并限定列的输入数据类型。
为了避免在措辞上引起误解，我们先了解几个基本概念：

- 表（table）：存储数据的特定结构。
- 模式（schema）：定义表的结构信息。
- 列/字段（column/field）：表中的列，存储一系列特定的数据，列组成表。
- 行/记录（row/record）：表中的行，代表一条记录。
- 标量（scalar）：指的是单一数据，与之相对的是集合 （collection）。

#### NoSQL

NoSQL最初指No SQL或No Relational，现在NoSQL社区一般会解释为Not Only SQL。NoSQL数据库泛指不使用传统关系型数据库中的表格形式的数据库。近年来，NoSQL数据库越来越流行，被大量应用在实时（real-time）Web程序和大型程序中。与传统的SQL数据库相比，它在速度和可扩展性方面有很大的优势，除此之外还拥有无模式（schema- free）、分布式、水平伸缩（horizontally scalable）等特点。

最常用的两种NoSQL数据库如下所示：

1. 文档存储（document store）
文档存储是NoSQL数据库中最流行的种类，它可以作为主数据库使用。文档存储使用的文档类似SQL数据库中的记录，文档使用类JSON格式来表示数据。常见的文档存储DBMS有MongoDB、CouchDB等。
2. 键值对存储（key-value store）
键值对存储在形态上类似Python中的字典，通过键来存取数据，在读取上非常快，通常用来存储临时内容，作为缓存使用。常见的键值对 DBMS有Redis、Riak等，其中Redis不仅可以管理键值对数据库，还可以作为缓存后端（cache backend）和消息代理（message broker）。
另外，还有列存储（column store，又被称为宽列式存储）、图存储（graph store）等类型的NoSQL数据库，这里不再展开介绍。

### ORM魔法

在Web应用里使用原生SQL语句操作数据库主要存在下面两类问题：

- 手动编写SQL语句比较乏味，而且视图函数中加入太多SQL语句会降低代码的易读性。另外还会容易出现安全问题，比如SQL注入。
- 常见的开发模式是在开发时使用简单的SQLite，而在部署时切换 到MySQL等更健壮的DBMS。但是对于不同的DBMS，我们需要使用不同的Python接口库，这让DBMS的切换变得不太容易。

尽管使用ORM可以避免SQL注入问题，但你仍然需要对传入的查询参数进行验证。
另外，在执行原生SQL语句时也要注意避免使用字符串 拼接或字符串格式化的方式传入参数。
使用ORM可以很大程度上解决这些问题。它会自动帮你处理查询 参数的转义，尽可能地避免SQL注入的发生。
另外，它为不同的DBMS提供统一的接口，让切换工作变得非常简单。
ORM扮演翻译的角色，能够将我们的Python语言转换为DBMS能够读懂的SQL指令，让我们能 够使用Python来操控数据库。

尽管ORM非常方便，但如果你对SQL相当熟悉，那么自己编写SQL代码可以获得更大的灵活性和性能优势。
就像是使用IDE一样，ORM对初学者来说非常方便，但进阶以后你也许会想要自己掌控一切。
ORM把底层的SQL数据实体转化成高层的Python对象，这样一来， 你甚至不需要了解SQL，只需要通过Python代码即可完成数据库操作，ORM主要实现了三层映射关系：

- 表→Python类。
- 字段（列）→类属性。
- 记录（行）→类实例。

比如，我们要创建一个contacts表来存储留言，其中包含用户名称和电话号码两个字段。
在SQL中，下面的代码用来创建这个表，要向表中插入一条记录，需要使用下面的SQL语句：

```sql
CREATE TABLE contacts(
    name varchar(100) NOT NULL,
    phone_number varchar(32),
);
-- 插入一条记录
INSERT INTO contacts(name, phone_number) VALUES('Grey Li', '12345678');
```

如果使用ORM，我们可以使用类似下面的Python类来定义这个表：
使用ORM则只需要创建一个Contact类的实例，传入对应的参数表示各个列的数据即可。
下面的代码和使用上面的SQL语句效果相同：

```Python
from foo_orm import Model, Column, String


class Contact(Model):
    __tablename__ = 'contacts'
    name = Column(String(100), nullable=False)
    phone_number = Column(String(32))

# 插入一条记录
contact = Contact(name='Grey Li', phone_number='12345678')
```

除了便于使用，ORM还有下面这些优点：

- 灵活性好。你既能使用高层对象来操作数据库，又支持执行原生 SQL语句。
- 提升效率。从高层对象转换成原生SQL会牺牲一些性能，但这微不足道的性能牺牲换取的是巨大的效率提升。
- 可移植性好。ORM通常支持多种DBMS，包括MySQL、PostgreSQL、Oracle、SQLite等。你可以随意更换DBMS，只需要稍微 改动少量配置。

使用Python实现的ORM有SQLAlchemy、Peewee、PonyORM等。其中SQLAlchemy是Python社区使用最广泛的ORM之一，我们将介绍如何在Flask程序中使用它。SQL-Alchemy，直译过来就是SQL炼金术，下一节我们会见识到SQLAlchemy的神奇力量。

### 使用Flask-SQLAlchemy管理数据库

扩展Flask-SQLAlchemy集成了SQLAlchemy，它简化了连接数据库服务器、管理数据库操作会话等各类工作，让Flask中的数据处理体验变得更加轻松。
下面在示例程序中实例化Flask-SQLAlchemy提供的SQLAlchemy类，传入程序实例app，以完成扩展的初始化。

```Python
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)
```

## 第6章 电子邮件

## 总结