# 插件清单模式（Manifest Schema）注意事项

本文档记录了 Claude Code 插件清单校验器中**未见于文档但强制执行的约束**。

这些规则基于真实的安装失败案例、校验器行为以及与已知可用插件的对比。
设置这些规则是为了防止隐性故障和重复的回归问题。

如果你编辑 `.claude-plugin/plugin.json`，请先阅读本文。

---

## 摘要（优先阅读）

Claude 插件清单校验器**极其严格且具有主观性**。
它执行了一些在公开模式（Schema）参考文档中未完全说明的规则。

最常见的失败模式是：

> 清单看起来很合理，但校验器以模糊的错误拒绝它，例如：
> `agents: Invalid input`

本文档将解释其原因。

---

## 必填字段

### `version`（强制性）

即便在某些示例中被省略，校验器也要求必须包含 `version` 字段。

如果缺失，在应用市场安装或 CLI 校验期间可能会失败。

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

即便只有一个条目，**也不接受字符串（Strings）**。

### 错误写法（Invalid）

```json
{
  "agents": "./agents"
}
```

### 正确写法（Valid）

```json
{
  "agents": ["./agents/planner.md"]
}
```

这适用于所有组件路径字段。

---

## 路径解析规则（至关重要）

### Agents 必须使用显式文件路径

校验器**不接受 `agents` 使用目录路径**。

即便如下写法也会失败：

```json
{
  "agents": ["./agents/"]
}
```

相反，你必须显式列举智能体（Agent）文件：

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

### Commands 和 Skills

* `commands` 和 `skills` 仅在**包裹在数组中**时才接受目录路径。
* 使用显式文件路径是最安全且面向未来的做法。

---

## 校验器行为备注

* `claude plugin validate` 比某些应用市场预览更严格。
* 校验可能在本地通过，但如果路径含义模糊，则在安装时可能会失败。
* 错误通常很笼统（`Invalid input`），且不指示根本原因。
* 跨平台安装（尤其是 Windows）对路径假设的容忍度较低。

请假设校验器是“带有敌意的”且完全字面化的。

---

## 已知的反模式（Anti-Patterns）

这些看起来正确但会被拒绝：

* 使用字符串值而非数组
* 为 `agents` 提供目录数组
* 缺失 `version`
* 依赖推断路径
* 假设应用市场的行为与本地校验一致

不要耍小聪明。请保持显式。

---

## 最小已知有效示例

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

该结构已通过 Claude 插件校验器的验证。

---

## 对贡献者的建议

在提交涉及 `plugin.json` 的更改之前：

1. 为 agents 使用显式文件路径
2. 确保所有组件字段均为数组
3. 包含 `version`
4. 运行：

```bash
claude plugin validate .claude-plugin/plugin.json
```

如有疑问，宁可繁琐也不要追求便利。

---

## 为什么存在此文件

此仓库被广泛 fork 并用作参考实现。

在此记录校验器的特性：

* 防止重复出现的问题
* 减少贡献者的挫败感
* 随着生态系统的演进保持插件的稳定性

如果校验器发生变化，请首先更新本文档。
