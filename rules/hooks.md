# 钩子系统（Hooks System）

## 钩子类型（Hook Types）

- **工具调用前（PreToolUse）**：在工具执行之前（验证、参数修改）
- **工具调用后（PostToolUse）**：在工具执行之后（自动格式化、检查）
- **会话终止（Stop）**：当会话结束时（最终验证）

## 当前已配置的钩子（Current Hooks）（位于 ~/.claude/settings.json 中）

### 工具调用前（PreToolUse）
- **tmux 提醒**：针对耗时较长的命令（npm, pnpm, yarn, cargo 等）建议使用 tmux
- **git push 审查**：在推送（push）之前打开 Zed 进行代码审查
- **文档拦截器（doc blocker）**：拦截不必要的 .md/.txt 文件创建

### 工具调用后（PostToolUse）
- **PR 创建**：记录 PR URL 和 GitHub Actions 状态
- **Prettier**：编辑后自动格式化 JS/TS 文件
- **TypeScript 检查**：编辑 .ts/.tsx 文件后运行 tsc
- **console.log 警告**：对已编辑文件中的 console.log 发出警告

### 会话终止（Stop）
- **console.log 审计**：在会话结束前检查所有已修改的文件中是否存在 console.log

## 自动授权许可（Auto-Accept Permissions）

请谨慎使用：
- 仅对受信任且定义明确的任务方案启用
- 在探索性工作中禁用
- 严禁使用 `dangerously-skip-permissions` 标志
- 改为在 `~/.claude.json` 中配置 `allowedTools`

## TodoWrite 最佳实践

使用 TodoWrite 工具（Tool）以：
- 跟踪多步骤任务的进度
- 验证对指令的理解程度
- 实现实时引导（steering）
- 展示细粒度的实现步骤

待办事项列表（Todo list）能够揭示：
- 步骤顺序错乱
- 遗漏项
- 多余的不必要项
- 粒度错误
- 需求误读
