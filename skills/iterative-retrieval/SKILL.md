---
name: iterative-retrieval
description: 用于逐步优化上下文检索以解决子智能体（subagent）上下文问题的模式
---

# 迭代检索模式（Iterative Retrieval Pattern）

解决多智能体工作流中的“上下文问题”，即子智能体（subagent）在开始工作前不知道自己需要哪些上下文。

## 问题（The Problem）

子智能体启动时只有有限的上下文。它们不知道：
- 哪些文件包含相关的代码
- 代码库中存在哪些模式（Patterns）
- 项目使用了哪些术语

标准方法往往会失败：
- **发送所有内容**：超出上下文限制
- **什么都不发**：智能体（Agent）缺乏关键信息
- **猜测需要什么**：经常出错

## 解决方案：迭代检索（Iterative Retrieval）

一个分为 4 个阶段的循环，用于逐步优化上下文：

```
┌─────────────────────────────────────────────┐
│                                             │
│   ┌──────────┐      ┌──────────┐            │
│   │ DISPATCH │─────▶│ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   LOOP   │◀─────│  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        最多 3 个循环，然后继续执行          │
└─────────────────────────────────────────────┘
```

### 阶段 1：分发（DISPATCH）

初始的广泛查询，用于收集候选文件：

```javascript
// 从高层意图开始
const initialQuery = {
  patterns: ['src/**/*.ts', 'lib/**/*.ts'],
  keywords: ['authentication', 'user', 'session'],
  excludes: ['*.test.ts', '*.spec.ts']
};

// 分发给检索智能体
const candidates = await retrieveFiles(initialQuery);
```

### 阶段 2：评估（EVALUATE）

评估检索到的内容的关联度：

```javascript
function evaluateRelevance(files, task) {
  return files.map(file => ({
    path: file.path,
    relevance: scoreRelevance(file.content, task),
    reason: explainRelevance(file.content, task),
    missingContext: identifyGaps(file.content, task)
  }));
}
```

评分标准：
- **高 (0.8-1.0)**：直接实现了目标功能
- **中 (0.5-0.7)**：包含相关的模式或类型
- **低 (0.2-0.4)**：有间接关联
- **无 (0-0.2)**：无关，排除

### 阶段 3：优化（REFINE）

根据评估结果更新搜索标准：

```javascript
function refineQuery(evaluation, previousQuery) {
  return {
    // 添加在高关联度文件中发现的新模式
    patterns: [...previousQuery.patterns, ...extractPatterns(evaluation)],

    // 添加在代码库中发现的术语
    keywords: [...previousQuery.keywords, ...extractKeywords(evaluation)],

    // 排除已确认的无关路径
    excludes: [...previousQuery.excludes, ...evaluation
      .filter(e => e.relevance < 0.2)
      .map(e => e.path)
    ],

    // 针对特定缺口
    focusAreas: evaluation
      .flatMap(e => e.missingContext)
      .filter(unique)
  };
}
```

### 阶段 4：循环（LOOP）

使用优化后的标准重复该过程（最多 3 个循环）：

```javascript
async function iterativeRetrieve(task, maxCycles = 3) {
  let query = createInitialQuery(task);
  let bestContext = [];

  for (let cycle = 0; cycle < maxCycles; cycle++) {
    const candidates = await retrieveFiles(query);
    const evaluation = evaluateRelevance(candidates, task);

    // 检查我们是否已经拥有足够的上下文
    const highRelevance = evaluation.filter(e => e.relevance >= 0.7);
    if (highRelevance.length >= 3 && !hasCriticalGaps(evaluation)) {
      return highRelevance;
    }

    // 优化并继续
    query = refineQuery(evaluation, query);
    bestContext = mergeContext(bestContext, highRelevance);
  }

  return bestContext;
}
```

## 实践示例

### 示例 1：Bug 修复上下文

```
任务：“修复身份验证令牌过期 bug”

循环 1：
  分发（DISPATCH）：在 src/** 中搜索 "token"、"auth"、"expiry"
  评估（EVALUATE）：发现 auth.ts (0.9)、tokens.ts (0.8)、user.ts (0.3)
  优化（REFINE）：添加 "refresh"、"jwt" 关键字；排除 user.ts

循环 2：
  分发（DISPATCH）：搜索优化后的术语
  评估（EVALUATE）：发现 session-manager.ts (0.95)、jwt-utils.ts (0.85)
  优化（REFINE）：上下文已足够（2 个高关联度文件）

结果：auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts
```

### 示例 2：功能实现

```
任务：“为 API 端点添加速率限制（rate limiting）”

循环 1：
  分发（DISPATCH）：在 routes/** 中搜索 "rate"、"limit"、"api"
  评估（EVALUATE）：无匹配项 —— 代码库使用了 "throttle" 术语
  优化（REFINE）：添加 "throttle"、"middleware" 关键字

循环 2：
  分发（DISPATCH）：搜索优化后的术语
  评估（EVALUATE）：发现 throttle.ts (0.9)、middleware/index.ts (0.7)
  优化（REFINE）：需要路由模式

循环 3：
  分发（DISPATCH）：搜索 "router"、"express" 模式
  评估（EVALUATE）：发现 router-setup.ts (0.8)
  优化（REFINE）：上下文已足够

结果：throttle.ts, middleware/index.ts, router-setup.ts
```

## 与智能体（Agents）集成

在智能体提示词（Prompts）中使用：

```markdown
为此任务检索上下文时：
1. 从广泛的关键字搜索开始
2. 评估每个文件的关联度（0-1 评分）
3. 识别仍缺失的上下文
4. 优化搜索标准并重复（最多 3 个循环）
5. 返回关联度 >= 0.7 的文件
```

## 最佳实践

1. **先广后窄，逐步收敛** —— 不要过度设定初始查询。
2. **学习代码库术语** —— 第一个循环通常能揭示命名规范。
3. **跟踪缺失内容** —— 明确地识别差距（Gap）是优化的动力。
4. **见好就收** —— 3 个高关联度的文件优于 10 个平庸的文件。
5. **果断排除** —— 低关联度的文件不会突然变得相关。

## 相关资源

- [长篇指南（The Longform Guide）](https://x.com/affaanmustafa/status/2014040193557471352) —— 子智能体编排部分
- `continuous-learning` 技能 —— 用于随时间改进的模式
- `~/.claude/agents/` 中的智能体定义
