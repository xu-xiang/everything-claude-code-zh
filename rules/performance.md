# 性能优化（Performance Optimization）

## 模型选择策略（Model Selection Strategy）

**Haiku 4.5**（具备 Sonnet 90% 的能力，节省 3 倍成本）：
- 频繁调用的轻量级智能体（Agents）
- 结对编程与代码生成
- 多智能体系统中的执行者智能体（Worker agents）

**Sonnet 4.5**（最佳编程模型）：
- 主力开发工作
- 编排多智能体工作流（Workflow）
- 复杂的编程任务

**Opus 4.5**（最深层的推理能力）：
- 复杂的架构决策
- 极高的推理需求
- 研究与分析任务

## 上下文窗口管理（Context Window Management）

在以下场景中，避免触及上下文窗口（Context Window）最后 20% 的容量：
- 大规模重构
- 涉及多个文件的功能实现
- 调试复杂的交互逻辑

对上下文敏感度较低的任务：
- 单文件编辑
- 独立工具函数创建
- 文档更新
- 简单的 Bug 修复

## Ultrathink + 计划模式（Plan Mode）

对于需要深度推理的复杂任务：
1. 使用 `ultrathink` 以获得增强的思维过程
2. 启用 **计划模式（Plan Mode）** 以采用结构化方法
3. 通过多轮评审（Critique rounds）来“预热引擎”
4. 使用分角色的子智能体（Sub-agents）进行多样化分析

## 构建故障排除（Build Troubleshooting）

如果构建失败：
1. 使用 **build-error-resolver** 智能体
2. 分析错误消息
3. 采用增量方式修复
4. 每次修复后进行验证
