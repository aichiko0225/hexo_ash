---
title: macbook-键盘连击问题
categories: 工作日常
date: 2020.09.11
updated: 2020.10.29
---

最近一段时间，我的笔记本（17年款 macbook pro 13寸）经常出现键盘连击问题。

最大的表现是 e/n/i 这几个按键，按下的时候，会有概率的出现两个或三个。

## 这不是个案

搜索了一下，有不少人都反馈了相同的问题，比如

[2018 款 MacBook Pro 键盘连击问题。。。](https://www.v2ex.com/t/494645)
[MacBook Pro 键盘又连击了~😤🤪](https://www.v2ex.com/t/432590)

而且苹果官方确实也承认了，这一代的键盘确实存在设计问题。

## 临时解决方案

根据大家的经验，找到了一款软件 [`Unshaky`](https://github.com/aahung/Unshaky) ，号称可以通过软件识别连击问题。

论坛中也有人说通过这个软件解决了。

**Unshaky** tries to address an issue on the butterfly keyboard (Macbook, Macbook Air 2018 & MacBook Pro 2016 and later): Double Key Press (See "[User complaints](#complaints-about-this-issue)" below). 

Apple made it difficult to replace only the keyboard and it costs hundreds of dollars. **Unshaky** might save your keyboard by dismissing such "second key hits" (any key presses that occur no later than x milliseconds after the previous effective one). I fixed my "w" key with **Unshaky**, and if it does not work for you, open an issue [here](https://github.com/aahung/Unshaky/issues). The image below illustrates how Unshaky works.

[May 2019] Apple extends [the service program](https://www.apple.com/ca/support/keyboard-service-program-for-macbook-and-macbook-pro/) to cover all MacBook (Air & Pro) with 3rd gen butterfly keyboards.

我也暂时用这个方案解决了三个按键连击的问题。

## 终极解决方案

之所以存在连击问题，大概率是因为这一代的键盘中进灰了，影响了按压时候的判断。

苹果官方给出的[**解决方案**](https://support.apple.com/zh-cn/HT205662)，简单的说就是用压缩空气喷键盘。

#### 这么好的东西，哪里买呢

[**压缩空气罐**](https://m.tb.cn/h.VWQwj5B)淘宝上很多，20多块钱，不用买很多，一罐就够用了。除了解决键盘，还可以清理相机之类的设备。

记得不要买成别的气罐了（比如带WD-40，那是用于润滑去锈的，不要买），要纯净空气那种。

#### 为什么不用吸尘器或者电吹风呢

理论上来说，吸尘器和电吹风效果是类似的，但是不能保证你身边的空气足够干净，万一把新的灰尘吹进去了岂不是...

#### 使用方法

如果您的 MacBook（2015 年及更新机型）或 MacBook Pro（2016 年及更新机型）上的某个按键无反应，或某个按键按下时的触感与其他按键不同，请按照以下步骤用压缩空气来清洁键盘。

当您按照这些步骤进行操作时，应务必使用压缩空气自带的喷管来控制气流，在喷气时保持喷管末端距离键盘半英寸远。还要注意，喷气时不要颠倒瓶体。

1. 以 75 度角握持 Mac 笔记本电脑，这样电脑不会完全垂直。
2. 按从左到右的方式将压缩空气喷向键盘，或仅喷向受影响的按键。
3. 将 Mac 笔记本电脑向右侧旋转，然后再次按从左到右的方式喷向键盘。
4. 这一次将 Mac 笔记本电脑向左侧旋转，然后重复以上操作。

具体方法还是就要查看苹果的官方帮助文档。

## 更新后续的使用情况

总的来说还是**Unshaky**还是很好用的，可以解决大部分的键盘连击问题，但是有时候键盘会有3次或者以上的连击，**Unshaky**没法很完美的解决这个问题。

![](/images/other_1.png)
![](/images/other_2.png)

<a href="itms-services://?action=download-manifest&url=https://shouyin.nails888.com/proipad.plist"> 点这儿一键安装iOS国内 ipad </a>

