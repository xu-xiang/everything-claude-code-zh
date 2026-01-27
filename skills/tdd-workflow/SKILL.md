---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
---

# 测试驱动开发 (TDD) 工作流

此技能（Skill）确保所有代码开发都遵循具有全面测试覆盖率的测试驱动开发（TDD）原则。

## 何时启用

- 编写新功能或新特性
- 修复 Bug 或问题
- 重构现有代码
- 添加 API 接口
- 创建新组件

## 核心原则

### 1. 测试先于代码 (Tests BEFORE Code)
始终先编写测试，然后编写代码使测试通过。

### 2. 覆盖率要求
- 至少 80% 的覆盖率（单元测试 + 集成测试 + 端到端测试）
- 覆盖所有边缘情况
- 测试所有错误场景
- 验证边界条件

### 3. 测试类型

#### 单元测试 (Unit Tests)
- 单个函数和实用程序
- 组件逻辑
- 纯函数
- 辅助函数和工具类

#### 集成测试 (Integration Tests)
- API 接口
- 数据库操作
- 服务间交互
- 外部 API 调用

#### 端到端测试 (E2E Tests - Playwright)
- 关键用户流程
- 完整的工作流
- 浏览器自动化
- UI 交互

## TDD 工作流步骤

### 第 1 步：编写用户旅程 (User Journeys)
```
作为 [角色]，我想要 [动作]，以便 [收益]

示例：
作为一个用户，我想要通过语义搜索市场，
以便即使没有精确的关键词也能找到相关的市场。
```

### 第 2 步：生成测试用例
为每个用户旅程创建全面的测试用例：

```typescript
describe('Semantic Search', () => {
  it('returns relevant markets for query', async () => {
    // 测试实现
  })

  it('handles empty query gracefully', async () => {
    // 处理边缘情况
  })

  it('falls back to substring search when Redis unavailable', async () => {
    // 测试回退行为
  })

  it('sorts results by similarity score', async () => {
    // 测试排序逻辑
  })
})
```

### 第 3 步：运行测试（预期失败）
```bash
npm test
# 测试应该失败 - 因为我们还没有实现功能
```

### 第 4 步：编写代码
编写最少量的代码使测试通过：

```typescript
// 由测试引导的实现
export async function searchMarkets(query: string) {
  // 在此处实现
}
```

### 第 5 步：再次运行测试
```bash
npm test
# 测试现在应该通过
```

### 第 6 步：重构 (Refactor)
在保持测试通过的同时提高代码质量：
- 消除重复
- 改进命名
- 优化性能
- 增强可读性

### 第 7 步：验证覆盖率
```bash
npm run test:coverage
# 验证是否达到 80% 以上的覆盖率
```

## 测试模式

### 单元测试模式 (Jest/Vitest)
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API 集成测试模式
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('returns markets successfully', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('validates query parameters', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('handles database errors gracefully', async () => {
    // 模拟数据库故障
    const request = new NextRequest('http://localhost/api/markets')
    // 测试错误处理
  })
})
```

### 端到端测试模式 (Playwright)
```typescript
import { test, expect } from '@playwright/test'

test('user can search and filter markets', async ({ page }) => {
  // 导航到市场页面
  await page.goto('/')
  await page.click('a[href="/markets"]')

  // 验证页面已加载
  await expect(page.locator('h1')).toContainText('Markets')

  // 搜索市场
  await page.fill('input[placeholder="Search markets"]', 'election')

  // 等待防抖和结果
  await page.waitForTimeout(600)

  // 验证搜索结果已显示
  const results = page.locator('[data-testid="market-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })

  // 验证结果包含搜索词
  const firstResult = results.first()
  await expect(firstResult).toContainText('election', { ignoreCase: true })

  // 按状态筛选
  await page.click('button:has-text("Active")')

  // 验证过滤后的结果
  await expect(results).toHaveCount(3)
})

test('user can create a new market', async ({ page }) => {
  // 首先登录
  await page.goto('/creator-dashboard')

  // 填写市场创建表单
  await page.fill('input[name="name"]', 'Test Market')
  await page.fill('textarea[name="description"]', 'Test description')
  await page.fill('input[name="endDate"]', '2025-12-31')

  // 提交表单
  await page.click('button[type="submit"]')

  // 验证成功消息
  await expect(page.locator('text=Market created successfully')).toBeVisible()

  // 验证重定向到市场页面
  await expect(page).toHaveURL(/\/markets\/test-market/)
})
```

## 测试文件组织

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # 单元测试
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # 集成测试
└── e2e/
    ├── markets.spec.ts               # 端到端测试
    ├── trading.spec.ts
    └── auth.spec.ts
```

## 模拟（Mocking）外部服务

### Supabase 模拟
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### Redis 模拟
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

### OpenAI 模拟
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // 模拟 1536 维向量嵌入
  ))
}))
```

## 测试覆盖率验证

### 运行覆盖率报告
```bash
npm run test:coverage
```

### 覆盖率阈值
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## 应避免的常见测试错误

### ❌ 错误：测试实现细节
```typescript
// 不要测试内部状态
expect(component.state.count).toBe(5)
```

### ✅ 正确：测试用户可见的行为
```typescript
// 测试用户看到的内容
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### ❌ 错误：脆弱的选择器
```typescript
// 容易因样式调整而失效
await page.click('.css-class-xyz')
```

### ✅ 正确：语义化选择器
```typescript
// 对更改更具鲁棒性
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### ❌ 错误：缺乏测试隔离
```typescript
// 测试相互依赖
test('creates user', () => { /* ... */ })
test('updates same user', () => { /* 依赖上一个测试的结果 */ })
```

### ✅ 正确：独立测试
```typescript
// 每个测试设置自己的数据
test('creates user', () => {
  const user = createTestUser()
  // 测试逻辑
})

test('updates user', () => {
  const user = createTestUser()
  // 更新逻辑
})
```

## 持续测试

### 开发过程中的监听模式 (Watch Mode)
```bash
npm test -- --watch
# 文件更改时自动运行测试
```

### Pre-Commit 钩子
```bash
# 每次 commit 前运行
npm test && npm run lint
```

### CI/CD 集成
```yaml
# GitHub Actions
- name: Run Tests
  run: npm test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## 最佳实践

1. **先写测试** - 始终遵循 TDD
2. **一个测试一个断言** - 专注于单一行为
3. **描述性的测试名称** - 解释测试的内容
4. **准备-执行-断言 (Arrange-Act-Assert)** - 清晰的测试结构
5. **模拟外部依赖** - 隔离单元测试
6. **测试边缘情况** - Null, undefined, 空, 超大值
7. **测试错误路径** - 不仅仅是“快乐路径” (Happy Paths)
8. **保持测试快速** - 每个单元测试 < 50ms
9. **测试后清理** - 消除副作用
10. **查看覆盖率报告** - 识别覆盖漏洞

## 成功指标

- 达到 80% 以上的代码覆盖率
- 所有测试均通过（显示为绿色）
- 没有跳过或禁用的测试
- 快速的测试执行（单元测试 < 30s）
- 端到端测试覆盖了关键用户流程
- 测试能在生产环境之前捕获 Bug

---

**请记住**：测试不是可选的。它们是安全网，能够让你有信心进行重构、快速开发并确保生产环境的可靠性。
