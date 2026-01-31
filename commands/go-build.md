---
description: 增量修复 Go 构建错误、go vet 警告和 linter 问题。调用 go-build-resolver 智能体（Agent）进行最小化、外科手术式的修复。
---

# Go 构建与修复 (Go Build and Fix)

此命令会调用 **go-build-resolver** 智能体（Agent），以最小的改动增量修复 Go 构建错误。

## 此命令的作用

1. **运行诊断**：执行 `go build`、`go vet`、`staticcheck`
2. **解析错误**：按文件分组并按严重程度排序
3. **增量修复**：一次修复一个错误
4. **验证每次修复**：每次更改后重新运行构建
5. **报告摘要**：显示已修复的内容和剩余的问题

## 何时使用

在以下情况下使用 `/go-build`：
- `go build ./...` 失败并报错
- `go vet ./...` 报告问题
- `golangci-lint run` 显示警告
- 模块依赖关系损坏
- 拉取了破坏构建的更改后

## 运行的诊断命令

```bash
# 主要构建检查
go build ./...

# 静态分析
go vet ./...

# 扩展 lint 检查（如果可用）
staticcheck ./...
golangci-lint run

# 模块问题
go mod verify
go mod tidy -v
```

## 会话示例

```text
User: /go-build

Agent:
# Go 构建修复 (Go Build Resolution)

## 初始诊断

```bash
$ go build ./...
internal/service/user.go:25:15: undefined: UserRepository
internal/handler/api.go:42:9: cannot use x (type string) as type int
internal/handler/api.go:58:2: missing return at end of function
```

发现错误：3

## 修复 1：未定义标识符 (Undefined Identifier)

文件：internal/service/user.go:25
错误：undefined: UserRepository
原因：缺少导入 (Missing import)

```go
// 添加了导入
import "project/internal/repository"

// 更改了
var repo UserRepository
// 为
var repo repository.UserRepository
```

```bash
$ go build ./...
# 剩余 2 个错误
```

## 修复 2：类型不匹配 (Type Mismatch)

文件：internal/handler/api.go:42
错误：cannot use x (type string) as type int

```go
// 更改了
count := params.Get("count")
// 为
countStr := params.Get("count")
count, _ := strconv.Atoi(countStr)
```

```bash
$ go build ./...
# 剩余 1 个错误
```

## 修复 3：缺少返回 (Missing Return)

文件：internal/handler/api.go:58
错误：missing return at end of function

```go
func GetUser(id string) (*User, error) {
    if id == "" {
        return nil, ErrInvalidID
    }
    user := findUser(id)
    // 添加了缺少的 return
    return user, nil
}
```

```bash
$ go build ./...
# 构建成功！
```

## 最终验证

```bash
$ go vet ./...
# 无问题

$ go test ./...
ok      project/internal/service   0.015s
ok      project/internal/handler   0.023s
```

## 摘要

| 指标 | 计数 |
|------|------|
| 已修复构建错误 | 3 |
| 已修复 Vet 警告 | 0 |
| 修改的文件 | 2 |
| 剩余问题 | 0 |

构建状态：✅ 成功 (SUCCESS)
```

## 常见修复错误

| 错误 | 典型修复方案 |
|------|--------------|
| `undefined: X` | 添加导入或修复拼写错误 |
| `cannot use X as Y` | 类型转换或修复赋值 |
| `missing return` | 添加 return 语句 |
| `X does not implement Y` | 添加缺失的方法 |
| `import cycle` | 重构包结构 |
| `declared but not used` | 删除或使用该变量 |
| `cannot find package` | 执行 `go get` 或 `go mod tidy` |

## 修复策略

1.  **构建错误优先** - 代码必须能编译
2.  **Vet 警告次之** - 修复可疑结构
3.  **Lint 警告第三** - 样式和最佳实践
4.  **一次一个修复** - 验证每次更改
5.  **最小化更改** - 不要重构，只管修复

## 停止条件

如果出现以下情况，智能体（Agent）将停止并报告：
- 尝试 3 次后同一错误仍然存在
- 修复引入了更多错误
- 需要架构调整
- 缺少外部依赖项

## 相关命令

- `/go-test` - 构建成功后运行测试
- `/go-review` - 审查代码质量
- `/verify` - 完整的验证循环

## 相关

- 智能体 (Agent)：`agents/go-build-resolver.md`
- 技能 (Skill)：`skills/golang-patterns/`
