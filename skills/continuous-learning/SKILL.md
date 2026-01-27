---
name: continuous-learning
description: 自动从 Claude Code 会话（Sessions）中提取可重用的模式，并将其保存为学习到的技能以供未来使用。
---

# 持续学习技能（Continuous Learning Skill）

在会话结束时自动评估 Claude Code 会话（Sessions），以提取可保存为学习技能（Learned Skills）的可重用模式。

## 工作原理

该技能作为 **停止钩子（Stop hook）** 在每个会话结束时运行：

1. **会话评估（Session Evaluation）**：检查会话是否有足够的消息（默认：10 条以上）
2. **模式检测（Pattern Detection）**：识别会话中可提取的模式
3. **技能提取（Skill Extraction）**：将有用的模式保存到 `~/.claude/skills/learned/`

## 配置

编辑 `config.json` 进行自定义：

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/skills/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## 模式类型

| 模式（Pattern） | 描述（Description） |
|---------|-------------|
| `error_resolution` | 特定错误的解决方式 |
| `user_corrections` | 来自用户修正的模式 |
| `workarounds` | 框架/库特有问题的变通方案 |
| `debugging_techniques` | 有效的调试方法 |
| `project_specific` | 项目特定的约定 |

## 钩子设置（Hook Setup）

添加到你的 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"
      }]
    }]
  }
}
```

## 为什么使用停止钩子（Stop Hook）？

- **轻量级（Lightweight）**：在会话结束时运行一次
- **非阻塞（Non-blocking）**：不会给每条消息增加延迟
- **完整上下文（Complete context）**：可以访问完整的会话记录

## 相关内容

- [长篇指南（The Longform Guide）](https://x.com/affaanmustafa/status/2014040193557471352) - 关于持续学习的部分
- `/learn` 命令 - 在会话中手动提取模式

---

## 对比笔记（研究：2025年1月）

### vs Homunculus (github.com/humanplane/homunculus)

Homunculus v2 采用了更复杂的方法：

| 特性（Feature） | 我们的方法（Our Approach） | Homunculus v2 |
|---------|--------------|---------------|
| 观测（Observation） | 停止钩子（Stop hook，会话结束时） | PreToolUse/PostToolUse 钩子（100% 可靠） |
| 分析（Analysis） | 主上下文（Main context） | 后台智能体（Background agent，Haiku） |
| 粒度（Granularity） | 完整技能（Full skills） | 原子化的“本能（instincts）” |
| 置信度（Confidence） | 无 | 0.3-0.9 加权 |
| 演进（Evolution） | 直接转化为技能 | 本能（Instincts）→ 聚类（cluster）→ 技能/命令/智能体 |
| 共享（Sharing） | 无 | 导出/导入本能 |

**来自 homunculus 的关键洞察：**
> “v1 依赖技能进行观测。技能是概率性的——它们的触发率约为 50-80%。v2 使用钩子进行观测（100% 可靠），并将本能（instincts）作为学习行为的原子单位。”

### 潜在的 v2 增强功能

1. **基于本能的学习（Instinct-based learning）** - 带有置信度评分的小型原子化行为
2. **后台观测器（Background observer）** - 并行分析的 Haiku 智能体
3. **置信度衰减（Confidence decay）** - 如果出现矛盾，本能将失去置信度
4. **领域标签（Domain tagging）** - 代码风格（code-style）、测试（testing）、git、调试（debugging）等
5. **演进路径（Evolution path）** - 将相关的本能聚类为技能/命令

参见：`/Users/affoon/Documents/tasks/12-continuous-learning-v2.md` 以获取完整规范。
