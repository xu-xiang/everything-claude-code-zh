# 编排（Orchestrate）命令

用于复杂任务的顺序智能体（Agent）工作流。

## 用法

`/orchestrate [workflow-type] [task-description]`

## 工作流类型

### feature
完整功能实现工作流：
```
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

### bugfix
Bug 调查与修复工作流：
```
explorer -> tdd-guide -> code-reviewer
```

### refactor
安全重构工作流：
```
architect -> code-reviewer -> tdd-guide
```

### security
侧重安全的评审：
```
security-reviewer -> code-reviewer -> architect
```

## 执行模式

对于工作流中的每个智能体（Agent）：

1. **调用智能体**：携带来自上一个智能体的上下文。
2. **收集输出**：将其作为结构化的交接（Handoff）文档。
3. **传递**：交给链条中的下一个智能体。
4. **汇总结果**：生成最终报告。

## 交接（Handoff）文档格式

在智能体之间创建交接文档：

```markdown
## HANDOFF: [previous-agent] -> [next-agent]

### Context
[工作总结]

### Findings
[关键发现或决策]

### Files Modified
[涉及的文件列表]

### Open Questions
[留给下一个智能体的未解决事项]

### Recommendations
[建议的后续步骤]
```

## 示例：功能开发工作流（Feature Workflow）

```
/orchestrate feature "添加用户认证功能"
```

执行流程：

1. **规划智能体（Planner Agent）**
   - 分析需求
   - 创建实现计划
   - 识别依赖项
   - 输出：`HANDOFF: planner -> tdd-guide`

2. **TDD 指导智能体（TDD Guide Agent）**
   - 读取规划智能体（Planner）的交接文档
   - 测试先行（先编写测试）
   - 编写实现代码以通过测试
   - 输出：`HANDOFF: tdd-guide -> code-reviewer`

3. **代码评审智能体（Code Reviewer Agent）**
   - 评审实现代码
   - 检查潜在问题
   - 提出改进建议
   - 输出：`HANDOFF: code-reviewer -> security-reviewer`

4. **安全评审智能体（Security Reviewer Agent）**
   - 安全审计
   - 漏洞检查
   - 最终批准
   - 输出：最终报告

## 最终报告格式

```
ORCHESTRATION REPORT
====================
Workflow: feature
Task: 添加用户认证功能
Agents: planner -> tdd-guide -> code-reviewer -> security-reviewer

SUMMARY
-------
[一段话总结]

AGENT OUTPUTS
-------------
Planner: [摘要]
TDD Guide: [摘要]
Code Reviewer: [摘要]
Security Reviewer: [摘要]

FILES CHANGED
-------------
[列出所有修改的文件]

TEST RESULTS
------------
[测试通过/失败摘要]

SECURITY STATUS
---------------
[安全发现项]

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

## 并行执行

对于独立的检查项，可以并行运行智能体：

```markdown
### Parallel Phase
同时运行：
- code-reviewer (质量评审)
- security-reviewer (安全评审)
- architect (设计评审)

### Merge Results
将所有输出汇总到单个报告中
```

## 参数

$ARGUMENTS:
- `feature <description>` - 完整功能实现工作流
- `bugfix <description>` - Bug 修复工作流
- `refactor <description>` - 重构工作流
- `security <description>` - 安全评审工作流
- `custom <agents> <description>` - 自定义智能体序列

## 自定义工作流示例

```
/orchestrate custom "architect,tdd-guide,code-reviewer" "重构缓存层"
```

## 技巧

1. **从规划开始**：对于复杂功能，优先使用规划智能体（Planner）。
2. **始终包含代码评审**：在合并前，务必包含代码评审智能体（Code Reviewer）。
3. **涉及敏感操作使用安全评审**：在处理鉴权、支付或敏感信息（PII）时，请使用安全评审智能体（Security Reviewer）。
4. **保持交接文档简洁**：专注于下一个智能体所需的信息。
5. **在环节间运行验证**：如有必要，在智能体交接间运行验证（Verification）。
