---
title: JavaScript 温习记录（二）
date: 2020-11-02
categories: JavaScript
tags: 
- Web
- 基础知识
---


## 写在前面的话

`JavaScript` 语言的内容，前面基本上也记录的差不多了。这里就聊一些`JavaScript`语言更深入的问题，加深对这个语言的理解。
`C` 和 `Java` 始终是 `JavaScript` 的基础，很多概念都是直接继承过来的，所以学习 `C` 是很重要的。我基本上每年都会对 `C` 有一个回顾，然后把数据结构的书再看一遍。
扯远了，这边只是记录 `JavaScript` 一些知识点，让我以后更好地上手 `JavaScript`，也是学习`React`的一个必要的过程。虽然我已经有一个上线的 `React` 项目，但是`React`的很多原理我基本上是抓瞎的。
作为一个移动端，在现在大前端的趋势下，多一个`React`的能力也挺好的。好几年前已经用`Vue`上线过一个项目了，但是那个项目比较简单，所以几年过去，我基本上忘的差不多了。

## 继承与原型链

对于使用过基于类的语言 (如 `Java` 或 `C++`) 的开发人员来说，`JavaScript` 有点令人困惑，因为它是动态的，并且本身不提供一个 class 实现。（在 ES2015/ES6 中引入了 class 关键字，但那只是语法糖，`JavaScript` 仍然是基于原型的）。

当谈到继承时，`JavaScript` 只有一种结构：对象。每个实例对象（ object ）都有一个私有属性（称之为 __proto__ ）指向它的构造函数的原型对象（**prototype**）。该原型对象也有一个自己的原型对象( __proto__ ) ，层层向上直到一个对象的原型对象为 null。根据定义，null 没有原型，并作为这个原型链中的最后一个环节。

几乎所有 `JavaScript` 中的对象都是位于原型链顶端的 `Object` 的实例。

尽管这种原型继承通常被认为是 `JavaScript` 的弱点之一，但是原型继承模型本身实际上比经典模型更强大。例如，在原型模型的基础上构建经典模型相当简单。

### 基于原型链的继承

`JavaScript` 对象是动态的属性“包”（指其自己的属性）。`JavaScript` 对象有一个指向一个原型对象的链。当试图访问一个对象的属性时，它不仅仅在该对象上搜寻，还会搜寻该对象的原型，以及该对象的原型的原型，依次层层向上搜索，直到找到一个名字匹配的属性或到达原型链的末尾。

> 遵循**ECMAScript**标准，someObject.[[`Prototype`]] 符号是用于指向 someObject 的原型。从 **ECMAScript 6** 开始，[[Prototype]] 可以通过 `Object.getPrototypeOf()` 和 `Object.setPrototypeOf()` 访问器来访问。这个等同于 `JavaScript` 的非标准但许多浏览器实现的属性 __proto__。
>
> 但它不应该与构造函数 `func` 的 `prototype` 属性相混淆。被构造函数创建的实例对象的 [[Prototype]] 指向 func 的 `prototype` 属性。`Object.prototype` 属性表示 `Object` 的原型对象。

```js
// 让我们从一个函数里创建一个对象o，它自身拥有属性a和b的：
let f = function () {
   this.a = 1;
   this.b = 2;
}
/* 这么写也一样
function f() {
  this.a = 1;
  this.b = 2;
}
*/

let o = new f(); // {a: 1, b: 2}

// 在f函数的原型上定义属性
f.prototype.b = 3;
f.prototype.c = 4;

// 不要在 f 函数的原型上直接定义 f.prototype = {b:3,c:4};这样会直接打破原型链
// o.[[Prototype]] 有属性 b 和 c
//  (其实就是 o.__proto__ 或者 o.constructor.prototype)
// o.[[Prototype]].[[Prototype]] 是 Object.prototype.
// 最后o.[[Prototype]].[[Prototype]].[[Prototype]]是null
// 这就是原型链的末尾，即 null，
// 根据定义，null 就是没有 [[Prototype]]。

// 综上，整个原型链如下:
// {a:1, b:2} ---> {b:3, c:4} ---> Object.prototype---> null

console.log(o.a); // 1
// a是o的自身属性吗？是的，该属性的值为 1

console.log(o.b); // 2
// b是o的自身属性吗？是的，该属性的值为 2
// 原型上也有一个'b'属性，但是它不会被访问到。
// 这种情况被称为"属性遮蔽 (property shadowing)"

console.log(o.c); // 4
// c是o的自身属性吗？不是，那看看它的原型上有没有
// c是o.[[Prototype]]的属性吗？是的，该属性的值为 4

console.log(o.d); // undefined
// d 是 o 的自身属性吗？不是，那看看它的原型上有没有
// d 是 o.[[Prototype]] 的属性吗？不是，那看看它的原型上有没有
// o.[[Prototype]].[[Prototype]] 为 null，停止搜索
// 找不到 d 属性，返回 undefined
```

### 在 JavaScript 中使用原型

接下去，来仔细分析一下这些应用场景下， `JavaScript` 在背后做了哪些事情。
正如之前提到的，在 `JavaScript` 中，函数（function）是允许拥有属性的。所有的函数会有一个特别的属性 —— `prototype` 。请注意，以下的代码是独立的（出于严谨，假定页面没有其他的`JavaScript`代码）。为了最佳的学习体验，我们强烈建议阁下打开浏览器的控制台（在Chrome和火狐浏览器中，按Ctrl+Shift+I即可），进入“console”选项卡，然后把如下的`JavaScript`代码复制粘贴到窗口中，最后通过按下回车键运行代码。

```js
function doSomething(){}
console.log( doSomething.prototype );
// 和声明函数的方式无关，
// JavaScript 中的函数永远有一个默认原型属性。
var doSomething = function(){};
console.log( doSomething.prototype );
```

在控制台显示的JavaScript代码块中，我们可以看到doSomething函数的一个默认属性prototype。而这段代码运行之后，控制台应该显示类似如下的结果：

```js
{
    constructor: ƒ doSomething(),
    __proto__: {
        constructor: ƒ Object(),
        hasOwnProperty: ƒ hasOwnProperty(),
        isPrototypeOf: ƒ isPrototypeOf(),
        propertyIsEnumerable: ƒ propertyIsEnumerable(),
        toLocaleString: ƒ toLocaleString(),
        toString: ƒ toString(),
        valueOf: ƒ valueOf()
    }
}

// 我们可以给doSomething函数的原型对象添加新属性
function doSomething(){}
doSomething.prototype.foo = "bar";
console.log( doSomething.prototype );

// 可以看到运行后的结果

{
    foo: "bar",
    constructor: ƒ doSomething(),
    __proto__: {
        constructor: ƒ Object(),
        hasOwnProperty: ƒ hasOwnProperty(),
        isPrototypeOf: ƒ isPrototypeOf(),
        propertyIsEnumerable: ƒ propertyIsEnumerable(),
        toLocaleString: ƒ toLocaleString(),
        toString: ƒ toString(),
        valueOf: ƒ valueOf()
    }
}
```

现在我们可以通过`new`操作符来创建基于这个原型对象的`doSomething`实例。使用`new`操作符，只需在调用`doSomething`函数语句之前添加`new`。这样，便可以获得这个函数的一个实例对象。一些属性就可以添加到该原型对象中。

```js
function doSomething(){}
doSomething.prototype.foo = "bar"; // add a property onto the prototype
var doSomeInstancing = new doSomething();
doSomeInstancing.prop = "some value"; // add a property onto the object
console.log( doSomeInstancing );

{
    prop: "some value",
    __proto__: {
        foo: "bar",
        constructor: ƒ doSomething(),
        __proto__: {
            constructor: ƒ Object(),
            hasOwnProperty: ƒ hasOwnProperty(),
            isPrototypeOf: ƒ isPrototypeOf(),
            propertyIsEnumerable: ƒ propertyIsEnumerable(),
            toLocaleString: ƒ toLocaleString(),
            toString: ƒ toString(),
            valueOf: ƒ valueOf()
        }
    }
}
```

如上所示, `doSomeInstancing` 中的`__proto__`是 `doSomething.prototype`. 但这是做什么的呢？当你访问`doSomeInstancing` 中的一个属性，浏览器首先会查看`doSomeInstancing` 中是否存在这个属性。

如果 `doSomeInstancing` 不包含属性信息, 那么浏览器会在 `doSomeInstancing` 的 `__proto__` 中进行查找(同 `doSomething.prototype`). 如属性在 `doSomeInstancing` 的 `__proto__` 中查找到，则使用 `doSomeInstancing` 中 `__proto__` 的属性。

否则，如果 `doSomeInstancing` 中 `__proto__` 不具有该属性，则检查`doSomeInstancing` 的 `__proto__` 的  `__proto__` 是否具有该属性。默认情况下，任何函数的原型属性 `__proto__` 都是 `window.Object.prototype`. 因此, 通过`doSomeInstancing` 的 `__proto__` 的  `__proto__`  ( 同 `doSomething.prototype` 的 `__proto__` (同  `Object.prototype`)) 来查找要搜索的属性。

如果属性不存在 `doSomeInstancing` 的 `__proto__` 的  `__proto__` 中， 那么就会在 `doSomeInstancing` 的 `__proto__` 的  `__proto__` 的  `__proto__` 中查找。然而, 这里存在个问题：`doSomeInstancing` 的 `__proto__` 的  `__proto__` 的  `__proto__` 其实不存在。因此，只有这样，在 `__proto__` 的整个原型链被查看之后，这里没有更多的 `__proto__` ， 浏览器断言该属性不存在，并给出属性值为 `undefined` 的结论。

### 使用不同的方法来创建对象和生成原型链

#### 使用语法结构创建的对象

```js
var o = {a: 1};

// o 这个对象继承了 Object.prototype 上面的所有属性
// o 自身没有名为 hasOwnProperty 的属性
// hasOwnProperty 是 Object.prototype 的属性
// 因此 o 继承了 Object.prototype 的 hasOwnProperty
// Object.prototype 的原型为 null
// 原型链如下:
// o ---> Object.prototype ---> null

var a = ["yo", "whadup", "?"];

// 数组都继承于 Array.prototype
// (Array.prototype 中包含 indexOf, forEach 等方法)
// 原型链如下:
// a ---> Array.prototype ---> Object.prototype ---> null
function f(){
  return 2;
}
```

#### 使用构造器创建的对象

```js
function Graph() {
  this.vertices = [];
  this.edges = [];
}

Graph.prototype = {
  addVertex: function(v){
    this.vertices.push(v);
  }
};

var g = new Graph();
// g 是生成的对象，他的自身属性有 'vertices' 和 'edges'。
// 在 g 被实例化时，g.[[Prototype]] 指向了 Graph.prototype。
```

#### 使用 Object.create 创建的对象

ECMAScript 5 中引入了一个新方法：`Object.create()`。可以调用这个方法来创建一个新对象。新对象的原型就是调用 create 方法时传入的第一个参数：

```js
var a = {a: 1};
// a ---> Object.prototype ---> null

var b = Object.create(a);
// b ---> a ---> Object.prototype ---> null
console.log(b.a); // 1 (继承而来)

var c = Object.create(b);
// c ---> b ---> a ---> Object.prototype ---> null

var d = Object.create(null);
// d ---> null
console.log(d.hasOwnProperty); // undefined, 因为d没有继承Object.prototype
```

#### 使用 class 关键字创建的对象

**ECMAScript6** 引入了一套新的关键字用来实现 class。使用基于类语言的开发人员会对这些结构感到熟悉，但它们是不同的。`JavaScript` 仍然基于原型。这些新的关键字包括 `class`, `constructor`，`static`，`extends` 和 `super`。

```js
"use strict";

class Polygon {
  constructor(height, width) {
    this.height = height;
    this.width = width;
  }
}

class Square extends Polygon {
  constructor(sideLength) {
    super(sideLength, sideLength);
  }
  get area() {
    return this.height * this.width;
  }
  set sideLength(newLength) {
    this.height = newLength;
    this.width = newLength;
  }
}

var square = new Square(2);
```

## 内存管理

像C语言这样的底层语言一般都有底层的内存管理接口，比如 `malloc()`和`free()`。相反，`JavaScript`是在创建变量（对象，字符串等）时自动进行了分配内存，并且在不使用它们时“自动”释放。 释放的过程称为垃圾回收。这个“自动”是混乱的根源，并让`JavaScript`（和其他高级语言）开发者错误的感觉他们可以不关心内存管理。

### 内存生命周期

不管什么程序语言，内存生命周期基本是一致的：

- 分配你所需要的内存
- 使用分配到的内存（读、写）
- 不需要时将其释放\归还

所有语言第二部分都是明确的。第一和第三部分在底层语言中是明确的，但在像`JavaScript`这些高级语言中，大部分都是隐含的。

#### JavaScript 的内存分配

为了不让程序员费心分配内存，`JavaScript` 在定义变量时就完成了内存分配。

```js
var n = 123; // 给数值变量分配内存
var s = "azerty"; // 给字符串分配内存

var o = {
  a: 1,
  b: null
}; // 给对象及其包含的值分配内存

// 给数组及其包含的值分配内存（就像对象一样）
var a = [1, null, "abra"];

function f(a){
  return a + 2;
} // 给函数（可调用的对象）分配内存

// 函数表达式也能分配一个对象
someElement.addEventListener('click', function(){
  someElement.style.backgroundColor = 'blue';
}, false);
```

通过函数调用分配内存

```js
var d = new Date(); // 分配一个 Date 对象

var e = document.createElement('div'); // 分配一个 DOM 元素

// 有些方法分配新变量或者新对象：
var s = "azerty";
var s2 = s.substr(0, 3); // s2 是一个新的字符串
// 因为字符串是不变量，
// JavaScript 可能决定不分配内存，
// 只是存储了 [0-3] 的范围。

var a = ["ouais ouais", "nan nan"];
var a2 = ["generation", "nan nan"];
var a3 = a.concat(a2);
// 新数组有四个元素，是 a 连接 a2 的结果
```

使用值的过程实际上是对分配内存进行读取与写入的操作。读取与写入可能是写入一个变量或者一个对象的属性值，甚至传递函数的参数。

#### 当内存不再需要使用时释放

大多数内存管理的问题都在这个阶段。在这里最艰难的任务是找到“哪些被分配的内存确实已经不再需要了”。它往往要求开发人员来确定在程序中哪一块内存不再需要并且释放它。

高级语言解释器嵌入了“垃圾回收器”，它的主要工作是跟踪内存的分配和使用，以便当分配的内存不再使用时，自动释放它。这只能是一个近似的过程，因为要知道是否仍然需要某块内存是无法判定的（无法通过某种算法解决）。

### 垃圾回收

如上文所述自动寻找是否一些内存“不再需要”的问题是无法判定的。因此，垃圾回收实现只能有限制的解决一般问题。

垃圾回收算法主要依赖于引用的概念。在内存管理的环境中，一个对象如果有访问另一个对象的权限（隐式或者显式），叫做一个对象引用另一个对象。例如，一个`Javascript`对象具有对它原型的引用（隐式引用）和对它属性的引用（显式引用）。

在这里，“对象”的概念不仅特指 `JavaScript` 对象，还包括函数作用域（或者全局词法作用域）。

这是最初级的垃圾收集算法。此算法把“对象是否不再需要”简化定义为“对象有没有其他对象引用到它”。如果没有引用指向该对象（零引用），对象将被垃圾回收机制回收。

```js
var o = {
  a: {
    b:2
  }
};
// 两个对象被创建，一个作为另一个的属性被引用，另一个被分配给变量o
// 很显然，没有一个可以被垃圾收集

var o2 = o; // o2变量是第二个对“这个对象”的引用

o = 1;      // 现在，“这个对象”只有一个o2变量的引用了，“这个对象”的原始引用o已经没有

var oa = o2.a; // 引用“这个对象”的a属性
// 现在，“这个对象”有两个引用了，一个是o2，一个是oa

o2 = "yo"; // 虽然最初的对象现在已经是零引用了，可以被垃圾回收了
// 但是它的属性a的对象还在被oa引用，所以还不能回收

oa = null; // a属性的那个对象现在也是零引用了
// 它可以被垃圾回收了
```

该算法有个限制：无法处理循环引用的事例。在下面的例子中，两个对象被创建，并互相引用，形成了一个循环。它们被调用之后会离开函数作用域，所以它们已经没有用了，可以被回收了。然而，引用计数算法考虑到它们互相都有至少一次引用，所以它们不会被回收。

```js
function f(){
  var o = {};
  var o2 = {};
  o.a = o2; // o 引用 o2
  o2.a = o; // o2 引用 o

  return "azerty";
}

f();
```

这里的内存管理讲的很一般，如果要详细的了解，还是要去看 `C` 的指针部分的内容。不过 `C` 的指针内容很复杂，需要慢慢斟酌，慢慢理解

## 函数

函数算是 `js` 里面花样最多的了，其他语言也有闭包，函数式编程，但是花样这么多，用法这么乱的挺少的。起码`Swift`的 函数真的很好用，然后对于引用对象的 拷贝也是正常的 `C` 的逻辑，`js`的我现在很难理解，也看不到底层的内存分布是怎么个逻辑。

还是先看看 函数的 教程吧

### 箭头函数

箭头函数表达式的语法比函数表达式更简洁，并且没有自己的`this`，`arguments`，`super`或`new.target`。箭头函数表达式更适用于那些本来需要匿名函数的地方，并且它不能用作构造函数。

#### 语法

基础语法

```js
(param1, param2, …, paramN) => { statements }
(param1, param2, …, paramN) => expression
//相当于：(param1, param2, …, paramN) =>{ return expression; }

// 当只有一个参数时，圆括号是可选的：
(singleParam) => { statements }
singleParam => { statements }

// 没有参数的函数应该写成一对圆括号。
() => { statements }
```

高级语法

```js
//加括号的函数体返回对象字面量表达式：
params => ({foo: bar})

//支持剩余参数和默认参数
(param1, param2, ...rest) => { statements }
(param1 = defaultValue1, param2, …, paramN = defaultValueN) => {
  statements
}

//同样支持参数列表解构
let f = ([a, b] = [1, 2], {x: c} = {x: a + b}) => a + b + c;
f();  // 6
```

#### 描述

引入箭头函数有两个方面的作用：更简短的函数并且不绑定this。

更短的函数

```js
var elements = [
  'Hydrogen',
  'Helium',
  'Lithium',
  'Beryllium'
];

elements.map(function(element) {
  return element.length;
}); // 返回数组：[8, 6, 7, 9]

// 上面的普通函数可以改写成如下的箭头函数
elements.map((element) => {
  return element.length;
}); // [8, 6, 7, 9]

// 当箭头函数只有一个参数时，可以省略参数的圆括号
elements.map(element => {
 return element.length;
}); // [8, 6, 7, 9]

// 当箭头函数的函数体只有一个 `return` 语句时，可以省略 `return` 关键字和方法体的花括号
elements.map(element => element.length); // [8, 6, 7, 9]

// 在这个例子中，因为我们只需要 `length` 属性，所以可以使用参数解构
// 需要注意的是字符串 `"length"` 是我们想要获得的属性的名称，而 `lengthFooBArX` 则只是个变量名，
// 可以替换成任意合法的变量名
elements.map(({ "length": lengthFooBArX }) => lengthFooBArX); // [8, 6, 7, 9]
```

没有单独的`this`

在箭头函数出现之前，每一个新函数根据它是被如何调用的来定义这个函数的`this`值：

- 如果是该函数是一个构造函数，this指针指向一个新的对象
- 在严格模式下的函数调用下，this指向undefined
- 如果是该函数是一个对象的方法，则它的this指针指向这个对象
- 等等

`This`被证明是令人厌烦的面向对象风格的编程。

```js
function Person() {
  // Person() 构造函数定义 `this`作为它自己的实例.
  this.age = 0;

  setInterval(function growUp() {
    // 在非严格模式, growUp()函数定义 `this`作为全局对象,
    // 与在 Person()构造函数中定义的 `this`并不相同.
    this.age++;
  }, 1000);
}

var p = new Person();

// 在ECMAScript 3/5中，通过将this值分配给封闭的变量，可以解决this问题。

function Person() {
  var that = this;
  that.age = 0;

  setInterval(function growUp() {
    // 回调引用的是`that`变量, 其值是预期的对象.
    that.age++;
  }, 1000);
}
```

箭头函数不会创建自己的`this`,它只会从自己的作用域链的上一层继承`this`。因此，在下面的代码中，传递给`setInterval`的函数内的`this`与封闭函数中的`this`值相同.
严格模式的其他规则依然不变.

```js
function Person(){
  this.age = 0;

  setInterval(() => {
    this.age++; // |this| 正确地指向 p 实例
  }, 1000);
}

var p = new Person();
```

通过 `call` 或 `apply` 调用
由于 箭头函数没有自己的`this`指针，通过 `call()` 或 `apply()` 方法调用一个函数时，只能传递参数（不能绑定this---译者注），他们的第一个参数会被忽略。（这种现象对于bind方法同样成立---译者注）

```js
var adder = {
  base : 1,
  
  add : function(a) {
    var f = v => v + this.base;
    return f(a);
  },

  addThruCall: function(a) {
    var f = v => v + this.base;
    var b = {
      base : 2
    };
    
    return f.call(b, a);
  }
};

console.log(adder.add(1));         // 输出 2
console.log(adder.addThruCall(1)); // 仍然输出 2
```

箭头函数不绑定`Arguments` 对象。因此，在本示例中，`arguments`只是引用了封闭作用域内的`arguments`：

```js
var arguments = [1, 2, 3];
var arr = () => arguments[0];

arr(); // 1

function foo(n) {
  var f = () => arguments[0] + n; // 隐式绑定 foo 函数的 arguments 对象. arguments[0] 是 n,即传给foo函数的第一个参数
  return f();
}

foo(1); // 2
foo(2); // 4
foo(3); // 6
foo(3,2);//6
foo(4);//8

// 在大多数情况下，使用剩余参数是相较使用arguments对象的更好选择。

function foo(arg) {
  var f = (...args) => args[0];
  return f(arg);
}
foo(1); // 1

function foo(arg1,arg2) {
    var f = (...args) => args[1];
    return f(arg1,arg2);
}
foo(1,2);  //2
```

## 最后

就到这里吧，js的内容看得我头疼，又很困。

## 参考文档

[JavaScript](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript)
