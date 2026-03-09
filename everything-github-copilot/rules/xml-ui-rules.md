# XML / UI 规则

## XML View 项目

1. 避免在 UI 层堆积复杂业务逻辑。
2. 注意空视图、错误态、加载态切换。
3. 留意重复 findViewById / binding 调用。
4. 监听器注册后应考虑解除绑定时机���
5. 注意 RecyclerView 刷新粒度与性能影响。

## Compose 项目

1. 保持状态单向流动。
2. 不在 Composable 内执行不必要副作用。
3. 谨慎使用 `LaunchedEffect`、`rememberCoroutineScope`、`DisposableEffect`。
4. 关注重组频率和不必要对象创建。
5. UI 层不直接承载复杂业务判断。

## 通用要求

- 修改 UI 时，必须说明预期交互是否变化。
- 如果引入状态变量，说明其生命周期和来源。