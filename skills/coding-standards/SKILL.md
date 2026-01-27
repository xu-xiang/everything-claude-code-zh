---
name: coding-standards
description: 适用于 TypeScript、JavaScript、React 和 Node.js 开发的通用编码标准、最佳实践和模式。
---

# 编码标准与最佳实践（Coding Standards & Best Practices）

适用于所有项目的通用编码标准。

## 代码质量原则（Code Quality Principles）

### 1. 可读性优先（Readability First）
- 代码被阅读的次数远多于编写的次数
- 使用清晰的变量和函数名称
- 优先选择自解释代码，而非过多注释
- 保持一致的格式化风格

### 2. KISS 原则（Keep It Simple, Stupid）
- 采用最简单的可行方案
- 避免过度工程（Over-engineering）
- 拒绝过早优化
- 易于理解胜过奇技淫巧

### 3. DRY 原则（Don't Repeat Yourself）
- 将公共逻辑提取到函数中
- 创建可复用的组件
- 在模块间共享工具函数（Utilities）
- 避免复制粘贴式编程

### 4. YAGNI 原则（You Aren't Gonna Need It）
- 不要在需求出现前构建功能
- 避免投机性的通用化设计
- 仅在必要时增加复杂性
- 从简单开始，在需要时重构

## TypeScript/JavaScript 标准

### 变量命名

```typescript
// ✅ 推荐：描述性名称
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// ❌ 糟糕：语义不明
const q = 'election'
const flag = true
const x = 1000
```

### 函数命名

```typescript
// ✅ 推荐：动词-名词模式
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// ❌ 糟糕：语义不明或仅有名词
async function market(id: string) { }
function similarity(a, b) { }
function email(e) { }
```

### 不可变模式（Immutability Pattern - 至关重要）

```typescript
// ✅ 始终使用展开运算符（Spread Operator）
const updatedUser = {
  ...user,
  name: 'New Name'
}

const updatedArray = [...items, newItem]

// ❌ 严禁直接修改（Mutate）
user.name = 'New Name'  // 糟糕
items.push(newItem)     // 糟糕
```

### 错误处理（Error Handling）

```typescript
// ✅ 推荐：全面的错误处理
async function fetchData(url: string) {
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}

// ❌ 糟糕：缺少错误处理
async function fetchData(url) {
  const response = await fetch(url)
  return response.json()
}
```

### Async/Await 最佳实践

```typescript
// ✅ 推荐：尽可能并行执行
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// ❌ 糟糕：非必要的串行执行
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

### 类型安全（Type Safety）

```typescript
// ✅ 推荐：定义明确的类型
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> {
  // 实现代码
}

// ❌ 糟糕：使用 'any'
function getMarket(id: any): Promise<any> {
  // 实现代码
}
```

## React 最佳实践

### 组件结构（Component Structure）

```typescript
// ✅ 推荐：带类型的函数式组件
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}

// ❌ 糟糕：无类型，结构不明
export function Button(props) {
  return <button onClick={props.onClick}>{props.children}</button>
}
```

### 自定义 Hook（Custom Hooks）

```typescript
// ✅ 推荐：可复用的自定义 Hook
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// 使用示例
const debouncedQuery = useDebounce(searchQuery, 500)
```

### 状态管理（State Management）

```typescript
// ✅ 推荐：正确的状态更新方式
const [count, setCount] = useState(0)

// 基于前一个状态的函数式更新
setCount(prev => prev + 1)

// ❌ 糟糕：直接引用状态
setCount(count + 1)  // 在异步场景下可能会获取到旧值
```

### 条件渲染（Conditional Rendering）

```typescript
// ✅ 推荐：清晰的条件渲染
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}

// ❌ 糟糕：三元运算符地狱
{isLoading ? <Spinner /> : error ? <ErrorMessage error={error} /> : data ? <DataDisplay data={data} /> : null}
```

## API 设计标准

### REST API 惯例

```
GET    /api/markets              # 列出所有市场
GET    /api/markets/:id          # 获取特定市场
POST   /api/markets              # 创建新市场
PUT    /api/markets/:id          # 更新市场（完整更新）
PATCH  /api/markets/:id          # 更新市场（部分更新）
DELETE /api/markets/:id          # 删除市场

# 用于过滤的查询参数
GET /api/markets?status=active&limit=10&offset=0
```

### 响应格式（Response Format）

```typescript
// ✅ 推荐：一致的响应结构
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

// 成功响应
return NextResponse.json({
  success: true,
  data: markets,
  meta: { total: 100, page: 1, limit: 10 }
})

// 错误响应
return NextResponse.json({
  success: false,
  error: 'Invalid request'
}, { status: 400 })
```

### 输入验证（Input Validation）

```typescript
import { z } from 'zod'

// ✅ 推荐：Schema 验证
const CreateMarketSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().min(1).max(2000),
  endDate: z.string().datetime(),
  categories: z.array(z.string()).min(1)
})

export async function POST(request: Request) {
  const body = await request.json()

  try {
    const validated = CreateMarketSchema.parse(body)
    // 使用验证后的数据继续执行
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        error: 'Validation failed',
        details: error.errors
      }, { status: 400 })
    }
  }
}
```

## 文件组织（File Organization）

### 项目结构

```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API 路由
│   ├── markets/           # 市场相关页面
│   └── (auth)/           # 认证相关页面（路由分组）
├── components/            # React 组件
│   ├── ui/               # 通用 UI 组件
│   ├── forms/            # 表单组件
│   └── layouts/          # 布局组件
├── hooks/                # 自定义 React hooks
├── lib/                  # 工具函数与配置
│   ├── api/             # API 客户端
│   ├── utils/           # 辅助函数
│   └── constants/       # 常量
├── types/                # TypeScript 类型定义
└── styles/              # 全局样式
```

### 文件命名

```
components/Button.tsx          # 组件使用 PascalCase
hooks/useAuth.ts              # Hook 使用 camelCase 并以 'use' 开头
lib/formatDate.ts             # 工具函数使用 camelCase
types/market.types.ts         # 类型定义使用 camelCase 并带 .types 后缀
```

## 注释与文档

### 何时编写注释

```typescript
// ✅ 推荐：解释“为什么”这样做，而不是“在做什么”
// 使用指数退避算法（Exponential backoff），避免在服务中断期间使 API 过载
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)

// 此处故意使用变更（Mutation），以提高大型数组的处理性能
items.push(newItem)

// ❌ 糟糕：陈述显而易见的事实
// 将计数器加 1
count++

// 将名称设置为用户的名称
name = user.name
```

### 公共 API 的 JSDoc

```typescript
/**
 * 使用语义相似度搜索市场。
 *
 * @param query - 自然语言搜索查询
 * @param limit - 最大结果数量（默认：10）
 * @returns 按相似度得分排序的市场数组
 * @throws {Error} 如果 OpenAI API 失败或 Redis 不可用时抛出错误
 *
 * @example
 * ```typescript
 * const results = await searchMarkets('election', 5)
 * console.log(results[0].name) // "Trump vs Biden"
 * ```
 */
export async function searchMarkets(
  query: string,
  limit: number = 10
): Promise<Market[]> {
  // 实现代码
}
```

## 性能最佳实践（Performance Best Practices）

### 记忆化（Memoization）

```typescript
import { useMemo, useCallback } from 'react'

// ✅ 推荐：记忆化高开销的计算
const sortedMarkets = useMemo(() => {
  return markets.sort((a, b) => b.volume - a.volume)
}, [markets])

// ✅ 推荐：记忆化回调函数
const handleSearch = useCallback((query: string) => {
  setSearchQuery(query)
}, [])
```

### 懒加载（Lazy Loading）

```typescript
import { lazy, Suspense } from 'react'

// ✅ 推荐：懒加载重型组件
const HeavyChart = lazy(() => import('./HeavyChart'))

export function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart />
    </Suspense>
  )
}
```

### 数据库查询

```typescript
// ✅ 推荐：仅选择需要的列
const { data } = await supabase
  .from('markets')
  .select('id, name, status')
  .limit(10)

// ❌ 糟糕：选择所有列
const { data } = await supabase
  .from('markets')
  .select('*')
```

## 测试标准（Testing Standards）

### 测试结构（AAA 模式）

```typescript
test('正确计算相似度', () => {
  // 安排（Arrange）
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // 执行（Act）
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // 断言（Assert）
  expect(similarity).toBe(0)
})
```

### 测试命名

```typescript
// ✅ 推荐：描述性的测试名称
test('当没有市场匹配查询时返回空数组', () => { })
test('当缺失 OpenAI API 密钥时抛出错误', () => { })
test('当 Redis 不可用时回退到子字符串搜索', () => { })

// ❌ 糟糕：模糊的测试名称
test('正常工作', () => { })
test('测试搜索', () => { })
```

## 代码异味检测（Code Smell Detection）

警惕以下反模式：

### 1. 过长函数
```typescript
// ❌ 糟糕：函数超过 50 行
function processMarketData() {
  // 100 行代码
}

// ✅ 推荐：拆分为更小的函数
function processMarketData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}
```

### 2. 过深嵌套
```typescript
// ❌ 糟糕：超过 5 层的嵌套
if (user) {
  if (user.isAdmin) {
    if (market) {
      if (market.isActive) {
        if (hasPermission) {
          // 执行操作
        }
      }
    }
  }
}

// ✅ 推荐：卫语句（Early Returns）
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return

// 执行操作
```

### 3. 魔术数字（Magic Numbers）
```typescript
// ❌ 糟糕：未解释的数字
if (retryCount > 3) { }
setTimeout(callback, 500)

// ✅ 推荐：命名的常量
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500

if (retryCount > MAX_RETRIES) { }
setTimeout(callback, DEBOUNCE_DELAY_MS)
```

**记住**：代码质量是不容妥协的。清晰、可维护的代码是实现快速开发和自信重构的基石。
