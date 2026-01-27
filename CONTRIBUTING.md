# 贡献指南（Contributing to Everything Claude Code）

感谢你参与贡献。本仓库旨在成为 Claude Code 用户的社区资源。

## 我们在寻找什么（What We're Looking For）

### 智能体（Agents）

能出色处理特定任务的新智能体（Agents）：
- 特定语言的审查器（Python, Go, Rust）
- 框架专家（Django, Rails, Laravel, Spring）
- DevOps 专家（Kubernetes, Terraform, CI/CD）
- 领域专家（ML 流水线, 数据工程, 移动端）

### 技能（Skills）

工作流（Workflow）定义和领域知识：
- 语言最佳实践
- 框架模式
- 测试策略
- 架构指南
- 领域特定知识

### 命令（Commands）

调用实用工作流的斜杠命令（Slash commands）：
- 部署命令
- 测试命令
- 文档命令
- 代码生成命令

### 钩子（Hooks）

实用的自动化操作：
- Lint/格式化钩子
- 安全检查
- 验证钩子
- 通知钩子

### 规则（Rules）

必须遵守的指南：
- 安全规则
- 代码风格规则
- 测试要求
- 命名规范

### MCP 配置（MCP Configurations）

新增或改进的 MCP 服务配置：
- 数据库集成
- 云服务商 MCP
- 监控工具
- 通讯工具

---

## 如何贡献（How to Contribute）

### 1. Fork 仓库

```bash
git clone https://github.com/YOUR_USERNAME/everything-claude-code.git
cd everything-claude-code
```

### 2. 创建分支

```bash
git checkout -b add-python-reviewer
```

### 3. 添加你的贡献

将文件放入相应的目录中：
- `agents/` 用于新增智能体
- `skills/` 用于技能（Skills，可以是单个 .md 文件或目录）
- `commands/` 用于斜杠命令
- `rules/` 用于规则文件
- `hooks/` 用于钩子配置
- `mcp-configs/` 用于 MCP 服务配置

### 4. 遵循格式要求

**智能体（Agents）** 应当包含 Frontmatter：

```markdown
---
name: agent-name
description: What it does
tools: Read, Grep, Glob, Bash
model: sonnet
---

Instructions here...
```

**技能（Skills）** 应当清晰且具备可操作性：

```markdown
# Skill Name

## When to Use

...

## How It Works

...

## Examples

...
```

**命令（Commands）** 应当解释其功能：

```markdown
---
description: Brief description of command
---

# Command Name

Detailed instructions...
```

**钩子（Hooks）** 应当包含描述：

```json
{
  "matcher": "...",
  "hooks": [...],
  "description": "What this hook does"
}
```

### 5. 测试你的贡献

在提交之前，请确保你的配置可以在 Claude Code 中正常运行。

### 6. 提交 PR

```bash
git add .
git commit -m "Add Python code reviewer agent"
git push origin add-python-reviewer
```

然后开启一个 PR 并说明：
- 你添加了什么
- 为什么它很有用
- 你是如何测试它的

---

## 指南（Guidelines）

### 建议（Do）

- 保持配置聚焦且模块化
- 包含清晰的描述
- 提交前进行测试
- 遵循现有模式
- 记录任何依赖项

### 避免（Don't）

- 包含敏感数据（API 密钥、Token、路径）
- 添加过度复杂或过于冷门的配置
- 提交未经测试的配置
- 创建重复的功能
- 添加需要特定付费服务且无替代方案的配置

---

## 文件命名

- 使用小写字母并以连字符连接：`python-reviewer.md`
- 具有描述性：使用 `tdd-workflow.md` 而非 `workflow.md`
- 智能体/技能名称应与文件名匹配

---

## 有疑问？

请提交 Issue 或在 X 上联系：[@affaanmustafa](https://x.com/affaanmustafa)

---

感谢你的贡献。让我们一起构建一个伟大的资源库。