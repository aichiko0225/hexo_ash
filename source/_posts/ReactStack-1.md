---
title: React 技术栈（一）
date: 2021-06-19
categories: IT技术
tags: 
- React
- JavaScript
- 基础知识
---

## ECMAScript 6 简介

除开`JavaScript`的基础内容，`React` 必备的知识肯定非 ES6，其实前面的文章已经讲了一部分的ES6的内容，这边只记录，我觉得比较重要的ES6的内容
ECMAScript 6.0（以下简称 ES6）是 `JavaScript` 语言的下一代标准，已经在 2015 年 6 月正式发布了。它的目标，是使得 `JavaScript` 语言可以用来编写复杂的大型应用程序，成为企业级开发语言。

<!-- more -->

### let 和 const 命令

`let` `var`这个很简单，不需要解释了，跟现在新的语言的用法一致，`const` 就是类似 `C` 里面修饰指针，则指针不变，修饰常量则常量不可变化，没什么可说的。
`JavaScript` 以前的var就挺曹丹的，现在的用法起码像个人了。

### 箭头函数

箭头函数有几个使用注意点。

- （1）箭头函数没有自己的this对象（详见下文）。

- （2）不可以当作构造函数，也就是说，不可以对箭头函数使用new命令，否则会抛出一个错误。

- （3）不可以使用arguments对象，该对象在函数体内不存在。如果要用，可以用 rest 参数代替。

- （4）不可以使用yield命令，因此箭头函数不能用作 Generator 函数。

上面四点中，最重要的是第一点。对于普通函数来说，内部的this指向函数运行时所在的对象，但是这一点对箭头函数不成立。它没有自己的this对象，内部的this就是定义时上层作用域中的this。
也就是说，箭头函数内部的this指向是固定的，相比之下，普通函数的this指向是可变的。

```js
function foo() {
  setTimeout(() => {
    console.log('id:', this.id);
  }, 100);
}

var id = 21;

foo.call({ id: 42 });
// id: 42
```

上面代码中，setTimeout()的参数是一个箭头函数，这个箭头函数的定义生效是在foo函数生成时，而它的真正执行要等到 100 毫秒后。
如果是普通函数，执行时this应该指向全局对象window，这时应该输出21。但是，箭头函数导致this总是指向函数定义生效时所在的对象（本例是{id: 42}），所以打印出来的是42。

箭头函数的什么教程一大堆，在我看来都是为了之前的设计买单而已，如果真的是像写Java 一样写，this的指向不会出现任何问题，普通函数的this 是不确定的，那么使用普通函数的时候bind一个this就完全可以解决了。

`JavaScript` 是一个很让人头疼的语言，有些人总是摸着规则的边缘写代码，然后减少了几行代码，以为有多厉害。我只想说，并不是人家看不懂就厉害的，那些白痴们。
如果只学习`JavaScript`一种语言，那他的代码肯定是乱七八糟的。所以我每年基本上都会复习一下C的知识，还是很有用的，了解程序运行的底层逻辑，才能更好地写代码。

### 对象的扩展

对象（object）是 JavaScript 最重要的数据结构。ES6 对它进行了重大升级，本章介绍数据结构本身的改变，下一章介绍`Object`对象的新增方法。

#### 属性的赋值器（setter）和取值器（getter）

```js
const cart = {
  _wheels: 4,

  get wheels () {
    return this._wheels;
  },

  set wheels (value) {
    if (value < this._wheels) {
      throw new Error('数值太小了！');
    }
    this._wheels = value;
  }
}
```

#### super 关键字

我们知道，this关键字总是指向函数所在的当前对象，ES6 又新增了另一个类似的关键字super，指向当前对象的原型对象。

```js
const proto = {
  foo: 'hello'
};

const obj = {
  foo: 'world',
  find() {
    return super.foo;
  }
};

Object.setPrototypeOf(obj, proto);
obj.find() // "hello"
```

上面代码中，对象obj.find()方法之中，通过super.foo引用了原型对象proto的foo属性。

注意，super关键字表示原型对象时，只能用在对象的方法之中，用在其他地方都会报错。

```js
// 报错
const obj = {
  foo: super.foo
}

// 报错
const obj = {
  foo: () => super.foo
}

// 报错
const obj = {
  foo: function () {
    return super.foo
  }
}
```

上面三种`super`的用法都会报错，因为对于 `JavaScript` 引擎来说，这里的`super`都没有用在对象的方法之中。第一种写法是`super`用在属性里面，第二种和第三种写法是`super`用在一个函数里面，然后赋值给foo属性。目前，只有对象方法的简写法可以让 `JavaScript` 引擎确认，定义的是对象的方法。

`JavaScript` 引擎内部，`super.foo`等同于`Object.getPrototypeOf(this).foo`（属性）或`Object.getPrototypeOf(this).foo.call(this)`（方法）。

```js
const proto = {
  x: 'hello',
  foo() {
    console.log(this.x);
  },
};

const obj = {
  x: 'world',
  foo() {
    super.foo();
  }
}

Object.setPrototypeOf(obj, proto);

obj.foo() // "world"
```

上面代码中，super.foo指向原型对象proto的foo方法，但是绑定的this却还是当前对象obj，因此输出的就是world。

 