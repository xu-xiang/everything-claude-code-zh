# 智能体编排 (Agent Orchestration)

## 可用智能体 (Available Agents)

位于 `~/.claude/agents/`：

| 智能体 (Agent) | 用途 | 适用场景 |
|-------|---------|-------------|
| planner | 实现规划 | 复杂特性、重构 |
| architect | 系统设计 | 架构决策 |
| tdd-guide | 测试驱动开发 (TDD) | 新特性、Bug 修复 |
| code-reviewer | 代码审查 | 代码编写/修改后 |
| security-reviewer | 安全分析 | 提交代码前 |
| build-error-resolver | 修复构建错误 | 构建失败时 |
| e2e-runner | 端到端 (E2E) 测试 | 关键用户流程 |
| refactor-cleaner | 冗余代码清理 | 代码维护 |
| doc-updater | 文档更新 | 更新文档 |

## 立即调用智能体 (Immediate Agent Usage)

以下情况无需用户提示即可直接调用：
1. 复杂特性请求 - 使用 **planner** 智能体
2. 刚刚编写/修改的代码 - 使用 **code-reviewer** 智能体
3. Bug 修复或新特性 - 使用 **tdd-guide** 智能体
4. 架构决策 - 使用 **architect** 智能体

## 并行任务执行 (Parallel Task Execution)

对于相互独立的操作，**务必**使用并行任务执行：

```markdown
# 推荐：并行执行
并行启动 3 个智能体：
1. 智能体 1：对 auth.ts 进行安全分析
2. 智能体 2：对缓存系统进行性能审查
3. 智能体 3：对 utils.ts 进行类型检查

# 避忌：在不必要时采用串行执行
先启动智能体 1，然后智能体 2，最后智能体 3
```

## 多维度分析 (Multi-Perspective Analysis)

针对复杂问题，使用分角色子智能体：
- 事实审查员 (Factual Reviewer)
- 资深工程师 (Senior Engineer)
- 安全专家 (Security Expert)
- 一致性审查员 (Consistency Reviewer)
- 冗余检查员 (Redundancy Checker)
