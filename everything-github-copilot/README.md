# everything-github-copilot

一套面向 **Android Studio + GitHub Copilot 插件** 的可用 Copilot 规范目录，适用于：

- Android 系统开发
- Android 应用开发
- Kotlin / Java / XML / Gradle 工程
- 代码分析、修复、重构、测试、安全审查

## 设计原则

本目录不是 GitHub Copilot 的“原生配置目录”，而是用于：

1. 给开发者提供稳定的提问模板
2. 给 Copilot Chat 提供一致的上下文约束
3. 减少 AI 生成代码时的风格漂移
4. 在 Android 系统 / 应用开发中强调最小改动、兼容性与安全性

## 使用方式

在 Android Studio 中使用 GitHub Copilot Chat 时：

1. 先阅读 `contexts/` 中对应场景的上下文
2. 在提问前引用 `rules/` 中相关规则
3. 从 `prompts/` 中选择合适模板
4. 在提交前使用 `checklists/` 做人工核查

## 推荐优先阅读

1. `copilot-usage.md`
2. `rules/general-engineering-rules.md`
3. `rules/android-system-rules.md`
4. `rules/android-app-rules.md`
5. `checklists/change-review-checklist.md`

## 适用范围

### Android 系统开发
适用于：
- framework
- system service
- Binder / AIDL
- 权限、兼容性、稳定性相关改动

### Android 应用开发
适用于：
- Activity / Fragment / ViewModel / Repository
- Compose / XML UI
- 网络、存储、状态管理、测试

## 不包含的能力

本目录不依赖：
- Claude Code hooks
- MCP servers
- Claude 专属 plugins
- IDE 自动注入系统提示

因此它是“可迁移使用规范”，不是“自动运行配置”。