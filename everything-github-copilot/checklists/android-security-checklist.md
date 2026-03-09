# Android 安全检查清单

## 通用
- 是否新增了敏感日志？
- 是否泄露了用户数据、token、设备信息？
- 是否缺少输入校验？

## Android 组件
- Activity / Service / Receiver / Provider 是否错误导出？
- Intent 输入是否校验？
- PendingIntent 使用是否安全？

## 系统开发
- 是否缺少调用者身份校验？
- 是否缺少权限校验？
- 是否跨用户处理不当？
- 是否清理 / 恢复调用身份不当？

## 数据
- 文件、数据库、SharedPreferences 是否有越权风险？
- IPC 传输的数据是否可被伪造或滥用？