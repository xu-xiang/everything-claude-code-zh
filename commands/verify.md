# 验证（Verification）命令

对当前代码库状态进行全面验证。

## 指令（Instructions）

请按以下确切顺序执行验证：

1. **构建检查（Build Check）**
   - 运行此项目的构建命令
   - 如果构建失败，报告错误并停止（STOP）

2. **类型检查（Type Check）**
   - 运行 TypeScript/类型检查器
   - 报告所有错误及其对应的 `file:line`（文件:行号）

3. **代码规范检查（Lint Check）**
   - 运行 Linter
   - 报告警告与错误

4. **测试套件（Test Suite）**
   - 运行所有测试
   - 报告通过/失败的数量
   - 报告覆盖率百分比

5. **Console.log 审计**
   - 在源文件中搜索 `console.log`
   - 报告其所在位置

6. **Git 状态（Git Status）**
   - 显示未提交的更改
   - 显示自上次提交以来修改的文件

## 输出（Output）

生成一份简洁的验证报告：

```
VERIFICATION: [PASS/FAIL]

Build:    [OK/FAIL]
Types:    [OK/X errors]
Lint:     [OK/X issues]
Tests:    [X/Y passed, Z% coverage]
Secrets:  [OK/X found]
Logs:     [OK/X console.logs]

Ready for PR: [YES/NO]
```

如果存在任何关键问题，请列出这些问题并给出修复建议。

## 参数（Arguments）

`$ARGUMENTS` 可以是：
- `quick` - 仅执行构建 + 类型检查
- `full` - 执行所有检查（默认）
- `pre-commit` - 执行与提交相关的检查
- `pre-pr` - 执行完整检查以及安全扫描
