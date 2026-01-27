# Everything Claude Code (Claude Code 全集)

[![Stars](https://img.shields.io/github/stars/affaan-m/everything-claude-code?style=flat)](https://github.com/affaan-m/everything-claude-code/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Shell](https://img.shields.io/badge/-Shell-4EAA25?logo=gnu-bash&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?logo=typescript&logoColor=white)
![Go](https://img.shields.io/badge/-Go-00ADD8?logo=go&logoColor=white)
![Markdown](https://img.shields.io/badge/-Markdown-000000?logo=markdown&logoColor=white)

**来自 Anthropic 黑客松获胜者的 Claude Code 配置完整合集。**

包含生产级智能体（Agents）、技能（Skills）、钩子（Hooks）、命令（Commands）、规约（Rules）以及 MCP 配置，这些都是在超过 10 个月的真实产品开发与深度日常使用中演进出来的。

---

## 指南文档

本仓库仅包含原始代码。以下指南将解释一切。

<table>
<tr>
<td width="50%">
<a href="https://x.com/affaanmustafa/status/2012378465664745795">
<img src="https://github.com/user-attachments/assets/1a471488-59cc-425b-8345-5245c7efbcef" alt="The Shorthand Guide to Everything Claude Code" />
</a>
</td>
<td width="50%">
<a href="https://x.com/affaanmustafa/status/2014040193557471352">
<img src="https://github.com/user-attachments/assets/c9ca43bc-b149-427f-b551-af6840c368f0" alt="The Longform Guide to Everything Claude Code" />
</a>
</td>
</tr>
<tr>
<td align="center"><b>简明指南 (Shorthand Guide)</b><br/>安装设置、基础概念与哲学。<b>请先阅读此篇。</b></td>
<td align="center"><b>深度指南 (Longform Guide)</b><br/>Token 优化、内存持久化、评测（Evals）与并行化。</td>
</tr>
</table>

| 主题 | 你将学到什么 |
|-------|-------------------|
| Token 优化 | 模型选择、系统提示词瘦身、后台进程 |
| 内存持久化 | 自动跨会话保存/加载上下文的钩子（Hooks） |
| 持续学习 | 从会话中自动提取模式并转化为可复用的技能（Skills） |
| 验证循环 | 检查点 vs 持续评测、打分器类型、pass@k 指标 |
| 并行化 | Git worktrees、级联法（Cascade method）、何时扩展实例 |
| 子智能体编排 | 上下文问题、迭代检索模式（Iterative retrieval pattern） |

---

## 跨平台支持

本插件现已全面支持 **Windows、macOS 和 Linux**。所有钩子和脚本均已使用 Node.js 重写，以实现最大兼容性。

### 包管理器检测

插件会自动检测你偏好的包管理器（npm, pnpm, yarn, 或 bun），优先级如下：

1. **环境变量**：`CLAUDE_PACKAGE_MANAGER`
2. **项目配置**：`.claude/package-manager.json`
3. **package.json**：`packageManager` 字段
4. **锁文件**：根据 package-lock.json, yarn.lock, pnpm-lock.yaml, 或 bun.lockb 检测
5. **全局配置**：`~/.claude/package-manager.json`
6. **备选项**：第一个可用的包管理器

设置你偏好的包管理器：

```bash
# 通过环境变量
export CLAUDE_PACKAGE_MANAGER=pnpm

# 通过全局配置
node scripts/setup-package-manager.js --global pnpm

# 通过项目配置
node scripts/setup-package-manager.js --project bun

# 检测当前设置
node scripts/setup-package-manager.js --detect
```

或者在 Claude Code 中使用 `/setup-pm` 命令。

---

## 核心内容

本仓库是一个 **Claude Code 插件** —— 你可以直接安装，也可以手动复制组件。

```
everything-claude-code/
|-- .claude-plugin/   # 插件与市场清单
|   |-- plugin.json         # 插件元数据与组件路径
|   |-- marketplace.json    # 用于 /plugin marketplace add 的市场目录
|
|-- agents/           # 用于任务委派的专用子智能体
|   |-- planner.md           # 功能实现规划
|   |-- architect.md         # 系统设计决策
|   |-- tdd-guide.md         # 测试驱动开发 (TDD)
|   |-- code-reviewer.md     # 质量与安全审查
|   |-- security-reviewer.md # 漏洞分析
|   |-- build-error-resolver.md # 构建错误修复
|   |-- e2e-runner.md        # Playwright E2E 测试
|   |-- refactor-cleaner.md  # 冗余代码清理
|   |-- doc-updater.md       # 文档同步
|   |-- go-reviewer.md       # Go 代码审查 (新增)
|   |-- go-build-resolver.md # Go 构建错误解决 (新增)
|
|-- skills/           # 工作流定义与领域知识
|   |-- coding-standards/           # 编程语言最佳实践
|   |-- backend-patterns/           # API、数据库、缓存模式
|   |-- frontend-patterns/          # React, Next.js 模式
|   |-- continuous-learning/        # 从会话中自动提取模式 (深度指南)
|   |-- continuous-learning-v2/     # 基于本能 (Instinct) 的学习与置信度评分
|   |-- iterative-retrieval/        # 为子智能体提供渐进式上下文精炼
|   |-- strategic-compact/          # 手动压缩建议 (深度指南)
|   |-- tdd-workflow/               # TDD 方法论
|   |-- security-review/            # 安全检查清单
|   |-- eval-harness/               # 验证循环评估 (深度指南)
|   |-- verification-loop/          # 持续验证 (深度指南)
|   |-- golang-patterns/            # Go 惯用法与最佳实践 (新增)
|   |-- golang-testing/             # Go 测试模式、TDD、基准测试 (新增)
|
|-- commands/         # 用于快速执行的斜杠命令 (/命令)
|   |-- tdd.md              # /tdd - 测试驱动开发
|   |-- plan.md             # /plan - 实现规划
|   |-- e2e.md              # /e2e - E2E 测试生成
|   |-- code-review.md      # /code-review - 质量审查
|   |-- build-fix.md        # /build-fix - 修复构建错误
|   |-- refactor-clean.md   # /refactor-clean - 冗余代码移除
|   |-- learn.md            # /learn - 会话中途提取模式 (深度指南)
|   |-- checkpoint.md       # /checkpoint - 保存验证状态 (深度指南)
|   |-- verify.md           # /verify - 运行验证循环 (深度指南)
|   |-- setup-pm.md         # /setup-pm - 配置包管理器
|   |-- go-review.md        # /go-review - Go 代码审查 (新增)
|   |-- go-test.md          # /go-test - Go TDD 工作流 (新增)
|   |-- go-build.md         # /go-build - 修复 Go 构建错误 (新增)
|
|-- rules/            # 必须遵守的指南 (复制到 ~/.claude/rules/)
|   |-- security.md         # 强制性安全检查
|   |-- coding-style.md     # 不可变性、文件组织结构
|   |-- testing.md          # TDD、80% 覆盖率要求
|   |-- git-workflow.md     # Commit 格式、PR 流程
|   |-- agents.md           # 何时委派给子智能体
|   |-- performance.md      # 模型选择、上下文管理
|
|-- hooks/            # 基于触发器的自动化
|   |-- hooks.json                # 所有钩子配置 (PreToolUse, PostToolUse, Stop 等)
|   |-- memory-persistence/       # 会话生命周期钩子 (深度指南)
|   |-- strategic-compact/        # 压缩建议 (深度指南)
|
|-- scripts/          # 跨平台 Node.js 脚本 (新增)
|   |-- lib/                     # 共享实用程序
|   |   |-- utils.js             # 跨平台文件/路径/系统工具
|   |   |-- package-manager.js   # 包管理器检测与选择
|   |-- hooks/                   # 钩子实现
|   |   |-- session-start.js     # 会话启动时加载上下文
|   |   |-- session-end.js       # 会话结束时保存状态
|   |   |-- pre-compact.js       # 压缩前的状态保存
|   |   |-- suggest-compact.js   # 策略性压缩建议
|   |   |-- evaluate-session.js  # 从会话中提取模式
|   |-- setup-package-manager.js # 交互式包管理器设置
|
|-- tests/            # 测试套件 (新增)
|   |-- lib/                     # 库测试
|   |-- hooks/                   # 钩子测试
|   |-- run-all.js               # 运行所有测试
|
|-- contexts/         # 动态系统提示词注入上下文 (深度指南)
|   |-- dev.md              # 开发模式上下文
|   |-- review.md           # 代码审查模式上下文
|   |-- research.md         # 研究/探索模式上下文
|
|-- examples/         # 示例配置与会话
|   |-- CLAUDE.md           # 项目级配置示例
|   |-- user-CLAUDE.md      # 用户级配置示例
|
|-- mcp-configs/      # MCP 服务器配置
|   |-- mcp-servers.json    # GitHub, Supabase, Vercel, Railway 等
|
|-- marketplace.json  # 自托管市场配置 (用于 /plugin marketplace add)
```

---

## 生态工具

### ecc.tools - 技能生成器 (Skill Creator)

自动根据你的仓库生成 Claude Code 技能（Skills）。

[安装 GitHub App](https://github.com/apps/skill-creator) | [ecc.tools](https://ecc.tools)

分析你的仓库并创建：
- **SKILL.md 文件** - 开箱即用的 Claude Code 技能
- **本能 (Instinct) 集合** - 适用于 continuous-learning-v2
- **模式提取** - 从你的 commit 历史中学习

```bash
# 安装 GitHub App 后，技能将出现在：
~/.claude/skills/generated/
```

与 `continuous-learning-v2` 技能完美配合，实现遗传式的本能学习。

---

## 安装方法

### 方案 1：作为插件安装（推荐）

使用本仓库最简单的方法 —— 作为 Claude Code 插件安装：

```bash
# 将此仓库添加为市场
/plugin marketplace add affaan-m/everything-claude-code

# 安装插件
/plugin install everything-claude-code@everything-claude-code
```

或者直接添加到你的 `~/.claude/settings.json` 中：

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

安装后你即可立即使用所有命令、智能体、技能和钩子。

> **注意：** Claude Code 插件系统目前不支持通过插件分发 `rules`（[上游限制](https://code.claude.com/docs/en/plugins-reference)）。你需要手动安装规约（Rules）：
> 
> ```bash
> # 先克隆仓库
> git clone https://github.com/affaan-m/everything-claude-code.git
> 
> # 选项 A：用户级规约 (适用于所有项目)
> cp -r everything-claude-code/rules/* ~/.claude/rules/
> 
> # 选项 B：项目级规约 (仅适用于当前项目)
> mkdir -p .claude/rules
> cp -r everything-claude-code/rules/* .claude/rules/
> ```

---

### 方案 2：手动安装

如果你更喜欢手动控制安装内容：

```bash
# 克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git

# 将智能体复制到你的 Claude 配置目录
cp everything-claude-code/agents/*.md ~/.claude/agents/

# 复制规约 (Rules)
cp everything-claude-code/rules/*.md ~/.claude/rules/

# 复制命令 (Commands)
cp everything-claude-code/commands/*.md ~/.claude/commands/

# 复制技能 (Skills)
cp -r everything-claude-code/skills/* ~/.claude/skills/
```

#### 将钩子 (Hooks) 添加到 settings.json

将 `hooks/hooks.json` 中的钩子配置复制到你的 `~/.claude/settings.json`。

#### 配置 MCP

将 `mcp-configs/mcp-servers.json` 中需要的 MCP 服务器配置复制到你的 `~/.claude.json`。

**重要：** 请将 `YOUR_*_HERE` 占位符替换为你实际的 API 密钥。

---

## 核心概念

### 智能体 (Agents)

子智能体负责处理具有特定范围的委派任务。示例：

```markdown
---
name: code-reviewer
description: 审查代码的质量、安全性与可维护性
tools: ["Read", "Grep", "Glob", "Bash"]
model: opus
---

你是一个资深代码审查员...
```

### 技能 (Skills)

技能是由命令或智能体调用的工作流定义：

```markdown
# TDD 工作流

1. 首先定义接口
2. 编写失败的测试 (RED)
3. 实现最简代码 (GREEN)
4. 重构 (IMPROVE)
5. 验证 80% 以上的覆盖率
```

### 钩子 (Hooks)

钩子在工具事件上触发。示例 —— 警告关于 console.log 的使用：

```json
{
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx|js|jsx)$\"",
  "hooks": [{
    "type": "command",
    "command": "#!/bin/bash\ngrep -n 'console\.log' \"$file_path\" && echo '[Hook] 移除 console.log' >&2"
  }]
}
```

### 规约 (Rules)

规约是必须始终遵循的指南。保持模块化：

```
~/.claude/rules/
  security.md      # 禁止硬编码密钥
  coding-style.md  # 不可变性、文件限制
  testing.md       # TDD、覆盖率要求
```

---

## 运行测试

本插件包含完整的测试套件：

```bash
# 运行所有测试
node tests/run-all.js

# 运行单个测试文件
node tests/lib/utils.test.js
node tests/lib/package-manager.test.js
node tests/hooks/hooks.test.js
```

---

## 贡献指南

**欢迎并鼓励大家做出贡献。**

本仓库旨在作为一个社区资源。如果你有：
- 有用的智能体或技能
- 巧妙的钩子
- 更好的 MCP 配置
- 改进后的规约

请提交贡献！参见 [CONTRIBUTING.md](CONTRIBUTING.md) 获取指南。

### 贡献思路

- 特定语言的技能 (Python, Rust 模式) —— Go 已包含！
- 特定框架的配置 (Django, Rails, Laravel)
- DevOps 智能体 (Kubernetes, Terraform, AWS)
- 测试策略 (针对不同框架)
- 领域特定知识 (机器学习, 数据工程, 移动端)

---

## 背景故事

自实验性推出以来，我一直在使用 Claude Code。在 2025 年 9 月的 Anthropic x Forum Ventures 黑客松中，我与 [@DRodriguezFX](https://x.com/DRodriguezFX) 合作构建了 [zenith.chat](https://zenith.chat)，并最终获胜 —— 整个过程完全使用了 Claude Code。

这些配置在多个生产级应用中经过了实战测试。

---

## 重要注意事项

### 上下文窗口管理

**关键：** 不要一次性启用所有 MCP。开启过多工具会将你 200k 的上下文窗口压缩到 70k。

经验法则：
- 配置 20-30 个 MCP
- 每个项目保持启用 10 个以下
- 活跃工具总数保持在 80 个以下

在项目配置中使用 `disabledMcpServers` 来禁用不常用的服务器。

### 自定义

这些配置适合我的工作流。你应该：
1. 从产生共鸣的内容开始
2. 根据你的技术栈进行修改
3. 移除你不使用的部分
4. 添加你自己的模式

---

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=affaan-m/everything-claude-code&type=Date)](https://star-history.com/#affaan-m/everything-claude-code&Date)

---

## 相关链接

- **简明指南 (从这里开始)：** [The Shorthand Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2012378465664745795)
- **深度指南 (进阶)：** [The Longform Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2014040193557471352)
- **关注：** [@affaanmustafa](https://x.com/affaanmustafa)
- **zenith.chat:** [zenith.chat](https://zenith.chat)

---

## 许可证

MIT - 自由使用，根据需要修改，如果可以请回馈社区。

---

**如果对你有帮助，请给本仓库点个 Star。阅读两篇指南。构建伟大的产品。**
