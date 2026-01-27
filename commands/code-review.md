# 代码审查 (Code Review)

对未提交的更改进行全面的安全和质量审查：

1. 获取已更改的文件：`git diff --name-only HEAD`

2. 对每个更改的文件，检查以下项：

**安全问题 (Security Issues) (严重 - CRITICAL):**
- 硬编码的凭据、API 密钥、令牌 (Tokens)
- SQL 注入漏洞
- XSS 漏洞  
- 缺少输入验证
- 不安全的依赖项
- 路径遍历风险

**代码质量 (Code Quality) (高 - HIGH):**
- 函数长度 > 50 行
- 文件长度 > 800 行
- 嵌套深度 > 4 层
- 缺少错误处理
- `console.log` 语句
- TODO/FIXME 注释
- 公共 API 缺少 JSDoc

**最佳实践 (Best Practices) (中 - MEDIUM):**
- 变更模式 (Mutation patterns)（应改用不可变模式 (immutable)）
- 代码/注释中使用 Emoji
- 新代码缺少测试
- 无障碍访问问题 (a11y)

3. 生成包含以下内容的报告：
   - 严重程度 (Severity)：严重 (CRITICAL)、高 (HIGH)、中 (MEDIUM)、低 (LOW)
   - 文件位置和行号
   - 问题描述
   - 修复建议

4. 如果发现“严重 (CRITICAL)”或“高 (HIGH)”级别的问题，则阻止提交 (Block commit)

绝不要批准带有安全漏洞的代码！
