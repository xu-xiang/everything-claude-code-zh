**语言：** [English](README.md) | 繁體中文

# Everything Claude Code

[![Stars](https://img.shields.io/github/stars/affaan-m/everything-claude-code?style=flat)](https://github.com/affaan-m/everything-claude-code/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Shell](https://img.shields.io/badge/-Shell-4EAA25?logo=gnu-bash&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?logo=typescript&logoColor=white)
![Go](https://img.shields.io/badge/-Go-00ADD8?logo=go&logoColor=white)
![Markdown](https://img.shields.io/badge/-Markdown-000000?logo=markdown&logoColor=white)

<p align="left">
  <a href="README.md">English</a> |
  <span>简体中文</span>
</p>

**由 Anthropic 黑客松获胜者整理的 Claude Code 配置完整合集。**

这是在 10 个月以上高强度日常开发真实产品的过程中，不断演进出的生产级智能体（Agents）、技能（Skills）、钩子（Hooks）、命令（Commands）、规则（Rules）以及 MCP 配置。

---

## 指南（The Guides）

本仓库仅包含原始代码。以下指南将解释所有细节。

<table>
<tr>
<td width="50%">
<a href="the-shortform-guide_zh.md">
<img src="https://github.com/user-attachments/assets/1a471488-59cc-425b-8345-5245c7efbcef" alt="Everything Claude Code 简明指南" />
</a>
</td>
<td width="50%">
<a href="the-longform-guide.md">
<img src="https://github.com/user-attachments/assets/c9ca43bc-b149-427f-b551-af6840c368f0" alt="Everything Claude Code 深度指南" />
</a>
</td>
</tr>
<tr>
<td align="center"><b>简明指南 (Shorthand Guide)</b><br/>安装、基础、哲学。<b>请先阅读此篇。</b></td>
<td align="center"><b>深度指南 (Longform Guide)</b><br/>Token 优化、内存持久化、评测（Evals）、并行化。</td>
</tr>
</table>

| 主题 | 你将学到什么 |
|-------|-------------------|
| Token 优化 | 模型选择、系统提示词精简、后台进程 |
| 内存持久化 | 跨会话（Session）自动保存/加载上下文的钩子（Hooks） |
| 持续学习 | 从会话中自动提取模式并转化为可复用的技能（Skills） |
| 验证循环 | 检查点（Checkpoint）与持续评测（Evals）、评分器类型、pass@k 指标 |
| 并行化 | Git worktrees、级联方法、何时扩展实例 |
| 子智能体编排 | 上下文问题、迭代检索模式 |

---

## 跨平台支持

该插件现已全面支持 **Windows、macOS 和 Linux**。所有钩子（Hooks）和脚本都已使用 Node.js 重写，以实现最大的兼容性。

### 包管理器检测

插件会自动检测你偏好的包管理器（npm, pnpm, yarn, 或 bun），优先级如下：

1. **环境变量**：`CLAUDE_PACKAGE_MANAGER`
2. **项目配置**：`.claude/package-manager.json`
3. **package.json**：`packageManager` 字段
4. **锁文件**：根据 package-lock.json, yarn.lock, pnpm-lock.yaml 或 bun.lockb 检测
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

## 包含内容

本仓库是一个 **Claude Code 插件** —— 你可以直接安装它，或者手动复制组件。

```
everything-claude-code/
|-- .claude-plugin/   # 插件与市场清单
|   |-- plugin.json         # 插件元数据与组件路径
|   |-- marketplace.json    # 用于 /plugin marketplace add 的市场目录
|
|-- agents/           # 用于任务委派的专用子智能体（Subagents）
|   |-- planner.md           # 功能实现规划
|   |-- architect.md         # 系统设计决策
|   |-- tdd-guide.md         # 测试驱动开发（TDD）
|   |-- code-reviewer.md     # 代码质量与安全评审
|   |-- security-reviewer.md # 漏洞分析
|   |-- build-error-resolver.md # 构建错误解决
|   |-- e2e-runner.md        # Playwright 端到端测试
|   |-- refactor-cleaner.md  # 死代码清理
|   |-- doc-updater.md       # 文档同步
|   |-- go-reviewer.md       # Go 代码评审（新增）
|   |-- go-build-resolver.md # Go 构建错误解决（新增）
|
|-- skills/           # 工作流（Workflow）定义与领域知识
|   |-- coding-standards/           # 语言最佳实践
|   |-- backend-patterns/           # API、数据库、缓存模式
|   |-- frontend-patterns/          # React、Next.js 模式
|   |-- continuous-learning/        # 从会话中自动提取模式（深度指南内容）
|   |-- continuous-learning-v2/     # 基于直觉（Instinct）的带置信度评分学习系统
|   |-- iterative-retrieval/        # 子智能体的渐进式上下文精炼
|   |-- strategic-compact/          # 手动压缩建议（深度指南内容）
|   |-- tdd-workflow/               # TDD 方法论
|   |-- security-review/            # 安全自查表
|   |-- eval-harness/               # 验证循环评测（深度指南内容）
|   |-- verification-loop/          # 持续验证（深度指南内容）
|   |-- golang-patterns/            # Go 惯用法与最佳实践（新增）
|   |-- golang-testing/             # Go 测试模式、TDD、基准测试（新增）
|
|-- commands/         # 用于快速执行的斜杠命令（Slash Commands）
|   |-- tdd.md              # /tdd - 测试驱动开发
|   |-- plan.md             # /plan - 实现规划
|   |-- e2e.md              # /e2e - 端到端测试生成
|   |-- code-review.md      # /code-review - 质量评审
|   |-- build-fix.md        # /build-fix - 修复构建错误
|   |-- refactor-clean.md   # /refactor-clean - 移除死代码
|   |-- learn.md            # /learn - 会话中途提取模式（深度指南内容）
|   |-- checkpoint.md       # /checkpoint - 保存验证状态（深度指南内容）
|   |-- verify.md           # /verify - 运行验证循环（深度指南内容）
|   |-- setup-pm.md         # /setup-pm - 配置包管理器
|   |-- go-review.md        # /go-review - Go 代码评审（新增）
|   |-- go-test.md          # /go-test - Go TDD 工作流（新增）
|   |-- go-build.md         # /go-build - 修复 Go 构建错误（新增）
|   |-- skill-create.md     # /skill-create - 从 git 历史生成技能（新增）
|   |-- instinct-status.md  # /instinct-status - 查看已学习的直觉（新增）
|   |-- instinct-import.md  # /instinct-import - 导入直觉（新增）
|   |-- instinct-export.md  # /instinct-export - 导出直觉（新增）
|   |-- evolve.md           # /evolve - 将相关直觉聚类为技能（新增）
|
|-- rules/            # 必须遵守的准则（复制到 ~/.claude/rules/）
|   |-- security.md         # 强制性安全检查
|   |-- coding-style.md     # 不可变性、文件组织
|   |-- testing.md          # TDD、80% 覆盖率要求
|   |-- git-workflow.md     # 提交格式、PR 流程
|   |-- agents.md           # 何时委派给子智能体
|   |-- performance.md      # 模型选择、上下文管理
|
|-- hooks/            # 基于触发器的自动化
|   |-- hooks.json                # 所有钩子配置（PreToolUse, PostToolUse, Stop 等）
|   |-- memory-persistence/       # 会话生命周期钩子（深度指南内容）
|   |-- strategic-compact/        # 压缩建议（深度指南内容）
|
|-- scripts/          # 跨平台 Node.js 脚本（新增）
|   |-- lib/                     # 共享实用程序
|   |   |-- utils.js             # 跨平台文件/路径/系统工具
|   |   |-- package-manager.js   # 包管理器检测与选择
|   |-- hooks/                   # 钩子实现
|   |   |-- session-start.js     # 会话开始时加载上下文
|   |   |-- session-end.js       # 会话结束时保存状态
|   |   |-- pre-compact.js       # 压缩前状态保存
|   |   |-- suggest-compact.js   # 战略性压缩建议
|   |   |-- evaluate-session.js  # 从会话中提取模式
|   |-- setup-package-manager.js # 交互式包管理器设置
|
|-- tests/            # 测试套件（新增）
|   |-- lib/                     # 库测试
|   |-- hooks/                   # 钩子测试
|   |-- run-all.js               # 运行所有测试
|
|-- contexts/         # 动态系统提示词注入上下文（深度指南内容）
|   |-- dev.md              # 开发模式上下文
|   |-- review.md           # 代码评审模式上下文
|   |-- research.md         # 研究/探索模式上下文
|
|-- examples/         # 配置与会话示例
|   |-- CLAUDE.md           # 项目级配置示例
|   |-- user-CLAUDE.md      # 用户级配置示例
|
|-- mcp-configs/      # MCP 服务配置
|   |-- mcp-servers.json    # GitHub, Supabase, Vercel, Railway 等
|
|-- marketplace.json  # 自托管市场配置（用于 /plugin marketplace add）
```

---

## 生态工具

### 技能创建器（Skill Creator）

有两种方法可以从你的仓库生成 Claude Code 技能：

#### 方案 A：本地分析（内置）

使用 `/skill-create` 命令进行本地分析，无需外部服务：

```bash
/skill-create                    # 分析当前仓库
/skill-create --instincts        # 同时为持续学习（continuous-learning）生成直觉（instincts）
```

该命令会在本地分析你的 git 历史并生成 SKILL.md 文件。

#### 方案 B：GitHub App（高级）

适用于高级功能（1万+ commit、自动 PR、团队共享）：

[安装 GitHub App](https://github.com/apps/skill-creator) | [ecc.tools](https://ecc.tools)

```bash
# 在任何 issue 下留言：
/skill-creator analyze

# 或者在 push 到默认分支时自动触发
```

两种方案都会创建：
- **SKILL.md 文件** - 可直接用于 Claude Code 的技能
- **直觉集合（Instinct collections）** - 用于 continuous-learning-v2
- **模式提取（Pattern extraction）** - 从你的提交历史中学习

### 持续学习（Continuous Learning）v2

基于直觉（instinct）的学习系统会自动学习你的开发模式：

```bash
/instinct-status        # 显示带有置信度的已学习直觉
/instinct-import <file> # 导入他人的直觉
/instinct-export        # 导出你的直觉以便分享
/evolve                 # 将相关的直觉聚类为技能（skills）
```

详见 `skills/continuous-learning-v2/` 的完整文档。

---

## 要求

### Claude Code CLI 版本

**最低版本：v2.1.0 或更高**

由于插件系统处理钩子（hooks）方式的变更，本插件要求 Claude Code CLI v2.1.0+。

检查你的版本：
```bash
claude --version
```

### 重要：钩子（Hooks）自动加载行为

> ⚠️ **对贡献者的提醒：** 请勿在 `.claude-plugin/plugin.json` 中添加 `"hooks"` 字段。这是由回归测试强制执行的。

Claude Code v2.1+ 会**自动加载**已安装插件中约定的 `hooks/hooks.json`。在 `plugin.json` 中显式声明会导致重复检测错误：

```
Duplicate hooks file detected: ./hooks/hooks.json resolves to already-loaded file
```

**历史背景：** 此问题在本仓库中曾多次出现修复/回退循环（[#29](https://github.com/affaan-m/everything-claude-code/issues/29), [#52](https://github.com/affaan-m/everything-claude-code/issues/52), [#103](https://github.com/affaan-m/everything-claude-code/issues/103)）。Claude Code 版本间的行为差异导致了混淆。我们现在已加入回归测试以防止此类问题再次发生。

---

## 安装

### 方案 1：作为插件安装（推荐）

这是使用本仓库最简单的方法 —— 作为 Claude Code 插件安装：

```bash
# 将此仓库添加为市场（marketplace）
/plugin marketplace add affaan-m/everything-claude-code

# 安装插件
/plugin install everything-claude-code@everything-claude-code
```

或者直接添加到你的 `~/.claude/settings.json`：

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

安装后即可立即使用所有命令（commands）、智能体（agents）、技能（skills）和钩子（hooks）。

> **注意：** Claude Code 插件系统目前不支持通过插件分发规则（`rules`）（这是 [上游限制](https://code.claude.com/docs/en/plugins-reference)）。你需要手动安装规则：
>
> ```bash
> # 首先克隆仓库
> git clone https://github.com/affaan-m/everything-claude-code.git
>
> # 方案 A：用户级规则（应用于所有项目）
> cp -r everything-claude-code/rules/* ~/.claude/rules/
>
> # 方案 B：项目级规则（仅应用于当前项目）
> mkdir -p .claude/rules
> cp -r everything-claude-code/rules/* .claude/rules/
> ```

---

### 方案 2：手动安装

如果你更倾向于手动控制安装的内容：

```bash
# 克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git

# 复制智能体（agents）到你的 Claude 配置目录
cp everything-claude-code/agents/*.md ~/.claude/agents/

# 复制规则（rules）
cp everything-claude-code/rules/*.md ~/.claude/rules/

# 复制命令（commands）
cp everything-claude-code/commands/*.md ~/.claude/commands/

# 复制技能（skills）
cp -r everything-claude-code/skills/* ~/.claude/skills/
```

#### 将钩子（hooks）添加到 settings.json

将 `hooks/hooks.json` 中的钩子配置复制到你的 `~/.claude/settings.json` 中。

#### 配置 MCPs

将 `mcp-configs/mcp-servers.json` 中你需要的 MCP 服务配置复制到你的 `~/.claude.json`。

**重要：** 请将 `YOUR_*_HERE` 占位符替换为你真实的 API 密钥。

---

## 核心概念

### 智能体（Agents）

子智能体（Subagents）负责处理受限范围内的委派任务。示例：

```markdown
---
name: code-reviewer
description: 评审代码质量、安全性与可维护性
tools: ["Read", "Grep", "Glob", "Bash"]
model: opus
---

你是一名资深代码评审员...
```

### 技能（Skills）

技能（Skills）是可由命令或智能体调用的工作流定义：

```markdown
# TDD 工作流

1. 首先定义接口
2. 编写失败的测试（RED）
3. 实现最简代码（GREEN）
4. 重构（IMPROVE）
5. 验证覆盖率是否达到 80% 以上
```

### 钩子（Hooks）

钩子（Hooks）在工具事件发生时触发。示例 —— 针对 console.log 发出警告：

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

规则（Rules）是必须始终遵守的准则。请保持它们的模块化：

```
~/.claude/rules/
  security.md      # 禁止硬编码密钥
  coding-style.md  # 不可变性、文件限制
  testing.md       # TDD、覆盖率要求
```

---

## 运行测试

本插件包含一个全面的测试套件：

```bash
# 运行所有测试
node tests/run-all.js

# 运行单个测试文件
node tests/lib/utils.test.js
node tests/lib/package-manager.test.js
node tests/hooks/hooks.test.js
```

---

## 贡献

**非常欢迎并鼓励贡献。**

本仓库旨在成为一个社区资源。如果你有：
- 有用的智能体或技能
- 巧妙的钩子
- 更好的 MCP 配置
- 改进后的规则

请提交你的贡献！参考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

### 贡献思路

- 语言专用技能（Python, Rust 模式）—— 已包含 Go！
- 框架专用配置（Django, Rails, Laravel）
- DevOps 智能体（Kubernetes, Terraform, AWS）
- 测试策略（不同框架）
- 领域特定知识（机器学习、数据工程、移动开发）

---

## 背景

我从 Claude Code 实验阶段就开始使用了。在 2025 年 9 月的 Anthropic x Forum Ventures 黑客松中，我与 [@DRodriguezFX](https://x.com/DRodriguezFX) 合作开发了 [zenith.chat](https://zenith.chat)，并获得了冠军 —— 该项目完全使用 Claude Code 构建。

这些配置在多个生产级应用中经过了实战检验。

---

## 重要提示

### 上下文窗口管理

**至关重要：** 不要一次性启用所有 MCP。如果启用的工具过多，你的 200k 上下文窗口可能会缩减到 70k。

经验法则：
- 配置 20-30 个 MCP
- 每个项目保持启用 10 个以内
- 活跃工具总数控制在 80 个以内

在项目配置中使用 `disabledMcpServers` 来禁用不需要的服务。

### 自定义

这些配置适用于我的工作流。你应该：
1. 从你产生共鸣的内容开始
2. 根据你的技术栈进行修改
3. 移除你不需要的内容
4. 加入你自己的模式

---

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=affaan-m/everything-claude-code&type=Date)](https://star-history.com/#affaan-m/everything-claude-code&Date)

---

## 相关链接

- **简明指南（入门必读）：** [Everything Claude Code 简明指南](https://x.com/affaanmustafa/status/2012378465664745795)
- **深度指南（进阶参考）：** [Everything Claude Code 深度指南](https://x.com/affaanmustafa/status/2014040193557471352)
- **关注我：** [@affaanmustafa](https://x.com/affaanmustafa)
- **zenith.chat：** [zenith.chat](https://zenith.chat)

---

## 许可证

MIT - 自由使用，按需修改，如果可以请回馈社区。

---

**如果对你有帮助，请给本仓库点个 Star。阅读两份指南。构建伟大的产品。**
