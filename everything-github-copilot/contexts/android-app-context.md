# Android 应用开发上下文

本项目可能包含以下层次：

- UI 层：Activity / Fragment / Compose
- 展示层：ViewModel
- 业务层：UseCase / Interactor
- 数据层：Repository / DataSource
- 基础设施层：网络、数据库、缓存

## 关注点

1. 状态管理清晰。
2. 生命周期安全。
3. 异步逻辑边界明确。
4. UI 行为可预测。
5. 错误处理清晰。
6. 尽量便于测试。

## 提问建议

向 Copilot 提问时，尽量说明：
- 当前类位于哪一层
- 是否使用 Compose
- 是否使用协程 / Flow / LiveData
- 是否要求保留现有 API 和页面行为