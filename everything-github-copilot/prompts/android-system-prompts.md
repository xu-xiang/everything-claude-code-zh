# Android 系统开发提问模板

## 1. 分析 system service 代码
请基于 `contexts/android-system-context.md` 和 `rules/android-system-rules.md`，
先分析这段 system service 代码的职责、线程模型、权限边界和潜在风险，
再给出最小修改建议。先不要直接改代码。

## 2. 分析 Binder / AIDL 调用链
请基于 `contexts/binder-aidl-context.md`，
分析这段 Binder / AIDL 代码的调用方向、线程影响、权限检查、异常传播和性能风险。
请按“问题理解 / 风险点 / 最小修改建议 / 验证方式”输出。

## 3. 修复 framework 兼容性问题
请严格遵循 `rules/android-system-rules.md`，
为这个 framework 问题提供最小修复方案，保持现有外部行为不变，
并说明兼容性风险和回归验证点。

## 4. 审查 system_server 修改
请作为 Android framework reviewer，
审查这段运行在 system_server 中的改动，重点关注：
- 锁与线程
- 长耗时操作
- 权限校验
- 稳定性
- 回归风险
请按严重程度排序输出问题。