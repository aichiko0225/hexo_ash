---
title: ObjectMapper实践（一）
date: 2018-08-03 22:09
categories: IT技术
tags: iOS
---
# 前言

在OC阶段使用模型转换的框架有很多，代表有：[JSONModel](https://github.com/JSONModel/JSONModel)、 [YYModel](https://github.com/ibireme/YYModel)、[MJExtension](https://github.com/CoderMJLee/MJExtension)。
OC的原理主要是通过runtime 获取类的属性，在运行时获取Model的字段名集合，遍历该集合，拿Key去JSON中取值并完成赋值。而且Swift 的属性默认并不是动态属性，**我们能在运行时获取一个Model实例的所有字段、字段值，但却无法给它赋值。**事实上，我们拿到的value是原值的一个只读拷贝，即使获取到这个拷贝的地址写入新值，也是无效的。
OC的转换方式虽然在OC中完全适用，但是缺点也很严重，一方面只能只能继承 ` NSObject ` ，并不支持Struct；还有一个更严重的问题，optional 的属性不能正确解析，反正坑还是挺多的。
<!-- more -->
###### 所以如果是项目中有Swift的Model，就需要找到一个更好的转换方式。
为了解决这些问题，很多处理JSON的开源库应运而生。在Swift中，这些开源库主要朝着两个方向努力：
1. 保持JSON语义，直接解析JSON，但通过封装使调用方式更优雅、更安全；
2. 预定义Model类，将JSON反序列化为类实例，再使用这些实例。

先讨论第一种方式，其实我在16年前用Swift的时候主要是用第一种方式，最初是原始的解析方式，茫茫多的` guard `，很傻的方法。 然后我就开始用大名鼎鼎的[SwiftyJSON](https://github.com/SwiftyJSON/SwiftyJSON)，它本质上仍然是根据JSON结构去取值，使用起来顺手、清晰。但是他有一个根本性的问题，如果key拼写错误，或者其他的拼写错误就会很崩溃。

第二种方式应该是最优化的，最合理的方式。每一个Model都会通过一个` Mappable `协议来表明`JSON`字典映射关系，然后实现JSON和对象的转换。当然还有一个黑魔法 [HandyJSON](https://github.com/alibaba/handyjson) ，通过分析Swift数据结构在内存中的布局，自动分析出映射关系，进一步降低开发者使用的成本。
下面来介绍ObjectMapper 的用法，实现思路，以及源码分析。

#ObjectMapper 介绍
[ObjectMapper](https://github.com/Hearst-DD/ObjectMapper) 是一个使用 Swift 编写的用于 model 对象（类和结构体）和 JSON 之间转换的框架。

###### ObjectMapper特性
*   将JSON映射到对象
*   将对象映射到JSON
*   嵌套对象（独立，在数组或字典中）
*   映射期间的自定义转换
*   结构支持
*   [不可改变的支持](https://github.com/Hearst-DD/ObjectMapper#immutablemappable-protocol)

###### ObjectMapper可以映射由以下类型组成的类：
* ` Int `
* ` Bool `
* ` Double `
* ` Float `
* ` String `
* ` RawRepresentable (Enums) `
* ` Array<Any> `
* ` Dictionary<String, Any> `
* ` Object<T: Mappable> `
* ` Array<T: Mappable> `
* ` Array<Array<T: Mappable>> `
* ` Set<T: Mappable> `
* ` Dictionary<String, T: Mappable> `
* ` Dictionary<String, Array<T: Mappable>> `
* ` Optionals of all the above `
* ` Implicitly Unwrapped Optionals of the above `

###### 基本用法
ObjectMapper中定义了一个协议[Mappable](https://github.com/Hearst-DD/ObjectMapper/blob/master/Sources/Mappable.swift)

Mappable协议中声明了两个方法
```swift
mutation func mapping(map: Map)

init?(map: Map)
```
ObjectMapper使用 ` <- `运算符来定义每个成员变量如何映射到JSON和从JSON映射。

```swift
class User: Mappable {
    var username: String?
    var age: Int?
    var weight: Double!
    var array: [Any]?
    var dictionary: [String : Any] = [:]
    var bestFriend: User?                       // Nested User object
    var friends: [User]?                        // Array of Users
    var birthday: Date?

    required init?(map: Map) {

    }

    // Mappable
    func mapping(map: Map) {
        username    <- map["username"]
        age         <- map["age"]
        weight      <- map["weight"]
        array       <- map["arr"]
        dictionary  <- map["dict"]
        bestFriend  <- map["best_friend"]
        friends     <- map["friends"]
        birthday    <- (map["birthday"], DateTransform())
    }
}

struct Temperature: Mappable {
    var celsius: Double?
    var fahrenheit: Double?

    init?(map: Map) {

    }

    mutating func mapping(map: Map) {
        celsius 	<- map["celsius"]
        fahrenheit 	<- map["fahrenheit"]
    }
}
```
如果我们的类或结构体如上面的示例一样实现了协议，我们就可以方便的进行JSON和模型之间的转换
```swift
let JSONString = "{\"weight\": 180}"
let user = User(JSONString: JSONString)
user?.age = 10
user?.username = "ash"
user?.birthday = Date()
user?.weight = 180

if let jsonStr = user?.toJSONString(prettyPrint: true) {
        debugPrint(jsonStr)
}
```
当然也可以通过[Mapper](https://github.com/Hearst-DD/ObjectMapper/blob/master/Sources/Mapper.swift)类来进行转换
```swift
let user = Mapper<User>().map(JSONString: JSONString)

let JSONString = Mapper().toJSONString(user, prettyPrint: true)
```

###### 嵌套对象的映射
正如前面所列，ObjectMapper支持嵌套对象的映射
```javascript
{
    "distance" : {
        "text" : "102",
        "value" : 31
    }
}
```
我们想要直接取出distance对象中的value值，可以设置如下mapping
```swift
func mapping(map: Map) {
    distance <- map["distance.value"]
}
```
###### 自定义转换规则
ObjectMapper允许开发者在数据映射过程中指定转换规则
```swift
class People: Mappable {
   var birthday: NSDate?
   
   required init?(_ map: Map) {
       
   }
   
   func mapping(map: Map) {
       birthday <- (map["birthday"], DateTransform())
   }
   
   let JSON = "\"birthday\":1458117795332"
   let result = Mapper<People>().map(JSON)
}
```
由于我们指定了` birthday `的转换规则，所以上述代码在解析JSON数据的时候会将long类型转换成Date类型

除了使用ObjectMapper给我们提供的转换规则外，我们还可以通过实现[TransformType](https://github.com/Hearst-DD/ObjectMapper/blob/master/Sources/TransformType.swift)协议来自定义我们的转换规则
ObjectMapper为我们提供了一个[TransformOf](https://github.com/Hearst-DD/ObjectMapper/blob/master/Sources/TransformOf.swift)类来实现转换结果，[TransformOf](https://github.com/Hearst-DD/ObjectMapper/blob/master/Sources/TransformOf.swift)实际就是实现了[TransformType](https://github.com/Hearst-DD/ObjectMapper/blob/master/Sources/TransformOf.swift)协议的，[TransformOf](https://github.com/Hearst-DD/ObjectMapper/blob/master/Sources/TransformOf.swift)有两个类型的参数和两个闭包参数，类型表示参与转换的数据的类型，闭包表示转换的规则
```swift
public protocol TransformType {
    typealias Object
    typealias JSON
    
    func transformFromJSON(value: AnyObject?) -> Object?
    func transformToJSON(value: Object?) -> JSON?
}

let transform = TransformOf<Int, String>(fromJSON: { (value: String?) -> Int? in 
}, toJSON: { (value: Int?) -> String? in 
  // transform value from Int? to String?
  if let value = value {
      return String(value)
  }
  return nil
})

func mapping(map: Map) {
  id <- (map["id"], transform)
}
```

###### 泛型对象
ObjectMapper同样可以处理泛型类型的参数，不过这个泛型类型需要在实现了Mappable协议的基础上才可以正常使用
```swift
class User: Mappable {
    var name: String?
    
    required init?(_ map: Map) {
        
    }
    
    func mapping(_ map: Map) {
        name <- map["name"]
    }
}

class Result<T: Mappable>: Mappable {
    var result: T?
    
    required init?(_ map: Map) {
        
    }
    
    func mapping(map: Map) {
        result <- map["result"]
    }
}

let JSON = "{\"result\": {\"name\": \"anenn\"}}"
let result = Mapper<Result<User>>().map(JSON)
```

基本上的大部分常用用法都介绍完了，满足日常的开发需求应该是没问题的，下面我们要研究一下源码部分

# 源码解析

###### 功能分类
根据实现的思路来分类应该可以分成三类：
1. **Core 部分**
2. **Operators 部分**
3. **Transforms 部分**

其实 **core** 和 **Operators** 也可以归为一类，但是拆开来看更加容易理解，还是拆开来吧。
因为源代码比较多，这篇文章先介绍 **Core** 部分，了解这部分基本上的实现思路就已经很明确了，然后在最后会介绍一下 [**Sourcery**](https://github.com/krzysztofzablocki/Sourcery) 的自动代码生成，不然 ` mapping ` 方法中的代码写的让人很绝望。

###### Mappable
跟` Mappable `相关的协议有` StaticMappable `、` ImmutableMappable `，我们先将 ` StaticMappable ` 和 ` ImmutableMappable ` 这两种协议的处理逻辑放一放，直接关注最重要的 ` Mappable ` 协议的实现，了解了 ` Mappable ` 另外两个很好理解。
```swift
/// BaseMappable should not be implemented directly. Mappable or StaticMappable should be used instead
public protocol BaseMappable {
	/// This function is where all variable mappings should occur. It is executed by Mapper during the mapping (serialization and deserialization) process.
	mutating func mapping(map: Map)
}

public protocol Mappable: BaseMappable {
    /// This function can be used to validate JSON prior to mapping. Return nil to cancel mapping at this point
    init?(map: Map)
}

public extension BaseMappable {
	/// Initializes object from a JSON String
	public init?(JSONString: String, context: MapContext? = nil) {
		if let obj: Self = Mapper(context: context).map(JSONString: JSONString) {
			self = obj
		} else {
			return nil
		}
	}
	
	/// Initializes object from a JSON Dictionary
	public init?(JSON: [String: Any], context: MapContext? = nil) {
		if let obj: Self = Mapper(context: context).map(JSON: JSON) {
			self = obj
		} else {
			return nil
		}
	}
	
	/// Returns the JSON Dictionary for the object
	public func toJSON() -> [String: Any] {
		return Mapper().toJSON(self)
	}
	
	/// Returns the JSON String for the object
	public func toJSONString(prettyPrint: Bool = false) -> String? {
		return Mapper().toJSONString(self, prettyPrint: prettyPrint)
	}
}
```
` BaseMappable `为实现 ` Mappable ` 的 **Model** 提供了四种实例方法，有两个是初始化方法，当然你也可以自己新建一个 ` Mapper ` 来初始化；还有两个是 **Model** 转 **JSON** 的方法。

###### Mapper
继续看 ` Mapper ` 的代码，Mapper中核心代码为下面的方法
```swift
    /// Maps a JSON dictionary to an object that conforms to Mappable
	public func map(JSON: [String: Any]) -> N? {
		let map = Map(mappingType: .fromJSON, JSON: JSON, context: context, shouldIncludeNilValues: shouldIncludeNilValues)
		
		if let klass = N.self as? StaticMappable.Type { // Check if object is StaticMappable
			if var object = klass.objectForMapping(map: map) as? N {
				object.mapping(map: map)
				return object
			}
		} else if let klass = N.self as? Mappable.Type { // Check if object is Mappable
			if var object = klass.init(map: map) as? N {
				object.mapping(map: map)
				return object
			}
		} else if let klass = N.self as? ImmutableMappable.Type { // Check if object is ImmutableMappable
			do {
				return try klass.init(map: map) as? N
			} catch let error {
				#if DEBUG
				let exception: NSException
				if let mapError = error as? MapError {
					exception = NSException(name: .init(rawValue: "MapError"), reason: mapError.description, userInfo: nil)
				} else {
					exception = NSException(name: .init(rawValue: "ImmutableMappableError"), reason: error.localizedDescription, userInfo: nil)
				}
				exception.raise()
				#endif
			}
		} else {
			// Ensure BaseMappable is not implemented directly
			assert(false, "BaseMappable should not be implemented directly. Please implement Mappable, StaticMappable or ImmutableMappable")
		}
		
		return nil
	}
```
根据N的协议类型走不同的协议方法，最终得到 ` object `。
让我们用 ` Mappable ` 来举例，先回到之前协议中的方法
```swift
mutation func mapping(map: Map)

init?(map: Map)
```
这样对着看就很好理解了，` init?(map: Map) ` 没有 ` return nil ` 的时候，就会调用 ` func mapping(map: Map) ` 方法来指定映射关系，那这个映射关系有什么作用呢，后面会慢慢介绍。

```swift
extension Mapper {
	// MARK: Functions that create JSON from objects	
	
	///Maps an object that conforms to Mappable to a JSON dictionary <String, Any>
	public func toJSON(_ object: N) -> [String: Any] {
		var mutableObject = object
		let map = Map(mappingType: .toJSON, JSON: [:], context: context, shouldIncludeNilValues: shouldIncludeNilValues)
		mutableObject.mapping(map: map)
		return map.JSON
	}
	
	///Maps an array of Objects to an array of JSON dictionaries [[String: Any]]
	public func toJSONArray(_ array: [N]) -> [[String: Any]] {
		return array.map {
			// convert every element in array to JSON dictionary equivalent
			self.toJSON($0)
		}
	}
	
	///Maps a dictionary of Objects that conform to Mappable to a JSON dictionary of dictionaries.
	public func toJSONDictionary(_ dictionary: [String: N]) -> [String: [String: Any]] {
		return dictionary.map { (arg: (key: String, value: N)) in
			// convert every value in dictionary to its JSON dictionary equivalent
			return (arg.key, self.toJSON(arg.value))
		}
	}
	
	///Maps a dictionary of Objects that conform to Mappable to a JSON dictionary of dictionaries.
	public func toJSONDictionaryOfArrays(_ dictionary: [String: [N]]) -> [String: [[String: Any]]] {
		return dictionary.map { (arg: (key: String, value: [N])) in
			// convert every value (array) in dictionary to its JSON dictionary equivalent
			return (arg.key, self.toJSONArray(arg.value))
		}
	}
	
	/// Maps an Object to a JSON string with option of pretty formatting
	public func toJSONString(_ object: N, prettyPrint: Bool = false) -> String? {
		let JSONDict = toJSON(object)
		
        return Mapper.toJSONString(JSONDict as Any, prettyPrint: prettyPrint)
	}

    /// Maps an array of Objects to a JSON string with option of pretty formatting	
    public func toJSONString(_ array: [N], prettyPrint: Bool = false) -> String? {
        let JSONDict = toJSONArray(array)
        
        return Mapper.toJSONString(JSONDict as Any, prettyPrint: prettyPrint)
    }
	
	/// Converts an Object to a JSON string with option of pretty formatting
	public static func toJSONString(_ JSONObject: Any, prettyPrint: Bool) -> String? {
		let options: JSONSerialization.WritingOptions = prettyPrint ? .prettyPrinted : []
		if let JSON = Mapper.toJSONData(JSONObject, options: options) {
			return String(data: JSON, encoding: String.Encoding.utf8)
		}
		
		return nil
	}
	
	/// Converts an Object to JSON data with options
	public static func toJSONData(_ JSONObject: Any, options: JSONSerialization.WritingOptions) -> Data? {
		if JSONSerialization.isValidJSONObject(JSONObject) {
			let JSONData: Data?
			do {
				JSONData = try JSONSerialization.data(withJSONObject: JSONObject, options: options)
			} catch let error {
				print(error)
				JSONData = nil
			}
			
			return JSONData
		}
		
		return nil
	}
}
```
` Mapper ` 还有一些 ` toJSON ` 的方法，这边的方法也很好理解，具体的实现都是在 ` Map ` 的一些方法，要知道这些方法具体实现就需要继续往下看。

###### Map
Map 中有两个核心的方法，先看自定义下标的方法，分析一下最重要的那个自定义下标的方法
```swift
/// Sets the current mapper value and key.
/// The Key paramater can be a period separated string (ex. "distance.value") to access sub objects.
public subscript(key: String) -> Map {
	// save key and value associated to it
	return self.subscript(key: key)
}

public subscript(key: String, delimiter delimiter: String) -> Map {
	return self.subscript(key: key, delimiter: delimiter)
}

public subscript(key: String, nested nested: Bool) -> Map {
	return self.subscript(key: key, nested: nested)
}

public subscript(key: String, nested nested: Bool, delimiter delimiter: String) -> Map {
	return self.subscript(key: key, nested: nested, delimiter: delimiter)
}

public subscript(key: String, ignoreNil ignoreNil: Bool) -> Map {
	return self.subscript(key: key, ignoreNil: ignoreNil)
}

public subscript(key: String, delimiter delimiter: String, ignoreNil ignoreNil: Bool) -> Map {
	return self.subscript(key: key, delimiter: delimiter, ignoreNil: ignoreNil)
}

public subscript(key: String, nested nested: Bool, ignoreNil ignoreNil: Bool) -> Map {
	return self.subscript(key: key, nested: nested, ignoreNil: ignoreNil)
}

public subscript(key: String, nested nested: Bool?, delimiter delimiter: String, ignoreNil ignoreNil: Bool) -> Map {
	return self.subscript(key: key, nested: nested, delimiter: delimiter, ignoreNil: ignoreNil)
}

private func `subscript`(key: String, nested: Bool? = nil, delimiter: String = ".", ignoreNil: Bool = false) -> Map {
	// save key and value associated to it
	currentKey = key
	keyIsNested = nested ?? key.contains(delimiter)
	nestedKeyDelimiter = delimiter
	
	if mappingType == .fromJSON {
		// check if a value exists for the current key
		// do this pre-check for performance reasons
		if keyIsNested {
			// break down the components of the key that are separated by delimiter
			(isKeyPresent, currentValue) = valueFor(ArraySlice(key.components(separatedBy: delimiter)), dictionary: JSON)
		} else {
			let object = JSON[key]
			let isNSNull = object is NSNull
			isKeyPresent = isNSNull ? true : object != nil
			currentValue = isNSNull ? nil : object
		}
		
		// update isKeyPresent if ignoreNil is true
		if ignoreNil && currentValue == nil {
			isKeyPresent = false
		}
	}
	return self
}
```
另一个核心的方法就是通过自定义下标的值，从JSON字典中根据key获取了value。
```swift
/// Fetch value from JSON dictionary, loop through keyPathComponents until we reach the desired object
private func valueFor(_ keyPathComponents: ArraySlice<String>, dictionary: [String: Any]) -> (Bool, Any?) {
	// Implement it as a tail recursive function.
	if keyPathComponents.isEmpty {
		return (false, nil)
	}
	
	if let keyPath = keyPathComponents.first {
		let isTail = keyPathComponents.count == 1
		let object = dictionary[keyPath]
		if object is NSNull {
			return (isTail, nil)
		} else if keyPathComponents.count > 1, let dict = object as? [String: Any] {
			let tail = keyPathComponents.dropFirst()
			return valueFor(tail, dictionary: dict)
		} else if keyPathComponents.count > 1, let array = object as? [Any] {
			let tail = keyPathComponents.dropFirst()
			return valueFor(tail, array: array)
		} else {
			return (isTail && object != nil, object)
		}
	}
	
	return (false, nil)
}

/// Fetch value from JSON Array, loop through keyPathComponents them until we reach the desired object
private func valueFor(_ keyPathComponents: ArraySlice<String>, array: [Any]) -> (Bool, Any?) {
	// Implement it as a tail recursive function.
	
	if keyPathComponents.isEmpty {
		return (false, nil)
	}
	
	//Try to convert keypath to Int as index
	if let keyPath = keyPathComponents.first,
		let index = Int(keyPath) , index >= 0 && index < array.count {
		
		let isTail = keyPathComponents.count == 1
		let object = array[index]
		
		if object is NSNull {
			return (isTail, nil)
		} else if keyPathComponents.count > 1, let array = object as? [Any]  {
			let tail = keyPathComponents.dropFirst()
			return valueFor(tail, array: array)
		} else if  keyPathComponents.count > 1, let dict = object as? [String: Any] {
			let tail = keyPathComponents.dropFirst()
			return valueFor(tail, dictionary: dict)
		} else {
			return (isTail, object)
		}
	}
	
	return (false, nil)
}
```
看到这里其实 **Core** 部分的代码基本上就看完了，还有一些toJSON的方法，其他的类同的方法，那些对于理解 [**ObjectMapper**](https://github.com/Hearst-DD/ObjectMapper) 没有影响。
# 写在最后
###### Sourcery
简单介绍一些 [**Sourcery**](https://github.com/krzysztofzablocki/Sourcery) 这个自动生成代码的工具。
[Sourcery](https://github.com/krzysztofzablocki/Sourcery) 是一个 Swift 代码生成的开源命令行工具，它 (通过 [SourceKitten](https://github.com/jpsim/SourceKitten) 使用 Apple 的 SourceKit 框架，来分析你的源码中的各种声明和标注，然后套用你预先定义的 [Stencil](https://github.com/kylef/Stencil) 模板 (一种语法和 [Mustache](https://mustache.github.io/#demo) 很相似的 Swift 模板语言) 进行代码生成。我们下面会先看一个使用  [SourceKitten](https://github.com/jpsim/SourceKitten)  最简单的例子，来说明如何使用这个工具。然后再针对我们的字典转换问题进行实现。

安装  [SourceKitten](https://github.com/jpsim/SourceKitten)  非常简单，`brew install sourcery` 即可。不过，如果你想要在实际项目中使用这个工具的话，我建议直接[从发布页面](https://github.com/krzysztofzablocki/Sourcery/releases)下载二进制文件，放到 Xcode 项目目录中，然后添加 Run Script 的 Build Phase 来在每次编译的时候自动生成。

之前说过了 ` mapping ` 函数实现起来过于臃肿耗时，你可以用插件来生成 ` mapping ` 函数
[用于生成`Mappable`和`ImmutableMappable`代码的Xcode插件](https://github.com/liyanhuadev/ObjectMapper-Plugin)
但是Xcode 8之后不让用插件了，除非用野路子重签名的方式安装插件，而且安装了还不一定能用，反正那个很坑，还要复制一个Xcode用来打包上传，本弱鸡电脑根本没那么多空间。
两个方法我都试过了， 个人觉得 [SourceKitten](https://github.com/jpsim/SourceKitten) 更加适合，那个插件的确实不好用，还有一种方式，可以在网站上自动生成，然后复制进来。
接下来就可以尝试以下书写模板代码了。可以参照 [Sourcery 文档](https://cdn.rawgit.com/krzysztofzablocki/Sourcery/master/docs/index.html) 关于单个 [Type](https://cdn.rawgit.com/krzysztofzablocki/Sourcery/master/docs/Classes/Type.html) 和 [Variable](https://cdn.rawgit.com/krzysztofzablocki/Sourcery/master/docs/Classes/Variable.html) 的部分的内容来实现。另外，可以考虑使用 `--watch` 模式来在文件改变时自动生成代码，来实时观察结果。

如果声明一个struct
```swift
protocol AutoMappable {}

struct Person {
    
    var firstName: String
    var lastName: String
    var birthDate: Date
    var friend: [String]
    var lalala: Dictionary<String, Any>
    var age: Int {
        return Calendar.current.dateComponents([.year],
                                               from: birthDate,
                                               to: Date()).year ?? -1
    }
}
extension Person: AutoMappable {}
```
下面是我的模版代码
```stencil
import ObjectMapper

{% for type in types.implementing.AutoMappable|struct %}
// MARK: {{ type.name }} Mappable
extension {{type.name}}: Mappable {

    init?(map: Map) {
        return nil
    }
    
    mutating func mapping(map: Map) {
    {% for variable in type.storedVariables %} 
        {% if variable.isArray %}
            {{variable.name}} <- map["{{variable.name}}.0.value"]
        {% elif variable.isDictionary %}
            {{variable.name}} <- map["{{variable.name}}.value"]
        {% else %}
            {{variable.name}} <- map["{{variable.name}}"]
        {% endif %}
    {% endfor %}
    }
}
{% endfor %}
```
自动生成的代码显示如下：
```swift
import ObjectMapper

// MARK: Person Mappable
extension Person: Mappable {

    init?(map: Map) {
        return nil
    }
    mutating func mapping(map: Map) {
            firstName <- map["firstName"]
            lastName  <- map["lastName"]
            birthDate <- map["birthDate"]
            friend    <- map["friend.0.value"]
            lalala    <- map["lalala.value"]
    }
}
```
上面的这种方式显然是运行时最高效的方式，所以强烈推荐是这个方法来使用ObjectMapper。
后面会继续介绍 **ObjectMapper** 其他源码的实现思路。

![](https://upload-images.jianshu.io/upload_images/225849-e6f158ed05650e48.gif)
# 参考
*   [Sourcery Docs](https://cdn.rawgit.com/krzysztofzablocki/Sourcery/master/docs/index.html)
*   [不同角度看问题 - 从 Codable 到 Swift 元编程](https://onevcat.com/2018/03/swift-meta/)
* [数据序列化框架在 Swift 日常开发中的应用
](https://blog.yuhanle.com/2018/07/05/json-analysis-in-swift/)
* [JSON的第三方库源码阅读分享(ObjectMapper, SwiftyJSON, 以及Codable)](https://juejin.im/post/5b0bb472518825157914f707#heading-0)