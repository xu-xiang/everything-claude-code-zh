---
name: instinct-status
description: 显示所有已学习的直觉（Instincts）及其置信度水平
command: /instinct-status
implementation: python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py status
---

# Instinct Status 命令

按领域（Domain）分组显示所有已学习的直觉（Instincts）及其置信度得分。

## 实现

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py status
```

## 用法

```
/instinct-status
/instinct-status --domain code-style
/instinct-status --low-confidence
```

## 执行逻辑

1. 从 `~/.claude/homunculus/instincts/personal/` 读取所有个人直觉文件
2. 从 `~/.claude/homunculus/instincts/inherited/` 读取继承的直觉
3. 按领域分组显示，并附带置信度进度条

## 输出格式

```
📊 直觉状态 (Instinct Status)
==================

## 代码风格 (4 个直觉)

### prefer-functional-style
触发条件 (Trigger)：编写新函数时
动作 (Action)：优先使用函数式模式而非类
置信度 (Confidence)：████████░░ 80%
来源 (Source)：session-observation | 最后更新：2025-01-22

### use-path-aliases
触发条件 (Trigger)：导入模块时
动作 (Action)：使用 @/ 路径别名而非相对导入
置信度 (Confidence)：██████░░░░ 60%
来源 (Source)：repo-analysis (github.com/acme/webapp)

## 测试 (2 个直觉)

### test-first-workflow
触发条件 (Trigger)：添加新功能时
动作 (Action)：先写测试，再写实现
置信度 (Confidence)：█████████░ 90%
来源 (Source)：session-observation

## 工作流 (3 个直觉)

### grep-before-edit
触发条件 (Trigger)：修改代码时
动作 (Action)：先用 Grep 搜索，用 Read 确认，再进行编辑 (Edit)
置信度 (Confidence)：███████░░░ 70%
来源 (Source)：session-observation

---
总计：9 个直觉（4 个个人，5 个继承）
观察器 (Observer)：运行中（上次分析：5 分钟前）
```

## 参数 (Flags)

- `--domain <name>`：按领域过滤（code-style、testing、git 等）
- `--low-confidence`：仅显示置信度 < 0.5 的直觉
- `--high-confidence`：仅显示置信度 >= 0.7 的直觉
- `--source <type>`：按来源过滤（session-observation、repo-analysis、inherited）
- `--json`：以 JSON 格式输出，供程序化使用
