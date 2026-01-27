---
description: 针对地道模式、并发安全、错误处理和安全性的全面 Go 代码审查。调用 go-reviewer 智能体 (Agent)。
---

# Go 代码审查 (Go Code Review)

此命令调用 **go-reviewer** 智能体 (Agent) 进行针对 Go 语言特性的全面代码审查。

## 此命令的作用

1. **识别 Go 代码变更**：通过 `git diff` 查找已修改的 `.go` 文件
2. **运行静态分析**：执行 `go vet`、`staticcheck` 和 `golangci-lint`
3. **安全扫描**：检查 SQL 注入、命令注入、竞态条件等安全隐患
4. **并发审查**：分析 Goroutine 安全、通道 (Channel) 使用、互斥锁 (Mutex) 模式
5. **地道 Go 检查**：验证代码是否遵循 Go 惯例和最佳实践
6. **生成报告**：按严重程度对问题进行分类

## 适用场景

在以下情况下使用 `/go-review`：
- 编写或修改 Go 代码后
- 提交 Go 代码变更前
- 审查包含 Go 代码的拉取请求 (Pull Request)
- 熟悉新的 Go 代码库
- 学习地道的 Go 模式

## 审查类别

### 致命 (CRITICAL) - 必须修复
- SQL/命令注入漏洞
- 未经同步的并发访问（竞态条件）
- Goroutine 泄露
- 硬编码的凭据
- 不安全的指针 (Unsafe Pointer) 使用
- 关键路径中被忽略的错误

### 高危 (HIGH) - 建议修复
- 缺失包含上下文 (Context) 的错误包装
- 使用 Panic 代替错误返回
- 上下文 (Context) 未透传
- 导致死锁的无缓冲通道
- 接口未实现错误
- 缺失互斥锁保护

### 中等 (MEDIUM) - 酌情考虑
- 非地道的代码模式
- 导出的标识符缺失 Godoc 注释
- 低效的字符串拼接
- 切片 (Slice) 未预分配容量
- 未使用表驱动测试 (Table-driven tests)

## 运行的自动化检查

```bash
# 静态分析
go vet ./...

# 高级检查（如果已安装）
staticcheck ./...
golangci-lint run

# 竞态检测
go build -race ./...

# 安全漏洞
govulncheck ./...
```

## 使用示例

```text
用户: /go-review

智能体 (Agent):
# Go 代码审查报告 (Go Code Review Report)

## 已审查的文件
- internal/handler/user.go (已修改)
- internal/service/auth.go (已修改)

## 静态分析结果
✓ go vet: 无问题
✓ staticcheck: 无问题

## 发现的问题

[致命] 竞态条件 (Race Condition)
文件: internal/service/auth.go:45
问题: 未经同步访问共享 Map
```go
var cache = map[string]*Session{}  // 并发访问！

func GetSession(id string) *Session {
    return cache[id]  // 竞态条件
}
```
修复: 使用 sync.RWMutex 或 sync.Map
```go
var (
    cache   = map[string]*Session{}
    cacheMu sync.RWMutex
)

func GetSession(id string) *Session {
    cacheMu.RLock()
    defer cacheMu.RUnlock()
    return cache[id]
}
```

[高危] 缺失错误上下文
文件: internal/handler/user.go:28
问题: 返回错误时未包含上下文信息
```go
return err  // 缺失上下文
```
修复: 包装上下文信息
```go
return fmt.Errorf("get user %s: %w", userID, err)
```

## 总结
- 致命 (CRITICAL): 1
- 高危 (HIGH): 1
- 中等 (MEDIUM): 0

建议: ❌ 在修复“致命”问题前禁止合并
```

## 批准标准

| 状态 | 条件 |
|--------|-----------|
| ✅ 批准 (Approve) | 无致命 (CRITICAL) 或高危 (HIGH) 问题 |
| ⚠️ 警告 (Warning) | 仅存在中等 (MEDIUM) 问题（谨慎合并） |
| ❌ 阻断 (Block) | 发现致命 (CRITICAL) 或高危 (HIGH) 问题 |

## 与其他命令的集成

- 先使用 `/go-test` 确保测试通过
- 如果出现构建错误，使用 `/go-build`
- 在提交代码前使用 `/go-review`
- 针对非 Go 特定的问题，使用 `/code-review`

## 相关内容

- 智能体 (Agent): `agents/go-reviewer.md`
- 技能 (Skills): `skills/golang-patterns/`, `skills/golang-testing/`
