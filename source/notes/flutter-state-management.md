---
title: Flutter 状态管理入门速记
date: 2026-03-15 16:25:00
updated: 2026-03-15 16:25:00
wiki: notes
tags:
  - Flutter
  - State
---

# Flutter 状态管理入门速记

{% note color:green 目标 用最小心智负担理解 setState、Provider、Riverpod 的区别 %}

## 1. 从 setState 开始

```dart
class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(child: Text('count: $count')),
      floatingActionButton: FloatingActionButton(
        onPressed: () => setState(() => count++),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

适合：

- 页面内部的小状态
- 生命周期和页面强绑定

## 2. Provider（中小项目够用）

```dart
class CounterModel extends ChangeNotifier {
  int count = 0;

  void inc() {
    count++;
    notifyListeners();
  }
}
```

```dart
ChangeNotifierProvider(
  create: (_) => CounterModel(),
  child: const App(),
)
```

```dart
Consumer<CounterModel>(
  builder: (_, model, __) => Text('count: ${model.count}'),
)
```

适合：

- 有跨组件共享状态需求
- 团队成员都熟悉 ChangeNotifier 风格

## 3. Riverpod（可测试性更好）

```dart
final counterProvider = StateProvider<int>((ref) => 0);
```

```dart
class CounterText extends ConsumerWidget {
  const CounterText({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('count: $count');
  }
}
```

```dart
ref.read(counterProvider.notifier).state++;
```

{% note color:blue 建议 新项目如果没有历史包袱，可以直接从 Riverpod 起步。 %}

## 4. 选型建议

{% box 快速决策 color:cyan %}
- 单页简单状态：`setState`
- 中小项目共享状态：`Provider`
- 追求可测试和可维护：`Riverpod`
{% endbox %}

## 5. 常见问题

{% folding open:false color:yellow 为什么页面频繁重建？ %}
通常是 watch 了过大的状态，或 widget 拆分不够细。

优化方式：

1. 状态切片
2. 拆分小组件
3. 使用 selector（Provider）或精细 watch（Riverpod）
{% endfolding %}
