# 安全审查提问模板

## 1. Android 安全审查
请基于 `checklists/android-security-checklist.md`，
审查这段 Android 代码的安全风险，重点关注：
- 权限
- 导出组件
- Intent 输入
- Binder 调用
- 敏感日志
- 数据泄露风险

请按严重程度排序输出。

## 2. 系统权���审查
请作为 Android security reviewer，
审查这段 framework / system service 代码的权限校验、身份处理和跨用户边界问题。