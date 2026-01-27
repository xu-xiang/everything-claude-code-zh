# 项目示例 CLAUDE.md

这是一个项目级 CLAUDE.md 文件的示例。请将其放置在项目根目录下。

## 项目概览

[简要描述您的项目 - 功能、技术栈]

## 核心规则

### 1. 代码组织

- 倾向于使用多个小文件，而非少数大文件
- 高内聚，低耦合
- 通常为 200-400 行，单文件最大不超过 800 行
- 按功能/领域（Feature/Domain）组织，而非按类型组织

### 2. 代码风格

- 代码、注释或文档中不得使用表情符号（Emoji）
- 始终坚持不可变性（Immutability） - 严禁直接修改对象或数组
- 生产代码中严禁使用 `console.log`
- 使用 try/catch 进行妥善的错误处理
- 使用 Zod 或类似工具进行输入验证

### 3. 测试

- 测试驱动开发（TDD）：先写测试
- 最低 80% 的覆盖率
- 为工具函数编写单元测试
- 为 API 编写集成测试
- 为核心流程编写端到端（E2E）测试

### 4. 安全

- 严禁硬编码秘钥（Secrets）
- 敏感数据使用环境变量
- 验证所有用户输入
- 仅使用参数化查询（Parameterized queries）
- 启用跨站请求伪造（CSRF）防护

## 文件结构

```
src/
|-- app/              # Next.js 应用路由
|-- components/       # 可复用的 UI 组件
|-- hooks/            # 自定义 React hooks
|-- lib/              # 工具库
|-- types/            # TypeScript 定义
```

## 关键模式

### API 响应格式

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}
```

### 错误处理

```typescript
try {
  const result = await operation()
  return { success: true, data: result }
} catch (error) {
  console.error('操作失败:', error)
  return { success: false, error: '用户友好提示信息' }
}
```

## 环境变量

```bash
# 必填
DATABASE_URL=
API_KEY=

# 选填
DEBUG=false
```

## 可用命令

- `/tdd` - 测试驱动开发（TDD）工作流
- `/plan` - 创建实现方案
- `/code-review` - 代码质量评审
- `/build-fix` - 修复构建错误

## Git 工作流

- 约定式提交（Conventional commits）：`feat:`, `fix:`, `refactor:`, `docs:`, `test:`
- 严禁直接提交到 main 分支
- 合并请求（PRs）必须经过评审
- 所有测试必须通过后方可合并
