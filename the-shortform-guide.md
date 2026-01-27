# Claude Code 全方位速查手册

![页眉：Anthropic 黑客松获胜者 - Claude Code 提示与技巧](./assets/images/shortform/00-header.png)

---

**自 2 月份实验性推出以来，我一直是 Claude Code 的忠实用户。我与 [@DRodriguezFX](https://x.com/DRodriguezFX) 合作，完全使用 Claude Code 开发了 [zenith.chat](https://zenith.chat)，并赢得了 Anthropic x Forum Ventures 黑客松。**

以下是我在 10 个月的日常使用后总结出的完整配置：技能（Skills）、生命周期钩子（Hooks）、子智能体（Subagents）、模型上下文协议（MCPs）、插件（Plugins）以及真正行之有效的实践方案。

---

## 技能（Skills）与命令（Commands）

技能（Skills）类似于规则，但被限定在特定的作用域和工作流中。当你需要执行特定工作流时，它们是提示词（Prompts）的快捷方式。

在使用 Opus 4.5 进行长时间编码后，想要清理废弃代码和散落的 .md 文件？运行 `/refactor-clean`。需要测试？使用 `/tdd`、`/e2e`、`/test-coverage`。技能还可以包含代码映射（Codemaps）——这是一种让 Claude 快速导航代码库的方法，而不会在探索过程中浪费上下文（Context）。

![终端显示链式命令](./assets/images/shortform/02-chaining-commands.jpeg)
*链式调用多个命令*

命令（Commands）是通过斜杠命令（Slash Commands）执行的技能。它们在功能上有重叠，但存储方式不同：

- **技能 (Skills)**: `~/.claude/skills/` - 更广泛的工作流定义
- **命令 (Commands)**: `~/.claude/commands/` - 快速可执行的提示词

```bash
# 示例技能结构
~/.claude/skills/
  pmx-guidelines.md      # 项目特定模式
  coding-standards.md    # 语言最佳实践
  tdd-workflow/          # 包含 README.md 的多文件技能
  security-review/       # 基于清单的技能
```

---

## 生命周期钩子（Hooks）

生命周期钩子（Hooks）是基于触发器的自动化功能，在特定事件发生时触发。与技能不同，它们被限制在工具调用（Tool Calls）和生命周期事件中。

**钩子类型：**

1. **PreToolUse** - 工具执行前（验证、提醒）
2. **PostToolUse** - 工具执行后（格式化、反馈循环）
3. **UserPromptSubmit** - 发送消息时
4. **Stop** - Claude 完成响应时
5. **PreCompact** - 上下文压缩前
6. **Notification** - 权限请求

**示例：在执行耗时命令前发送 tmux 提醒**

```json
{
  "PreToolUse": [
    {
      "matcher": "tool == \"Bash\" && tool_input.command matches \"(npm|pnpm|yarn|cargo|pytest)\"",
      "hooks": [
        {
          "type": "command",
          "command": "if [ -z \"$TMUX\" ]; then echo '[Hook] Consider tmux for session persistence' >&2; fi"
        }
      ]
    }
  ]
}
```

![PostToolUse 钩子反馈](./assets/images/shortform/03-posttooluse-hook.png)
*运行 PostToolUse 钩子时在 Claude Code 中获得的反馈示例*

**专家提示：** 使用 `hookify` 插件可以通过对话方式创建钩子，而无需手动编写 JSON。运行 `/hookify` 并描述你的需求即可。

---

## 子智能体（Subagents）

子智能体（Subagents）是你的编排器（主 Claude 实例）可以委派任务的进程，具有受限的作用域。它们可以在后台或前台运行，从而为主智能体释放上下文空间。

子智能体与技能配合得非常好——能够执行部分技能集的子智能体可以被委派任务并自主使用这些技能。它们还可以通过特定的工具权限进行沙箱化处理。

```bash
# 示例子智能体结构
~/.claude/agents/
  planner.md           # 功能实现规划
  architect.md         # 系统设计决策
  tdd-guide.md         # 测试驱动开发
  code-reviewer.md     # 质量/安全审查
  security-reviewer.md # 漏洞分析
  build-error-resolver.md
  e2e-runner.md
  refactor-cleaner.md
```

为每个子智能体配置允许的工具、MCP 和权限，以实现适当的作用域限定。

---

## 规则（Rules）与记忆（Memory）

你的 `.rules` 文件夹存放着 Claude 应该始终遵循的最佳实践 `.md` 文件。有两种方法：

1. **单个 CLAUDE.md** - 所有内容放在一个文件中（用户级或项目级）
2. **Rules 文件夹** - 按关注点分组的模块化 `.md` 文件

```bash
~/.claude/rules/
  security.md      # 禁止硬编码密钥，验证输入
  coding-style.md  # 不可变性，文件组织
  testing.md       # TDD 工作流，80% 覆盖率
  git-workflow.md  # 提交格式，PR 流程
  agents.md        # 何时委派给子智能体
  performance.md   # 模型选择，上下文管理
```

**示例规则：**

- 代码库中严禁使用表情符号 (Emojis)
- 前端避免使用紫色调
- 部署前始终测试代码
- 优先采用模块化代码而非超大文件
- 严禁提交 `console.log`

---

## 模型上下文协议（MCPs）

模型上下文协议（MCPs）将 Claude 直接连接到外部服务。它不是 API 的替代品，而是围绕 API 的提示词驱动封装，允许在导航信息时具有更高的灵活性。

**示例：** Supabase MCP 让 Claude 能够拉取特定数据，直接在上游运行 SQL，无需复制粘贴。数据库、部署平台等同理。

![Supabase MCP 列出数据表](./assets/images/shortform/04-supabase-mcp.jpeg)
*Supabase MCP 列出 public 模式下数据表的示例*

**Claude 内部的 Chrome：** 是一个内置的 MCP 插件，允许 Claude 自主控制浏览器——通过点击来查看功能运行情况。

**关键点：上下文窗口（Context Window）管理**

对 MCP 要精挑细选。我将所有 MCP 保留在用户配置中，但**禁用所有不使用的 MCP**。导航至 `/plugins` 并向下滚动或运行 `/mcp`。

![/plugins 界面](./assets/images/shortform/05-plugins-interface.jpeg)
*使用 /plugins 导航至 MCP，查看当前已安装的 MCP 及其状态*

由于启用了过多工具，你在压缩前的 200k 上下文窗口可能实际上只剩 70k。性能会显著下降。

**经验法则：** 配置中保留 20-30 个 MCP，但保持启用的少于 10 个 / 活跃工具少于 80 个。

```bash
# 检查已启用的 MCP
/mcp

# 在 ~/.claude.json 的 projects.disabledMcpServers 中禁用不使用的 MCP
```

---

## 插件（Plugins）

插件（Plugins）封装了工具以便于安装，避免繁琐的手动设置。一个插件可以是技能（Skill）与 MCP 的组合，也可以是绑定在一起的钩子（Hooks）/工具（Tools）。

**安装插件：**

```bash
# 添加市场
claude plugin marketplace add https://github.com/mixedbread-ai/mgrep

# 打开 Claude，运行 /plugins，找到新市场，并从中安装
```

![显示 mgrep 的市场标签页](./assets/images/shortform/06-marketplaces-mgrep.jpeg)
*显示新安装的 Mixedbread-Grep 市场*

如果你经常在编辑器之外运行 Claude Code，**LSP 插件**特别有用。语言服务器协议（Language Server Protocol）为 Claude 提供了实时类型检查、转到定义和智能补全功能，无需打开 IDE。

```bash
# 已启用插件示例
typescript-lsp@claude-plugins-official  # TypeScript 智能提示
pyright-lsp@claude-plugins-official     # Python 类型检查
hookify@claude-plugins-official         # 对话式创建钩子
mgrep@Mixedbread-Grep                   # 比 ripgrep 更好的搜索
```

与 MCP 同样的警告——注意你的上下文窗口。

---

## 技巧与建议

### 键盘快捷键

- `Ctrl+U` - 删除整行（比狂按退格键快）
- `!` - 快速 Bash 命令前缀
- `@` - 搜索文件
- `/` - 启动斜杠命令
- `Shift+Enter` - 多行输入
- `Tab` - 切换思考过程显示
- `Esc Esc` - 中断 Claude / 恢复代码

### 并行工作流

- **派生** (`/fork`) - 派生对话以并行执行不重叠的任务，而不是让排队的请求堆积
- **Git 工作树 (Worktrees)** - 用于并行运行多个 Claude 实例而不会产生冲突。每个工作树都是一个独立的检出目录

```bash
git worktree add ../feature-branch feature-branch
# 现在在每个工作树中运行独立的 Claude 实例
```

### 使用 tmux 处理耗时命令

串流并观察 Claude 运行的日志/Bash 进程：

https://github.com/user-attachments/assets/shortform/07-tmux-video.mp4

```bash
tmux new -s dev
# Claude 在这里运行命令，你可以随时分离 (detach) 和重新连接 (reattach)
tmux attach -t dev
```

### mgrep > grep

`mgrep` 是对 ripgrep/grep 的重大改进。通过插件市场安装，然后使用 `/mgrep` 技能。同时支持本地搜索和网络搜索。

```bash
mgrep "function handleSubmit"  # 本地搜索
mgrep --web "Next.js 15 app router changes"  # 网络搜索
```

### 其他有用命令

- `/rewind` - 回退到之前的状态
- `/statusline` - 自定义显示分支、上下文占比、待办事项 (Todos)
- `/checkpoints` - 文件级撤销点
- `/compact` - 手动触发上下文压缩

### GitHub Actions CI/CD

使用 GitHub Actions 在 PR 上设置代码审查。配置完成后，Claude 可以自动审查 PR。

![Claude 机器人批准 PR](./assets/images/shortform/08-github-pr-review.jpeg)
*Claude 批准了一个漏洞修复 PR*

### 沙箱化（Sandboxing）

对风险操作使用沙箱模式——Claude 在受限环境中运行，不会影响你的实际系统。

---

## 关于编辑器

编辑器的选择会显著影响 Claude Code 的工作流。虽然 Claude Code 可以从任何终端运行，但配合功能强大的编辑器可以解锁实时文件跟踪、快速导航和集成命令执行。

### Zed（我的首选）

我使用 [Zed](https://zed.dev) —— 用 Rust 编写，速度极快。瞬间打开，处理庞大的代码库也游刃有余，且几乎不占用系统资源。

**为什么 Zed + Claude Code 是绝佳组合：**

- **速度** - 基于 Rust 的性能意味着当 Claude 快速编辑文件时不会有延迟。你的编辑器能跟上节奏
- **智能体面板集成** - Zed 的 Claude 集成让你在 Claude 编辑时实时跟踪文件更改。无需离开编辑器即可在 Claude 引用的文件间跳转
- **CMD+Shift+R 命令面板** - 在可搜索的 UI 中快速访问所有自定义斜杠命令、调试器和构建脚本
- **极低的资源占用** - 在执行繁重操作时不会与 Claude 争夺 RAM/CPU。运行 Opus 时这一点很重要
- **Vim 模式** - 如果你习惯 Vim，它有完整的 Vim 键绑定支持

![带有自定义命令的 Zed 编辑器](./assets/images/shortform/09-zed-editor.jpeg)
*使用 CMD+Shift+R 弹出自定义命令下拉列表的 Zed 编辑器。右下角的牛眼图标显示了跟随模式 (Following mode)。*

**编辑器通用技巧：**

1. **分屏显示** - 一侧是运行 Claude Code 的终端，另一侧是编辑器
2. **Ctrl + G** - 在 Zed 中快速打开 Claude 当前正在处理的文件
3. **自动保存** - 开启自动保存，确保 Claude 读取的文件始终是最新的
4. **Git 集成** - 使用编辑器的 Git 功能在提交前审查 Claude 的更改
5. **文件监听器** - 大多数编辑器会自动重载更改后的文件，请确认该功能已启用

### VSCode / Cursor

这也是一个可行的选择，并且与 Claude Code 配合良好。你可以通过终端形式使用它，利用 `\ide` 自动与编辑器同步并启用 LSP 功能（现在在某种程度上与插件功能重叠）。或者你可以选择扩展程序，它与编辑器集成度更高，并拥有匹配的 UI。

![VS Code Claude Code 扩展](./assets/images/shortform/10-vscode-extension.jpeg)
*VS Code 扩展为 Claude Code 提供了原生图形界面，直接集成到你的 IDE 中。*

---

## 我的配置

### 插件 (Plugins)

**已安装：**（我通常一次只启用 4-5 个）

```markdown
ralph-wiggum@claude-code-plugins       # 循环自动化
frontend-design@claude-code-plugins    # UI/UX 模式
commit-commands@claude-code-plugins    # Git 工作流
security-guidance@claude-code-plugins  # 安全检查
pr-review-toolkit@claude-code-plugins  # PR 自动化
typescript-lsp@claude-plugins-official # TS 智能提示
hookify@claude-plugins-official        # 钩子创建
code-simplifier@claude-plugins-official
feature-dev@claude-code-plugins
explanatory-output-style@claude-plugins-official
code-review@claude-code-plugins
context7@claude-plugins-official       # 实时文档
pyright-lsp@claude-plugins-official    # Python 类型
mgrep@Mixedbread-Grep                  # 更好的搜索
```

### MCP 服务器

**已配置（用户级）：**

```json
{
  "github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"] },
  "firecrawl": { "command": "npx", "args": ["-y", "firecrawl-mcp"] },
  "supabase": {
    "command": "npx",
    "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref=YOUR_REF"]
  },
  "memory": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"] },
  "sequential-thinking": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
  },
  "vercel": { "type": "http", "url": "https://mcp.vercel.com" },
  "railway": { "command": "npx", "args": ["-y", "@railway/mcp-server"] },
  "cloudflare-docs": { "type": "http", "url": "https://docs.mcp.cloudflare.com/mcp" },
  "cloudflare-workers-bindings": {
    "type": "http",
    "url": "https://bindings.mcp.cloudflare.com/mcp"
  },
  "clickhouse": { "type": "http", "url": "https://mcp.clickhouse.cloud/mcp" },
  "AbletonMCP": { "command": "uvx", "args": ["ableton-mcp"] },
  "magic": { "command": "npx", "args": ["-y", "@magicuidesign/mcp@latest"] }
}
```

关键在于：我配置了 14 个 MCP，但每个项目只启用 ~5-6 个。这能保持上下文窗口的健康。

### 关键钩子 (Key Hooks)

```json
{
  "PreToolUse": [
    { "matcher": "npm|pnpm|yarn|cargo|pytest", "hooks": ["tmux reminder"] },
    { "matcher": "Write && .md file", "hooks": ["block unless README/CLAUDE"] },
    { "matcher": "git push", "hooks": ["open editor for review"] }
  ],
  "PostToolUse": [
    { "matcher": "Edit && .ts/.tsx/.js/.jsx", "hooks": ["prettier --write"] },
    { "matcher": "Edit && .ts/.tsx", "hooks": ["tsc --noEmit"] },
    { "matcher": "Edit", "hooks": ["grep console.log warning"] }
  ],
  "Stop": [
    { "matcher": "*", "hooks": ["check modified files for console.log"] }
  ]
}
```

### 自定义状态栏 (Custom Status Line)

显示用户、目录、带脏标记的 Git 分支、剩余上下文 %、模型、时间和待办事项计数：

![自定义状态栏](./assets/images/shortform/11-statusline.jpeg)
*我的 Mac 根目录下的状态栏示例*

```
affoon:~ ctx:65% Opus 4.5 19:52
▌▌ 规划模式已开启 (按 shift+tab 切换)
```

### 规则结构 (Rules Structure)

```
~/.claude/rules/
  security.md      # 强制性安全检查
  coding-style.md  # 不可变性，文件大小限制
  testing.md       # TDD，80% 覆盖率
  git-workflow.md  # 约定式提交 (Conventional commits)
  agents.md        # 子智能体委派规则
  patterns.md      # API 响应格式
  performance.md   # 模型选择 (Haiku vs Sonnet vs Opus)
  hooks.md         # 钩子文档说明
```

### 子智能体 (Subagents)

```
~/.claude/agents/
  planner.md           # 分解功能需求
  architect.md         # 系统设计
  tdd-guide.md         # 测试先行
  code-reviewer.md     # 质量审查
  security-reviewer.md # 漏洞扫描
  build-error-resolver.md
  e2e-runner.md        # Playwright 测试
  refactor-cleaner.md  # 废弃代码清理
  doc-updater.md       # 保持文档同步
```

---

## 核心要点

1. **不要过度复杂化** - 将配置视为微调，而非架构设计
2. **上下文窗口极其珍贵** - 禁用不使用的 MCP 和插件
3. **并行执行** - 派生对话，利用 Git 工作树
4. **自动化重复性任务** - 为格式化、代码检查、提醒设置钩子
5. **明确子智能体的作用域** - 受限的工具 = 专注的执行

---

## 参考资料

- [插件参考 (Plugins Reference)](https://code.claude.com/docs/en/plugins-reference)
- [钩子文档 (Hooks Documentation)](https://code.claude.com/docs/en/hooks)
- [检查点功能 (Checkpointing)](https://code.claude.com/docs/en/checkpointing)
- [交互模式 (Interactive Mode)](https://code.claude.com/docs/en/interactive-mode)
- [记忆系统 (Memory System)](https://code.claude.com/docs/en/memory)
- [子智能体 (Subagents)](https://code.claude.com/docs/en/sub-agents)
- [MCP 概览 (MCP Overview)](https://code.claude.com/docs/en/mcp-overview)

---

**注：** 以上仅为部分细节。进阶模式请参阅 [长篇指南 (Longform Guide)](./the-longform-guide.md)。

---

*与 [@DRodriguezFX](https://x.com/DRodriguezFX) 在纽约共同开发 [zenith.chat](https://zenith.chat)，并赢得 Anthropic x Forum Ventures 黑客松。*
