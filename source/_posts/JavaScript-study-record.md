---
title: JavaScript 温习记录（一）
date: 2020-10-30
categories: JavaScript
tags: 
- Web
- 基础知识
---

## 写在前面的话

最近用react-native 完成了一个公司的项目，JavaScript 其实已经看过很多遍了，上个月就看了一遍全部的教程，但是没有系统的记录，以及一些比较麻烦的地方。
有一些三方的源码还是看的不太懂，而且js的坑不算少，我希望能够记录一下，下次能够快速定位问题。
（起码我可以看得懂三方的源代码o(╯□╰)o）

## 让我们愉快的开始吧

JavaScript ( JS ) 是一种具有函数优先的轻量级，解释型或即时编译型的编程语言。虽然它是作为开发Web 页面的脚本语言而出名的，但是它也被用到了很多非浏览器环境中，例如 Node.js、 Apache CouchDB 和 Adobe Acrobat。JavaScript 是一种基于原型编程、多范式的动态脚本语言，并且支持面向对象、命令式和声明式（如函数式编程）风格。了解更多 JavaScript。

一些基础的知识这里就不说了，主要是一些值得注意的。

### Promises

从 ECMAScript 6 开始，JavaScript 增加了对 Promise 对象的支持，它允许你对延时和异步操作流进行控制。
Promise 对象有以下几种状态：

- pending：初始的状态，即正在执行，不处于 fulfilled 或 rejected 状态。
- fulfilled：成功的完成了操作。
- rejected：失败，没有完成操作。
- settled：Promise 处于 fulfilled 或 rejected 二者中的任意一个状态, 不会是 pending。

通过 XHR 加载图片
你可以在 MDN GitHub promise-test 中找到这个简单的例子，它使用了 Promise 和 XMLHttpRequest 来加载一张图片，你也可以直接在这个页面查看他的效果。同时为了让你更清楚的了解 Promise 和 XHR 的结构，代码中每一个步骤后都附带了注释。

这里有一个未注释的版本，展现了 Promise 的工作流，希望可以对你的理解有所帮助。

```js
function imgLoad(url) {
  return new Promise(function(resolve, reject) {
    var request = new XMLHttpRequest();
    request.open('GET', url);
    request.responseType = 'blob';
    request.onload = function() {
      if (request.status === 200) {
        resolve(request.response);
      } else {
        reject(Error('Image didn\'t load successfully; error code:' 
                     + request.statusText));
      }
    };
    request.onerror = function() {
      reject(Error('There was a network error.'));
    };
    request.send();
  });
}
```

**Promise** 这里只是简单介绍，后面会用单独的部分来讲解的

### 函数

函数是 JavaScript 中的基本组件之一。 一个函数是 JavaScript 过程 — 一组执行任务或计算值的语句。要使用一个函数，你必须将其定义在你希望调用它的作用域内。

一个JavaScript 函数用function关键字定义，后面跟着函数名和圆括号。

函数很重要，函数作用域很重要，最关键的是js的作用域有很多奇葩的地方

在函数内定义的变量不能在函数之外的任何地方访问，因为变量仅仅在该函数的域的内部有定义。相对应的，一个函数可以访问定义在其范围内的任何变量和函数。换言之，定义在全局域中的函数可以访问所有定义在全局域中的变量。在另一个函数中定义的函数也可以访问在其父函数中定义的所有变量和父函数有权访问的任何其他变量。

```js
// 下面的变量定义在全局作用域(global scope)中
var num1 = 20,
    num2 = 3,
    name = "Chamahk";

// 本函数定义在全局作用域
function multiply() {
    return num1 * num3;
}

function change() {
    num1 = 40;
    num2 = 3;
}

function multiplyWithNumber(num1: number, num2: number) {
    const num = num1 * num2;
    return num;
}

multiply(); // 返回 60

multiplyWithNumber(num1, num2)

change();

multiply(); // 返回 ??? 120

var c = {
  num: 10
}

var d = {}

var a = {
  init(num, obj) {
    this.num = num
    this.obj = obj
  }
}

a.init(c.num, d)
c.num = 20
d = { aaaa: 1 }

var b = {
  num: a.num,

  change: function() {
    num = 20
  }
}

b.change()

a.num
b.num

```

#### 嵌套函数和闭包

你可以在一个函数里面嵌套另外一个函数。嵌套（内部）函数对其容器（外部）函数是私有的。它自身也形成了一个闭包。一个闭包是一个可以自己拥有独立的环境与变量的表达式（通常是函数）。

既然嵌套函数是一个闭包，就意味着一个嵌套函数可以”继承“容器函数的参数和变量。换句话说，内部函数包含外部函数的作用域。

```js
function outside(x) {
  function inside(y) {
    return x + y;
  }
  return inside;
}
fn_inside = outside(3); // 可以这样想：给一个函数，使它的值加3
result = fn_inside(5); // returns 8

result1 = outside(3)(5); // returns 8
```

闭包是 JavaScript 中最强大的特性之一。JavaScript 允许函数嵌套，并且内部函数可以访问定义在外部函数中的所有变量和函数，以及外部函数能访问的所有变量和函数。
但是，外部函数却不能够访问定义在内部函数中的变量和函数。这给内部函数的变量提供了一定的安全性。

此外，由于内部函数可以访问外部函数的作用域，因此当内部函数生存周期大于外部函数时，外部函数中定义的变量和函数的生存周期将比内部函数执行时间长。当内部函数以某一种方式被任何一个外部函数作用域访问时，一个闭包就产生了。

#### 函数参数

从ECMAScript 6开始，有两个新的类型的参数：默认参数，剩余参数。
在JavaScript中，函数参数的默认值是undefined。然而，在某些情况下设置不同的默认值是有用的。这时默认参数可以提供帮助。

剩余参数语法允许将不确定数量的参数表示为数组。在下面的例子中，使用剩余参数收集从第二个到最后参数。然后，我们将这个数组的每一个数与第一个参数相乘。这个例子是使用了一个箭头函数，这将在下面介绍。

```js
function multiply(multiplier, ...theArgs) {
  return theArgs.map(x => multiplier * x);
}

var arr = multiply(2, 1, 2, 3);
console.log(arr); // [2, 4, 6]
```

#### 箭头函数

箭头函数表达式（也称胖箭头函数）相比函数表达式具有较短的语法并以词法的方式绑定 this。箭头函数总是匿名的。另见 hacks.mozilla.org 的博文：[“深度了解ES6：箭头函数”](https://hacks.mozilla.org/2015/06/es6-in-depth-arrow-functions/)。

有两个因素会影响引入箭头函数：更简洁的函数和 this。

### 数字和日期

#### 数字

在 JavaScript 里面，数字均为双精度浮点类型（double-precision 64-bit binary format IEEE 754），即一个介于±2−1023和±2+1024之间的数字，或约为±10−308到±10+308，数字精度为53位。整数数值仅在±(253 - 1)的范围内可以表示准确。

JavaScript最近添加了 BigInt 的支持，能够用于表示极大的数字。使用 BigInt 的时候有一些注意事项，例如，你不能让 BigInt 和 Number 直接进行运算，你也不能用 Math 对象去操作 BigInt 数字。

请参见Javascript指南中的 [JavaScript 数据类型和数据结构](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Data_structures) ，了解其他更多的基本类型。

#### 日期对象

JavaScript没有日期数据类型。但是你可以在你的程序里使用 Date 对象和其方法来处理日期和时间。Date对象有大量的设置、获取和操作日期的方法。 它并不含有任何属性。
JavaScript 处理日期数据类似于Java。这两种语言有许多一样的处理日期的方法，也都是以1970年1月1日00:00:00以来的毫秒数来储存数据类型的。

处理日期时间的Date对象方法可分为以下几类：

- "set" 方法, 用于设置Date对象的日期和时间的值。
- "get" 方法,用于获取Date对象的日期和时间的值。
- "to" 方法,用于返回Date对象的字符串格式的值。
- parse 和UTC 方法, 用于解析Date字符串。

### 正则表达式

正则表达式是用于匹配字符串中字符组合的模式。在 JavaScript中，正则表达式也是对象。这些模式被用于 RegExp 的 exec 和 test 方法, 以及 String 的 match、matchAll、replace、search 和 split 方法。本章介绍 JavaScript 正则表达式。

| 字符 | 含义 |
| :----: | :---- |
| \\ | 依照下列规则匹配：</br>在非特殊字符之前的反斜杠表示下一个字符是特殊字符，不能按照字面理解。例如，前面没有 "\" 的 "b" 通常匹配小写字母 "b"，即字符会被作为字面理解，无论它出现在哪里。但如果前面加了 "\"，它将不再匹配任何字符，而是表示一个字符边界。</br>在特殊字符之前的反斜杠表示下一个字符不是特殊字符，应该按照字面理解。详情请参阅下文中的 "转义（Escaping）" 部分。</br>如果你想将字符串传递给 RegExp 构造函数，不要忘记在字符串字面量中反斜杠是转义字符。所以为了在模式中添加一个反斜杠，你需要在字符串字面量中转义它。/[a-z]\s/i 和 new RegExp("[a-z]\\s", "i") 创建了相同的正则表达式：一个用于搜索后面紧跟着空白字符（\s 可看后文）并且在 a-z 范围内的任意字符的表达式。为了通过字符串字面量给 RegExp 构造函数创建包含反斜杠的表达式，你需要在字符串级别和正则表达式级别都对它进行转义。例如 /[a-z]:\\/i 和 new RegExp("[a-z]:\\\\","i") 会创建相同的表达式，即匹配类似 "C:\" 字符串。 |
| ^ | 匹配输入的开始 |
| $ | 匹配输入的结束 |
| * | 匹配前一个表达式 0 次或多次。等价于 {0,} |
| + | 匹配前面一个表达式 1 次或者多次。等价于 {1,} |
| ? | 匹配前面一个表达式 0 次或者 1 次。等价于 {0,1}。 |
| . | （小数点）默认匹配除换行符之外的任何单个字符。 |
| x\|y | 匹配‘x’或者‘y’。</br> 例如, /a{2,}/ 匹配 "aa", "aaaa" 和 "aaaaa" 但是不匹配 "a"。 |
| (x) | 像下面的例子展示的那样，它会匹配 'x' 并且记住匹配项。其中括号被称为捕获括号。|
| (?:x) | 匹配 'x' 但是不记住匹配项。这种括号叫作非捕获括号，使得你能够定义与正则表达式运算符一起使用的子表达式。 |
| x(?=y) | 匹配'x'仅仅当'x'后面跟着'y'.这种叫做先行断言。 |
| (?<=y)x | 匹配'x'仅当'x'前面是'y'.这种叫做后行断言。 |
| x(?!y) | 仅仅当'x'后面不跟着'y'时匹配'x'，这被称为正向否定查找。 |
| (?<!y)x | 仅仅当'x'前面不是'y'时匹配'x'，这被称为反向否定查找。 |
| {n} | n 是一个正整数，匹配了前面一个字符刚好出现了 n 次。</br>比如， /a{2}/ 不会匹配“candy”中的'a',但是会匹配“caandy”中所有的 a，以及“caaandy”中的前两个'a'。 |
| {n,} | n是一个正整数，匹配前一个字符至少出现了n次。</br>例如, /a{2,}/ 匹配 "aa", "aaaa" 和 "aaaaa" 但是不匹配 "a"。 |
| {n,m} | n 和 m 都是整数。匹配前面的字符至少n次，最多m次。如果 n 或者 m 的值是0， 这个值被忽略。</br>例如，/a{1, 3}/ 并不匹配“cndy”中的任意字符，匹配“candy”中的a，匹配“caandy”中的前两个a，也匹配“caaaaaaandy”中的前三个a。注意，当匹配”caaaaaaandy“时，匹配的值是“aaa”，即使原始的字符串中有更多的a。 |
| [xyz] | 一个字符集合。匹配方括号中的任意字符，包括转义序列。你可以使用破折号（-）来指定一个字符范围。对于点（.）和星号（*）这样的特殊符号在一个字符集中没有特殊的意义。他们不必进行转义，不过转义也是起作用的。</br>例如，[abcd] 和[a-d]是一样的。他们都匹配"brisket"中的‘b’,也都匹配“city”中的‘c’。/[a-z.]+/ 和/[\w.]+/与字符串“test.i.ng”匹配。 |
| [^xyz] | 一个反向字符集。也就是说， 它匹配任何没有包含在方括号中的字符。你可以使用破折号（-）来指定一个字符范围。任何普通字符在这里都是起作用的。|
| [\b] | 匹配一个退格(U+0008)。（不要和\b混淆了。） |
| \\b | 匹配一个词的边界。一个词的边界就是一个词不被另外一个“字”字符跟随的位置或者前面跟其他“字”字符的位置，例如在字母和空格之间。注意，匹配中不包括匹配的字边界。换句话说，一个匹配的词的边界的内容的长度是0。（不要和[\b]混淆了）</br>使用"moon"举例：</br>/\bm/匹配“moon”中的‘m’；</br>/oo\b/并不匹配"moon"中的'oo'，因为'oo'被一个“字”字符'n'紧跟着。</br>/oon\b/匹配"moon"中的'oon'，因为'oon'是这个字符串的结束部分。这样他没有被一个“字”字符紧跟着。 |
| \\B | 匹配一个非单词边界。 |
| \\d | 匹配一个数字。等价于[0-9]。</br>例如， /\d/ 或者 /[0-9]/ 匹配"B2 is the suite number."中的'2'。 |
| \\D | 匹配一个非数字字符。等价于[^0-9]。 |
| \\f | 匹配一个换页符 (U+000C)。|
| \\n | 匹配一个换行符 (U+000A)。|
| \\r | 匹配一个回车符 (U+000D)。|
| \\s | 匹配一个空白字符，包括空格、制表符、换页符和换行符。|
| \\S | 匹配一个非空白字符。|
| \\t | 匹配一个水平制表符 (U+0009)。|
| \\v | 匹配一个垂直制表符 (U+000B)。|
| \\w | 匹配一个单字字符（字母、数字或者下划线）。等价于 [A-Za-z0-9_]。</br>例如, /\w/ 匹配 "apple," 中的 'a'，"$5.28,"中的 '5' 和 "3D." 中的 '3'。|
| \\W | 匹配一个非单字字符。等价于 [^A-Za-z0-9_]。</br>例如, /\W/ 或者 /[^A-Za-z0-9_]/ 匹配 "50%." 中的 '%'。|
| \\n | 在正则表达式中，它返回最后的第n个子捕获匹配的子字符串(捕获的数目以左括号计数)。</br>比如 /apple(,)\sorange\1/ 匹配"apple, orange, cherry, peach."中的'apple, orange,' 。|
| \\0 | 匹配 NULL（U+0000）字符， 不要在这后面跟其它小数，因为 \0<digits> 是一个八进制转义序列。|
| \\xhh | 匹配一个两位十六进制数（\x00-\xFF）表示的字符。|
| \uhhhh |匹配一个四位十六进制数表示的 UTF-16 代码单元。|
| \u{hhhh}或\u{hhhhh} |（仅当设置了u标志时）匹配一个十六进制数表示的 Unicode 字符。|

### 数组对象(Array object)

数组(`array`)是一个有序的数据集合，我们可以通过数组名称(name)和索引(index)进行访问。例如，我们定义了一个数组emp，数组中的每个元素包含了一个雇员的名字以及其作为索引的员工号。那么emp[1]将会代表1号员工，emp[2]将会代表2号员工，以此类推。

JavaScript中没有明确的数组数据类型。但是，我们可以通过使用内置Array对象和它的方法对数组进行操作。Array对象有很多操作数组的方法，比如合并、反转、排序等。数组对象有一个决定数组长度和使用正则表达式操作其他属性的属性。

```js
var arr = new Array(element0, element1, ..., elementN);
var arr = Array(element0, element1, ..., elementN);
var arr = [element0, element1, ..., elementN];

// 译者注: var arr=[4] 和 var arr=new Array(4)是不等效的，
// 后者4指数组长度，所以使用字面值(literal)的方式应该不仅仅是便捷，同时也不易踩坑

var arr = new Array(arrayLength);
var arr = Array(arrayLength);

// 这样有同样的效果
var arr = [];
arr.length = arrayLength;
```

#### 数组的方法(array methods)

Array 对象具有下列方法：
concat() 连接两个数组并返回一个新的数组。

```js
var myArray = new Array("1", "2", "3");
myArray = myArray.concat("a", "b", "c"); 
// myArray is now ["1", "2", "3", "a", "b", "c"]
```

join(deliminator = ',') 将数组的所有元素连接成一个字符串。

```js
var myArray = new Array("Wind", "Rain", "Fire");
var list = myArray.join(" - "); // list is "Wind - Rain - Fire"
```

push() 在数组末尾添加一个或多个元素，并返回数组操作后的长度。

```js
var myArray = new Array("1", "2");
myArray.push("3"); // myArray is now ["1", "2", "3"]
```

pop() 从数组移出最后一个元素，并返回该元素。

```js
var myArray = new Array("1", "2", "3");
var last = myArray.pop();
// myArray is now ["1", "2"], last = "3"
```

shift() 从数组移出第一个元素，并返回该元素。

```js
var myArray = new Array ("1", "2", "3");
var first = myArray.shift(); 
// myArray is now ["2", "3"], first is "1"
```

unshift() 在数组开头添加一个或多个元素，并返回数组的新长度。

```js
var myArray = new Array ("1", "2", "3");
myArray.unshift("4", "5"); 
// myArray becomes ["4", "5", "1", "2", "3"]
```

其他的就不一一介绍了

#### 类型化数组(Typed Arrays )

JavaScript typed arrays 是类数组对象（array-like object），其提供访问原始二进制数据的机制。 就像你知道的那样, Array 对象动态增长和收缩，可以有任何JavaScript值。但对于类型化数组，JavaScript引擎执行优化使得这些数组访问速度快速。 随着Web应用程序变得越来越强大，添加音频和视频处理等功能、可以使用 WebSockets 、使用原始数据， 这都需要访问原始的二进制数据，所以专门的优化将有助于JavaScript代码能够快速和容易地操纵原始二进制数据类型的数组。

### 映射

#### Map对象

ECMAScript 2015 引入了一个新的数据结构来将一个值映射到另一个值。一个Map对象就是一个简单的键值对映射集合，可以按照数据插入时的顺序遍历所有的元素。

#### Object和Map的比较

一般地，objects会被用于将字符串类型映射到数值。Object允许设置键值对、根据键获取值、删除键、检测某个键是否存在。而Map具有更多的优势。

`Object`的键均为`Strings`类型，在`Map`里键可以是任意类型。
必须手动计算`Object`的尺寸，但是可以很容易地获取使用Map的尺寸。
`Map`的遍历遵循元素的插入顺序。
`Object`有原型，所以映射中有一些缺省的键。（可以用 `map = Object.create(null)` 回避）。

这三条提示可以帮你决定用`Map`还是`Object`：

如果键在运行时才能知道，或者所有的键类型相同，所有的值类型相同，那就使用`Map`。
如果需要将原始值存储为键，则使用`Map`，因为`Object`将每个键视为字符串，不管它是一个数字值、布尔值还是任何其他原始值。
如果需要对个别元素进行操作，使用`Object`。

#### WeakMap对象

WeakMap对象也是键值对的集合。它的键必须是对象类型，值可以是任意类型。它的键被弱保持，也就是说，当其键所指对象没有其他地方引用的时候，它会被GC回收掉。WeakMap提供的接口与Map相同。

与Map对象不同的是，WeakMap的键是不可枚举的。不提供列出其键的方法。列表是否存在取决于垃圾回收器的状态，是不可预知的。

### 对象（Object）

javascript 中的对象(物体)，和其它编程语言中的对象一样，可以比照现实生活中的对象(物体)来理解它。 javascript 中对象(物体)的概念可以比照着现实生活中实实在在的物体来理解。

在javascript中，一个对象可以是一个单独的拥有属性和类型的实体。我们拿它和一个杯子做下类比。一个杯子是一个对象(物体)，拥有属性。杯子有颜色，图案，重量，由什么材质构成等等。同样，javascript对象也有属性来定义它的特征。

#### 创建新对象

JavaScript 拥有一系列预定义的对象。另外，你可以创建你自己的对象。从  JavaScript 1.2 之后，你可以通过对象初始化器（Object Initializer）创建对象。或者你可以创建一个构造函数并使用该函数和 new 操作符初始化对象。

### Promise

`Promise` 是一个对象，它代表了一个异步操作的最终完成或者失败。因为大多数人仅仅是使用已创建的 `Promise` 实例对象，所以本教程将首先说明怎样使用 `Promise`，再说明如何创建 `Promise`。

本质上 `Promise` 是一个函数返回的对象，我们可以在它上面绑定回调函数，这样我们就不需要在一开始把回调函数作为参数传入这个函数了。

假设现在有一个名为 `createAudioFileAsync()` 的函数，它接收一些配置和两个回调函数，然后异步地生成音频文件。一个回调函数在文件成功创建时被调用，另一个则在出现异常时被调用。

#### 链式调用

连续执行两个或者多个异步操作是一个常见的需求，在上一个操作执行成功之后，开始下一个的操作，并带着上一步操作所返回的结果。我们可以通过创造一个 Promise 链来实现这种需求。

```js
doSomething().then(function(result) {
  return doSomethingElse(result);
})
.then(function(newResult) {
  return doThirdThing(newResult);
})
.then(function(finalResult) {
  console.log('Got the final result: ' + finalResult);
})
.catch(failureCallback);

// 我们也可以用箭头函数来表示
doSomething()
.then(result => doSomethingElse(result))
.then(newResult => doThirdThing(newResult))
.then(finalResult => {
  console.log(`Got the final result: ${finalResult}`);
})
.catch(failureCallback);

```

#### 错误传递

在之前的回调地狱示例中，你可能记得有 3 次 failureCallback 的调用，而在 Promise 链中只有尾部的一次调用。
通常，一遇到异常抛出，浏览器就会顺着 Promise 链寻找下一个 onRejected 失败回调函数或者由 .catch() 指定的回调函数。这和以下同步代码的工作原理（执行过程）非常相似。

```js
try {
  let result = syncDoSomething();
  let newResult = syncDoSomethingElse(result);
  let finalResult = syncDoThirdThing(newResult);
  console.log(`Got the final result: ${finalResult}`);
} catch(error) {
  failureCallback(error);
}

// 在 ECMAScript 2017 标准的 async/await 语法糖中，这种异步代码的对称性得到了极致的体现：

async function foo() {
  try {
    const result = await doSomething();
    const newResult = await doSomethingElse(result);
    const finalResult = await doThirdThing(newResult);
    console.log(`Got the final result: ${finalResult}`);
  } catch(error) {
    failureCallback(error);
  }
}
```

#### Promise 拒绝事件

当 Promise 被拒绝时，会有下文所述的两个事件之一被派发到全局作用域（通常而言，就是window；如果是在 web worker 中使用的话，就是 Worker 或者其他 worker-based 接口）。这两个事件如下所示：

- rejectionhandled
    当 Promise 被拒绝、并且在 reject 函数处理该 rejection 之后会派发此事件。
- unhandledrejection
    当 Promise 被拒绝，但没有提供 reject 函数来处理该 rejection 时，会派发此事件。

以上两种情况中，`PromiseRejectionEvent` 事件都有两个属性，一个是 `promise` 属性，该属性指向被驳回的 `Promise`，另一个是 `reason` 属性，该属性用来说明 `Promise` 被驳回的原因。

### 元编程

从ECMAScript 2015 开始，JavaScript 获得了 Proxy 和 Reflect 对象的支持，允许你拦截并定义基本语言操作的自定义行为（例如，属性查找，赋值，枚举，函数调用等）。借助这两个对象，你可以在 JavaScript 元级别进行编程。

#### 代理

在 ECMAScript 6 中引入的 Proxy 对象可以拦截某些操作并实现自定义行为。

```js
let handler = {
  get: function(target, name){
    return name in target ? target[name] : 42;
  }
};

let p = new Proxy({}, handler);
p.a = 1;

console.log(p.a, p.b); // 1, 42
```

Proxy 对象定义了一个目标（这里是一个空对象）和一个实现了 get 陷阱的 handler 对象。这里，代理的对象在获取未定义的属性时不会返回 undefined，而是返回 42。

#### 反射

Reflect 是一个内置对象，它提供了可拦截 JavaScript 操作的方法。该方法和代理句柄类似，但 Reflect 方法并不是一个函数对象。

## 客户端 Web API

当你给网页或者网页应用编写客户端的JavaScript时， 你很快会遇上应用程序接口（API ）—— 这些编程特性可用来操控网站所基于的浏览器与操作系统的不同方面，或是操控由其他网站或服务端传来的数据。在这个单元里，我们将一同探索什么是API，以及如何使用一些在你开发中将经常遇见的API。

- Web API简介
  首先, 我们将从一个更高的角度来看这些API —它们是什么，它们怎么起作用的，你该怎么在自己的代码中使用它们以及他们是怎么构成的？ 我们依旧会再来看一看这些API有哪些主要的种类和他们会有哪些用处。
- 操作文档
  当你在制作WEB页面和APP时,一个你最经常想要做的事就是通过一些方法来操作WEB文档。这其中最常见的方法就是使用文档对象模型Document Object Model (DOM)，它是一系列大量使用了 Document object的API来控制HTML和样式信息。通过这篇文章，我们来看看使用DOM方面的一些细节， 以及其他一些有趣的API能够通过一些有趣的方式改变你的环境。
- 从服务器获取数据
  在现代网页及其APP中另外一个很常见的任务就是与服务器进行数据交互时不再刷新整个页面，这看起来微不足道，但却对一个网页的展现和交互上起到了很大的作用，在这篇文章里，我们将阐述这个概念，然后来了解实现这个功能的技术，例如 XMLHttpRequest 和 Fetch API.（抓取API）。
- 第三方 API
  到目前为止我们所涉及的API都是浏览器内置的，但并不代表所有。许多大网站如Google Maps, Twitter, Facebook, PayPal等，都提供他们的API给开发者们去使用他们的数据（比如在你的博客里展示你分享的推特内容）或者服务（如在你的网页里展示定制的谷歌地图或接入Facebook登录功能）。这篇文章介绍了浏览器API和第三方API 的差别以及一些最新的典型应用。
- 绘制图形
  浏览器包含多种强大的图形编程工具，从可缩放矢量图形语言Scalable Vector Graphics (SVG) language，到HTML绘制元素` <canvas> `元素(The Canvas API and WebGL). 这篇文章提供了部分canvas的简介，以及让你更深入学习的资源。
- 视频和音频 API
  HTML5能够通过元素标签嵌入富媒体——`<video> and <audio>`——而将有自己的API来控制回放，搜索等功能。本文向您展示了如何创建自定义播放控制等常见的任务。
- 客户端存储
  现代web浏览器拥有很多不同的技术，能够让你存储与网站相关的数据，并在需要时调用它们，能够让你长期保存数据、保存离线网站及其他实现其他功能。本文解释了这些功能的基本原理。

详细的内容以后在慢慢补充吧，这种 api 对于我来说没多大作用，我还是主要在语言方面多了解一些。

## 重新介绍 JavaScript（JS 教程）

为什么会有这一篇“重新介绍”呢？因为 `JavaScript` 堪称世界上被人误解最深的编程语言。虽然常被嘲为“玩具语言”，但在它看似简洁的外衣下，还隐藏着强大的语言特性。 `JavaScript` 目前广泛应用于众多知名应用中，对于网页和移动开发者来说，深入理解 `JavaScript` 就尤为必要。

我们有必要先从这门语言的历史谈起。在1995 年 Netscape 一位名为 Brendan Eich 的工程师创造了 `JavaScript`，随后在 1996 年初，`JavaScript` 首先被应用于 Netscape 2 浏览器上。最初的 `JavaScript` 名为 LiveScript，但是因为一个糟糕的营销策略而被重新命名，该策略企图利用Sun Microsystem的Java语言的流行性，将它的名字从最初的 LiveScript 更改为 `JavaScript`——尽管两者之间并没有什么共同点。这便是之后混淆产生的根源。

几个月后，Microsoft 随 IE 3 发布推出了一个与之基本兼容的语言 JScript。又过了几个月，Netscape 将 `JavaScript` 提交至 Ecma International（一个欧洲标准化组织）， ECMAScript 标准第一版便在 1997 年诞生了，随后在 1999 年以 ECMAScript 第三版的形式进行了更新，从那之后这个标准没有发生过大的改动。由于委员会在语言特性的讨论上发生分歧，ECMAScript 第四版尚未推出便被废除，但随后于 2009 年 12 月发布的 ECMAScript 第五版引入了第四版草案加入的许多特性。第六版标准已经于 2015 年 6 月发布。

与大多数编程语言不同，`JavaScript` 没有输入或输出的概念。它是一个在宿主环境（host environment）下运行的脚本语言，任何与外界沟通的机制都是由宿主环境提供的。浏览器是最常见的宿主环境，但在非常多的其他程序中也包含 `JavaScript` 解释器，如 Adobe Acrobat、Adobe Photoshop、SVG 图像、Yahoo! 的 Widget 引擎，Node.js 之类的服务器端环境，NoSQL 数据库（如开源的 Apache CouchDB）、嵌入式计算机，以及包括 GNOME （注：GNU/Linux 上最流行的 GUI 之一）在内的桌面环境等等。

### 概览

`JavaScript` 是一种多范式的动态语言，它包含类型、运算符、标准内置（ built-in）对象和方法。它的语法来源于 `Java` 和 `C`，所以这两种语言的许多语法特性同样适用于 `JavaScript`。`JavaScript` 通过原型链而不是类来支持面向对象编程（有关 ES6 类的内容参考这里Classes，有关对象原型参考见此继承与原型链）。`JavaScript`同样支持函数式编程——因为它们也是对象，函数也可以被保存在变量中，并且像其他对象一样被传递。

先从任何编程语言都不可缺少的组成部分——“类型”开始。`JavaScript` 程序可以修改值（value），这些值都有各自的类型。`JavaScript` 中的类型包括：

- `Number`（数字）
- `String`（字符串）
- `Boolean`（布尔）
- `Function`（函数）
- `Object`（对象）
- `Symbol`（ES2015 新增）

还有看上去有些…奇怪的 `undefined`（未定义）类型和 `null`（空）类型。此外还有`Array`（数组）类型，以及分别用于表示日期和正则表达式的 `Date`（日期）和 `RegExp`（正则表达式），这三种类型都是特殊的对象。严格意义上说，`Function`（函数）也是一种特殊的对象。所以准确来说，`JavaScript` 中的类型应该包括这些：

- `Number`（数字）
- `String`（字符串）
- `Boolean`（布尔）
- `Symbol`（符号）（ES2015 新增）
- `Object`（对象）
  - `Function`（函数）
  - `Array`（数组）
  - `Date`（日期）
  - `RegExp`（正则表达式）
- `null`（空）
- `undefined`（未定义）

`JavaScript` 还有一种内置的 `Error`（错误）类型。但是，如果我们继续使用上面的分类，事情便容易得多；所以，现在，我们先讨论上面这些类型。

### 数字

根据语言规范，`JavaScript` 采用“遵循 IEEE 754 标准的双精度 64 位格式”（"double-precision 64-bit format IEEE 754 values"）表示数字。——在`JavaScript`（除了BigInt）当中，并不存在整数/整型(`Integer`)。

```js
console.log(3 / 2);             // 1.5,not 1
console.log(Math.floor(3 / 2)); // 1

// 你可以使用内置函数 parseInt() 将字符串转换为整型。

parseInt("123", 10); // 123
parseInt("010", 10); // 10

// 一些老版本的浏览器会将首字符为“0”的字符串当做八进制数字，2013 年以前的 JavaScript 实现

parseInt("010");  //  8
parseInt("0x10"); // 16

// 这是因为字符串以数字 0 开头，parseInt()函数会把这样的字符串视作八进制数字；
// 同理，0x开头的字符串则视为十六进制数字。
```

`JavaScript` 还有两个特殊值：`Infinity`（正无穷）和 -`Infinity`（负无穷）：
可以使用内置函数 `isFinite()` 来判断一个变量是否是一个有穷数， 如果类型为`Infinity`, -`Infinity` 或 `NaN`则返回`false`：

```js
1 / 0; //  Infinity
-1 / 0; // -Infinity

isFinite(1/0); // false
isFinite(Infinity); // false
isFinite(-Infinity); // false
isFinite(NaN); // false

isFinite(0); // true
isFinite(2e64); // true

isFinite("0"); // true
// 如果是纯数值类型的检测，则返回 false：
Number.isFinite("0"); // false
```

### 字符串

`JavaScript` 中的字符串是一串`Unicode` 字符序列。这对于那些需要和多语种网页打交道的开发者来说是个好消息。更准确地说，它们是一串`UTF-16`编码单元的序列，每一个编码单元由一个 16 位二进制数表示。每一个`Unicode`字符由一个或两个编码单元来表示。

### 其他类型

与其他类型不同，`JavaScript` 中的 `null` 表示一个空值（`non-value`），必须使用 `null` 关键字才能访问，`undefined` 是一个“`undefined`（未定义）”类型的对象，表示一个未初始化的值，也就是还没有被分配的值。我们之后再具体讨论变量，但有一点可以先简单说明一下，`JavaScript` 允许声明变量但不对其赋值，一个未被赋值的变量就是 `undefined` 类型。还有一点需要说明的是，`undefined` 实际上是一个不允许修改的常量。

JavaScript 包含布尔类型，这个类型的变量有两个可能的值，分别是 true 和 false（两者都是关键字）。根据具体需要，JavaScript 按照如下规则将变量转换成布尔类型：

- `false`、0、空字符串（""）、`NaN`、`null` 和 `undefined` 被转换为 `false`
- 所有其他值被转换为 `true`

### 变量

在 `JavaScript` 中声明一个新变量的方法是使用关键字 `let` 、`const` 和 `var`：

`let` 语句声明一个块级作用域的本地变量，并且可选的将其初始化为一个值。
`const` 允许声明一个不可变的常量。这个常量在定义域内总是可见的。
`var` 是最常见的声明变量的关键字。它没有其他两个关键字的种种限制。这是因为它是传统上在 `JavaScript` 声明变量的唯一方法。
使用 `var` 声明的变量在它所声明的整个函数都是可见的。

剩下的对象，函数就不一一记录了，其实跟上面的没多大区别，只是强化一下记忆。有语言基础的人应该会很好理解这些内容。

## 最后

`JavaScript`还有很多的内容， 继承和原型链 是特别重要的内容，下一篇文章会详细聊一聊。

## 参考文档

[JavaScript](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript)
