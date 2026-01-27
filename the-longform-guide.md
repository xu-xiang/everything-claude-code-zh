# Claude Code 终极长篇指南 (The Longform Guide)

![Header: The Longform Guide to Everything Claude Code](./assets/images/longform/01-header.png)

---

> **前提条件**：本指南建立在 [Claude Code 终极速查指南 (The Shorthand Guide)](./the-shortform-guide.md) 之上。如果你尚未配置技能（Skills）、钩子（Hooks）、子智能体（Subagents）、MCP 和插件（Plugins），请先阅读该指南。

![Reference to Shorthand Guide](./assets/images/longform/02-shortform-reference.png)
*速查指南 - 请先阅读*

在速查指南中，我介绍了基础配置：技能与命令、钩子、子智能体、MCP、插件以及构成高效 Claude Code 工作流骨架的配置模式。那是设置指南和基础架构。

本长篇指南将深入探讨区分“高效会话”与“低效浪费”的关键技术。如果你还没读过速查指南，请先回去完成配置。接下来的内容假定你已经配置好并运行着技能、智能体、钩子和 MCP。

本指南的主题包括：Token 经济学、记忆持久化、验证模式、并行化策略以及构建可复用工作流的复利效应。这些是我在 10 个月以上的日常使用中精炼出的模式，它们决定了你是会在第一个小时内就陷入上下文腐烂（Context Rot），还是能够维持数小时的高效会话。

速查和长篇指南中涵盖的所有内容都可以在 GitHub 上找到：`github.com/affaan-m/everything-claude-code`

---

## 技巧与诀窍 (Tips and Tricks)

### 某些 MCP 是可替代的，替换后可释放上下文窗口

对于版本控制（GitHub）、数据库（Supabase）、部署（Vercel、Railway）等 MCP —— 绝大多数平台都已经拥有强大的 CLI，MCP 本质上只是对其进行的封装。MCP 虽然是个不错的封装层，但它是以牺牲上下文窗口为代价的。

为了让 CLI 像 MCP 一样工作，但又不实际使用 MCP（从而避免上下文窗口减小），可以考虑将这些功能捆绑到技能（Skills）和命令（Commands）中。剥离 MCP 暴露的易用工具，并将其转化为命令。

示例：不要一直加载 GitHub MCP，而是创建一个 `/gh-pr` 命令，该命令封装了带有你偏好选项的 `gh pr create`。不要让 Supabase MCP 消耗上下文，而是创建直接使用 Supabase CLI 的技能。

通过延迟加载（Lazy Loading），上下文窗口的问题基本得到了解决。但 Token 使用量和成本并不能以同样的方式解决。CLI + 技能的方法仍然是一种 Token 优化手段。

---

## 重要内容 (IMPORTANT STUFF)

### 上下文与记忆管理 (Context and Memory Management)

为了在跨会话中共享记忆，最佳方案是使用一个技能或命令来总结和检查进度，然后将其保存到 `.claude` 文件夹中的 `.tmp` 文件中，并在会话结束前不断追加内容。第二天，它可以将该文件作为上下文并从你中断的地方继续。为每个会话创建一个新文件，以免旧的上下文污染新的工作。

![Session Storage File Tree](./assets/images/longform/03-session-storage.png)
*会话存储示例 -> https://github.com/affaan-m/everything-claude-code/tree/main/examples/sessions*

Claude 会创建一个总结当前状态的文件。查看它，如果需要则要求修改，然后开启新会话。对于新对话，只需提供该文件路径。当你达到上下文限制并需要继续复杂工作时，这特别有用。这些文件应包含：
- 哪些方法有效（有证据可验证）
- 尝试过但无效的方法
- 尚未尝试的方法以及剩余工作

**战略性清理上下文：**

一旦你设定了计划并清理了上下文（现在 Claude Code 的计划模式（Plan Mode）中是默认选项），你就可以根据计划进行工作。当你积累了大量与执行不再相关的探索性上下文时，这非常有用。对于战略性压缩（Strategic Compacting），请禁用自动压缩（Auto Compact）。手动按逻辑间隔进行压缩，或者创建一个为你执行压缩的技能。

**进阶：动态系统提示词注入 (Dynamic System Prompt Injection)**

我学到的一个模式：不要只把所有内容放在 `CLAUDE.md`（用户作用域）或 `.claude/rules/`（项目作用域）中（这些会在每个会话加载），而是使用 CLI 标志动态注入上下文。

```bash
claude --system-prompt "$(cat memory.md)"
```

这让你能更精确地控制何时加载哪些上下文。系统提示词（System Prompt）内容的优先级高于用户消息，而用户消息的优先级高于工具结果。

**实践设置：**

```bash
# 日常开发
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'

# PR 审查模式
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'

# 研究/探索模式
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'
```

**进阶：记忆持久化钩子 (Memory Persistence Hooks)**

大多数人不知道这些有助于记忆的钩子：

- **PreCompact 钩子**：在上下文压缩发生之前，将重要状态保存到文件。
- **Stop 钩子 (会话结束)**：在会话结束时，将学到的内容持久化到文件。
- **SessionStart 钩子**：在新会话开始时，自动加载之前的上下文。

我构建了这些钩子，它们位于仓库中的 `github.com/affaan-m/everything-claude-code/tree/main/hooks/memory-persistence`。

---

### 持续学习 / 记忆 (Continuous Learning / Memory)

如果你不得不重复多次相同的提示词，而 Claude 遇到了相同的问题或给出了你听过的回答 —— 那么这些模式必须被追加到技能（Skills）中。

**问题：** 浪费 Token、浪费上下文、浪费时间。

**解决方案：** 当 Claude Code 发现非琐碎的事项 —— 调试技术、权宜之计、某些特定于项目的模式 —— 它会将这些知识保存为新技能。下次出现类似问题时，该技能会自动加载。

我构建了一个执行此操作的持续学习技能：`github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning`。

**为什么使用 Stop 钩子（而不是 UserPromptSubmit）：**

核心设计决策是使用 **Stop 钩子** 而不是 UserPromptSubmit。UserPromptSubmit 在每条消息上运行，会给每个提示词增加延迟。Stop 在会话结束时运行一次 —— 轻量级，不会在会话期间拖慢你的速度。

---

### Token 优化 (Token Optimization)

**首要策略：子智能体架构 (Subagent Architecture)**

优化你使用的工具，并设计子智能体架构，以便委派足以完成任务的最便宜模型。

**模型选择快速参考：**

![Model Selection Table](./assets/images/longform/04-model-selection.png)
*各种常见任务中子智能体的假设设置及其选择理由*

| 任务类型 | 模型 | 理由 |
| :--- | :--- | :--- |
| 探索/搜索 | Haiku | 快速、廉价，足以寻找文件 |
| 简单编辑 | Haiku | 单文件修改，指令明确 |
| 多文件实现 | Sonnet | 编码的最佳平衡点 |
| 复杂架构 | Opus | 需要深度推理 |
| PR 审查 | Sonnet | 理解上下文，捕捉细微差别 |
| 安全分析 | Opus | 无法承担遗漏漏洞的代价 |
| 编写文档 | Haiku | 结构简单 |
| 调试复杂 Bug | Opus | 需要在大脑中构建整个系统 |

90% 的编码任务默认使用 Sonnet。当第一次尝试失败、任务涉及 5 个以上文件、需要架构决策或属于安全关键代码时，升级到 Opus。

**价格参考：**

![Claude Model Pricing](./assets/images/longform/05-pricing-table.png)
*来源：https://platform.claude.com/docs/en/about-claude/pricing*

**工具特定优化：**

将 grep 替换为 mgrep —— 与传统的 grep 或 ripgrep 相比，平均可减少约 50% 的 Token：

![mgrep Benchmark](./assets/images/longform/06-mgrep-benchmark.png)
*在我们进行的 50 项任务基准测试中，在判断质量相似或更好的情况下，mgrep + Claude Code 使用的 Token 比基于 grep 的工作流少约 2 倍。来源：https://github.com/mixedbread-ai/mgrep*

**模块化代码库的益处：**

保持代码库更加模块化，主文件行数保持在几百行而不是几千行，这有助于优化 Token 成本并提高任务一次性成功的概率。

---

### 验证循环与评测 (Verification Loops and Evals)

**基准测试工作流：**

对比在有和没有技能的情况下要求相同任务，并检查输出差异：

派生（Fork）对话，在其中一个没有技能的工作区启动新工作树（Worktree），最后拉取一个 diff，查看记录了什么。

**评测模式类型：**

- **基于检查点的评测 (Checkpoint-Based Evals)**：设置明确的检查点，根据定义的标准进行验证，在继续之前进行修复。
- **持续评测 (Continuous Evals)**：每隔 N 分钟或在重大更改后运行，全量测试套件 + Lint。

**核心指标：**

```
pass@k: k 次尝试中至少有一次成功
        k=1: 70%  k=3: 91%  k=5: 97%

pass^k: 所有 k 次尝试必须全部成功
        k=1: 70%  k=3: 34%  k=5: 17%
```

当你只需要它工作时，使用 **pass@k**。当一致性至关重要时，使用 **pass^k**。

---

## 并行化 (PARALLELIZATION)

在多 Claude 终端设置中派生（Fork）对话时，请确保派生出的动作与原始对话的范围界定明确。在代码更改方面，尽量减少重叠。

**我偏好的模式：**

主聊天用于代码更改，派生聊天用于关于代码库及其当前状态的问题，或对外部服务的研究。

**关于终端数量：**

![Boris on Parallel Terminals](./assets/images/longform/07-boris-parallel.png)
*Boris (Anthropic) 谈论运行多个 Claude 实例*

Boris 对并行化有一些建议。他建议诸如在本地运行 5 个 Claude 实例并在上游运行 5 个。我不建议随意设置终端数量。增加终端应该是出于真正的必要。

你的目标应该是：**如何以最小可行数量的并行化完成尽可能多的工作。**

**用于并行实例的 Git 工作树 (Worktrees)：**

```bash
# 为并行工作创建工作树
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
git worktree add ../project-refactor refactor-branch

# 每个工作树获得自己的 Claude 实例
cd ../project-feature-a && claude
```

如果你开始扩展实例，并且有多个 Claude 实例在相互重叠的代码上工作，那么必须使用 git 工作树，并为每个实例制定非常明确的计划。使用 `/rename <name here>` 为你所有的聊天命名。

![Two Terminal Setup](./assets/images/longform/08-two-terminals.png)
*启动设置：左侧终端用于编码，右侧终端用于提问 —— 使用 /rename 和 /fork*

**级联法 (The Cascade Method)：**

运行多个 Claude Code 实例时，采用“级联”模式进行组织：

- 在右侧的新标签页中开启新任务
- 从左向右扫视，从旧到新
- 同时关注最多 3-4 个任务

---

## 基础工作 (GROUNDWORK)

**双实例启动模式 (The Two-Instance Kickoff Pattern)：**

为了管理我自己的工作流，我喜欢在一个空仓库中启动 2 个开启的 Claude 实例。

**实例 1：脚手架智能体 (Scaffolding Agent)**
- 搭建脚手架和基础工作
- 创建项目结构
- 设置配置（CLAUDE.md、rules、agents）

**实例 2：深度研究智能体 (Deep Research Agent)**
- 连接你所有的服务、进行网页搜索
- 创建详细的 PRD
- 创建架构 Mermaid 图表
- 汇总带有实际文档片段的参考资料

**llms.txt 模式：**

如果可用，你可以在许多文档参考资料中找到 `llms.txt`，只需在到达其文档页面后执行 `/llms.txt` 即可。这会为你提供一个干净的、针对 LLM 优化的文档版本。

**哲学：构建可复用的模式**

来自 @omarsar0：“早期，我花时间构建可复用的工作流/模式。构建过程很乏味，但随着模型和智能体控制能力的提高，这产生了巨大的复利效应。”

**值得投入的内容：**

- 子智能体 (Subagents)
- 技能 (Skills)
- 命令 (Commands)
- 规划模式 (Planning patterns)
- MCP 工具
- 上下文工程模式 (Context engineering patterns)

---

## 智能体与子智能体的最佳实践

**子智能体上下文问题：**

子智能体存在的意义在于通过返回总结（Summaries）而不是倾倒（Dumping）所有内容来节省上下文。但编排者（Orchestrator）拥有子智能体所缺乏的语义上下文。子智能体只知道字面上的查询，不知道请求背后的“目的”。

**迭代检索模式 (Iterative Retrieval Pattern)：**

1. 编排者评估子智能体的每一次返回
2. 在接受之前提出追问
3. 子智能体回到源头，获取答案，返回
4. 循环直到满足要求（最多 3 个周期）

**关键：** 传递客观上下文，而不只是查询。

**带有顺序阶段的编排者：**

```markdown
阶段 1: 研究 (使用 Explore 智能体) → research-summary.md
阶段 2: 规划 (使用 Planner 智能体) → plan.md
阶段 3: 实现 (使用 TDD-Guide 智能体) → 代码更改
阶段 4: 审查 (使用 Code-Reviewer 智能体) → review-comments.md
阶段 5: 验证 (必要时使用 Build-Error-Resolver) → 完成或返回循环
```

**核心规则：**

1. 每个智能体接收一个明确的输入，并产生一个明确的输出
2. 输出成为下一阶段的输入
3. 绝不跳过阶段
4. 在智能体切换之间使用 `/clear`
5. 将中间输出存储在文件中

---

## 有趣的内容 / 非关键但有趣的技巧

### 自定义状态栏 (Custom Status Line)

你可以使用 `/statusline` 进行设置 —— 随后 Claude 会说你目前还没有设置，但可以为你配置并询问你想要在其中加入什么。

另请参阅：https://github.com/sirmalloc/ccstatusline

### 语音转录

通过语音与 Claude Code 对话。对许多人来说，这比打字更快。

- Mac 上的 superwhisper, MacWhisper
- 即使有转录错误，Claude 也能理解意图

### 终端别名 (Terminal Aliases)

```bash
alias c='claude'
alias gb='github'
alias co='code'
alias q='cd ~/Desktop/projects'
```

---

## 里程碑

![25k+ GitHub Stars](./assets/images/longform/09-25k-stars.png)
*一周内获得 25,000+ GitHub Stars*

---

## 资源 (Resources)

**智能体编排：**

- https://github.com/ruvnet/claude-flow - 拥有 54 个以上专业智能体的企业级编排平台

**自进化记忆：**

- https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning
- rlancemartin.github.io/2025/12/01/claude_diary/ - 会话反思模式

**系统提示词参考：**

- https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools - 系统提示词集合 (110k stars)

**官方：**

- Anthropic Academy: anthropic.skilljar.com

---

## 参考资料 (References)

- [Anthropic: 揭秘 AI 智能体评测 (Demystifying evals for AI agents)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [YK: 32 个 Claude Code 技巧 (32 Claude Code Tips)](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)
- [RLanceMartin: 会话反思模式 (Session Reflection Pattern)](https://rlancemartin.github.io/2025/12/01/claude_diary/)
- @PerceptualPeak: 子智能体上下文协商
- @menhguin: 智能体抽象层级列表
- @omarsar0: 复利效应哲学

---

*两个指南中涵盖的所有内容都可以在 GitHub 上的 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 找到*
