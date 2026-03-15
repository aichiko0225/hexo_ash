---
title: React Hooks 速记
date: 2026-03-15 16:20:00
updated: 2026-03-15 16:20:00
wiki: notes
tags:
  - React
  - Hooks
---

# React Hooks 速记

{% note color:green 适用场景 这是一篇偏实战的 Hooks 速查笔记 %}

## 1. useState

```tsx
import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(prev => prev + 1)}>
      count: {count}
    </button>
  )
}
```

要点：

- 基于上一个状态更新时，优先用函数写法：`setState(prev => next)`。
- 对象/数组更新要返回新引用，不要原地改。

## 2. useEffect

```tsx
import { useEffect, useState } from 'react'

export default function Profile({ userId }: { userId: string }) {
  const [profile, setProfile] = useState<any>(null)

  useEffect(() => {
    let cancelled = false

    fetch(`/api/profile/${userId}`)
      .then(res => res.json())
      .then(data => {
        if (!cancelled) setProfile(data)
      })

    return () => {
      cancelled = true
    }
  }, [userId])

  return <pre>{JSON.stringify(profile, null, 2)}</pre>
}
```

要点：

- 依赖数组必须和逻辑一致，避免“遗漏依赖”带来的脏数据。
- 副作用要有清理函数（订阅、定时器、异步竞态）。

## 3. useMemo / useCallback

```tsx
import { useMemo, useCallback, useState } from 'react'

export default function List({ list }: { list: number[] }) {
  const [keyword, setKeyword] = useState('')

  const filtered = useMemo(() => {
    return list.filter(item => String(item).includes(keyword))
  }, [list, keyword])

  const onChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setKeyword(e.target.value)
  }, [])

  return (
    <>
      <input value={keyword} onChange={onChange} />
      <div>{filtered.join(', ')}</div>
    </>
  )
}
```

{% note color:yellow 注意 useMemo/useCallback 不是越多越好，先定位性能瓶颈再加。 %}

## 4. 常见坑

{% folding child:codeblock open:false color:orange 闭包陷阱示例 %}
```tsx
useEffect(() => {
  const id = setInterval(() => {
    console.log(count) // 可能一直打印旧值
  }, 1000)
  return () => clearInterval(id)
}, [])
```
{% endfolding %}

修复方式：

- 加正确依赖，或者
- 用 `useRef` 保存最新值，或者
- 通过函数式更新避免读取旧闭包。

## 5. 我的实践清单

- 先写正确逻辑，再做性能优化。
- `eslint-plugin-react-hooks` 必开。
- 复杂状态用 `useReducer`，跨组件共享再上 Zustand/Redux。
