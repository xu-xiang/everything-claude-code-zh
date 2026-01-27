---
name: security-review
description: 当添加身份认证（authentication）、处理用户输入、使用凭据（secrets）、创建 API 端点或实现支付/敏感功能时，请使用此技能。提供全面的安全检查清单和模式。
---

# 安全审查技能 (Security Review Skill)

此技能确保所有代码遵循安全最佳实践，并识别潜在的漏洞。

## 何时激活

- 实现身份认证（authentication）或授权（authorization）时
- 处理用户输入或文件上传时
- 创建新的 API 端点时
- 处理凭据（secrets）或证书（credentials）时
- 实现支付功能时
- 存储或传输敏感数据时
- 集成第三方 API 时

## 安全检查清单

### 1. 凭据管理 (Secrets Management)

#### ❌ 严禁这样做
```typescript
const apiKey = "sk-proj-xxxxx"  // 硬编码凭据
const dbPassword = "password123" // 在源代码中
```

#### ✅ 务必这样做
```typescript
const apiKey = process.env.OPENAI_API_KEY
const dbUrl = process.env.DATABASE_URL

// 验证凭据是否存在
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

#### 验证步骤
- [ ] 不存在硬编码的 API 密钥、令牌（tokens）或密码
- [ ] 所有凭据均存储在环境变量中
- [ ] `.env.local` 已包含在 .gitignore 中
- [ ] Git 历史记录中没有凭据
- [ ] 生产环境凭据配置在托管平台（如 Vercel, Railway）

### 2. 输入校验 (Input Validation)

#### 始终校验用户输入
```typescript
import { z } from 'zod'

// 定义校验模式 (Schema)
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

// 在处理前校验
export async function createUser(input: unknown) {
  try {
    const validated = CreateUserSchema.parse(input)
    return await db.users.create(validated)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors }
    }
    throw error
  }
}
```

#### 文件上传校验
```typescript
function validateFileUpload(file: File) {
  // 大小检查 (最大 5MB)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('File too large (max 5MB)')
  }

  // 类型检查
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type')
  }

  // 后缀检查
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif']
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error('Invalid file extension')
  }

  return true
}
```

#### 验证步骤
- [ ] 所有用户输入均通过模式（schemas）校验
- [ ] 限制文件上传（大小、类型、后缀）
- [ ] 不在查询中直接使用原始用户输入
- [ ] 使用白名单校验（而非黑名单）
- [ ] 错误消息不泄露敏感信息

### 3. SQL 注入防护 (SQL Injection Prevention)

#### ❌ 严禁拼接 SQL 字符串
```typescript
// 危险 - 存在 SQL 注入漏洞
const query = `SELECT * FROM users WHERE email = '${userEmail}'`
await db.query(query)
```

#### ✅ 始终使用参数化查询
```typescript
// 安全 - 参数化查询
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// 或者使用原生 SQL
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
)
```

#### 验证步骤
- [ ] 所有数据库查询均使用参数化查询
- [ ] SQL 中没有字符串拼接
- [ ] 正确使用 ORM 或查询构建器（query builder）
- [ ] Supabase 查询已正确清理（sanitized）

### 4. 认证与授权 (Authentication & Authorization)

#### JWT 令牌处理
```typescript
// ❌ 错误：使用 localStorage (易受 XSS 攻击)
localStorage.setItem('token', token)

// ✅ 正确：使用 httpOnly cookies
res.setHeader('Set-Cookie',
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`)
```

#### 授权检查
```typescript
export async function deleteUser(userId: string, requesterId: string) {
  // 始终先验证授权
  const requester = await db.users.findUnique({
    where: { id: requesterId }
  })

  if (requester.role !== 'admin') {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 403 }
    )
  }

  // 执行删除
  await db.users.delete({ where: { id: userId } })
}
```

#### 行级安全性 (Supabase RLS)
```sql
-- 在所有表上启用 RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 用户只能查看自己的数据
CREATE POLICY "Users view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- 用户只能更新自己的数据
CREATE POLICY "Users update own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

#### 验证步骤
- [ ] 令牌存储在 httpOnly cookies 中（而非 localStorage）
- [ ] 在敏感操作前进行授权检查
- [ ] 在 Supabase 中启用了行级安全性（Row Level Security）
- [ ] 实现了基于角色的访问控制（RBAC）
- [ ] 会话管理（Session management）安全

### 5. XSS 防护 (XSS Prevention)

#### 清理 HTML
```typescript
import DOMPurify from 'isomorphic-dompurify'

// 始终清理用户提供的 HTML
function renderUserContent(html: string) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  })
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

#### 内容安全策略 (CSP)
```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://api.example.com;
    `.replace(/\s{2,}/g, ' ').trim()
  }
]
```

#### 验证步骤
- [ ] 已清理用户提供的 HTML
- [ ] 配置了 CSP 响应头
- [ ] 没有未经校验的动态内容渲染
- [ ] 使用了 React 内置的 XSS 防护机制

### 6. CSRF 防护 (CSRF Protection)

#### CSRF 令牌
```typescript
import { csrf } from '@/lib/csrf'

export async function POST(request: Request) {
  const token = request.headers.get('X-CSRF-Token')

  if (!csrf.verify(token)) {
    return NextResponse.json(
      { error: 'Invalid CSRF token' },
      { status: 403 }
    )
  }

  // 处理请求
}
```

#### SameSite Cookies
```typescript
res.setHeader('Set-Cookie',
  `session=${sessionId}; HttpOnly; Secure; SameSite=Strict`)
```

#### 验证步骤
- [ ] 对状态变更操作使用了 CSRF 令牌
- [ ] 所有 cookies 均设置了 SameSite=Strict
- [ ] 实现了双重提交 cookie 模式（double-submit cookie pattern）

### 7. 速率限制 (Rate Limiting)

#### API 速率限制
```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 100, // 每个窗口 100 次请求
  message: 'Too many requests'
})

// 应用到路由
app.use('/api/', limiter)
```

#### 高消耗操作
```typescript
// 对搜索操作执行更严格的速率限制
const searchLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 分钟
  max: 10, // 每分钟 10 次请求
  message: 'Too many search requests'
})

app.use('/api/search', searchLimiter)
```

#### 验证步骤
- [ ] 在所有 API 端点上启用了速率限制
- [ ] 对高消耗操作执行更严格的限制
- [ ] 基于 IP 的速率限制
- [ ] 基于用户的速率限制（已认证用户）

### 8. 敏感数据泄露 (Sensitive Data Exposure)

#### 日志记录
```typescript
// ❌ 错误：记录敏感数据
console.log('User login:', { email, password })
console.log('Payment:', { cardNumber, cvv })

// ✅ 正确：脱敏敏感数据
console.log('User login:', { email, userId })
console.log('Payment:', { last4: card.last4, userId })
```

#### 错误消息
```typescript
// ❌ 错误：暴露内部细节
catch (error) {
  return NextResponse.json(
    { error: error.message, stack: error.stack },
    { status: 500 }
  )
}

// ✅ 正确：通用的错误消息
catch (error) {
  console.error('Internal error:', error)
  return NextResponse.json(
    { error: 'An error occurred. Please try again.' },
    { status: 500 }
  )
}
```

#### 验证步骤
- [ ] 日志中不含密码、令牌或凭据
- [ ] 向用户展示通用的错误消息
- [ ] 仅在服务器日志中记录详细错误
- [ ] 不向用户暴露堆栈轨迹（stack traces）

### 9. 区块链安全 (Solana)

#### 钱包验证
```typescript
import { verify } from '@solana/web3.js'

async function verifyWalletOwnership(
  publicKey: string,
  signature: string,
  message: string
) {
  try {
    const isValid = verify(
      Buffer.from(message),
      Buffer.from(signature, 'base64'),
      Buffer.from(publicKey, 'base64')
    )
    return isValid
  } catch (error) {
    return false
  }
}
```

#### 交易验证
```typescript
async function verifyTransaction(transaction: Transaction) {
  // 验证收款人
  if (transaction.to !== expectedRecipient) {
    throw new Error('Invalid recipient')
  }

  // 验证金额
  if (transaction.amount > maxAmount) {
    throw new Error('Amount exceeds limit')
  }

  // 验证用户余额是否充足
  const balance = await getBalance(transaction.from)
  if (balance < transaction.amount) {
    throw new Error('Insufficient balance')
  }

  return true
}
```

#### 验证步骤
- [ ] 验证了钱包签名
- [ ] 校验了交易详情
- [ ] 交易前进行余额检查
- [ ] 不存在盲签（blind signing）交易

### 10. 依赖项安全 (Dependency Security)

#### 定期更新
```bash
# 检查漏洞
npm audit

# 自动修复可修复的问题
npm audit fix

# 更新依赖
npm update

# 检查过期的包
npm outdated
```

#### 锁定文件 (Lock Files)
```bash
# 始终提交 lock 文件
git add package-lock.json

# 在 CI/CD 中使用以确保可重现的构建
npm ci  # 而非 npm install
```

#### 验证步骤
- [ ] 依赖项保持最新
- [ ] 无已知漏洞（npm audit clean）
- [ ] 已提交 lock 文件
- [ ] 在 GitHub 上启用了 Dependabot
- [ ] 定期执行安全更新

## 安全测试

### 自动化安全测试
```typescript
// 测试身份认证
test('requires authentication', async () => {
  const response = await fetch('/api/protected')
  expect(response.status).toBe(401)
})

// 测试授权
test('requires admin role', async () => {
  const response = await fetch('/api/admin', {
    headers: { Authorization: `Bearer ${userToken}` }
  })
  expect(response.status).toBe(403)
})

// 测试输入校验
test('rejects invalid input', async () => {
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ email: 'not-an-email' })
  })
  expect(response.status).toBe(400)
})

// 测试速率限制
test('enforces rate limits', async () => {
  const requests = Array(101).fill(null).map(() =>
    fetch('/api/endpoint')
  )

  const responses = await Promise.all(requests)
  const tooManyRequests = responses.filter(r => r.status === 429)

  expect(tooManyRequests.length).toBeGreaterThan(0)
})
```

## 部署前安全检查清单

在**任何**生产环境部署之前：

- [ ] **凭据 (Secrets)**：无硬编码凭据，全部位于环境变量中
- [ ] **输入校验**：所有用户输入均已校验
- [ ] **SQL 注入**：所有查询均已参数化
- [ ] **XSS**：用户内容已清理
- [ ] **CSRF**：防护已启用
- [ ] **身份认证**：正确的令牌处理
- [ ] **授权**：角色检查已就位
- [ ] **速率限制**：在所有端点上启用
- [ ] **HTTPS**：在生产环境中强制执行
- [ ] **安全响应头**：已配置 CSP, X-Frame-Options
- [ ] **错误处理**：错误信息中无敏感数据
- [ ] **日志记录**：日志中无敏感数据
- [ ] **依赖项**：已更新且无漏洞
- [ ] **行级安全性**：在 Supabase 中启用
- [ ] **CORS**：已正确配置
- [ ] **文件上传**：已校验（大小、类型）
- [ ] **钱包签名**：已验证（如果是区块链项目）

## 资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js 安全指南](https://nextjs.org/docs/security)
- [Supabase 安全指南](https://supabase.com/docs/guides/auth)
- [Web Security Academy](https://portswigger.net/web-security)

---

**请记住**：安全并非可选项。一个漏洞就可能危害整个平台。如有疑虑，请宁可信其有，从严处理。
