---
name: instinct-import
description: 从队友、技能生成器（Skill Creator）或其他来源导入直觉（Instincts）
command: /instinct-import
implementation: python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py import <file>
---

# 直觉导入命令（Instinct Import Command）

## 实现

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py import <file-or-url> [--dry-run] [--force] [--min-confidence 0.7]
```

从以下来源导入直觉（Instincts）：
- 队友导出的文件
- 技能生成器（Skill Creator）（仓库分析）
- 社区集合
- 之前的机器备份

## 用法

```
/instinct-import team-instincts.yaml
/instinct-import https://github.com/org/repo/instincts.yaml
/instinct-import --from-skill-creator acme/webapp
```

## 执行流程

1. 获取直觉文件（本地路径或 URL）
2. 解析并验证格式
3. 检查是否与现有直觉重复
4. 合并或添加新直觉
5. 保存至 `~/.claude/homunculus/instincts/inherited/`

## 导入过程示例

```
📥 正在从 team-instincts.yaml 导入直觉：
================================================

发现 12 条待导入的直觉。

正在分析冲突...

## 新直觉 (8)
这些将被添加：
  ✓ use-zod-validation (置信度: 0.7)
  ✓ prefer-named-exports (置信度: 0.65)
  ✓ test-async-functions (置信度: 0.8)
  ...

## 重复直觉 (3)
已存在类似的直觉：
  ⚠️ prefer-functional-style
     本地：0.8 置信度，12 个观测项
     导入：0.7 置信度
     → 保留本地（置信度更高）

  ⚠️ test-first-workflow
     本地：0.75 置信度
     导入：0.9 置信度
     → 更新为导入的内容（置信度更高）

## 冲突直觉 (1)
这些与本地直觉相矛盾：
  ❌ use-classes-for-services
     与 avoid-classes 冲突
     → 跳过（需要手动解决）

---
导入 8 个新项，更新 1 个，跳过 3 个？
```

## 合并策略（Merge Strategies）

### 处理重复项
当导入的直觉与现有直觉匹配时：
- **高置信度胜出**：保留置信度（Confidence）较高的一方
- **合并证据**：累计观测项（Observation）计数
- **更新时间戳**：标记为最近已验证

### 处理冲突
当导入的直觉与现有直觉冲突时：
- **默认跳过**：不导入产生冲突的直觉
- **标记待审查**：将两者都标记为需要关注
- **手动解决**：由用户决定保留哪一个

## 来源追踪

导入的直觉会被标记以下字段：
```yaml
source: "inherited"
imported_from: "team-instincts.yaml"
imported_at: "2025-01-22T10:30:00Z"
original_source: "session-observation"  # 或 "repo-analysis"
```

## 技能生成器（Skill Creator）集成

从技能生成器（Skill Creator）导入时：

```
/instinct-import --from-skill-creator acme/webapp
```

这将获取通过仓库分析生成的直觉：
- 来源：`repo-analysis`
- 较高的初始置信度（0.7+）
- 已链接到源仓库

## 参数标志（Flags）

- `--dry-run`：预览而不执行导入
- `--force`：即使存在冲突也强制导入
- `--merge-strategy <higher|local|import>`：如何处理重复项
- `--from-skill-creator <owner/repo>`：从技能生成器（Skill Creator）分析结果导入
- `--min-confidence <n>`：仅导入置信度高于阈值的直觉

## 输出

导入完成后：
```
✅ 导入完成！

已添加：8 条直觉
已更新：1 条直觉
已跳过：3 条直觉（2 个重复，1 个冲突）

新直觉已保存至：~/.claude/homunculus/instincts/inherited/

运行 /instinct-status 查看所有直觉。
```