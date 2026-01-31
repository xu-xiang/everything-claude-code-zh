---
name: continuous-learning-v2
description: 基于直觉（Instinct）的学习系统，通过钩子（Hooks）观测会话，创建带有置信度评分（Confidence Scoring）的原子直觉，并将其演进为技能（Skills）、命令（Commands）或智能体（Agents）。
version: 2.0.0
---

# 持续学习 v2 - 基于直觉的架构（Instinct-Based Architecture）

这是一个先进的学习系统，通过原子化“直觉（Instincts）”——即带有置信度评分的小型习得行为，将你的 Claude Code 会话转化为可复用的知识。

## v2 版本新特性

| 特性 | v1 | v2 |
|---------|----|----|
| 观测（Observation） | Stop 钩子（会话结束时） | PreToolUse/PostToolUse (100% 可靠) |
| 分析（Analysis） | 主上下文（Main context） | 后台智能体 (Haiku) |
| 粒度（Granularity） | 完整技能（Full skills） | 原子化“直觉（Instincts）” |
| 置信度（Confidence） | 无 | 0.3-0.9 加权评分 |
| 演进（Evolution） | 直接转化为技能 | 直觉 → 聚类 → 技能/命令/智能体 |
| 共享（Sharing） | 无 | 导出/导入直觉 |

## 直觉模型（The Instinct Model）

直觉（Instinct）是一种小型习得行为：

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
---

# 偏好函数式风格（Prefer Functional Style）

## 动作（Action）
在合适的情况下，优先使用函数式模式（Functional Patterns）而非类（Classes）。

## 证据（Evidence）
- 观测到 5 次函数式模式偏好实例
- 用户在 2025-01-15 将基于类的方法修正为函数式方法
```

**属性：**
- **原子化（Atomic）** — 一个触发器对应一个动作
- **置信度加权（Confidence-weighted）** — 0.3 = 尝试性的，0.9 = 近乎确定
- **领域标签（Domain-tagged）** — 代码风格（code-style）、测试（testing）、git、调试（debugging）、工作流（workflow）等
- **证据支持（Evidence-backed）** — 追踪是哪些观测结果创建了它

## 工作原理

```
会话活动（Session Activity）
      │
      │ 钩子（Hooks）捕获提示词 + 工具使用 (100% 可靠)
      ▼
┌─────────────────────────────────────────┐
│         observations.jsonl              │
│   (提示词、工具调用、执行结果)          │
└─────────────────────────────────────────┘
      │
      │ 观测者智能体读取 (后台运行, Haiku)
      ▼
┌─────────────────────────────────────────┐
│          模式检测（PATTERN DETECTION）  │
│   • 用户修正 → 直觉                     │
│   • 错误解决 → 直觉                     │
│   • 重复工作流 → 直觉                   │
└─────────────────────────────────────────┘
      │
      │ 创建/更新
      ▼
┌─────────────────────────────────────────┐
│         instincts/personal/             │
│   • prefer-functional.md (0.7)          │
│   • always-test-first.md (0.9)          │
│   • use-zod-validation.md (0.6)         │
└─────────────────────────────────────────┘
      │
      │ /evolve 聚类
      ▼
┌─────────────────────────────────────────┐
│              evolved/                   │
│   • commands/new-feature.md             │
│   • skills/testing-workflow.md          │
│   • agents/refactor-specialist.md       │
└─────────────────────────────────────────┘
```

## 快速入门

### 1. 启用观测钩子（Observation Hooks）

将以下内容添加到你的 `~/.claude/settings.json` 中。

**如果作为插件安装**（推荐）：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh pre"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh post"
      }]
    }]
  }
}
```

**如果手动安装**到 `~/.claude/skills`：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh pre"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh post"
      }]
    }]
  }
}
```

### 2. 初始化目录结构

Python CLI 会自动创建这些目录，但你也可以手动创建：

```bash
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands}}
touch ~/.claude/homunculus/observations.jsonl
```

### 3. 使用直觉命令

```bash
/instinct-status     # 显示已习得的直觉及其置信度评分
/evolve              # 将相关的直觉聚类为技能/命令
/instinct-export     # 导出直觉以便分享
/instinct-import     # 从他人处导入直觉
```

## 命令（Commands）

| 命令 | 描述 |
|---------|-------------|
| `/instinct-status` | 显示所有已习得的直觉及置信度 |
| `/evolve` | 将相关的直觉聚类为技能/命令 |
| `/instinct-export` | 导出直觉以便分享 |
| `/instinct-import <file>` | 从他人处导入直觉 |

## 配置（Configuration）

编辑 `config.json`：

```json
{
  "version": "2.0",
  "observation": {
    "enabled": true,
    "store_path": "~/.claude/homunculus/observations.jsonl",
    "max_file_size_mb": 10,
    "archive_after_days": 7
  },
  "instincts": {
    "personal_path": "~/.claude/homunculus/instincts/personal/",
    "inherited_path": "~/.claude/homunculus/instincts/inherited/",
    "min_confidence": 0.3,
    "auto_approve_threshold": 0.7,
    "confidence_decay_rate": 0.05
  },
  "observer": {
    "enabled": true,
    "model": "haiku",
    "run_interval_minutes": 5,
    "patterns_to_detect": [
      "user_corrections",
      "error_resolutions",
      "repeated_workflows",
      "tool_preferences"
    ]
  },
  "evolution": {
    "cluster_threshold": 3,
    "evolved_path": "~/.claude/homunculus/evolved/"
  }
}
```

## 文件结构

```
~/.claude/homunculus/
├── identity.json           # 你的个人资料、技术水平
├── observations.jsonl      # 当前会话观测结果
├── observations.archive/   # 已处理的观测结果
├── instincts/
│   ├── personal/           # 自动习得的直觉
│   └── inherited/          # 从他人处导入的直觉
└── evolved/
    ├── agents/             # 生成的专家智能体
    ├── skills/             # 生成的技能
    └── commands/           # 生成的命令
```

## 与 Skill Creator 集成

当你使用 [Skill Creator GitHub App](https://skill-creator.app) 时，它现在会**同时**生成：
- 传统的 SKILL.md 文件（用于向下兼容）
- 直觉集合（用于 v2 学习系统）

来自仓库分析的直觉具有 `source: "repo-analysis"` 属性，并包含源仓库 URL。

## 置信度评分（Confidence Scoring）

置信度随时间演进：

| 分数 | 含义 | 行为 |
|-------|---------|----------|
| 0.3 | 尝试性的（Tentative） | 建议但不强制执行 |
| 0.5 | 中等（Moderate） | 在相关时应用 |
| 0.7 | 强（Strong） | 自动批准应用 |
| 0.9 | 近乎确定（Near-certain） | 核心行为 |

**置信度增加**的情况：
- 模式被重复观测到
- 用户没有修正建议的行为
- 来自其他来源的类似直觉达成一致

**置信度降低**的情况：
- 用户明确修正了该行为
- 模式长时间未被观测到
- 出现矛盾的证据

## 为什么使用钩子（Hooks）而非技能（Skills）进行观测？

> "v1 依赖技能进行观测。技能具有概率性——根据 Claude 的判断，其触发率约为 50-80%。"

钩子（Hooks）的触发是 **100% 确定性的**。这意味着：
- 每一个工具调用都会被观测到
- 不会遗漏任何模式
- 学习是全面的

## 向下兼容性

v2 完全兼容 v1：
- 现有的 `~/.claude/skills/learned/` 技能仍然有效
- Stop 钩子仍然运行（但现在也会为 v2 提供输入）
- 渐进式迁移路径：两者并行运行

## 隐私（Privacy）

- 观测结果保存在你本地机器上
- 只有**直觉**（模式）可以被导出
- 不会分享实际的代码或对话内容
- 你可以控制导出的内容

## 相关链接

- [Skill Creator](https://skill-creator.app) - 从仓库历史生成直觉
- [Homunculus](https://github.com/humanplane/homunculus) - v2 架构的灵感来源
- [长篇指南（The Longform Guide）](https://x.com/affaanmustafa/status/2014040193557471352) - 持续学习章节

---

*基于直觉的学习：通过每一次观测，教会 Claude 你的模式。*
