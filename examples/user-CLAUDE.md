# 用户级 CLAUDE.md 示例

这是一个用户级 CLAUDE.md 文件示例。请放置在 `~/.claude/CLAUDE.md`。

用户级配置全局适用于所有项目。用于：
- 个人编码偏好
- 你希望始终强制执行的通用规则
- 指向你的模块化规则的链接

---

## 核心哲学（Core Philosophy）

你是 Claude Code。我使用专门的智能体（Agents）和技能（Skills）处理复杂任务。

**核心原则：**
1. **智能体优先（Agent-First）**：将复杂工作委托给专门的智能体
2. **并行执行（Parallel Execution）**：尽可能使用 Task 工具配合多个智能体
3. **先计划后执行（Plan Before Execute）**：对复杂操作使用计划模式（Plan Mode）
4. **测试驱动（Test-Driven）**：在实现前编写测试
5. **安全第一（Security-First）**：绝不妥协安全性

---

## 模块化规则（Modular Rules）

详细指南位于 `~/.claude/rules/`：

| 规则文件 | 内容 |
|-----------|----------|
| security.md | 安全检查、密钥管理 |
| coding-style.md | 不可变性、文件组织、错误处理 |
| testing.md | 测试驱动开发（TDD）工作流、80% 覆盖率要求 |
| git-workflow.md | 提交格式、PR 工作流 |
| agents.md | 智能体编排（Agent Orchestration）、何时使用哪个智能体 |
| patterns.md | API 响应、仓库模式（Repository Patterns） |
| performance.md | 模型选择、上下文管理 |
| hooks.md | 钩子系统（Hooks System） |

---

## 可用智能体（Available Agents）

位于 `~/.claude/agents/`：

| 智能体 | 用途 |
|-------|---------|
| planner | 功能实现计划 |
| architect | 系统设计与架构 |
| tdd-guide | 测试驱动开发指南 |
| code-reviewer | 质量/安全代码审查 |
| security-reviewer | 安全漏洞分析 |
| build-error-resolver | 构建错误解决 |
| e2e-runner | Playwright 端到端（E2E）测试 |
| refactor-cleaner | 死代码清理 |
| doc-updater | 文档更新 |

---

## 个人偏好

### 隐私（Privacy）
- 始终脱敏日志；绝不粘贴密钥（API key/Token/密码/JWT）
- 分享前检查输出 - 移除任何敏感数据

### 代码风格（Code Style）
- 代码、注释或文档中不使用表情符号（Emoji）
- 偏好不可变性（Immutability） - 绝不修改对象或数组
- 倾向于多个小文件而非少数大文件
- 通常为 200-400 行，单文件最大 800 行

### Git
- 规范提交（Conventional Commits）：`feat:`、`fix:`、`refactor:`、`docs:`、`test:`
- 提交前始终在本地进行测试
- 小型、专注的提交

### 测试（Testing）
- 测试驱动开发（TDD）：先编写测试
- 最低 80% 覆盖率
- 关键流程需具备 单元 + 集成 + E2E 测试

---

## 编辑器集成（Editor Integration）

我使用 Zed 作为我的主要编辑器：
- 智能体面板（Agent Panel）用于文件追踪
- CMD+Shift+R 用于命令面板（Command Palette）
- 启用 Vim 模式

---

## 成功指标（Success Metrics）

当满足以下条件时，你即是成功的：
- 所有测试通过（80% 以上覆盖率）
- 无安全漏洞
- 代码具有可读性和可维护性
- 满足用户需求

---

**哲学**：智能体优先设计、并行执行、先行后动、测试先行、安全永恒。
