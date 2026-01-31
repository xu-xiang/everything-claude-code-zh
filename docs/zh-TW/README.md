# Everything Claude Code

[![Stars](https://img.shields.io/github/stars/affaan-m/everything-claude-code?style=flat)](https://github.com/affaan-m/everything-claude-code/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Shell](https://img.shields.io/badge/-Shell-4EAA25?logo=gnu-bash&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?logo=typescript&logoColor=white)
![Go](https://img.shields.io/badge/-Go-00ADD8?logo=go&logoColor=white)
![Markdown](https://img.shields.io/badge/-Markdown-000000?logo=markdown&logoColor=white)

**来自 Anthropic 黑客松冠军的完整 Claude Code 配置集。**

经过 10 个月以上密集日常使用、打造真实产品所淬炼出的生产就绪智能体（Agents）、技能（Skills）、钩子（Hooks）、指令（Commands）、规则（Rules）和 MCP 配置。

---

## 指南

本仓库仅包含原始代码。指南会解释所有内容。

<table>
<tr>
<td width="50%">
<a href="https://x.com/affaanmustafa/status/2012378465664745795">
<img src="https://github.com/user-attachments/assets/1a471488-59cc-425b-8345-5245c7efbcef" alt="Everything Claude Code 简明指南" />
</a>
</td>
<td width="50%">
<a href="https://x.com/affaanmustafa/status/2014040193557471352">
<img src="https://github.com/user-attachments/assets/c9ca43bc-b149-427f-b551-af6840c368f0" alt="Everything Claude Code 完整指南" />
</a>
</td>
</tr>
<tr>
<td align="center"><b>简明指南</b><br/>配置、基础、理念。<b>请先阅读此指南。</b></td>
<td align="center"><b>完整指南</b><br/>Token 优化、记忆持久化、评估、并行处理。</td>
</tr>
</table>

| 主题 | 学习内容 |
|------|----------|
| Token 优化 | 模型选择、系统提示精简、后台进程 |
| 记忆持久化 | 自动跨会话（Session）保存/加载上下文的钩子（Hooks） |
| 持续学习 | 从会话中自动提取模式并转化为可重用技能（Skills） |
| 验证循环 | 检查点 vs 持续评估、评分器类型、pass@k 指标 |
| 并行处理 | Git worktrees、串联方法、何时扩展实例 |
| 子智能体协调 | 上下文问题、渐进式检索模式 |

---

## 跨平台支持

此插件现已完整支持 **Windows、macOS 和 Linux**。所有钩子和脚本已使用 Node.js 重写以获得最佳兼容性。

### 包管理器检测

插件会自动检测您偏好的包管理器（npm、pnpm、yarn 或 bun），优先级如下：

1. **环境变量**：`CLAUDE_PACKAGE_MANAGER`
2. **项目配置**：`.claude/package-manager.json`
3. **package.json**：`packageManager` 字段
4. **锁文件**：从 package-lock.json、yarn.lock、pnpm-lock.yaml 或 bun.lockb 检测
5. **全局配置**：`~/.claude/package-manager.json`
6. **备选方案**：第一个可用的包管理器

设置您偏好的包管理器：

```bash
# 通过环境变量
export CLAUDE_PACKAGE_MANAGER=pnpm

# 通过全局配置
node scripts/setup-package-manager.js --global pnpm

# 通过项目配置
node scripts/setup-package-manager.js --project bun

# 检测当前配置
node scripts/setup-package-manager.js --detect
```

或在 Claude Code 中使用 `/setup-pm` 指令。

---

## 内容概览

本仓库是一个 **Claude Code 插件** - 可直接安装或手动复制组件。

```
everything-claude-code/
|-- .claude-plugin/   # 插件和市场清单
|   |-- plugin.json         # 插件元数据和组件路径
|   |-- marketplace.json    # 用于 /plugin marketplace add 的市场目录
|
|-- agents/           # 用于委派任务的专门子智能体（Agents）
|   |-- planner.md           # 功能实现规划
|   |-- architect.md         # 系统设计决策
|   |-- tdd-guide.md         # 测试驱动开发
|   |-- code-reviewer.md     # 质量与安全审查
|   |-- security-reviewer.md # 漏洞分析
|   |-- build-error-resolver.md
|   |-- e2e-runner.md        # Playwright E2E 测试
|   |-- refactor-cleaner.md  # 无用代码清理
|   |-- doc-updater.md       # 文档同步
|   |-- go-reviewer.md       # Go 代码审查（新增）
|   |-- go-build-resolver.md # Go 构建错误解决（新增）
|
|-- skills/           # 工作流（Workflow）定义和领域知识
|   |-- coding-standards/           # 编程语言最佳实践
|   |-- backend-patterns/           # API、数据库、缓存模式
|   |-- frontend-patterns/          # React、Next.js 模式
|   |-- continuous-learning/        # 从会话中自动提取模式（完整指南）
|   |-- continuous-learning-v2/     # 基于本能的学习与信心评分
|   |-- iterative-retrieval/        # 子代理的渐进式上下文精炼
|   |-- strategic-compact/          # 手动压缩建议（完整指南）
|   |-- tdd-workflow/               # TDD 方法论
|   |-- security-review/            # 安全性检查清单
|   |-- eval-harness/               # 验证循环评估（完整指南）
|   |-- verification-loop/          # 持续验证（完整指南）
|   |-- golang-patterns/            # Go 惯用法和最佳实践（新增）
|   |-- golang-testing/             # Go 测试模式、TDD、基准测试（新增）
|
|-- commands/         # 快速执行的斜杠指令（Commands）
|   |-- tdd.md              # /tdd - 测试驱动开发
|   |-- plan.md             # /plan - 实现规划
|   |-- e2e.md              # /e2e - E2E 测试生成
|   |-- code-review.md      # /code-review - 质量审查
|   |-- build-fix.md        # /build-fix - 修复构建错误
|   |-- refactor-clean.md   # /refactor-clean - 移除无用代码
|   |-- learn.md            # /learn - 会话中提取模式（完整指南）
|   |-- checkpoint.md       # /checkpoint - 保存验证状态（完整指南）
|   |-- verify.md           # /verify - 执行验证循环（完整指南）
|   |-- setup-pm.md         # /setup-pm - 设置包管理器
|   |-- go-review.md        # /go-review - Go 代码审查（新增）
|   |-- go-test.md          # /go-test - Go TDD 工作流（新增）
|   |-- go-build.md         # /go-build - 修复 Go 构建错误（新增）
|
|-- rules/            # 必须遵守的准则（Rules）（复制到 ~/.claude/rules/）
|   |-- security.md         # 强制性安全检查
|   |-- coding-style.md     # 不变性、文件组织
|   |-- testing.md          # TDD、80% 覆盖率要求
|   |-- git-workflow.md     # 提交格式、PR 流程
|   |-- agents.md           # 何时委派给子智能体
|   |-- performance.md      # 模型选择、上下文管理
|
|-- hooks/            # 基于触发器的自动化钩子（Hooks）
|   |-- hooks.json                # 所有钩子配置（PreToolUse、PostToolUse、Stop 等）
|   |-- memory-persistence/       # 会话生命周期钩子（完整指南）
|   |-- strategic-compact/        # 压缩建议（完整指南）
|
|-- scripts/          # 跨平台 Node.js 脚本（新增）
|   |-- lib/                     # 共享工具
|   |   |-- utils.js             # 跨平台文件/路径/系统工具
|   |   |-- package-manager.js   # 包管理器检测与选择
|   |-- hooks/                   # 钩子实现
|   |   |-- session-start.js     # 会话开始时加载上下文
|   |   |-- session-end.js       # 会话结束时保存状态
|   |   |-- pre-compact.js       # 压缩前状态保存
|   |   |-- suggest-compact.js   # 策略性压缩建议
|   |   |-- evaluate-session.js  # 从会话中提取模式
|   |-- setup-package-manager.js # 交互式包管理器设置
|
|-- tests/            # 测试套件（新增）
|   |-- lib/                     # 库测试
|   |-- hooks/                   # 钩子测试
|   |-- run-all.js               # 执行所有测试
|
|-- contexts/         # 动态系统提示词（Prompt）注入上下文（完整指南）
|   |-- dev.md              # 开发模式上下文
|   |-- review.md           # 代码审查模式上下文
|   |-- research.md         # 研究/探索模式上下文
|
|-- examples/         # 示例配置和会话
|   |-- CLAUDE.md           # 项目级配置示例
|   |-- user-CLAUDE.md      # 用户级配置示例
|
|-- mcp-configs/      # MCP 服务器配置
|   |-- mcp-servers.json    # GitHub、Supabase、Vercel、Railway 等
|
|-- marketplace.json  # 自托管市场配置（用于 /plugin marketplace add）
```

---

## 生态系统工具

### ecc.tools - 技能生成器

从您的仓库自动生成 Claude Code 技能（Skills）。

[安装 GitHub App](https://github.com/apps/skill-creator) | [ecc.tools](https://ecc.tools)

分析您的仓库并创建：
- **SKILL.md 文件** - 可直接用于 Claude Code 的技能
- **本能集合** - 用于 continuous-learning-v2
- **模式提取** - 从您的提交历史学习

```bash
# 安装 GitHub App 后，技能会出现在：
~/.claude/skills/generated/
```

与 `continuous-learning-v2` 技能无缝整合以继承本能。

---

## 安装

### 选项 1：以插件（Plugin）安装（推荐）

使用本仓库最简单的方式 - 安装为 Claude Code 插件：

```bash
# 将此仓库添加为市场
/plugin marketplace add affaan-m/everything-claude-code

# 安装插件
/plugin install everything-claude-code@everything-claude-code
```

或直接添加到您的 `~/.claude/settings.json`：

```json
{
  "extraKnownMarketplaces": {
    "everything-claude-code": {
      "source": {
        "source": "github",
        "repo": "affaan-m/everything-claude-code"
      }
    }
  },
  "enabledPlugins": {
    "everything-claude-code@everything-claude-code": true
  }
}
```

这会让您立即访问所有指令、智能体、技能和钩子。

---

### 选项 2：手动安装

如果您偏好手动控制安装内容：

```bash
# 克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git

# 将智能体复制到您的 Claude 配置
cp everything-claude-code/agents/*.md ~/.claude/agents/

# 复制规则
cp everything-claude-code/rules/*.md ~/.claude/rules/

# 复制指令
cp everything-claude-code/commands/*.md ~/.claude/commands/

# 复制技能
cp -r everything-claude-code/skills/* ~/.claude/skills/
```

#### 将钩子添加到 settings.json

将 `hooks/hooks.json` 中的钩子复制到您的 `~/.claude/settings.json`。

#### 配置 MCP

将 `mcp-configs/mcp-servers.json` 中所需的 MCP 服务器配置复制到您的 `~/.claude.json`。

**重要：** 将 `YOUR_*_HERE` 占位符替换为您实际的 API 密钥。

---

## 核心概念

### 智能体（Agents）

子智能体以有限范围处理委派的任务。示例：

```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and maintainability
tools: ["Read", "Grep", "Glob", "Bash"]
model: opus
---

You are a senior code reviewer...
```

### 技能（Skills）

技能是由指令或智能体调用的工作流定义：

```markdown
# TDD Workflow

1. Define interfaces first
2. Write failing tests (RED)
3. Implement minimal code (GREEN)
4. Refactor (IMPROVE)
5. Verify 80%+ coverage
```

### 钩子（Hooks）

钩子在工具（Tool）事件时触发。示例 - 警告 console.log：

```json
{
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx|js|jsx)$\"",
  "hooks": [{
    "type": "command",
    "command": "#!/bin/bash\ngrep -n 'console\\.log' \"$file_path\" && echo '[Hook] Remove console.log' >&2"
  }]
}
```

### 规则（Rules）

规则是必须遵守的准则。保持模块化：

```
~/.claude/rules/
  security.md      # 禁止硬编码密钥
  coding-style.md  # 不变性、文件组织
  testing.md       # TDD、80% 覆盖率要求
```

---

## 执行测试

插件包含完整的测试套件：

```bash
# 执行所有测试
node tests/run-all.js

# 执行个别测试文件
node tests/lib/utils.test.js
node tests/lib/package-manager.test.js
node tests/hooks/hooks.test.js
```

---

## 贡献

**欢迎并鼓励贡献。**

本仓库旨在成为社区资源。如果您有：
- 实用的智能体或技能
- 巧妙的钩子
- 更好的 MCP 配置
- 改进的规则

请贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md) 的指南。

### 贡献想法

- 特定语言的技能（Python、Rust 模式）- Go 现已包含！
- 特定框架的配置（Django、Rails、Laravel）
- DevOps 智能体（Kubernetes、Terraform、AWS）
- 测试策略（不同框架）
- 特定领域知识（ML、数据工程、移动开发）

---

## 背景

我从实验性推出就开始使用 Claude Code。2025 年 9 月与 [@DRodriguezFX](https://x.com/DRodriguezFX) 一起使用 Claude Code 打造 [zenith.chat](https://zenith.chat)，赢得了 Anthropic x Forum Ventures 黑客松。

这些配置已在多个生产应用程序中经过实战测试。

---

## 重要注意事项

### 上下文窗口管理

**关键：** 不要同时启用所有 MCP。启用过多工具会让您的 200k 上下文窗口缩减至 70k。

经验法则：
- 设置 20-30 个 MCP
- 每个项目启用少于 10 个
- 启用的工具少于 80 个

在项目配置中使用 `disabledMcpServers` 来禁用未使用的 MCP。

### 自定义

这些配置适合我的工作流。您应该：
1. 从您认同的部分开始
2. 根据您的技术栈修改
3. 移除不需要的部分
4. 添加您自己的模式

---

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=affaan-m/everything-claude-code&type=Date)](https://star-history.com/#affaan-m/everything-claude-code&Date)

---

## 链接

- **简明指南（从这里开始）：** [Everything Claude Code 简明指南](https://x.com/affaanmustafa/status/2012378465664745795)
- **完整指南（进阶）：** [Everything Claude Code 完整指南](https://x.com/affaanmustafa/status/2014040193557471352)
- **关注：** [@affaanmustafa](https://x.com/affaanmustafa)
- **zenith.chat：** [zenith.chat](https://zenith.chat)

---

## 授权

MIT - 自由使用、依需求修改、如可能请回馈贡献。

---

**如果有帮助请为本仓库点赞（Star）。阅读两份指南。打造伟大的作品。**
