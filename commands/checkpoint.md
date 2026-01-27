# 检查点（Checkpoint）指令

在工作流（Workflow）中创建或验证检查点。

## 用法

`/checkpoint [create|verify|list] [name]`

## 创建检查点（Create Checkpoint）

创建检查点时：

1. 运行 `/verify quick` 以确保当前状态干净
2. 使用检查点名称创建一个 git stash 或提交（Commit）
3. 将检查点记录到 `.claude/checkpoints.log`：

```bash
echo "$(date +%Y-%m-%d-%H:%M) | $CHECKPOINT_NAME | $(git rev-parse --short HEAD)" >> .claude/checkpoints.log
```

4. 报告检查点已创建

## 验证检查点（Verify Checkpoint）

对比检查点进行验证时：

1. 从日志中读取检查点
2. 将当前状态与检查点进行对比：
   - 自检查点以来新增的文件
   - 自检查点以来修改的文件
   - 当前与当时的测试通过率对比
   - 当前与当时的代码覆盖率对比

3. 报告：
```
CHECKPOINT COMPARISON: $NAME
============================
Files changed: X
Tests: +Y passed / -Z failed
Coverage: +X% / -Y%
Build: [PASS/FAIL]
```

## 列出检查点（List Checkpoints）

显示所有检查点，包括：
- 名称
- 时间戳
- Git SHA
- 状态（当前、落后、超前）

## 工作流（Workflow）

典型的检查点工作流：

```
[Start] --> /checkpoint create "feature-start"
   |
[Implement] --> /checkpoint create "core-done"
   |
[Test] --> /checkpoint verify "core-done"
   |
[Refactor] --> /checkpoint create "refactor-done"
   |
[PR] --> /checkpoint verify "feature-start"
```

## 参数（Arguments）

$ARGUMENTS:
- `create <name>` - 创建具名检查点
- `verify <name>` - 对比指定的检查点进行验证
- `list` - 显示所有检查点
- `clear` - 移除旧检查点（保留最后 5 个）
