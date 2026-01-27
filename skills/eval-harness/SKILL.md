---
name: eval-harness
description: 为 Claude Code 会话提供的正式评测框架，实现了评测驱动开发（Eval-Driven Development，EDD）原则
tools: Read, Write, Edit, Bash, Grep, Glob
---

# 评测套件技能（Eval Harness Skill）

一个为 Claude Code 会话提供的正式评测框架，实现了评测驱动开发（Eval-Driven Development，EDD）原则。

## 核心理念（Philosophy）

评测驱动开发（EDD）将评测（Evals）视为“AI 开发的单元测试”：
- 在实现代码之“前”定义预期行为
- 在开发过程中持续运行评测
- 跟踪每次变更带来的回归（Regressions）
- 使用 pass@k 指标来衡量可靠性

## 评测类型

### 能力评测（Capability Evals）
测试 Claude 是否能够完成之前无法完成的任务：
```markdown
[CAPABILITY EVAL: feature-name]
Task: Description of what Claude should accomplish
Success Criteria:
  - [ ] Criterion 1
  - [ ] Criterion 2
  - [ ] Criterion 3
Expected Output: Description of expected result
```

### 回归评测（Regression Evals）
确保变更不会破坏现有功能：
```markdown
[REGRESSION EVAL: feature-name]
Baseline: SHA or checkpoint name
Tests:
  - existing-test-1: PASS/FAIL
  - existing-test-2: PASS/FAIL
  - existing-test-3: PASS/FAIL
Result: X/Y passed (previously Y/Y)
```

## 评分器（Grader）类型

### 1. 基于代码的评分器（Code-Based Grader）
使用代码进行确定性检查：
```bash
# Check if file contains expected pattern
grep -q "export function handleAuth" src/auth.ts && echo "PASS" || echo "FAIL"

# Check if tests pass
npm test -- --testPathPattern="auth" && echo "PASS" || echo "FAIL"

# Check if build succeeds
npm run build && echo "PASS" || echo "FAIL"
```

### 2. 基于模型的评分器（Model-Based Grader）
使用 Claude 评估开放式输出：
```markdown
[MODEL GRADER PROMPT]
Evaluate the following code change:
1. Does it solve the stated problem?
2. Is it well-structured?
3. Are edge cases handled?
4. Is error handling appropriate?

Score: 1-5 (1=poor, 5=excellent)
Reasoning: [explanation]
```

### 3. 人工评分器（Human Grader）
标记以供人工审查：
```markdown
[HUMAN REVIEW REQUIRED]
Change: Description of what changed
Reason: Why human review is needed
Risk Level: LOW/MEDIUM/HIGH
```

## 指标（Metrics）

### pass@k
“k 次尝试中至少成功一次”
- pass@1：首次尝试成功率
- pass@3：3 次尝试内成功
- 典型目标：pass@3 > 90%

### pass^k
“k 次试验全部成功”
- 更高的可靠性门槛
- pass^3：连续 3 次成功
- 用于关键路径（Critical Paths）

## 评测工作流

### 1. 定义（编码前）
```markdown
## EVAL DEFINITION: feature-xyz

### Capability Evals
1. Can create new user account
2. Can validate email format
3. Can hash password securely

### Regression Evals
1. Existing login still works
2. Session management unchanged
3. Logout flow intact

### Success Metrics
- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
```

### 2. 实现
编写代码以通过定义的评测。

### 3. 评估
```bash
# Run capability evals
[Run each capability eval, record PASS/FAIL]

# Run regression evals
npm test -- --testPathPattern="existing"

# Generate report
```

### 4. 报告
```markdown
EVAL REPORT: feature-xyz
========================

Capability Evals:
  create-user:     PASS (pass@1)
  validate-email:  PASS (pass@2)
  hash-password:   PASS (pass@1)
  Overall:         3/3 passed

Regression Evals:
  login-flow:      PASS
  session-mgmt:    PASS
  logout-flow:     PASS
  Overall:         3/3 passed

Metrics:
  pass@1: 67% (2/3)
  pass@3: 100% (3/3)

Status: READY FOR REVIEW
```

## 集成模式

### 实现前（Pre-Implementation）
```
/eval define feature-name
```
在 `.claude/evals/feature-name.md` 创建评测定义文件。

### 实现中（During Implementation）
```
/eval check feature-name
```
运行当前评测并报告状态。

### 实现后（Post-Implementation）
```
/eval report feature-name
```
生成完整的评测报告。

## 评测存储

在项目中存储评测：
```
.claude/
  evals/
    feature-xyz.md      # 评测定义
    feature-xyz.log     # 评测运行历史
    baseline.json       # 回归基线
```

## 最佳实践

1. **在编码之“前”定义评测** —— 强制对成功准则进行清晰思考。
2. **频繁运行评测** —— 尽早发现回归。
3. **随着时间推移跟踪 pass@k** —— 监控可靠性趋势。
4. **尽可能使用代码评分器** —— 确定性（Deterministic）优于概率性（Probabilistic）。
5. **安全相关的由人工审查** —— 永远不要完全自动化安全检查。
6. **保持评测快速** —— 缓慢的评测往往不会被运行。
7. **将评测与代码一同进行版本控制** —— 评测是一等公民产物（First-class Artifacts）。

## 示例：添加身份验证

```markdown
## EVAL: add-authentication

### Phase 1: Define (10 min)
Capability Evals:
- [ ] User can register with email/password
- [ ] User can login with valid credentials
- [ ] Invalid credentials rejected with proper error
- [ ] Sessions persist across page reloads
- [ ] Logout clears session

Regression Evals:
- [ ] Public routes still accessible
- [ ] API responses unchanged
- [ ] Database schema compatible

### Phase 2: Implement (varies)
[Write code]

### Phase 3: Evaluate
Run: /eval check add-authentication

### Phase 4: Report
EVAL REPORT: add-authentication
==============================
Capability: 5/5 passed (pass@3: 100%)
Regression: 3/3 passed (pass^3: 100%)
Status: SHIP IT
```
