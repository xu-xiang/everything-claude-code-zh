# 通用模式（Common Patterns）

## API 响应格式（API Response Format）

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}
```

## 自定义 Hook 模式（Custom Hooks Pattern）

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}
```

## 仓储模式（Repository Pattern）

```typescript
interface Repository<T> {
  findAll(filters?: Filters): Promise<T[]>
  findById(id: string): Promise<T | null>
  create(data: CreateDto): Promise<T>
  update(id: string, data: UpdateDto): Promise<T>
  delete(id: string): Promise<void>
}
```

## 骨架项目（Skeleton Projects）

在实现新功能时：
1. 搜索经过实战检验的骨架项目（Skeleton Projects）
2. 使用并行智能体（Parallel Agents）评估备选项：
   - 安全性评估（Security assessment）
   - 可扩展性分析（Extensibility analysis）
   - 相关性评分（Relevance scoring）
   - 实施计划（Implementation planning）
3. 克隆最匹配的项目作为基础
4. 在已验证的结构内进行迭代
