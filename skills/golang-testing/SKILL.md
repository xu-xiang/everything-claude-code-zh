---
name: golang-testing
description: Go 测试模式，包括表格驱动测试、子测试、基准测试、模糊测试和测试覆盖率。遵循测试驱动开发（TDD）方法论及地道的 Go 语言实践。
---

# Go 测试模式 (Go Testing Patterns)

遵循测试驱动开发（TDD）方法论，编写可靠且易于维护的 Go 测试模式指南。

## 激活场景 (When to Activate)

- 编写新的 Go 函数或方法时
- 为现有代码增加测试覆盖率时
- 为性能关键型代码创建基准测试时
- 为输入验证实现模糊测试时
- 在 Go 项目中遵循 TDD 工作流时

## Go 的测试驱动开发 (TDD) 工作流

### 红-绿-重构 (RED-GREEN-REFACTOR) 循环

```
红色 (RED)      → 先写一个失败的测试
绿色 (GREEN)    → 编写最少的代码使测试通过
重构 (REFACTOR) → 在保持测试通过的前提下优化代码
重复 (REPEAT)   → 继续处理下一个需求
```

### Go 中 TDD 的具体步骤

```go
// 第 1 步：定义接口/签名
// calculator.go
package calculator

func Add(a, b int) int {
    panic("not implemented") // 占位符
}

// 第 2 步：编写失败的测试 (RED)
// calculator_test.go
package calculator

import "testing"

func TestAdd(t *testing.T) {
    got := Add(2, 3)
    want := 5
    if got != want {
        t.Errorf("Add(2, 3) = %d; want %d", got, want)
    }
}

// 第 3 步：运行测试 - 验证失败 (FAIL)
// $ go test
// --- FAIL: TestAdd (0.00s)
// panic: not implemented

// 第 4 步：实现最简代码 (GREEN)
func Add(a, b int) int {
    return a + b
}

// 第 5 步：运行测试 - 验证通过 (PASS)
// $ go test
// PASS

// 第 6 步：根据需要进行重构，并验证测试依然通过
```

## 表格驱动测试 (Table-Driven Tests)

Go 测试的标准模式。允许用最少的代码实现全面的覆盖。

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -2, -3},
        {"zero values", 0, 0, 0},
        {"mixed signs", -1, 1, 0},
        {"large numbers", 1000000, 2000000, 3000000},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

### 包含错误情况的表格驱动测试

```go
func TestParseConfig(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    *Config
        wantErr bool
    }{
        {
            name:  "valid config",
            input: `{"host": "localhost", "port": 8080}`,
            want:  &Config{Host: "localhost", Port: 8080},
        },
        {
            name:    "invalid JSON",
            input:   `{invalid}`,
            wantErr: true,
        },
        {
            name:    "empty input",
            input:   "",
            wantErr: true,
        },
        {
            name:  "minimal config",
            input: `{}`,
            want:  &Config{}, // 零值配置
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseConfig(tt.input)

            if tt.wantErr {
                if err == nil {
                    t.Error("expected error, got nil")
                }
                return
            }

            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }

            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("got %+v; want %+v", got, tt.want)
            }
        })
    }
}
```

## 子测试与子基准测试 (Subtests and Sub-benchmarks)

### 组织相关的测试

```go
func TestUser(t *testing.T) {
    // 所有子测试共享的设置
    db := setupTestDB(t)

    t.Run("Create", func(t *testing.T) {
        user := &User{Name: "Alice"}
        err := db.CreateUser(user)
        if err != nil {
            t.Fatalf("CreateUser failed: %v", err)
        }
        if user.ID == "" {
            t.Error("expected user ID to be set")
        }
    })

    t.Run("Get", func(t *testing.T) {
        user, err := db.GetUser("alice-id")
        if err != nil {
            t.Fatalf("GetUser failed: %v", err)
        }
        if user.Name != "Alice" {
            t.Errorf("got name %q; want %q", user.Name, "Alice")
        }
    })

    t.Run("Update", func(t *testing.T) {
        // ...
    })

    t.Run("Delete", func(t *testing.T) {
        // ...
    })
}
```

### 并行子测试

```go
func TestParallel(t *testing.T) {
    tests := []struct {
        name  string
        input string
    }{
        {"case1", "input1"},
        {"case2", "input2"},
        {"case3", "input3"},
    }

    for _, tt := range tests {
        tt := tt // 捕获循环变量
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // 并行运行子测试
            result := Process(tt.input)
            // 断言...
            _ = result
        })
    }
}
```

## 测试助手 (Test Helpers)

### 助手函数

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper() // 标记为助手函数

    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("failed to open database: %v", err)
    }

    // 测试结束时进行清理
    t.Cleanup(func() {
        db.Close()
    })

    // 运行迁移
    if _, err := db.Exec(schema); err != nil {
        t.Fatalf("failed to create schema: %v", err)
    }

    return db
}

func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func assertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v; want %v", got, want)
    }
}
```

### 临时文件与目录

```go
func TestFileProcessing(t *testing.T) {
    // 创建临时目录 - 会自动清理
    tmpDir := t.TempDir()

    // 创建测试文件
    testFile := filepath.Join(tmpDir, "test.txt")
    err := os.WriteFile(testFile, []byte("test content"), 0644)
    if err != nil {
        t.Fatalf("failed to create test file: %v", err)
    }

    // 运行测试
    result, err := ProcessFile(testFile)
    if err != nil {
        t.Fatalf("ProcessFile failed: %v", err)
    }

    // 断言...
    _ = result
}
```

## 黄金文件 (Golden Files)

针对存储在 `testdata/` 中的预期输出文件进行测试。

```go
var update = flag.Bool("update", false, "update golden files")

func TestRender(t *testing.T) {
    tests := []struct {
        name  string
        input Template
    }{
        {"simple", Template{Name: "test"}},
        {"complex", Template{Name: "test", Items: []string{"a", "b"}}},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Render(tt.input)

            golden := filepath.Join("testdata", tt.name+".golden")

            if *update {
                // 更新黄金文件：go test -update
                err := os.WriteFile(golden, got, 0644)
                if err != nil {
                    t.Fatalf("failed to update golden file: %v", err)
                }
            }

            want, err := os.ReadFile(golden)
            if err != nil {
                t.Fatalf("failed to read golden file: %v", err)
            }

            if !bytes.Equal(got, want) {
                t.Errorf("output mismatch:\ngot:\n%s\nwant:\n%s", got, want)
            }
        })
    }
}
```

## 使用接口进行 Mock (Mocking with Interfaces)

### 基于接口的 Mocking

```go
// 为依赖定义接口
type UserRepository interface {
    GetUser(id string) (*User, error)
    SaveUser(user *User) error
}

// 生产环境实现
type PostgresUserRepository struct {
    db *sql.DB
}

func (r *PostgresUserRepository) GetUser(id string) (*User, error) {
    // 真实的数据库查询
}

// 用于测试的 Mock 实现
type MockUserRepository struct {
    GetUserFunc  func(id string) (*User, error)
    SaveUserFunc func(user *User) error
}

func (m *MockUserRepository) GetUser(id string) (*User, error) {
    return m.GetUserFunc(id)
}

func (m *MockUserRepository) SaveUser(user *User) error {
    return m.SaveUserFunc(user)
}

// 使用 mock 进行测试
func TestUserService(t *testing.T) {
    mock := &MockUserRepository{
        GetUserFunc: func(id string) (*User, error) {
            if id == "123" {
                return &User{ID: "123", Name: "Alice"}, nil
            }
            return nil, ErrNotFound
        },
    }

    service := NewUserService(mock)

    user, err := service.GetUserProfile("123")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Name != "Alice" {
        t.Errorf("got name %q; want %q", user.Name, "Alice")
    }
}
```

## 基准测试 (Benchmarks)

### 基础基准测试

```go
func BenchmarkProcess(b *testing.B) {
    data := generateTestData(1000)
    b.ResetTimer() // 不计入准备时间

    for i := 0; i < b.N; i++ {
        Process(data)
    }
}

// 运行：go test -bench=BenchmarkProcess -benchmem
// 输出：BenchmarkProcess-8   10000   105234 ns/op   4096 B/op   10 allocs/op
```

### 不同规模的基准测试

```go
func BenchmarkSort(b *testing.B) {
    sizes := []int{100, 1000, 10000, 100000}

    for _, size := range sizes {
        b.Run(fmt.Sprintf("size=%d", size), func(b *testing.B) {
            data := generateRandomSlice(size)
            b.ResetTimer()

            for i := 0; i < b.N; i++ {
                // 制作副本以避免对已排序数据进行排序
                tmp := make([]int, len(data))
                copy(tmp, data)
                sort.Ints(tmp)
            }
        })
    }
}
```

### 内存分配基准测试

```go
func BenchmarkStringConcat(b *testing.B) {
    parts := []string{"hello", "world", "foo", "bar", "baz"}

    b.Run("plus", func(b *testing.B) {
        for i := 0; i < b.N; i++ {
            var s string
            for _, p := range parts {
                s += p
            }
            _ = s
        }
    })

    b.Run("builder", func(b *testing.B) {
        for i := 0; i < b.N; i++ {
            var sb strings.Builder
            for _, p := range parts {
                sb.WriteString(p)
            }
            _ = sb.String()
        }
    })

    b.Run("join", func(b *testing.B) {
        for i := 0; i < b.N; i++ {
            _ = strings.Join(parts, "")
        }
    })
}
```

## 模糊测试 (Fuzzing) (Go 1.18+)

### 基础模糊测试

```go
func FuzzParseJSON(f *testing.F) {
    // 添加种子语料库
    f.Add(`{"name": "test"}`)
    f.Add(`{"count": 123}`)
    f.Add(`[]`)
    f.Add(`""`)

    f.Fuzz(func(t *testing.T, input string) {
        var result map[string]interface{}
        err := json.Unmarshal([]byte(input), &result)

        if err != nil {
            // 随机输入产生无效 JSON 是符合预期的
            return
        }

        // 如果解析成功，重新编码应该也能成功
        _, err = json.Marshal(result)
        if err != nil {
            t.Errorf("Marshal failed after successful Unmarshal: %v", err)
        }
    })
}

// 运行：go test -fuzz=FuzzParseJSON -fuzztime=30s
```

### 多参数模糊测试

```go
func FuzzCompare(f *testing.F) {
    f.Add("hello", "world")
    f.Add("", "")
    f.Add("abc", "abc")

    f.Fuzz(func(t *testing.T, a, b string) {
        result := Compare(a, b)

        // 属性：Compare(a, a) 应该始终等于 0
        if a == b && result != 0 {
            t.Errorf("Compare(%q, %q) = %d; want 0", a, b, result)
        }

        // 属性：Compare(a, b) 和 Compare(b, a) 应该符号相反
        reverse := Compare(b, a)
        if (result > 0 && reverse >= 0) || (result < 0 && reverse <= 0) {
            if result != 0 || reverse != 0 {
                t.Errorf("Compare(%q, %q) = %d, Compare(%q, %q) = %d; inconsistent",
                    a, b, result, b, a, reverse)
            }
        }
    })
}
```

## 测试覆盖率 (Test Coverage)

### 运行覆盖率测试

```bash
# 基础覆盖率
go test -cover ./...

# 生成覆盖率配置文件
go test -coverprofile=coverage.out ./...

# 在浏览器中查看覆盖率
go tool cover -html=coverage.out

# 按函数查看覆盖率
go tool cover -func=coverage.out

# 配合竞态检测运行覆盖率
go test -race -coverprofile=coverage.out ./...
```

### 覆盖率目标

| 代码类型 | 目标 |
|-----------|--------|
| 关键业务逻辑 | 100% |
| 公共 API | 90%+ |
| 通用代码 | 80%+ |
| 生成的代码 | 排除 |

### 从覆盖率中排除生成的代码

```go
//go:generate mockgen -source=interface.go -destination=mock_interface.go

// 在覆盖率配置文件中，通过 build tags 排除：
// go test -cover -tags=!generate ./...
```

## HTTP 处理函数测试 (HTTP Handler Testing)

```go
func TestHealthHandler(t *testing.T) {
    // 创建请求
    req := httptest.NewRequest(http.MethodGet, "/health", nil)
    w := httptest.NewRecorder()

    // 调用处理函数
    HealthHandler(w, req)

    // 检查响应
    resp := w.Result()
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        t.Errorf("got status %d; want %d", resp.StatusCode, http.StatusOK)
    }

    body, _ := io.ReadAll(resp.Body)
    if string(body) != "OK" {
        t.Errorf("got body %q; want %q", body, "OK")
    }
}

func TestAPIHandler(t *testing.T) {
    tests := []struct {
        name       string
        method     string
        path       string
        body       string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "get user",
            method:     http.MethodGet,
            path:       "/users/123",
            wantStatus: http.StatusOK,
            wantBody:   `{"id":"123","name":"Alice"}`,
        },
        {
            name:       "not found",
            method:     http.MethodGet,
            path:       "/users/999",
            wantStatus: http.StatusNotFound,
        },
        {
            name:       "create user",
            method:     http.MethodPost,
            path:       "/users",
            body:       `{"name":"Bob"}`,
            wantStatus: http.StatusCreated,
        },
    }

    handler := NewAPIHandler()

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            var body io.Reader
            if tt.body != "" {
                body = strings.NewReader(tt.body)
            }

            req := httptest.NewRequest(tt.method, tt.path, body)
            req.Header.Set("Content-Type", "application/json")
            w := httptest.NewRecorder()

            handler.ServeHTTP(w, req)

            if w.Code != tt.wantStatus {
                t.Errorf("got status %d; want %d", w.Code, tt.wantStatus)
            }

            if tt.wantBody != "" && w.Body.String() != tt.wantBody {
                t.Errorf("got body %q; want %q", w.Body.String(), tt.wantBody)
            }
        })
    }
}
```

## 测试常用命令

```bash
# 运行所有测试
go test ./...

# 以详细输出运行测试
go test -v ./...

# 运行特定测试
go test -run TestAdd ./...

# 运行符合模式的测试
go test -run "TestUser/Create" ./...

# 开启竞态检测运行测试
go test -race ./...

# 运行测试并查看覆盖率
go test -cover -coverprofile=coverage.out ./...

# 仅运行短测试
go test -short ./...

# 设置超时时间运行测试
go test -timeout 30s ./...

# 运行基准测试
go test -bench=. -benchmem ./...

# 运行模糊测试
go test -fuzz=FuzzParse -fuzztime=30s ./...

# 多次运行测试（用于检测不稳定测试）
go test -count=10 ./...
```

## 最佳实践 (Best Practices)

**推荐做法 (DO):**
- 测试先行 (TDD)
- 使用表格驱动测试以实现全面覆盖
- 测试行为而非实现
- 在助手函数中使用 `t.Helper()`
- 为独立的测试使用 `t.Parallel()`
- 使用 `t.Cleanup()` 清理资源
- 使用描述场景的、有意义的测试名称

**不推荐做法 (DON'T):**
- 直接测试私有函数（应通过公共 API 测试）
- 在测试中使用 `time.Sleep()`（应使用 channel 或条件变量）
- 忽略不稳定的测试 (Flaky tests)（应修复或移除）
- Mock 一切（尽可能优先使用集成测试）
- 跳过错误路径的测试

## 与 CI/CD 集成

```yaml
# GitHub Actions 示例
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-go@v5
      with:
        go-version: '1.22'

    - name: Run tests
      run: go test -race -coverprofile=coverage.out ./...

    - name: Check coverage
      run: |
        go tool cover -func=coverage.out | grep total | awk '{print $3}' | \
        awk -F'%' '{if ($1 < 80) exit 1}'
```

**请记住**：测试即文档。它们展示了代码的预期用法。请清晰地编写并保持更新。
