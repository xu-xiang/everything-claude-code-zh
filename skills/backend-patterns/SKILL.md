---
name: backend-patterns
description: 后端架构模式、API 设计、数据库优化，以及 Node.js、Express 和 Next.js API 路由的服务端最佳实践。
---

# 后端开发模式

用于构建可扩展服务端应用程序的后端架构模式与最佳实践。

## API 设计模式

### RESTful API 结构

```typescript
// ✅ 基于资源的 URL
GET    /api/markets                 # 列出资源
GET    /api/markets/:id             # 获取单个资源
POST   /api/markets                 # 创建资源
PUT    /api/markets/:id             # 替换资源
PATCH  /api/markets/:id             # 更新资源
DELETE /api/markets/:id             # 删除资源

// ✅ 用于过滤、排序、分页的查询参数
GET /api/markets?status=active&sort=volume&limit=20&offset=0
```

### 仓库模式 (Repository Pattern)

```typescript
// 抽象数据访问逻辑
interface MarketRepository {
  findAll(filters?: MarketFilters): Promise<Market[]>
  findById(id: string): Promise<Market | null>
  create(data: CreateMarketDto): Promise<Market>
  update(id: string, data: UpdateMarketDto): Promise<Market>
  delete(id: string): Promise<void>
}

class SupabaseMarketRepository implements MarketRepository {
  async findAll(filters?: MarketFilters): Promise<Market[]> {
    let query = supabase.from('markets').select('*')

    if (filters?.status) {
      query = query.eq('status', filters.status)
    }

    if (filters?.limit) {
      query = query.limit(filters.limit)
    }

    const { data, error } = await query

    if (error) throw new Error(error.message)
    return data
  }

  // 其他方法...
}
```

### 服务层模式 (Service Layer Pattern)

```typescript
// 业务逻辑与数据访问分离
class MarketService {
  constructor(private marketRepo: MarketRepository) {}

  async searchMarkets(query: string, limit: number = 10): Promise<Market[]> {
    // 业务逻辑
    const embedding = await generateEmbedding(query)
    const results = await this.vectorSearch(embedding, limit)

    // 获取完整数据
    const markets = await this.marketRepo.findByIds(results.map(r => r.id))

    // 按相似度排序
    return markets.sort((a, b) => {
      const scoreA = results.find(r => r.id === a.id)?.score || 0
      const scoreB = results.find(r => r.id === b.id)?.score || 0
      return scoreA - scoreB
    })
  }

  private async vectorSearch(embedding: number[], limit: number) {
    // 向量搜索实现
  }
}
```

### 中间件模式 (Middleware Pattern)

```typescript
// 请求/响应处理流水线
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const token = req.headers.authorization?.replace('Bearer ', '')

    if (!token) {
      return res.status(401).json({ error: 'Unauthorized' })
    }

    try {
      const user = await verifyToken(token)
      req.user = user
      return handler(req, res)
    } catch (error) {
      return res.status(401).json({ error: 'Invalid token' })
    }
  }
}

// 使用方法
export default withAuth(async (req, res) => {
  // 处理器可以访问 req.user
})
```

## 数据库模式

### 查询优化

```typescript
// ✅ 推荐：仅选择需要的列
const { data } = await supabase
  .from('markets')
  .select('id, name, status, volume')
  .eq('status', 'active')
  .order('volume', { ascending: false })
  .limit(10)

// ❌ 不推荐：选择所有内容
const { data } = await supabase
  .from('markets')
  .select('*')
```

### 防止 N+1 查询

```typescript
// ❌ 不推荐：N+1 查询问题
const markets = await getMarkets()
for (const market of markets) {
  market.creator = await getUser(market.creator_id)  // N 次查询
}

// ✅ 推荐：批量获取
const markets = await getMarkets()
const creatorIds = markets.map(m => m.creator_id)
const creators = await getUsers(creatorIds)  // 1 次查询
const creatorMap = new Map(creators.map(c => [c.id, c]))

markets.forEach(market => {
  market.creator = creatorMap.get(market.creator_id)
})
```

### 事务模式 (Transaction Pattern)

```typescript
async function createMarketWithPosition(
  marketData: CreateMarketDto,
  positionData: CreatePositionDto
) {
  // 使用 Supabase 事务
  const { data, error } = await supabase.rpc('create_market_with_position', {
    market_data: marketData,
    position_data: positionData
  })

  if (error) throw new Error('Transaction failed')
  return data
}

// Supabase 中的 SQL 函数
CREATE OR REPLACE FUNCTION create_market_with_position(
  market_data jsonb,
  position_data jsonb
)
RETURNS jsonb
LANGUAGE plpgsql
AS $$
BEGIN
  -- 自动开始事务
  INSERT INTO markets VALUES (market_data);
  INSERT INTO positions VALUES (position_data);
  RETURN jsonb_build_object('success', true);
EXCEPTION
  WHEN OTHERS THEN
    -- 自动回滚
    RETURN jsonb_build_object('success', false, 'error', SQLERRM);
END;
$$;
```

## 缓存策略

### Redis 缓存层

```typescript
class CachedMarketRepository implements MarketRepository {
  constructor(
    private baseRepo: MarketRepository,
    private redis: RedisClient
  ) {}

  async findById(id: string): Promise<Market | null> {
    // 首先检查缓存
    const cached = await this.redis.get(`market:${id}`)

    if (cached) {
      return JSON.parse(cached)
    }

    // 缓存未命中 - 从数据库获取
    const market = await this.baseRepo.findById(id)

    if (market) {
      // 缓存 5 分钟
      await this.redis.setex(`market:${id}`, 300, JSON.stringify(market))
    }

    return market
  }

  async invalidateCache(id: string): Promise<void> {
    await this.redis.del(`market:${id}`)
  }
}
```

### 旁路缓存模式 (Cache-Aside Pattern)

```typescript
async function getMarketWithCache(id: string): Promise<Market> {
  const cacheKey = `market:${id}`

  // 尝试缓存
  const cached = await redis.get(cacheKey)
  if (cached) return JSON.parse(cached)

  // 缓存未命中 - 从数据库获取
  const market = await db.markets.findUnique({ where: { id } })

  if (!market) throw new Error('Market not found')

  // 更新缓存
  await redis.setex(cacheKey, 300, JSON.stringify(market))

  return market
}
```

## 错误处理模式

### 集中式错误处理器

```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message)
    Object.setPrototypeOf(this, ApiError.prototype)
  }
}

export function errorHandler(error: unknown, req: Request): Response {
  if (error instanceof ApiError) {
    return NextResponse.json({
      success: false,
      error: error.message
    }, { status: error.statusCode })
  }

  if (error instanceof z.ZodError) {
    return NextResponse.json({
      success: false,
      error: 'Validation failed',
      details: error.errors
    }, { status: 400 })
  }

  // 记录非预期错误
  console.error('Unexpected error:', error)

  return NextResponse.json({
    success: false,
    error: 'Internal server error'
  }, { status: 500 })
}

// 使用方法
export async function GET(request: Request) {
  try {
    const data = await fetchData()
    return NextResponse.json({ success: true, data })
  } catch (error) {
    return errorHandler(error, request)
  }
}
```

### 指数退避重试 (Retry with Exponential Backoff)

```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error

      if (i < maxRetries - 1) {
        // 指数退避：1s, 2s, 4s
        const delay = Math.pow(2, i) * 1000
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }

  throw lastError!
}

// 使用方法
const data = await fetchWithRetry(() => fetchFromAPI())
```

## 身份验证与授权

### JWT 令牌验证

```typescript
import jwt from 'jsonwebtoken'

interface JWTPayload {
  userId: string
  email: string
  role: 'admin' | 'user'
}

export function verifyToken(token: string): JWTPayload {
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload
    return payload
  } catch (error) {
    throw new ApiError(401, 'Invalid token')
  }
}

export async function requireAuth(request: Request) {
  const token = request.headers.get('authorization')?.replace('Bearer ', '')

  if (!token) {
    throw new ApiError(401, 'Missing authorization token')
  }

  return verifyToken(token)
}

// 在 API 路由中使用
export async function GET(request: Request) {
  const user = await requireAuth(request)

  const data = await getDataForUser(user.userId)

  return NextResponse.json({ success: true, data })
}
```

### 基于角色的访问控制 (RBAC)

```typescript
type Permission = 'read' | 'write' | 'delete' | 'admin'

interface User {
  id: string
  role: 'admin' | 'moderator' | 'user'
}

const rolePermissions: Record<User['role'], Permission[]> = {
  admin: ['read', 'write', 'delete', 'admin'],
  moderator: ['read', 'write', 'delete'],
  user: ['read', 'write']
}

export function hasPermission(user: User, permission: Permission): boolean {
  return rolePermissions[user.role].includes(permission)
}

export function requirePermission(permission: Permission) {
  return (handler: (request: Request, user: User) => Promise<Response>) => {
    return async (request: Request) => {
      const user = await requireAuth(request)

      if (!hasPermission(user, permission)) {
        throw new ApiError(403, 'Insufficient permissions')
      }

      return handler(request, user)
    }
  }
}

// 使用方法 - 高阶函数 (HOF) 包装处理器
export const DELETE = requirePermission('delete')(
  async (request: Request, user: User) => {
    // 处理器接收已验证身份且具备权限的用户
    return new Response('Deleted', { status: 200 })
  }
)
```

## 速率限制

### 简单的内存速率限制器

```typescript
class RateLimiter {
  private requests = new Map<string, number[]>()

  async checkLimit(
    identifier: string,
    maxRequests: number,
    windowMs: number
  ): Promise<boolean> {
    const now = Date.now()
    const requests = this.requests.get(identifier) || []

    // 移除窗口外的旧请求
    const recentRequests = requests.filter(time => now - time < windowMs)

    if (recentRequests.length >= maxRequests) {
      return false  // 超过速率限制
    }

    // 添加当前请求
    recentRequests.push(now)
    this.requests.set(identifier, recentRequests)

    return true
  }
}

const limiter = new RateLimiter()

export async function GET(request: Request) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown'

  const allowed = await limiter.checkLimit(ip, 100, 60000)  // 100 req/min

  if (!allowed) {
    return NextResponse.json({
      error: 'Rate limit exceeded'
    }, { status: 429 })
  }

  // 继续处理请求
}
```

## 后台作业与队列

### 简单队列模式

```typescript
class JobQueue<T> {
  private queue: T[] = []
  private processing = false

  async add(job: T): Promise<void> {
    this.queue.push(job)

    if (!this.processing) {
      this.process()
    }
  }

  private async process(): Promise<void> {
    this.processing = true

    while (this.queue.length > 0) {
      const job = this.queue.shift()!

      try {
        await this.execute(job)
      } catch (error) {
        console.error('Job failed:', error)
      }
    }

    this.processing = false
  }

  private async execute(job: T): Promise<void> {
    // 作业执行逻辑
  }
}

// 用于索引市场的用法
interface IndexJob {
  marketId: string
}

const indexQueue = new JobQueue<IndexJob>()

export async function POST(request: Request) {
  const { marketId } = await request.json()

  // 添加到队列而不是阻塞
  await indexQueue.add({ marketId })

  return NextResponse.json({ success: true, message: 'Job queued' })
}
```

## 日志与监控

### 结构化日志

```typescript
interface LogContext {
  userId?: string
  requestId?: string
  method?: string
  path?: string
  [key: string]: unknown
}

class Logger {
  log(level: 'info' | 'warn' | 'error', message: string, context?: LogContext) {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...context
    }

    console.log(JSON.stringify(entry))
  }

  info(message: string, context?: LogContext) {
    this.log('info', message, context)
  }

  warn(message: string, context?: LogContext) {
    this.log('warn', message, context)
  }

  error(message: string, error: Error, context?: LogContext) {
    this.log('error', message, {
      ...context,
      error: error.message,
      stack: error.stack
    })
  }
}

const logger = new Logger()

// 使用方法
export async function GET(request: Request) {
  const requestId = crypto.randomUUID()

  logger.info('Fetching markets', {
    requestId,
    method: 'GET',
    path: '/api/markets'
  })

  try {
    const markets = await fetchMarkets()
    return NextResponse.json({ success: true, data: markets })
  } catch (error) {
    logger.error('Failed to fetch markets', error as Error, { requestId })
    return NextResponse.json({ error: 'Internal error' }, { status: 500 })
  }
}
```

**提示**：后端模式支持构建可扩展且易于维护的服务端应用程序。请根据你的复杂度需求选择合适的模式。
