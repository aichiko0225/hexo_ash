---
title: 关于iOS 多线程的问题
date: 2020-02-02 15:33:44
categories: iOS
---

# 写在前面的话
`ReactiveCocoa` 5.0 看了两天，真是看的要吐血，网上基本上没有中文的文章,然后就只能看看git上的readme，看的晕乎乎的。我感觉ReactiveCocoa 的swift上手难度比OC要难很多，然后我看见了一个很有意思的博客主。
[@没故事的卓同学](http://www.jianshu.com/users/88a056103c02/latest_articles)  膜拜一下大神 🐶🐶

> 我有书半卷，逍遥曰化形。 
> 挥请仙佛退，送与鬼神听。 
> 副墨闻于讴，参寥传玄冥。 
>  一指掩天地，齐物自忘情。 

# 前言
- #### 基础知识
 在iOS中每个进程启动后都会建立一个主线程（UI线程），这个线程是其他线程的父线程。由于在iOS中除了主线程，其他子线程是独立于Cocoa Touch的，所以只有主线程可以更新UI界面（新版iOS中，使用其他线程更新UI可能也能成功，但是不推荐）。最好不要尝试在子线程中更新UI。

 当用户播放音频、下载资源、进行图像处理时往往希望做这些事情的时候其他操作不会被中断或者希望这些操作过程中更加顺畅。在单线程中一个线程只能做一件事情，一件事情处理不完另一件事就不能开始，这样势必影响用户体验。早在单核处理器时期就有多线程，这个时候多线程更多的用于解决线程阻塞造成的用户等待（通常是操作完UI后用户不再干涉，其他线程在等待队列中，CPU一旦空闲就继续执行，不影响用户其他UI操作），其处理能力并没有明显的变化。如今无论是移动操作系统还是PC、服务器都是多核处理器，于是“并行运算”就更多的被提及。一件事情我们可以分成多个步骤，在没有顺序要求的情况下使用多线程既能解决线程阻塞又能充分利用多核处理器运行能力。

<!-- more -->

- #### 进程和线程的关系
 1.  线程是进程的执行单元，进程的所有任务都在线程中执行！
 2.  线程是 CPU 调用的最小单位
 3. 进程是 CPU 分配资源和调度的单位
 4. 一个程序可以对应过个进程,一个进程中可有多个线程,但至少要有一条线程
 5. 同一个进程内的线程共享进程资源

看着比较绕口，但是挺好理解的。这篇文章主要是介绍多线程的用法，剩下的串行（Serial）和 并行（Parallelism） 等等多线程的基础知识可以查看 
[iOS开发之多线程编程总结](http://www.jianshu.com/p/95aa5446361d) 这篇文章，里面有详细的介绍。

- ####多线程开发的三种方式
 1.NSThread
 2.NSOperation
 3.GCD

三种方式是随着iOS的发展逐渐引入的，所以相比而言后者比前者更加简单易用，并且GCD也是目前苹果官方比较推荐的方式（它充分利用了多核处理器的运算性能）。

# 1. NSThread的使用
##### NSThread 主要有两种直接创建方式：
```objc
- (id)initWithTarget:(id)target selector:(SEL)selector object:(id)argument;
+ (void)detachNewThreadSelector:(SEL)aSelector toTarget:(id)aTarget withObject:(id)anArgument;
```
iOS 10 之后更新了两个新的API，可以直接将代码写在block中
```objc
+ (void)detachNewThreadWithBlock:(void (^)(void))block API_AVAILABLE(macosx(10.12), ios(10.0), watchos(3.0), tvos(10.0));
- (instancetype)initWithBlock:(void (^)(void))block API_AVAILABLE(macosx(10.12), ios(10.0), watchos(3.0), tvos(10.0));
```

##### NSThread的属性
```objc
@property double threadPriority NS_AVAILABLE(10_6, 4_0); // To be deprecated; use qualityOfService below
//threadPriority是线程的优先级，最高是1.0，最低为0.0；默认我们创建的优先级是0.5；

@property NSQualityOfService qualityOfService NS_AVAILABLE(10_10, 8_0); // read-only after the thread is started
//qualityOfService 则是threadPriority 的替代属性，qualityOfService是一个枚举属性，也是代表线程的优先级。

@property (nullable, copy) NSString *name NS_AVAILABLE(10_5, 2_0);
//name 则是线程的名称，方便后面出现问题的追踪！
```
比较常用的就是这三个属性

##### 使用NSThread下载图片
```objc
    //NSThread 的使用
    //使用类方法创建
    [NSThread detachNewThreadWithBlock:^{
        
    }];
    
    [NSThread detachNewThreadSelector:@selector(downloadImage) toTarget:self withObject:nil];
    
    //方法1：使用对象方法
    //创建一个线程，第一个参数是请求的操作，第二个参数是操作方法的参数
    NSThread *thread=[[NSThread alloc]initWithTarget:self selector:@selector(downloadImage) object:nil];
    
    NSThread *thread_0 = [[NSThread alloc]initWithBlock:^{
        
    }];
    //启动一个线程，注意启动一个线程并非就一定立即执行，而是处于就绪状态，当系统调度时才真正执行
    [thread start];
    [thread_0 start];

- (void)downloadImage {
    
    NSURL *url = [NSURL URLWithString:@"http://imgsrc.baidu.com/forum/w%3D580/sign=07bcb87477f082022d9291377bfafb8a/2da7adec54e736d185d9d05f9f504fc2d76269cd.jpg"];
    
    //线程延迟3s
    //线程可以设置name ，这里可以指定name 来进行休眠
    [NSThread sleepForTimeInterval:3.0];
    
    NSData *data = [NSData dataWithContentsOfURL:url];
    
    NSLog(@"downLoadImage:%@",[NSThread currentThread]);//在子线程中下载图片
    
    /*将数据显示到UI控件,注意只能在主线程中更新UI,
     另外performSelectorOnMainThread方法是NSObject的分类方法，每个NSObject对象都有此方法，
     它调用的selector方法是当前调用控件的方法，例如使用UIImageView调用的时候selector就是UIImageView的方法
     Object：代表调用方法的参数,不过只能传递一个参数(如果有多个参数请使用对象进行封装)
     waitUntilDone:是否线程任务完成执行
     */
    if (data) {
        [self performSelectorOnMainThread:@selector(updateImage:) withObject:data waitUntilDone:YES];
    }
}


- (void)updateImage:(NSData *)imageData {
    //更新image
    UIImage *image = [UIImage imageWithData:imageData];
    _imageView.image=image;
}

```
demo比较简单，viewDidLoad 中启动一个新的线程，这个线程在演示中大概用了5s左右，在这5s内UI线程是不会阻塞的，用户可以进行其他操作，大约5s之后图片下载完成，此时调用UI线程将图片显示到界面中（这个过程瞬间完成）。更新UI的时候使用主线程，这里调用了NSObject的分类扩展方法，调用主线程完成更新。

如果同时用NSThread开辟多个线程来下载图片并更新UI，我们就会发现NSThread 并不能有效的管理线程的顺序。虽然可以设置优先级来进行排序，但是对于同一优先级的线程来说无法有效的管理。在多线程并发同时处理同一个数据或者资源时，就会引出另一个问题：线程的同步与线程锁。

##### 线程的同步与锁
最直接的例子就是：多个窗口同时售票的售票系统！

```objc
@interface ViewController ()
{
    NSInteger _tickets;//总票数
    NSInteger _soldCounts;//当前卖出去票数
}

@property (nonatomic, strong) NSThread* ticketsThread_01;

@property (nonatomic, strong) NSThread* ticketsThread_02;

@property (nonatomic, strong) NSLock *ticketsLock;

- (void)threadLock {
    _tickets = 100;
    _soldCounts = 0;
    
    //锁对象
    self.ticketsLock = [[NSLock alloc] init];
    
    self.ticketsThread_01 = [[NSThread alloc] initWithTarget:self selector:@selector(sellAction) object:nil];
    self.ticketsThread_01.name = @"thread-1";
    [self.ticketsThread_01 start];
    
    self.ticketsThread_02 = [[NSThread alloc] initWithTarget:self selector:@selector(sellAction) object:nil];
    self.ticketsThread_02.name = @"thread-2";
    [self.ticketsThread_02 start];
}

- (void)sellAction {
    while (true) {
        //上锁
        [self.ticketsLock lock];
        if (_tickets >= 0) {
            [NSThread sleepForTimeInterval:0.5];
            _soldCounts = 100 - _tickets;
            NSLog(@"当前总票数是：%ld----->卖出：%ld----->线程名:%@",_tickets,_soldCounts,[NSThread currentThread]);
            _tickets--;
        }else{
            break;
        }
        //解锁
        [self.ticketsLock unlock];
    }
}
```

上面的demo中创建了两个线程来进行买票，因为有NSLock 的存在，线程会在NSLock 上锁的时候进行等待，NSLock 解锁之后才能进行操作。NSLock 还有NSCondition、NSRecursiveLock 循环锁、NSConditionLock 条件锁等几种类型，这里就不一一介绍了。
- - - 
# 2. GCD的使用
GCD(Grand Central Dispatch)是基于C语言开发的一套多线程开发机制，也是目前苹果官方推荐的多线程开发方法。前面也说过三种开发中GCD抽象层次最高，当然是用起来也最简单，只是它基于C语言开发，并不像NSOperation是面向对象的开发，而是完全面向过程的。对于熟悉C#异步调用的朋友对于GCD学习起来应该很快，因为它与C#中的异步调用基本是一样的。这种机制相比较于前面两种多线程开发方式最显著的优点就是它对于多核运算更加有效。

##### GCD 的基本概念
##### #任务和队列
- 任务：就是执行操作的意思，换句话说就是你在线程中执行的那段代码。在GCD中是放在block中的。执行任务有两种方式：**同步执行**和**异步执行**。两者的主要区别是：是否具备开启新线程的能力。
 1. 同步执行（sync）：只能在当前线程中执行任务，不具备开启新线程的能力
   - 必须等待当前语句执行完毕，才会执行下一条语句
   - 不会开启线程
   - 在当前主线程执行 block 的任务
   - ```dispatch_sync(queue, block);```
 2. 异步执行（async）：可以在新的线程中执行任务，具备开启新线程的能力
   - 不用等待当前语句执行完毕，就可以执行下一条语句
   - 会开启线程执行 block 的任务
   - 异步是多线程的代名词
   - ```dispatch_async(queue, block);```
- **队列**：这里的队列指任务队列，即用来存放任务的队列。队列是一种特殊的线性表，采用FIFO（先进先出）的原则，即新任务总是被插入到队列的末尾，而读取任务的时候总是从队列的头部开始读取。每读取一个任务，则从队列中释放一个任务。在GCD中有四种队列：**串行队列**、**并发队列**、**主队列**、**全局队列**。

  1. 串行队列：只有一个线程，加入到队列中的操作按添加顺序依次执行。
   - `dispatch_queue_create("queue", NULL);`
或者`dispatch_queue_create("queue", DISPATCH_QUEUE_SERIAL);`
  2.  并发队列：有多个线程，操作进来之后它会将这些队列安排在可用的处理器上，同时保证先进来的任务优先处理。
   - `dispatch_queue_create("queue", DISPATCH_QUEUE_CONCURRENT);`
*并发功能只有在异步（dispatch_async）函数下才有效*
 3. 主队列：主线程
   - `dispatch_get_main_queue();`
 4. 全局队列
   - 执行过程和并发队列一致，参考并发队列
   - `dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);`
   - 全局队列有四种线程优先级
```objc
#define DISPATCH_QUEUE_PRIORITY_HIGH 2
#define DISPATCH_QUEUE_PRIORITY_DEFAULT 0
#define DISPATCH_QUEUE_PRIORITY_LOW (-2)
#define DISPATCH_QUEUE_PRIORITY_BACKGROUND INT16_MIN
```

##### 串行队列（Serial Dispatch Queue）
```objc
#pragma mark - 串行队列同步和串行队列异步
//串行队列同步
- (void)serialQueueSyncMethod {
    //创建队列
    dispatch_queue_t queue = dispatch_queue_create("serialQueueSyncMethod", DISPATCH_QUEUE_SERIAL);
    //执行任务
    for (int i = 0; i < 6; i++) {
        NSLog(@"mainThread--->%d",i);
        dispatch_sync(queue, ^{
            NSLog(@"Current Thread=%@---->%d-----",[NSThread currentThread],i);
        });
    }
    NSLog(@"串行队列同步end");
}

//串行队列异步
- (void)serialQueueAsyncMethod {
    dispatch_queue_t queue = dispatch_queue_create("serialQueueAsyncMethod", DISPATCH_QUEUE_SERIAL);
    for (int i = 0; i < 6; i++) {
        NSLog(@"mainThread--->%d",i);
        dispatch_async(queue, ^{
            NSLog(@"Current Thread=%@---->%d-----",[NSThread currentThread],i);
        });
    }
    NSLog(@"串行队列异步end");
}
```
如果需要更新UI还使用了GCD方法的主线程队列`dispatch_get_main_queue()，`切换到主线程来更新UI。从上面的例子可以看出虽然串行队列是按照顺序依次执行的，但是**串行队列同步执行**不会开辟线程，而**串行队列异步执行**会仅会开辟一个新的线程，所有block任务之间是同步执行的。

##### 并发队列（Concurrent Dispatch Queue）
```objc
- (void)layoutUI {
    //创建多个图片控件用于显示图片
    _imageViews=[NSMutableArray array];
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 2; j++) {
            UIImageView *imageView = [[UIImageView alloc]initWithFrame:CGRectMake(10+110*i, 100+110*j, 100, 100)];
            [self.view addSubview:imageView];
            [_imageViews addObject:imageView];
        }
    }
}

#pragma mark - 并行队列同步和并行队列异步
//并行队列同步
- (IBAction)concurrentQueueSyncMethod:(id)sender {
    dispatch_queue_t queue = dispatch_queue_create("concurrentQueueSyncMethod", DISPATCH_QUEUE_CONCURRENT);
    
    for (int i = 0; i < 6; i++) {
        dispatch_sync(queue, ^{
            NSLog(@"Current Thread=%@---->%d-----",[NSThread currentThread],i);
            [self loadImage:i];
        });
    }
    NSLog(@"并行队列同步end");
}

//并行队列异步
- (IBAction)concurrentQueueAsyncMethod:(id)sender {
    dispatch_queue_t queue = dispatch_queue_create("concurrentQueueAsyncMethod", DISPATCH_QUEUE_CONCURRENT);
    
    for (int i = 0; i < 6; i++) {
        dispatch_async(queue, ^{
            NSLog(@"Current Thread=%@---->%d-----",[NSThread currentThread],i);
            [self loadImage:i];
        });
    }
    
    NSLog(@"并行队列异步end");
    
}

#pragma mark 加载图片
-(void)loadImage:(int)index{
    NSURL *url = [NSURL URLWithString:@"http://imgsrc.baidu.com/forum/w%3D580/sign=07bcb87477f082022d9291377bfafb8a/2da7adec54e736d185d9d05f9f504fc2d76269cd.jpg"];
    //如果在串行队列中会发现当前线程打印变化完全一样，因为他们在一个线程中
    NSLog(@"thread is :%@",[NSThread currentThread]);
    
    //请求数据
    NSData *data = [NSData dataWithContentsOfURL:url];
    //更新UI界面,此处调用了GCD主线程队列的方法
    
    if ([NSThread isMainThread]) {
        [self updateImageWithData:data andIndex:index];
    }else {
        dispatch_queue_t mainQueue= dispatch_get_main_queue();
        dispatch_sync(mainQueue, ^{
            [self updateImageWithData:data andIndex:index];
        });
    }
}

#pragma mark 将图片显示到界面
-(void)updateImageWithData:(NSData *)data andIndex:(int )index{
    UIImage *image=[UIImage imageWithData:data];
    UIImageView *imageView= _imageViews[index];
    imageView.image=image;
}

```

![并行队列同步和并行队列同步 请求图片 并更新UI](http://upload-images.jianshu.io/upload_images/2478081-c04df3a56ad26ccc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###### 并行队列小结
 1. **并发队列同步**执行和串行队列同步执行一样，都不会开辟新线程，block任务之间是同步执行的！所以点击并行队列同步并不会开辟新线程，所以点击后会出现所有图片的加载全部在主线程中（可以打印线程查看），主线程被阻塞，造成图片最终是一次性显示。
 2. **并发队列异步**执行结果中看到开辟了多个线程，并且执行顺序也不是顺序执行。因为异步开多线程的代名词，并发是开多条线程的代名词
 3. 在GDC中一个操作是多线程执行还是单线程执行取决于当前队列类型和执行方法，只有队列类型为并行队列并且使用异步方法执行时才能在多个线程中执行。
 4. 串行队列可以按顺序执行，并行队列的异步方法无法确定执行顺序。

##### 全局队列
**全局队列**是所有应用程序都能够使用的并发队列（Concurrent Dispatch Queue），原理和用法跟并发队列相同。大家可以参照上面的demo来看。

##### 其他任务执行方法
 1. `dispatch_apply()`:重复执行某个任务，但是注意这个方法没有办法异步执行（为了不阻塞线程可以使用`dispatch_async()`包装一下再执行）。
 2. `dispatch_once()`:单次执行一个任务，此方法中的任务只会执行一次，重复调用也没办法重复执行（单例模式中常用此方法）。
 3. `dispatch_after()`：延迟一定的时间后执行。
 4. `dispatch_barrier_async()`：使用此方法创建的任务首先会查看队列中有没有别的任务要执行，如果有，则会等待已有任务执行完毕再执行；同时在此方法后添加的任务必须等待此方法中任务执行后才能执行。（利用这个方法可以控制执行顺序，例如前面先加载最后一张图片的需求就可以先使用这个方法将最后一张图片加载的操作添加到队列，然后调用`dispatch_async()`添加其他图片加载任务）
 5. `dispatch_group_async()`：实现对任务分组管理，如果一组任务全部完成可以通过`dispatch_group_notify()`方法获得完成通知（需要定义`dispatch_group_t`作为分组标识）。

##### 任务组Dispatch Group
这里介绍一下Dispatch Group ，其他的几种执行方法比较简单，就不一一介绍了。
GCD的任务组在开发中是经常被使用到，当你一组任务结束后再执行一些操作时，使用任务组在合适不过了。dispatch_group的职责就是当队列中的所有任务都执行完毕后在去做一些操作，也就是说在任务组中执行的队列，当队列中的所有任务都执行完毕后就会发出一个通知来告诉用户任务组中所执行的队列中的任务执行完毕了。
```objc
//创建方法
dispatch_group_t group = dispatch_group_create();

//dispatch_group_t 相关联的有四个方法
void
dispatch_group_async(dispatch_group_t group,
	dispatch_queue_t queue,
	dispatch_block_t block);
//将线程加入dispatch_group_t中
long
dispatch_group_wait(dispatch_group_t group, dispatch_time_t timeout);
//group等待
void
dispatch_group_notify(dispatch_group_t group,
	dispatch_queue_t queue,
	dispatch_block_t block);
//group 完成后通知执行
void
dispatch_group_enter(dispatch_group_t group);
//手动进入dispatch_group_t
void
dispatch_group_leave(dispatch_group_t group);
//手动离开dispatch_group_t
```

下面会通过demo来详细介绍四种方法。
```objc

//自动执行任务组
- (void)GCDAutoDispatchGroupMethod {
    dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
    dispatch_group_t group = dispatch_group_create();
    
    for (int i = 0; i < 6; i++) {
        dispatch_group_async(group, queue, ^{
            NSLog(@"current Thread = %@----->%d",[NSThread currentThread],i);
            [self loadImage:i];
        });
    }
    
    dispatch_group_notify(group, dispatch_get_main_queue(), ^{
        NSLog(@"current Thread = %@----->group完成后执行",[NSThread currentThread]);
        UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"" message:@"图片加载完成" preferredStyle:UIAlertControllerStyleAlert];
        UIAlertAction *sureAction = [UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil];
        [alertController addAction:sureAction];
        [self presentViewController:alertController animated:YES completion:nil];
    });
}
```
上面的demo中将多个加载图片的放在group中，在图片加载完成后会立即运行`dispatch_group_notify`的block块。
另一种方式是手动的将队列与组进行关联然后使用异步将队列进行执行，也就是dispatch_group_enter()与dispatch_group_leave()方法的使用。

```objc
//手动执行任务组
- (void)GCDManualDispatchGroupMethod {
    dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
    dispatch_group_t group = dispatch_group_create();
    
    for (int i = 0; i < 6; i++) {
        
        dispatch_group_enter(group);//进入队列组
        
        dispatch_async(queue, ^{
            NSLog(@"current Thread = %@----->%d",[NSThread currentThread],i);
            
            dispatch_group_leave(group);//离开队列组
        });
    }
    
    dispatch_time_t time = dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1 * NSEC_PER_SEC));
    long result = dispatch_group_wait(group, DISPATCH_TIME_FOREVER);//阻塞当前线程，直到所有任务执行完毕才会继续往下执行
    if (result == 0) {
        //属于Dispatch Group 的block任务全部处理结束
        NSLog(@"Dispatch Group全部处理完毕");
        
    }else{
        //属于Dispatch Group 的block任务还在处理中
        NSLog(@"Dispatch Group正在处理");
    }
    
    for (int i = 0; i < 6; i++) {
        
        dispatch_group_enter(group);//进入队列组
        
        dispatch_async(queue, ^{
            NSLog(@"current Thread = %@----->%d",[NSThread currentThread],i);
            
            dispatch_group_leave(group);//离开队列组
        });
    }
    
    dispatch_group_notify(group, dispatch_get_main_queue(), ^{
        NSLog(@"current Thread = %@----->这是最后执行",[NSThread currentThread]);
    });
}
```
`dispatch_group_wait()`函数，该函数的职责就是阻塞当前线程，来等待任务组中的任务执行完毕。
 `dispatch_group_wait`可以使用 `DISPATCH_TIME_FOREVER`，也可以用`dispatch_time_t time = dispatch_time(DISPATCH_TIME_NOW, (int64_t)( 1 * NSEC_PER_SEC));`来阻塞具体时间，直到上面的任务执行完成。

##### 使用GCD解决资源抢占问题
在GCD中提供了一种信号机制，也可以解决资源抢占问题（和同步锁的机制并不一样）。GCD中信号量是dispatch_semaphore_t类型，支持信号通知和信号等待。每当发送一个信号通知，则信号量+1；每当发送一个等待信号时信号量-1,；如果信号量为0则信号会处于等待状态，直到信号量大于0开始执行。根据这个原理我们可以初始化一个信号量变量，默认信号量设置为1，每当有线程进入“加锁代码”之后就调用信号等待命令（此时信号量为0）开始等待，此时其他线程无法进入，执行完后发送信号通知（此时信号量为1），其他线程开始进入执行，如此一来就达到了线程同步目的。
```objc
     /*初始化信号量
     参数是信号量初始值
     */
    _semaphore=dispatch_semaphore_create(1);

    /*信号等待
     第二个参数：等待时间
     */
    dispatch_semaphore_wait(_semaphore, DISPATCH_TIME_FOREVER);
    //这里加入修改信息的代码
    //使用方法跟NSLock类似
    //信号通知
    dispatch_semaphore_signal(_semaphore);
```
- - - 
# 3. NSOperation的使用
使用NSOperation和NSOperationQueue进行多线程开发类似于C#中的线程池，只要将一个NSOperation（实际开中需要使用其子类NSInvocationOperation、NSBlockOperation）放到NSOperationQueue这个队列中线程就会依次启动。NSOperationQueue负责管理、执行所有的NSOperation，在这个过程中可以更加容易的管理线程总数和控制线程之间的依赖关系。

NSOperation有两个常用子类用于创建线程操作：NSInvocationOperation和NSBlockOperation，两种方式本质没有区别，但是是后者使用Block形式进行代码组织，使用相对方便。

把NSOperation 放在最后一方面是我自己用这个用的很少，然后NSOperation 的API也是比较简单的，NSInvocationOperation和NSBlockOperation的用法一目了然。
###### NSInvocationOperation 的使用
```objc
     /*创建一个调用操作
     object:调用方法参数
     */
    NSInvocationOperation *invocationOperation =  [[NSInvocationOperation alloc]initWithTarget:self selector:@selector(loadImage) object:nil];
    //创建完NSInvocationOperation对象并不会调用，它由一个start方法启动操作，但是注意如果直接调用start方法，则此操作会在主线程中调用，一般不会这么操作,而是添加到NSOperationQueue中
    //[invocationOperation start];
    
    //创建操作队列
    NSOperationQueue *operationQueue = [[NSOperationQueue alloc]init];
    //注意添加到操作队后，队列会开启一个线程执行此操作
    [operationQueue addOperation:invocationOperation];
```
###### NSBlockOperation 的使用
```objc
    //创建操作队列
    NSOperationQueue *operationQueue=[[NSOperationQueue alloc]init];
    operationQueue.maxConcurrentOperationCount=5;//设置最大并发线程数
    //创建多个线程用于填充图片
    for (int i=0; i<count; ++i) {
        //方法1：创建操作块添加到队列
//        //创建多线程操作
//        NSBlockOperation *blockOperation=[NSBlockOperation blockOperationWithBlock:^{
//            [self loadImage:[NSNumber numberWithInt:i]];
//        }];
//        //创建操作队列
//
//        [operationQueue addOperation:blockOperation];
        
        //方法2：直接使用操队列添加操作
        [operationQueue addOperationWithBlock:^{
            [self loadImage:[NSNumber numberWithInt:i]];
        }];
    }
```

NSOperation 的优势在于可以用添加依赖来控制线程运行的顺序。
```objc
- (IBAction)loadImageWithMultiThread:(id)sender {
    //创建操作队列
    NSOperationQueue *operationQueue = [[NSOperationQueue alloc]init];
    operationQueue.maxConcurrentOperationCount = 5;//设置最大并发线程数
    
    NSBlockOperation *lastBlockOperation = [NSBlockOperation blockOperationWithBlock:^{
        [self loadImage:5];
    }];
    //创建多个线程用于填充图片
    for (int i=0; i<6-1; ++i) {
        //方法1：创建操作块添加到队列
        //创建多线程操作
        NSBlockOperation *blockOperation = [NSBlockOperation blockOperationWithBlock:^{
            [self loadImage:i];
        }];
        //设置依赖操作为最后一张图片加载操作
        [blockOperation addDependency:lastBlockOperation];
        
        [operationQueue addOperation:blockOperation];
        
    }
    //将最后一个图片的加载操作加入线程队列
    [operationQueue addOperation:lastBlockOperation];
}
```
可以看到虽然加载最后一张图片的操作最后被加入到操作队列，但是它却是被第一个执行的。操作依赖关系可以设置多个，例如A依赖于B、B依赖于C…但是千万不要设置为循环依赖关系（例如A依赖于B，B依赖于C，C又依赖于A），否则是不会被执行的。

# 总结
 1. NSThread适合轻量级多线程开发，控制线程顺序比较难，同时线程总数无法控制（每次创建并不能重用之前的线程，只能创建一个新的线程）。
 2. NSOperation进行多线程开发可以控制线程总数及线程依赖关系。
 3. NSOperation是对GCD面向对象的ObjC封装，但是相比GCD基于C语言开发，效率却更高，建议如果任务之间有依赖关系或者想要监听任务完成状态的情况下优先选择NSOperation否则使用GCD。
 4. 在GCD中串行队列中的任务被安排到一个单一线程执行（不是主线程），可以方便地控制执行顺序；并发队列在多个线程中执行（前提是使用异步方法），顺序控制相对复杂，但是更高效。
 5. 在GDC中一个操作是多线程执行还是单线程执行取决于当前队列类型和执行方法，只有队列类型为并行队列并且使用异步方法执行时才能在多个线程中执行（如果是并行队列使用同步方法调用则会在主线程中执行）。

##### demo 下载地址：
https://github.com/aichiko/Thread_demo

#### 参考资料：
[iOS开发系列--并行开发其实很容易](http://www.cnblogs.com/kenshincui/p/3983982.html#summary)
[iOS开发之多线程编程](http://www.jianshu.com/p/01a9b8c9e963)