# 评测命令（Eval Command）

管理评测驱动开发（eval-driven development）工作流。

## 用法（Usage）

`/eval [define|check|report|list] [feature-name]`

## 定义评测（Define Evals）

`/eval define feature-name`

创建一个新的评测定义：

1. 创建 `.claude/evals/feature-name.md` 文件，使用以下模板：

```markdown
## EVAL: feature-name
创建时间：$(date)

### 能力评测（Capability Evals）
- [ ] [能力描述 1]
- [ ] [能力描述 2]

### 回归评测（Regression Evals）
- [ ] [现有行为 1 仍然正常工作]
- [ ] [现有行为 2 仍然正常工作]

### 通过准则（Success Criteria）
- 能力评测（capability evals）的 pass@3 > 90%
- 回归评测（regression evals）的 pass^3 = 100%
```

2. 提示用户填写具体准则。

## 检查评测（Check Evals）

`/eval check feature-name`

运行特定功能的评测：

1. 从 `.claude/evals/feature-name.md` 读取评测定义。
2. 对于每一项能力评测：
   - 尝试验证准则。
   - 记录 PASS/FAIL。
   - 在 `.claude/evals/feature-name.log` 中记录尝试日志。
3. 对于每一项回归评测：
   - 运行相关测试。
   - 与基准（baseline）进行对比。
   - 记录 PASS/FAIL。
4. 报告当前状态：

```
EVAL CHECK: feature-name
========================
能力（Capability）: X/Y 通过
回归（Regression）: X/Y 通过
状态（Status）: 进行中（IN PROGRESS）/ 已就绪（READY）
```

## 生成报告（Report Evals）

`/eval report feature-name`

生成完整的评测报告：

```
EVAL REPORT: feature-name
=========================
生成时间：$(date)

能力评测（CAPABILITY EVALS）
----------------
[eval-1]: PASS (pass@1)
[eval-2]: PASS (pass@2) - 需重试
[eval-3]: FAIL - 见备注

回归评测（REGRESSION EVALS）
----------------
[test-1]: PASS
[test-2]: PASS
[test-3]: PASS

指标（METRICS）
-------
能力 pass@1: 67%
能力 pass@3: 100%
回归 pass^3: 100%

备注（NOTES）
-----
[任何问题、边界情况或观察结果]

建议（RECOMMENDATION）
--------------
[可发布（SHIP）/ 需改进（NEEDS WORK）/ 阻塞（BLOCKED）]
```

## 列出评测（List Evals）

`/eval list`

显示所有评测定义：

```
EVAL DEFINITIONS
================
feature-auth      [3/5 通过] 进行中（IN PROGRESS）
feature-search    [5/5 通过] 已就绪（READY）
feature-export    [0/4 通过] 未开始（NOT STARTED）
```

## 参数（Arguments）

$ARGUMENTS:
- `define <name>` - 创建新的评测定义。
- `check <name>` - 运行并检查评测。
- `report <name>` - 生成完整报告。
- `list` - 显示所有评测。
- `clean` - 清除旧的评测日志（保留最近 10 次运行记录）。
