---
description: 强制执行 Go 的测试驱动开发（TDD）工作流。先编写表驱动测试（Table-Driven Tests），然后进行实现。使用 go test -cover 验证 80% 以上的覆盖率。
---

# Go TDD 命令

此命令使用地道的 Go 测试模式为 Go 代码强制执行测试驱动开发（Test-Driven Development，TDD）方法论。

## 此命令的作用

1. **定义类型/接口**：首先搭建函数签名的支架
2. **编写表驱动测试（Table-Driven Tests）**：创建全面的测试用例（RED/红灯）
3. **运行测试**：验证测试因预期的原因失败
4. **实现代码**：编写通过测试所需的最少代码（GREEN/绿灯）
5. **重构（Refactor）**：在保持测试通过的同时优化代码
6. **检查覆盖率**：确保 80% 以上的覆盖率

## 何时使用

在以下场景使用 `/go-test`：
- 实现新的 Go 函数
- 为现有代码增加测试覆盖率
- 修复 Bug（先编写失败的测试）
- 构建核心业务逻辑
- 在 Go 中学习 TDD 工作流（Workflow）

## TDD 周期

```
RED（红灯）      → 编写失败的表驱动测试
GREEN（绿灯）    → 实现通过测试所需的最少代码
REFACTOR（重构） → 优化代码，保持测试通过
REPEAT（循环）   → 下一个测试用例
```

## 会话示例

```text
User: /go-test 我需要一个验证电子邮件地址的函数

Agent:
# TDD 会话：电子邮件验证器

## 第 1 步：定义接口

```go
// validator/email.go
package validator

// ValidateEmail 检查给定的字符串是否为有效的电子邮件地址。
// 如果有效返回 nil，否则返回描述问题的错误。
func ValidateEmail(email string) error {
    panic("not implemented")
}
```

## 第 2 步：编写表驱动测试 (RED)

```go
// validator/email_test.go
package validator

import (
    "testing"
)

func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        // 有效邮箱
        {"simple email", "user@example.com", false},
        {"with subdomain", "user@mail.example.com", false},
        {"with plus", "user+tag@example.com", false},
        {"with dots", "first.last@example.com", false},

        // 无效邮箱
        {"empty string", "", true},
        {"no at sign", "userexample.com", true},
        {"no domain", "user@", true},
        {"no local part", "@example.com", true},
        {"double at", "user@@example.com", true},
        {"spaces", "user @example.com", true},
        {"no tld", "user@example", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if tt.wantErr && err == nil {
                t.Errorf("ValidateEmail(%q) = nil; want error", tt.email)
            }
            if !tt.wantErr && err != nil {
                t.Errorf("ValidateEmail(%q) = %v; want nil", tt.email, err)
            }
        })
    }
}
```

## 第 3 步：运行测试 - 验证失败

```bash
$ go test ./validator/...

--- FAIL: TestValidateEmail (0.00s)
    --- FAIL: TestValidateEmail/simple_email (0.00s)
        panic: not implemented

FAIL
```

✓ 测试如预期般失败 (panic)。

## 第 4 步：实现最少代码 (GREEN)

```go
// validator/email.go
package validator

import (
    "errors"
    "regexp"
)

var emailRegex = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

var (
    ErrEmailEmpty   = errors.New("email cannot be empty")
    ErrEmailInvalid = errors.New("email format is invalid")
)

func ValidateEmail(email string) error {
    if email == "" {
        return ErrEmailEmpty
    }
    if !emailRegex.MatchString(email) {
        return ErrEmailInvalid
    }
    return nil
}
```

## 第 5 步：运行测试 - 验证通过

```bash
$ go test ./validator/...

PASS
ok      project/validator    0.003s
```

✓ 所有测试通过！

## 第 6 步：检查覆盖率

```bash
$ go test -cover ./validator/...

PASS
coverage: 100.0% of statements
ok      project/validator    0.003s
```

✓ 覆盖率：100%

## TDD 完成！
```

## 测试模式

### 表驱动测试（Table-Driven Tests）
```go
tests := []struct {
    name     string
    input    InputType
    want     OutputType
    wantErr  bool
}{
    {"case 1", input1, want1, false},
    {"case 2", input2, want2, true},
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got, err := Function(tt.input)
        // 断言逻辑
    })
}
```

### 并行测试（Parallel Tests）
```go
for _, tt := range tests {
    tt := tt // 闭包捕获变量
    t.Run(tt.name, func(t *testing.T) {
        t.Parallel()
        // 测试主体
    })
}
```

### 测试助手（Test Helpers）
```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db := createDB()
    t.Cleanup(func() { db.Close() })
    return db
}
```

## 覆盖率命令

```bash
# 基础覆盖率
go test -cover ./...

# 生成覆盖率分析文件
go test -coverprofile=coverage.out ./...

# 在浏览器中查看结果
go tool cover -html=coverage.out

# 按函数查看覆盖率
go tool cover -func=coverage.out

# 配合竞态检测运行
go test -race -cover ./...
```

## 覆盖率目标

| 代码类型 | 目标 |
|-----------|--------|
| 核心业务逻辑 | 100% |
| 公共 API | 90%+ |
| 通用代码 | 80%+ |
| 生成的代码 | 排除 |

## TDD 最佳实践

**建议这样做：**
- **先**写测试，在进行任何实现之前
- 每次修改后都运行测试
- 使用表驱动测试以实现全面的覆盖
- 测试行为，而不是实现细节
- 包含边界情况（空值、nil、最大值）

**不要这样做：**
- 在测试之前编写实现代码
- 跳过 RED（红灯）阶段
- 直接测试私有函数
- 在测试中使用 `time.Sleep`
- 忽略不稳定的测试（Flaky tests）

## 相关命令

- `/go-build` - 修复构建错误
- `/go-review` - 实现后评审代码
- `/verify` - 运行完整验证循环

## 相关内容

- 技能（Skill）：`skills/golang-testing/`
- 技能（Skill）：`skills/tdd-workflow/`
