# 验证循环技能（Verification Loop Skill）

一个用于 Claude Code 会话的全面验证系统。

## 何时使用

在以下场景调用此技能（Skill）：
- 完成功能开发或重大代码变更后
- 创建 PR 之前
- 当你想确保质量门禁（Quality Gates）通过时
- 代码重构之后

## 验证阶段（Verification Phases）

### 阶段 1：构建验证（Build Verification）
```bash
# 检查项目是否可以构建
npm run build 2>&1 | tail -20
# 或者
pnpm build 2>&1 | tail -20
```

如果构建失败，请停止并修复后再继续。

### 阶段 2：类型检查（Type Check）
```bash
# TypeScript 项目
npx tsc --noEmit 2>&1 | head -30

# Python 项目
pyright . 2>&1 | head -30
```

报告所有类型错误。在继续之前修复关键错误。

### 阶段 3：Lint 检查（Lint Check）
```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

### 阶段 4：测试套件（Test Suite）
```bash
# 运行带有覆盖率报告的测试
npm run test -- --coverage 2>&1 | tail -50

# 检查覆盖率阈值
# 目标：最低 80%
```

报告内容：
- 总测试数：X
- 通过：X
- 失败：X
- 覆盖率：X%

### 阶段 5：安全扫描（Security Scan）
```bash
# 检查密钥
grep -rn "sk-" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# 检查 console.log
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### 阶段 6：差异审查（Diff Review）
```bash
# 显示变更内容
git diff --stat
git diff HEAD~1 --name-only
```

审查每个变更的文件，确认：
- 无意间的变更
- 缺失的错误处理
- 潜在的边缘情况

## 输出格式（Output Format）

运行完所有阶段后，生成一份验证报告：

```
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## 持续模式（Continuous Mode）

对于长时间的会话（Session），每 15 分钟或在重大变更后运行一次验证：

```markdown
设置心理检查点：
- 完成每个函数后
- 完成一个组件后
- 在开始下一个任务之前

运行：/verify
```

## 与钩子（Hooks）集成

此技能（Skill）是对 `PostToolUse` 钩子（Hooks）的补充，但提供了更深层次的验证。
钩子可以立即发现问题；此技能则提供全面的审查。
