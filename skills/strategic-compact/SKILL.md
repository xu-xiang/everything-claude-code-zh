---
name: strategic-compact
description: 建议在逻辑间隔进行手动上下文压缩（Context Compaction），以便在任务阶段中保留上下文，而不是依赖随机的自动压缩。
---

# 策略性压缩技能 (Strategic Compact Skill)

建议在工作流（Workflow）的关键点手动执行 `/compact`，而不是依赖随机触发的自动压缩。

## 为什么需要策略性压缩？

自动压缩会在随机时间点触发：
- 经常在任务进行中触发，导致丢失重要的上下文
- 无法识别逻辑上的任务边界
- 可能会中断复杂的多步操作

在逻辑边界处进行策略性压缩：
- **在探索之后，执行之前** —— 压缩研究阶段的上下文，保留实现计划
- **在完成里程碑之后** —— 为下一阶段开启全新开始
- **在重大上下文切换之前** —— 在切换到不同任务前清理探索相关的上下文

## 工作原理

`suggest-compact.sh` 脚本在工具调用前（PreToolUse，针对 `Edit`/`Write` 工具）运行，并且：

1. **跟踪工具调用** —— 统计会话（Session）中的工具调用次数
2. **阈值检测** —— 在达到可配置的阈值（默认：50 次调用）时给出建议
3. **定期提醒** —— 达到阈值后，每隔 25 次调用提醒一次

## 钩子 (Hook) 配置

添加至您的 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "tool == \"Edit\" || tool == \"Write\"",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/strategic-compact/suggest-compact.sh"
      }]
    }]
  }
}
```

## 配置

环境变量：
- `COMPACT_THRESHOLD` —— 首次建议前的工具调用次数（默认：50）

## 最佳实践

1. **在规划后压缩** —— 一旦计划最终确定，进行压缩以全新状态开始执行
2. **在调试后压缩** —— 在继续开发前清理错误修复相关的上下文
3. **不要在实现过程中压缩** —— 为相关变更保留上下文
4. **关注建议** —— 钩子（Hook）告诉您“何时”可以压缩，而“是否”压缩由您决定

## 相关资源

- [长篇指南 (The Longform Guide)](https://x.com/affaanmustafa/status/2014040193557471352) —— Token 优化章节
- 记忆持久化钩子 (Memory persistence hooks) —— 用于在压缩后仍需保留的状态
