# 项目指南技能（Project Guidelines Skill，示例）

这是一个特定项目的技能（Skill）示例。请将其用作你自定义项目的模板。

基于真实的生产应用：[Zenith](https://zenith.chat) - AI 驱动的客户发现平台。

---

## 何时使用 (When to Use)

在处理该特定项目时参考此技能。项目技能包含：
- 架构概览 (Architecture overview)
- 文件结构 (File structure)
- 代码模式 (Code patterns)
- 测试要求 (Testing requirements)
- 部署工作流 (Deployment workflow)

---

## 架构概览 (Architecture Overview)

**技术栈 (Tech Stack)：**
- **前端 (Frontend)**：Next.js 15 (App Router), TypeScript, React
- **后端 (Backend)**：FastAPI (Python), Pydantic 模型
- **数据库 (Database)**：Supabase (PostgreSQL)
- **AI**：Claude API（支持工具调用与结构化输出）
- **部署 (Deployment)**：Google Cloud Run
- **测试 (Testing)**：Playwright (E2E), pytest (后端), React Testing Library

**服务 (Services)：**
```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  Next.js 15 + TypeScript + TailwindCSS                     │
│  Deployed: Vercel / Cloud Run                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         Backend                             │
│  FastAPI + Python 3.11 + Pydantic                          │
│  Deployed: Cloud Run                                       │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Supabase │   │  Claude  │   │  Redis   │
        │ Database │   │   API    │   │  Cache   │
        └──────────┘   └──────────┘   └──────────┘
```

---

## 文件结构 (File Structure)

```
project/
├── frontend/
│   └── src/
│       ├── app/              # Next.js App Router 页面
│       │   ├── api/          # API 路由
│       │   ├── (auth)/       # 身份验证保护的路由
│       │   └── workspace/    # 主应用工作区
│       ├── components/       # React 组件
│       │   ├── ui/           # 基础 UI 组件
│       │   ├── forms/        # 表单组件
│       │   └── layouts/      # 布局组件
│       ├── hooks/            # 自定义 React 钩子 (Hooks)
│       ├── lib/              # 工具库
│       ├── types/            # TypeScript 类型定义
│       └── config/           # 配置
│
├── backend/
│   ├── routers/              # FastAPI 路由处理器
│   ├── models.py             # Pydantic 模型
│   ├── main.py               # FastAPI 应用入口
│   ├── auth_system.py        # 身份验证系统
│   ├── database.py           # 数据库操作
│   ├── services/             # 业务逻辑
│   └── tests/                # pytest 测试
│
├── deploy/                   # 部署配置
├── docs/                     # 文档
└── scripts/                  # 工具脚本
```

---

## 代码模式 (Code Patterns)

### API 响应格式 (FastAPI)

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, data: T) -> "ApiResponse[T]":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> "ApiResponse[T]":
        return cls(success=False, error=error)
```

### 前端 API 调用 (TypeScript)

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`/api${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      return { success: false, error: `HTTP ${response.status}` }
    }

    return await response.json()
  } catch (error) {
    return { success: false, error: String(error) }
  }
}
```

### Claude AI 集成 (结构化输出)

```python
from anthropic import Anthropic
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float

async def analyze_with_claude(content: str) -> AnalysisResult:
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}],
        tools=[{
            "name": "provide_analysis",
            "description": "Provide structured analysis",
            "input_schema": AnalysisResult.model_json_schema()
        }],
        tool_choice={"type": "tool", "name": "provide_analysis"}
    )

    # 提取工具调用结果
    tool_use = next(
        block for block in response.content
        if block.type == "tool_use"
    )

    return AnalysisResult(**tool_use.input)
```

### 自定义钩子 (React Hooks)

```typescript
import { useState, useCallback } from 'react'

interface UseApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useApi<T>(
  fetchFn: () => Promise<ApiResponse<T>>
) {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  })

  const execute = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }))

    const result = await fetchFn()

    if (result.success) {
      setState({ data: result.data!, loading: false, error: null })
    } else {
      setState({ data: null, loading: false, error: result.error! })
    }
  }, [fetchFn])

  return { ...state, execute }
}
```

---

## 测试要求 (Testing Requirements)

### 后端 (pytest)

```bash
# 运行所有测试
poetry run pytest tests/

# 运行并生成覆盖率报告
poetry run pytest tests/ --cov=. --cov-report=html

# 运行特定测试文件
poetry run pytest tests/test_auth.py -v
```

**测试结构：**
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### 前端 (React Testing Library)

```bash
# 运行测试
npm run test

# 运行并生成覆盖率报告
npm run test -- --coverage

# 运行 E2E 测试
npm run test:e2e
```

**测试结构：**
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { WorkspacePanel } from './WorkspacePanel'

describe('WorkspacePanel', () => {
  it('renders workspace correctly', () => {
    render(<WorkspacePanel />)
    expect(screen.getByRole('main')).toBeInTheDocument()
  })

  it('handles session creation', async () => {
    render(<WorkspacePanel />)
    fireEvent.click(screen.getByText('New Session'))
    expect(await screen.findByText('Session created')).toBeInTheDocument()
  })
})
```

---

## 部署工作流 (Deployment Workflow)

### 部署前自查清单 (Pre-Deployment Checklist)

- [ ] 所有测试在本地通过
- [ ] `npm run build` 成功 (前端)
- [ ] `poetry run pytest` 通过 (后端)
- [ ] 无硬编码的秘钥 (Secrets)
- [ ] 环境变量已记录文档
- [ ] 数据库迁移就绪

### 部署命令 (Deployment Commands)

```bash
# 构建并部署前端
cd frontend && npm run build
gcloud run deploy frontend --source .

# 构建并部署后端
cd backend
gcloud run deploy backend --source .
```

### 环境变量 (Environment Variables)

```bash
# 前端 (.env.local)
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# 后端 (.env)
DATABASE_URL=postgresql://...
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
```

---

## 核心规则 (Critical Rules)

1. 代码、注释或文档中**严禁使用 Emoji**
2. **不可变性 (Immutability)** - 永远不要直接改变对象或数组
3. **测试驱动开发 (TDD)** - 在实现之前编写测试
4. 最小 **80% 测试覆盖率**
5. **大量小文件** - 通常为 200-400 行，最多 800 行
6. 生产代码中**严禁使用 console.log**
7. 使用 try/catch 进行**妥善的错误处理**
8. 使用 Pydantic/Zod 进行**输入验证**

---

## 相关技能 (Related Skills)

- `coding-standards.md` - 通用代码最佳实践
- `backend-patterns.md` - API 与数据库模式
- `frontend-patterns.md` - React 与 Next.js 模式
- `tdd-workflow/` - 测试驱动开发 (TDD) 方法论
