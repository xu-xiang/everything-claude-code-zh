# Framework / System Service 上下文

适用于：
- ServiceManager 注册服务
- SystemService 生命周期
- manager-service 调用链
- framework API 到 service 实现链路

## 重点风险

1. 服务初始化顺序
2. Binder 线程池与调用线程
3. 锁竞争和嵌套调用
4. 权限检查遗漏
5. 异常处理导致的系统稳定性问题
6. 向下兼容问题