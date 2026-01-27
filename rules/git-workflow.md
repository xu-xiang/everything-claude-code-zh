# Git 工作流 (Git Workflow)

## 提交信息格式 (Commit Message Format)

```
<type>: <description>

<optional body>
```

类型 (Types): feat, fix, refactor, docs, test, chore, perf, ci

注意：归属归因 (Attribution) 已通过 `~/.claude/settings.json` 全局禁用。

## 拉取请求工作流 (Pull Request Workflow)

创建 PR 时：
1. 分析完整的提交历史（不仅是最近一次提交）
2. 使用 `git diff [base-branch]...HEAD` 查看所有变更
3. 起草详尽的 PR 摘要
4. 包含带有 TODO 的测试计划
5. 如果是新分支，使用 `-u` 参数推送

## 功能实现工作流 (Feature Implementation Workflow)

1. **规划先行 (Plan First)**
   - 使用 **planner** 智能体 (Agent) 创建实现计划
   - 识别依赖关系与风险
   - 拆分为多个阶段

2. **测试驱动开发 (TDD Approach)**
   - 使用 **tdd-guide** 智能体 (Agent)
   - 先编写测试 (RED)
   - 实现功能以通过测试 (GREEN)
   - 重构 (IMPROVE)
   - 验证 80% 以上的覆盖率

3. **代码评审 (Code Review)**
   - 在编写代码后立即使用 **code-reviewer** 智能体 (Agent)
   - 解决严重 (CRITICAL) 和高 (HIGH) 等级的问题
   - 尽可能修复中 (MEDIUM) 等级的问题

4. **提交与推送 (Commit & Push)**
   - 详细的提交信息
   - 遵循约定式提交 (Conventional Commits) 格式
