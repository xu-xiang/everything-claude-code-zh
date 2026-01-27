---
description: 重述需求、评估风险并创建分步实施计划。在修改任何代码之前，必须等待用户确认（CONFIRM）。
---

# 计划命令（Plan Command）

此命令调用 **计划智能体（planner agent）**，在编写任何代码之前创建一个全面的实施计划。

## 此命令的作用

1. **重述需求** - 澄清需要构建的内容
2. **识别风险** - 发现潜在问题和阻碍因素
3. **创建分步计划** - 将实施分解为不同阶段（Phases）
4. **等待确认** - 在继续操作之前**必须**获得用户批准

## 何时使用

在以下情况使用 `/plan`：
- 开始一个新功能（new feature）
- 进行重大架构变更（architectural changes）
- 进行复杂的重构（refactoring）
- 涉及多个文件或组件时
- 需求不明确或存在歧义时

## 工作原理

计划智能体（planner agent）将：

1. **分析请求**并以清晰的术语重述需求
2. **分解为阶段（Phases）**，并附带具体、可操作的步骤
3. **识别组件之间的依赖关系（Dependencies）**
4. **评估风险**和潜在阻碍因素
5. **预估复杂度（Complexity）**（高/中/低）
6. **展示计划**并**等待**您的明确确认

## 使用示例

```
用户：/plan 我需要在市场结算时添加实时通知

智能体 (planner)：
# 实施计划：实时市场结算通知

## 需求重述
- 当用户关注的市场结算时，向其发送通知
- 支持多个通知渠道（应用内、电子邮件、webhook）
- 确保通知能够可靠交付
- 包含市场结果和用户的持仓结算结果

## 实施阶段

### 第 1 阶段：数据库 Schema
- 添加 notifications 表，包含列：id, user_id, market_id, type, status, created_at
- 添加 user_notification_preferences 表用于渠道偏好设置
- 在 user_id 和 market_id 上创建索引以提高性能

### 第 2 阶段：通知服务
- 在 lib/notifications.ts 中创建通知服务
- 使用 BullMQ/Redis 实施通知队列
- 为投递失败添加重试逻辑
- 创建通知模板

### 第 3 阶段：集成点
- 挂钩（Hook）到市场结算逻辑（当状态变为 "resolved" 时）
- 查询在该市场有持仓的所有用户
- 为每个用户将通知加入队列

### 第 4 阶段：前端组件
- 在页眉创建 NotificationBell 组件
- 添加 NotificationList 模态框
- 通过 Supabase subscriptions 实施实时更新
- 添加通知偏好设置页面

## 依赖关系 (Dependencies)
- Redis（用于队列）
- 电子邮件服务 (SendGrid/Resend)
- Supabase 实时订阅 (real-time subscriptions)

## 风险
- 高 (HIGH)：电子邮件可达性（需要 SPF/DKIM）
- 中 (MEDIUM)：每个市场超过 1000 名用户时的性能问题
- 中 (MEDIUM)：如果市场结算频繁，可能会产生通知垃圾
- 低 (LOW)：实时订阅的开销

## 预估复杂度：中 (MEDIUM)
- 后端：4-6 小时
- 前端：3-4 小时
- 测试：2-3 小时
- 总计：9-13 小时

**等待确认**：是否继续执行此计划？(yes/no/modify)
```

## 重要提示

**关键 (CRITICAL)**：在您明确确认计划（如回答 "yes" 或 "proceed" 或类似的肯定回复）之前，计划智能体（planner agent）**不会**编写任何代码。

如果您想修改计划，请回复：
- "modify: [您的修改意见]"
- "different approach: [替代方案]"
- "skip phase 2 and do phase 3 first"（跳过第 2 阶段，先做第 3 阶段）

## 与其他命令的集成

计划完成后：
- 使用 `/tdd` 通过测试驱动开发（test-driven development）进行实施
- 如果出现构建错误，使用 `/build-and-fix`
- 使用 `/code-review` 评审已完成的实施

## 相关智能体

此命令调用位于以下路径的 `planner` 智能体：
`~/.claude/agents/planner.md`
