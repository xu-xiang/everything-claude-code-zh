# Android 应用开发提问模板

## 1. 分析 ViewModel
请基于 `contexts/android-app-context.md` 和 `rules/android-app-rules.md`，
分析这个 ViewModel 的状态管理、协程使用、错误处理和可测试性，
并给出最小改进建议。先不要直接重写。

## 2. 修复 UI Bug
请严格遵循 `rules/android-app-rules.md` 和 `rules/xml-ui-rules.md`，
分析这个 Android UI Bug 的根因，并给出最小修改方案。
请说明是否影响生命周期、状态恢复和用户可见行为。

## 3. 优化 Repository 逻辑
请分析这个 Repository 的职责边界、异常处理和数据流设计，
在不改变外部行为的前提下，给出最小优化建议。

## 4. Compose 状态问题
请分析这个 Compose 代码中的状态来源、重组风险和副作用使用方式，
指出潜在问题，并给出最小修改方案。