---
title: iOS GIF图片的加载和合成
date: 2017-02-11
categories: iOS
---

# 写在前面的

>不拘一世之利以为己私分，
>不以王天下为已处显。
>显则明。万物一府，死生同状。
<!-- more -->

*一颗伤心死掉的橘子树*
![那颗死掉的橘子树](http://upload-images.jianshu.io/upload_images/2478081-34221564e9b2bd12.jpg)

###### 扯淡结束开始进入文章正题
iOS中GIF图片是无法像jpg，png等一样直接加载出来的，有很多的第三方库也提供了这方面的功能，这里总结一下GIF图片加载的几种方式，以及使用多张png图片合成GIF图片的方法。

# 加载GIF图片
#### 1.使用UIWebView/WKWebView
使用UIWebView/WKWebView相当于使用coreText 将GIF的数据编码渲染到UIWebView/WKWebView上，使用data数据来加载，本地和网络图片差不多。

###### 下面使用本地图片来举例
```Swift
//1.使用webview来显示GIF

self.view.addSubview(webview)
webview.frame = self.view.bounds

let path = Bundle.main.path(forResource: "timg", ofType: "gif")
if let data = try? Data.init(contentsOf: URL.init(fileURLWithPath: path!)) {
    webview.load(data as Data, mimeType: "image/gif", characterEncodingName: "UTF-8", baseURL: Bundle.main.resourceURL!)
}

//当然也可以直接加载文件路径,下面两种load方法都可以实现
webview.load(URLRequest.init(url: URL.init(fileURLWithPath: path!)))
webview.loadFileURL(URL.init(fileURLWithPath: path!), allowingReadAccessTo: Bundle.main.resourceURL!)
//OC 的写法类似，就不重复写了。
```

![运行效果](http://upload-images.jianshu.io/upload_images/2478081-46f07bf71f2f7f15.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/300)

###### 小结
我本地的原图的宽度是500像素的，但是从上面的效果图可以看到，图片有并没有按照像素来显示，而是根据图片比例来显示，而且宽度自动为self.view的宽度。说明GIF图片数据在渲染时并不能控制图片显示的大小，以及GIF执行的帧数和运行次数。

#### 2.使用GIF 数据来实现
也可以使用 ImageIO 系统框架来实现GIF的播放，很多第三方开源的库也是这样做的。类似SDWebImage，Kingfisher，以及YYImage 都可以实现一句话来加载GIF图片的功能，其中Kingfisher 是swift语言，另外两个是OC的。

其实两种语言都一样，这边只是介绍swift语言。

**下面的方法是根据GIF的data数据来得到一个([UIImage], TimeInterval) 的元组**
```Swift
// MARK: - ImageIO
private func showGif() ->([UIImage], TimeInterval)? {
    let path = Bundle.main.path(forResource: "timg", ofType: "gif")
    let data = try? Data.init(contentsOf: URL.init(fileURLWithPath: path!))
    let source = CGImageSourceCreateWithData(data as! CFData, nil)
    let count = CGImageSourceGetCount(source!)
    let options: NSDictionary = [kCGImageSourceShouldCache as String: true, kCGImageSourceTypeIdentifierHint as String: kUTTypeGIF]
    var gifDuration = 0.0
    var images = [UIImage]()
    
    func frameDuration(from gifInfo: NSDictionary) -> Double {
        let gifDefaultFrameDuration = 0.100
        let unclampedDelayTime = gifInfo[kCGImagePropertyGIFUnclampedDelayTime as String] as? NSNumber
        let delayTime = gifInfo[kCGImagePropertyGIFDelayTime as String] as? NSNumber
        let duration = unclampedDelayTime ?? delayTime
        guard let frameDuration = duration else { return gifDefaultFrameDuration }
        
        return frameDuration.doubleValue > 0.011 ? frameDuration.doubleValue : gifDefaultFrameDuration
    }
    for i in 0 ..< count {
        guard let imageRef = CGImageSourceCreateImageAtIndex(source!, i, options) else {
            return nil
        }
        if count == 1 {
            //只有一张图片时
            gifDuration = Double.infinity//无穷大
        }else {
            // Animated GIF
            guard let properties = CGImageSourceCopyPropertiesAtIndex(source!, i, nil), let gifinfo = (properties as NSDictionary)[kCGImagePropertyGIFDictionary as String] as? NSDictionary  else {
                return nil
            }
            gifDuration += frameDuration(from: gifinfo)
        }
        images.append(UIImage.init(cgImage: imageRef, scale: UIScreen.main.scale, orientation: .up))
    }
    return (images, gifDuration)
}
```
然后在viewDidLoad 中调用下面的代码
```Swift
var imageView: UIImageView?
let (images, duration) = showGif()!
let animatedImage = UIImage.animatedImage(with: images, duration: duration)
imageView = UIImageView.init(image: animatedImage)

self.view.addSubview(imageView!)
imageView?.center = self.view.center
```
使用`let animatedImage = UIImage.animatedImage(with: images, duration: duration)`可以创建一个动画图片，然后使用`imageView = UIImageView.init(image: animatedImage)`创建一个UIImageView? （**为什么用这个方法呢，因为这个不用写imageView的width和height，会根据图片的像素自动渲染大小，不用设置大小。。。**）

![运行效果图](http://upload-images.jianshu.io/upload_images/2478081-06f5970b7ff51964.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/300)

###### 小结
原图的像素宽度为500，模拟器的屏幕为@2x的像素，所以图片显示大小应该是刚刚好的。这种相对于webView来显示就优化得多，也可以设置图片动画的持续时间。

同样的道理，我们如果用imags这个image数组 加入到ImageView动画组中，就可以设置动画的次数，就可以实现类似于新浪微博多个GIF图的微博 GIF图片会依次播放的功能。

```Swift
let (images, duration) = showGif()!
//let animatedImage = UIImage.animatedImage(with: images, duration: duration)
imageView = UIImageView.init(image: images.first)
        
self.view.addSubview(imageView!)
imageView?.center = self.view.center
        
imageView?.animationImages = images
imageView?.animationDuration = duration
imageView?.animationRepeatCount = 3
imageView?.startAnimating()
```
GIF图片的显示就介绍到这里

# GIF的合成
###### GIF图片合成思路：
多帧图像合成GIF的过程和GIF分解多帧图像的过程互逆，GIF图片分解过程倒过来推，就是GIF图像合成的过程。
从功能上来说，GIF图片的合成分为以下三个主要部分。 
（1）加载待处理的n张原始数据源。 
（2）在Document目录下构建GIF文件。 
（3）设置GIF文件属性，利用ImageIO编码GIF文件。

1.首先将图片加入到工程中
![图片导入到bundle中](http://upload-images.jianshu.io/upload_images/2478081-df10989d1514fa0e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/640)
然后将读取的图片依次加载到images中。
```Swift
let bundlePath = Bundle.main.path(forResource: "images", ofType: "bundle")
print("bundlePath === \(bundlePath)")
var images = [UIImage]()

for i in 1 ..< 10 {
    let path = bundlePath?.appending("/\(i).tiff")
    let image = UIImage.init(contentsOfFile: path!)
    images.append(image!)
}
```
2.构建在Document目录下的GIF文件路径。具体实现如下所示。
```Swift
//构建在Document目录下的GIF文件路径
let docs = NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true)
let documentsDirectory = docs[0] as String
let gifPath = documentsDirectory+"/mine.gif"
print("gifPath === \(gifPath)")

let url = CFURLCreateWithFileSystemPath(kCFAllocatorDefault, gifPath as CFString, CFURLPathStyle.cfurlposixPathStyle, false)
let destion = CGImageDestinationCreateWithURL(url!, kUTTypeGIF, images.count, nil)
//CGImageDestinationCreateWithURL方法的作用是创建一个图片的目标对象，为了便于大家理解，这里把图片目标对象比喻为一个集合体。 
//集合体中描述了构成当前图片目标对象的一系列参数，如图片的URL地址、图片类型、图片帧数、配置参数等。
//本代码中将mine.gif的本地文件路径作为参数1传递给这个图片目标对象，参数2描述了图片的类型为GIF图片，参数3表明当前GIF图片构成的帧数，参数4暂时给它一个空值。
```
3.待处理图片源已经加载到代码中，GIF图片Destination也已经完成构建，下面就需要使用ImageIO框架把多帧PNG图片编码到GIF图片中，其处理流程如下。
```Swift
//设置gif图片属性，利用9张tiff图片构建gif
let cgimagePropertiesDic = [kCGImagePropertyGIFDelayTime as String: 0.1]//设置每帧之间播放时间
let cgimagePropertiesDestDic = [kCGImagePropertyGIFDictionary as String: cgimagePropertiesDic]

for cgimage in images {
    // 依次为gif图像对象添加每一帧元素
    CGImageDestinationAddImage(destion!, cgimage.cgImage!, cgimagePropertiesDestDic as CFDictionary?)
}
let gifPropertiesDic:NSMutableDictionary = NSMutableDictionary()
gifPropertiesDic.setValue(kCGImagePropertyColorModelRGB, forKey: kCGImagePropertyColorModel as String)
gifPropertiesDic.setValue(16, forKey:kCGImagePropertyDepth as String)// 设置图像的颜色深度
gifPropertiesDic.setValue(3, forKey:kCGImagePropertyGIFLoopCount as String)// 设置Gif执行次数, 0则为无限执行
gifPropertiesDic.setValue(NSNumber.init(booleanLiteral: true), forKey: kCGImagePropertyGIFHasGlobalColorMap as String)
let gifDictionaryDestDic = [kCGImagePropertyGIFDictionary as String: gifPropertiesDic]
CGImageDestinationSetProperties(destion!, gifDictionaryDestDic as CFDictionary?)//为gif图像设置属性

CGImageDestinationFinalize(destion!)//最后释放 目标对象 destion

//生成GIF图片成功
```
这样就生成GIF图片成功了，最后我们来测试一下生成的GIF图片能否成功显示。
```Swift
//测试一下显示GIF图片
let (images2, duration) = showGif(path: gifPath)!
let animatedImage = UIImage.animatedImage(with: images2, duration: duration)
imageView = UIImageView.init(image: animatedImage)

self.view.addSubview(imageView!)
imageView?.center = self.view.center
```
**运行之后确实是可以显示的**
![大功告成！](http://upload-images.jianshu.io/upload_images/2478081-fa8bf6dab9678aca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/300)

# 最后的话
最后附上demo 的地址
https://github.com/aichiko/Swift_Diary
喜欢的话可以点赞一下。