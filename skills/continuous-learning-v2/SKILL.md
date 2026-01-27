---
name: continuous-learning-v2
description: 基于直觉的学习系统，通过钩子（hooks）观察会话，创建带有置信度评分的原子直觉（atomic instincts），并将其演化为技能/命令/智能体。
version: 2.0.0
---

# 持续学习 v2 - 基于直觉的架构 (Instinct-Based Architecture)

一个高级学习系统，通过原子“直觉（instincts）”——带有置信度评分的小型习得行为，将你的 Claude Code 会话转化为可复用的知识。

## v2 版本新特性

| 特性 | v1 | v2 |
|---------|----|----|
| 观察 (Observation) | Stop 钩子（会话结束） | PreToolUse/PostToolUse (100% 可靠) |
| 分析 (Analysis) | 主上下文 (Main context) | 后台智能体 (Haiku) |
| 粒度 (Granularity) | 完整技能 (Full skills) | 原子“直觉（instincts）” |
| 置信度 (Confidence) | 无 | 0.3-0.9 加权 |
| 演化 (Evolution) | 直接转换为技能 | 直觉 → 聚类 → 技能/命令/智能体 |
| 共享 (Sharing) | 无 | 导出/导入直觉 |

## 直觉模型 (The Instinct Model)

“直觉（instinct）”是一个小型的习得行为：

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
---

# 偏好函数式风格 (Prefer Functional Style)

## 操作 (Action)
在合适的时候，优先使用函数式模式而非类（class）。

## 证据 (Evidence)
- 观察到 5 次偏好函数式模式的实例
- 用户在 2025-01-15 将基于类的方法修正为函数式
```

**属性：**
- **原子性 (Atomic)** — 一个触发器，一个动作
- **置信度加权 (Confidence-weighted)** — 0.3 = 尝试性的，0.9 = 近乎确定
- **领域标签 (Domain-tagged)** — code-style、testing、git、debugging、workflow 等
- **证据支持 (Evidence-backed)** — 追踪是哪些观察结果创建了它

## 工作原理

```
会话活动 (Session Activity)
      │
      │ 钩子捕获提示词 + 工具使用 (100% 可靠)
      ▼
┌─────────────────────────────────────────┐
│         observations.jsonl              │
│   (提示词, 工具调用, 结果)                 │
└─────────────────────────────────────────┘
      │
      │ 观察者智能体读取 (后台运行, Haiku)
      ▼
┌─────────────────────────────────────────┐
│          模式检测 (PATTERN DETECTION)    │
│   • 用户修正 → 直觉                       │
│   • 错误修复 → 直觉                       │
│   • 重复工作流 → 直觉                     │
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

## 快速开始

### 1. 启用观察钩子 (Observation Hooks)

添加到你的 `~/.claude/settings.json`：

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

```bash
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands}}
touch ~/.claude/homunculus/observations.jsonl
```

### 3. 运行观察者智能体 (可选)

观察者可以在后台运行，分析观察结果：

```bash
# 启动后台观察者
~/.claude/skills/continuous-learning-v2/agents/start-observer.sh
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `/instinct-status` | 显示所有习得的直觉及其置信度 |
| `/evolve` | 将相关的直觉聚类为技能/命令 |
| `/instinct-export` | 导出直觉以便共享 |
| `/instinct-import <file>` | 从他人处导入直觉 |

## 配置

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
├── observations.jsonl      # 当前会话观察结果
├── observations.archive/   # 已处理的观察结果
├── instincts/
│   ├── personal/           # 自动习得的直觉
│   └── inherited/          # 从他人处导入的直觉
└── evolved/
    ├── agents/             # 生成的专家智能体
    ├── skills/             # 生成的技能
    └── commands/           # 生成的命令
```

## 与技能创建器 (Skill Creator) 集成

当你使用 [Skill Creator GitHub App](https://skill-creator.app) 时，它现在会**同时**生成：
- 传统的 SKILL.md 文件（为了向后兼容）
- 直觉集合 (Instinct collections)（为了 v2 学习系统）

来自仓库分析的直觉带有 `source: "repo-analysis"` 标签，并包含源仓库的 URL。

## 置信度评分 (Confidence Scoring)

置信度会随时间演化：

| 分数 | 含义 | 行为 |
|-------|---------|----------|
| 0.3 | 尝试性 (Tentative) | 建议但不强制执行 |
| 0.5 | 中等 (Moderate) | 在相关时应用 |
| 0.7 | 强 (Strong) | 自动批准应用 |
| 0.9 | 近乎确定 (Near-certain) | 核心行为 |

**置信度增加** 的情况：
- 模式被重复观察到
- 用户没有修正建议的行为
- 来自其他来源的类似直觉达成一致

**置信度降低** 的情况：
- 用户明确修正了该行为
- 模式在很长一段时间内没有被观察到
- 出现矛盾的证据

## 为什么使用钩子 (Hooks) 而非技能 (Skills) 进行观察？

> “v1 依赖技能进行观察。技能是概率性的——根据 Claude 的判断，它们的触发率约为 50-80%。”

钩子（Hooks）的触发是 **100% 确定性**的。这意味着：
- 每一个工具调用都会被观察到
- 不会遗漏任何模式
- 学习是全面的

## 向后兼容性

v2 完全兼容 v1：
- 现有的 `~/.claude/skills/learned/` 技能仍然有效
- Stop 钩子仍然运行（但现在也会输入到 v2 系统中）
- 渐进式迁移路径：并行运行两者

## 隐私

- 观察结果保存在你的本地机器上
- 只有 **直觉（instincts）**（即模式）可以被导出
- 不会共享实际的代码或对话内容
- 你可以控制哪些内容被导出

## 相关链接

- [Skill Creator](https://skill-creator.app) - 从仓库历史生成直觉
- [Homunculus](https://github.com/humanplane/homunculus) - v2 架构的灵感来源
- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - 持续学习章节

---

*基于直觉的学习：通过一次又一次的观察，教会 Claude 你的模式。*
