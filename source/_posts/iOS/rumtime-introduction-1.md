---
title: Runtime介绍(一)
date: 2020-02-08 22:39:02
categories: IT技术
tags:
 - iOS 
 - Runtime 
 - 基础知识
---

## Runtime简介

`Runtime` 又叫运行时，是一套底层的 C 语言 API，是 iOS 系统的核心之一。开发者在编码过程中，可以给任意一个对象发送消息，在编译阶段只是确定了要向接收者发送这条消息，而接受者将要如何响应和处理这条消息，那就要看运行时来决定了。
<!-- more -->
OC语言在编译期都会被编译为C语言的`Runtime`代码，二进制执行过程中执行的都是C语言代码。而OC的类本质上都是结构体，在编译时都会以结构体的形式被编译到二进制中。`Runtime`是一套由C、C++、汇编实现的API，所有的方法调用都叫做发送消息。

C语言中，在编译期，函数的调用就会决定调用哪个函数。
而OC的函数，属于动态调用过程，在编译期并不能决定真正调用哪个函数，只有在真正运行时才会根据函数的名称找到对应的函数来调用。

`Objective-C` 是一个动态语言，这意味着它不仅需要一个编译器，也需要一个运行时系统来动态得创建类和对象、进行消息传递和转发。

### Runtime使用

`Runtime`是一个共享动态库，其目录位于`/usr/include/objc`，由一系列的C函数和结构体构成。和`Runtime`系统发生交互的方式有三种，一般都是用前两种：

1. 使用OC源码
直接使用上层OC源码，底层会通过`Runtime`为其提供运行支持，上层不需要关心`Runtime`运行。
2. NSObject
在OC代码中绝大多数的类都是继承自NSObject的，`NSProxy`类例外。`Runtime`在`NSObject`中定义了一些基础操作，`NSObject`的子类也具备这些特性。
3. Runtime动态库
上层的OC源码都是通过`Runtime`实现的，我们一般不直接使用`Runtime`，直接和OC代码打交道就可以。

使用Runtime需要引入下面两个头文件，一些基础方法都定义在这两个文件中。

```Objc
#import <objc/runtime.h>
#import <objc/message.h>
```

关于库函数可以在[Objective-C Runtime Reference](https://developer.apple.com/documentation/objectivec/objective-c_runtime)中查看 Runtime 函数的详细文档。

关于这一点，其实还有一个小插曲。当我们导入了`objc/Runtime.h`和`objc/message.h`两个头文件之后，我们查找到了`Runtime`的函数之后，代码打完，发现没有代码提示了，那些函数里面的参数和描述都没有了。对于熟悉`Runtime`的开发者来说，这并没有什么难的，因为参数早已铭记于胸。但是对于新手来说，这是相当不友好的。而且，如果是从`iOS6`开始开发的同学，依稀可能能感受到，关于`Runtime`的具体实现的官方文档越来越少了？可能还怀疑是不是错觉。其实从`Xcode5`开始，苹果就不建议我们手动调用`Runtime`的API，也同样希望我们不要知道具体底层实现。所以IDE上面默认代了一个参数，禁止了`Runtime`的代码提示，源码和文档方面也删除了一些解释。
![](/images/runtime_1.webp)
如果发现导入了两个库文件之后，仍然没有代码提示，就需要把这里的设置改成NO，即可。

## NSObject介绍

在OC的世界中，除了`NSProxy`类以外，所有的类都是`NSObject`的子类。在`Foundation`框架下，`NSObject`和`NSProxy`两个基类，定义了类层次结构中该类下方所有类的公共接口和行为。`NSProxy`是专门用于实现代理对象的类，这个类暂时本篇文章不提。这两个类都遵循了`NSObject`协议。在`NSObject`协议中，声明了所有OC对象的公共方法。

```objc
@protocol NSObject

- (BOOL)isEqual:(id)object;
@property (readonly) NSUInteger hash;

@property (readonly) Class superclass;
- (Class)class OBJC_SWIFT_UNAVAILABLE("use 'type(of: anObject)' instead");
- (instancetype)self;

- (id)performSelector:(SEL)aSelector;
- (id)performSelector:(SEL)aSelector withObject:(id)object;
- (id)performSelector:(SEL)aSelector withObject:(id)object1 withObject:(id)object2;

- (BOOL)isProxy;

- (BOOL)isKindOfClass:(Class)aClass;
- (BOOL)isMemberOfClass:(Class)aClass;
- (BOOL)conformsToProtocol:(Protocol *)aProtocol;

- (BOOL)respondsToSelector:(SEL)aSelector;

- (instancetype)retain OBJC_ARC_UNAVAILABLE;
- (oneway void)release OBJC_ARC_UNAVAILABLE;
- (instancetype)autorelease OBJC_ARC_UNAVAILABLE;
- (NSUInteger)retainCount OBJC_ARC_UNAVAILABLE;

- (struct _NSZone *)zone OBJC_ARC_UNAVAILABLE;

@property (readonly, copy) NSString *description;
@optional
@property (readonly, copy) NSString *debugDescription;

@end

@interface NSObject <NSObject> {
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wobjc-interface-ivars"
    Class isa  OBJC_ISA_AVAILABILITY;
#pragma clang diagnostic pop
}
```

`objc_class`的源码如下：

```objc
#if !OBJC_TYPES_DEFINED
/// An opaque type that represents an Objective-C class.
typedef struct objc_class *Class;

/// Represents an instance of a class.
struct objc_object {
    Class _Nonnull isa  OBJC_ISA_AVAILABILITY;
};

struct objc_class {
    Class _Nonnull isa  OBJC_ISA_AVAILABILITY;

#if !__OBJC2__
    Class _Nullable super_class                              OBJC2_UNAVAILABLE;
    const char * _Nonnull name                               OBJC2_UNAVAILABLE;
    long version                                             OBJC2_UNAVAILABLE;
    long info                                                OBJC2_UNAVAILABLE;
    long instance_size                                       OBJC2_UNAVAILABLE;
    struct objc_ivar_list * _Nullable ivars                  OBJC2_UNAVAILABLE;
    struct objc_method_list * _Nullable * _Nullable methodLists                    OBJC2_UNAVAILABLE;
    struct objc_cache * _Nonnull cache                       OBJC2_UNAVAILABLE;
    struct objc_protocol_list * _Nullable protocols          OBJC2_UNAVAILABLE;
#endif

} OBJC2_UNAVAILABLE;
/* Use `Class` instead of `struct objc_class *` */
```

在这里可以看到，在一个类中，有超类的指针，类名，版本的信息。
`ivars`是`objc_ivar_list`成员变量列表的指针；`methodLists`是指向`objc_method_list`指针的指针。`*methodLists`是指向方法列表的指针。这里如果动态修改`*methodLists`的值来添加成员方法，这也是`Category`实现的原理，同样解释了`Category`不能添加属性的原因。

在`NSObject`的类中还定义了一个方法

```objc
+ (IMP)instanceMethodForSelector:(SEL)aSelector;
```

`IMP`则引出了另一个概念，这个后面会介绍，我们继续说`NSObject`。

![对象模型](/images/objc.webp)

图中实线是 super_class指针，虚线是isa指针。

1. `Root class (class)`其实就是`NSObject`，`NSObject`是没有超类的，所以`Root class(class)`的`superclass`指向`nil`。
2. 每个Class都有一个isa指针指向唯一的Meta class
3. `Root class(meta)`的superclass指向Root class(class)，也就是NSObject，形成一个回路。
4. 每个Meta class的isa指针都指向Root class (meta)。

我们其实应该明白，类对象和元类对象是唯一的，对象是可以在运行时创建无数个的。而在`main`方法执行之前，从 `dyld`到`runtime`这期间，类对象和元类对象在这期间被创建。

具体的实现需要看源代码，这里我就不讨论源代码的内容了。

## 相关概念

上面介绍了`NSObject`，下面介绍一下其他的相关概念。

### IMP

在`Runtime`中`IMP`本质上就是一个函数指针，其定义如下。在`IMP`中有两个默认的参数`id`和`SEL`，`id`也就是方法中的`self`，这和`objc_msgSend()`函数传递的参数一样。


`Runtime`中提供了很多对于`IMP`操作的`API`，下面就是不分`IMP`相关的函数定义。我们比较常见的是`method_exchangeImplementations`函数，`Method Swizzling`就是通过这个`API`实现的。

```objc
/// A pointer to the function of a method implementation. 
#if !OBJC_OLD_DISPATCH_PROTOTYPES
typedef void (*IMP)(void /* id, SEL, ... */ ); 
#else
typedef id _Nullable (*IMP)(id _Nonnull, SEL _Nonnull, ...); 
#endif

OBJC_EXPORT void
method_exchangeImplementations(Method _Nonnull m1, Method _Nonnull m2) 
    OBJC_AVAILABLE(10.5, 2.0, 9.0, 1.0, 2.0);

OBJC_EXPORT IMP _Nonnull
method_setImplementation(Method _Nonnull m, IMP _Nonnull imp) 
    OBJC_AVAILABLE(10.5, 2.0, 9.0, 1.0, 2.0);

OBJC_EXPORT IMP _Nonnull
method_getImplementation(Method _Nonnull m) 
    OBJC_AVAILABLE(10.5, 2.0, 9.0, 1.0, 2.0);

OBJC_EXPORT IMP _Nullable
class_getMethodImplementation(Class _Nullable cls, SEL _Nonnull name) 
    OBJC_AVAILABLE(10.5, 2.0, 9.0, 1.0, 2.0);
// ....
```

### Method

`Method`用来表示方法，其包含`SEL`和`IMP`，下面可以看一下`Method`结构体的定义。

```objc
typedef struct method_t *Method;

struct method_t {
    SEL name;
    const char *types;
    IMP imp;
};
```

在`Xcode`进行编译的时候，只会将`Xcode`的`Compile Sources`中.m声明的方法编译到`Method List`，而.h文件中声明的方法对`Method List`没有影响。

### Property

在`Runtime`中定义了属性的结构体，用来表示对象中定义的属性。`@property`修饰符用来修饰属性，修饰后的属性为`objc_property_t`类型，其本质是`property_t`结构体。其结构体定义如下。

```objc
typedef struct property_t *objc_property_t;

struct property_t {
    const char *name;
    const char *attributes;
};
```

可以通过下面两个函数，分别获取实例对象的属性列表，和协议的属性列表。

```objc
objc_property_t * class_copyPropertyList（Class cls，unsigned int * outCount）
objc_property_t * protocol_copyPropertyList（Protocol * proto，unsigned int * outCount）
```

可以通过下面两个方法，传入指定的`Class`和`propertyName`，获取对应的`objc_property_t`属性结构体。

```objc
objc_property_t class_getProperty（Class cls，const char * name）
objc_property_t protocol_getProperty（Protocol * proto，const char * name，BOOL isRequiredProperty，BOOL isInstanceProperty）
```

## 未完待续

