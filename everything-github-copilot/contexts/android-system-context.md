# Android 系统开发上下文

本项目可能包含以下模块：

- framework
- system service
- Binder / AIDL
- 权限和系统配置逻辑
- 启动流程相关逻辑

## 关注点

1. 兼容性高于“写法美观”。
2. 稳定性高于抽象纯度。
3. 涉及跨进程通信时，重点关注序列化成本、线程模型和异常传播。
4. system_server 中应避免长耗时、阻塞和锁竞争。
5. 涉及权限、用户、进程身份时，优先保守处理。

## 提问建议

在向 Copilot 提问时，可补充：
- 这是 framework 代码还是 system service 代码
- 是否在 system_server 中执行
- 是否涉及 Binder / AIDL
- 是否涉及权限校验
- 是否要求保持 API 行为不变