---
title: Vue 3 Composition API 实战速记
date: 2026-03-15 16:30:00
updated: 2026-03-15 16:30:00
wiki: notes
tags:
  - Vue3
  - CompositionAPI
---

# Vue 3 Composition API 实战速记

{% note color:green 定位 这篇笔记聚焦 setup 语法糖和组合式状态抽离 %}

## 1. ref 和 reactive

```vue
<script setup>
import { ref, reactive } from 'vue'

const count = ref(0)
const user = reactive({
  name: 'ash',
  role: 'admin'
})

const inc = () => {
  count.value += 1
}
</script>

<template>
  <button @click="inc">count: {{ count }}</button>
  <p>{{ user.name }} - {{ user.role }}</p>
</template>
```

要点：

- 基本类型用 `ref`
- 对象结构用 `reactive`
- 模板里会自动解包 `ref`

## 2. computed 和 watch

```vue
<script setup>
import { ref, computed, watch } from 'vue'

const keyword = ref('')
const list = ref(['react', 'vue', 'flutter'])

const filtered = computed(() => {
  return list.value.filter(item => item.includes(keyword.value))
})

watch(keyword, (val) => {
  console.log('keyword changed:', val)
})
</script>
```

{% note color:yellow 注意 computed 用于“派生值”，watch 用于“副作用”。 %}

## 3. 组合式函数（composable）

```ts
// composables/useCounter.ts
import { ref } from 'vue'

export function useCounter() {
  const count = ref(0)
  const inc = () => (count.value += 1)
  const reset = () => (count.value = 0)

  return { count, inc, reset }
}
```

```vue
<script setup lang="ts">
import { useCounter } from '@/composables/useCounter'

const { count, inc, reset } = useCounter()
</script>
```

## 4. 生命周期

```vue
<script setup>
import { onMounted, onUnmounted } from 'vue'

let timer

onMounted(() => {
  timer = setInterval(() => {
    console.log('tick')
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>
```

## 5. 我的实践建议

{% box 团队规范建议 color:blue %}
- 页面逻辑大于 80 行时，优先拆 composable。
- 组合函数命名统一为 `useXxx`。
- 副作用相关代码必须写清理逻辑。
{% endbox %}
