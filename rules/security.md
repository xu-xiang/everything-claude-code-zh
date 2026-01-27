# 安全指南 (Security Guidelines)

## 强制安全检查 (Mandatory Security Checks)

在任何提交（Commit）之前：
- [ ] 无硬编码凭据（API 密钥、密码、令牌/Tokens）
- [ ] 所有用户输入均已验证
- [ ] 预防 SQL 注入（使用参数化查询）
- [ ] 预防 XSS（对 HTML 进行净化处理/Sanitized）
- [ ] 已启用 CSRF 保护
- [ ] 身份验证/授权已验证
- [ ] 所有端点均已设置速率限制（Rate limiting）
- [ ] 错误消息不泄露敏感数据

## 凭据管理 (Secret Management)

```typescript
// 严禁：硬编码凭据
const apiKey = "sk-proj-xxxxx"

// 推荐：环境变量
const apiKey = process.env.OPENAI_API_KEY

if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

## 安全响应协议 (Security Response Protocol)

如果发现安全问题：
1. 立即停止（STOP）
2. 使用 **security-reviewer** 智能体（Agent）
3. 在继续之前修复严重（CRITICAL）问题
4. 轮换任何暴露的凭据
5. 审查整个代码库是否存在类似问题
