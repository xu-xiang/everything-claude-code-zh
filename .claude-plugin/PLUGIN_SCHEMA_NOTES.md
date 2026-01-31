# 插件清单模式（Plugin Manifest Schema）说明

本文档记录了 Claude Code 插件清单校验器（Validator）中**未公开但强制执行的约束条件**。

这些规则基于真实的安装失败案例、校验器行为分析以及与已知可用插件的对比。
它们的存在是为了防止隐性破坏（silent breakage）和重复出现的回归（regressions）问题。

如果你需要编辑 `.claude-plugin/plugin.json`，请务必先阅读本文。

---

## 摘要（优先阅读）

Claude 插件清单校验器非常**严格且具有确定性**。
它强制执行了一些在公共模式（Schema）引用中未完全记录的规则。

最常见的失败模式是：

> 清单看起来很合理，但校验器拒绝了它，并给出模糊的错误提示，例如
> `agents: Invalid input`

本文档将解释其原因。

---

## 必填字段

### `version`（强制要求）

校验器要求必须包含 `version` 字段，即使在某些示例中省略了它。

如果缺失该字段，在应用市场安装或 CLI 校验期间可能会失败。

示例：

```json
{
  "version": "1.1.0"
}
```

---

## 字段形态规则

以下字段**必须始终为数组（Arrays）**：

* `agents`
* `commands`
* `skills`
* `hooks`（如果存在）

即使只有一个条目，**也不接受字符串（Strings）类型**。

### 错误示例（Invalid）

```json
{
  "agents": "./agents"
}
```

### 正确示例（Valid）

```json
{
  "agents": ["./agents/planner.md"]
}
```

这一规则一致适用于所有组件路径字段。

---

## 路径解析规则（关键）

### Agents 必须使用显式文件路径

校验器**不接受 `agents` 字段使用目录路径**。

即使是以下写法也会失败：

```json
{
  "agents": ["./agents/"]
}
```

相反，你必须显式枚举智能体（Agent）文件：

```json
{
  "agents": [
    "./agents/planner.md",
    "./agents/architect.md",
    "./agents/code-reviewer.md"
  ]
}
```

这是校验错误最常见的来源。

### 命令（Commands）与技能（Skills）

* `commands` 和 `skills` **仅在包裹在数组中时**接受目录路径。
* 显式文件路径是最安全且最能兼容未来的做法。

---

## 校验器行为注意事项

* `claude plugin validate` 比某些应用市场预览（marketplace previews）更严格。
* 校验可能在本地通过，但如果路径含义模糊，在安装时可能会失败。
* 错误提示通常很通用（`Invalid input`），且不会指出根本原因。
* 跨平台安装（尤其是 Windows）对路径假设的容忍度较低。

请假设校验器是严苛且完全按字面意思理解的。

---

## `hooks` 字段：请勿添加

> ⚠️ **关键（CRITICAL）：** 请勿在 `plugin.json` 中添加 `"hooks"` 字段。这是一个回归测试强制要求的规则。

### 为什么这很重要

按照约定，Claude Code v2.1+ 会**自动加载**任何已安装插件中的 `hooks/hooks.json`。如果你在 `plugin.json` 中也声明了它，你会得到：

```
Duplicate hooks file detected: ./hooks/hooks.json resolves to already-loaded file.
The standard hooks/hooks.json is loaded automatically, so manifest.hooks should
only reference additional hook files.
```

### 反复变更的历史

这曾导致此仓库中出现多次“修复/回滚”循环：

| 提交 | 动作 | 触发原因 |
|--------|--------|---------|
| `22ad036` | 添加（ADD）hooks | 用户报告“钩子未加载” |
| `a7bc5f2` | 移除（REMOVE）hooks | 用户报告“重复钩子错误” (#52) |
| `779085e` | 添加（ADD）hooks | 用户报告“智能体未加载” (#88) |
| `e3a1306` | 移除（REMOVE）hooks | 用户报告“重复钩子错误” (#103) |

**根本原因：** Claude Code CLI 在不同版本间更改了行为：
- v2.1 之前：需要显式声明 `hooks`。
- v2.1+：按约定自动加载，显式声明会导致重复错误。

### 当前规则（由测试强制执行）

`tests/hooks/hooks.test.js` 中的测试 `plugin.json does NOT have explicit hooks declaration` 会阻止重新引入此声明。

**如果你要添加额外的钩子文件**（非 `hooks/hooks.json`），可以声明它们。但标准路径 `hooks/hooks.json` **绝不能**被声明。

---

## 已知的反模式（Anti-Patterns）

这些看起来正确但会被拒绝：

* 使用字符串值而非数组
* 在 `agents` 中使用目录数组
* 缺失 `version`
* 依赖推断路径
* 假设应用市场行为与本地校验一致
* **添加 `"hooks": "./hooks/hooks.json"`** —— 按约定自动加载，会导致重复错误

不要尝试“取巧”，请保持显式声明。

---

## 最小已知可用示例

```json
{
  "version": "1.1.0",
  "agents": [
    "./agents/planner.md",
    "./agents/code-reviewer.md"
  ],
  "commands": ["./commands/"],
  "skills": ["./skills/"]
}
```

此结构已通过 Claude 插件校验器的验证。

**重要提示：** 请注意这里**没有** `"hooks"` 字段。`hooks/hooks.json` 文件会按约定自动加载。显式添加它会导致重复错误。

---

## 贡献者建议

在提交涉及 `plugin.json` 的更改前：

1. 为智能体（Agents）使用显式文件路径
2. 确保所有组件字段均为数组
3. 包含 `version` 字段
4. 运行以下命令：

```bash
claude plugin validate .claude-plugin/plugin.json
```

如有疑问，宁可繁琐也不要为了方便而导致解析失败。

---

## 为什么存在此文件

此仓库被广泛 Fork 并作为参考实现。

在此记录校验器的奇特行为（quirks）是为了：

* 防止重复出现的问题
* 减少贡献者的挫败感
* 随着生态系统的演进保持插件的稳定性

如果校验器规则发生变化，请首先更新此文档。
