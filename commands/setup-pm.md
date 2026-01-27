---
description: 配置你偏好的包管理器 (npm/pnpm/yarn/bun)
disable-model-invocation: true
---

# 包管理器设置 (Package Manager Setup)

为本项目或全局配置你偏好的包管理器。

## 用法 (Usage)

```bash
# 检测当前包管理器
node scripts/setup-package-manager.js --detect

# 设置全局偏好
node scripts/setup-package-manager.js --global pnpm

# 设置项目偏好
node scripts/setup-package-manager.js --project bun

# 列出可用的包管理器
node scripts/setup-package-manager.js --list
```

## 检测优先级 (Detection Priority)

在确定使用哪个包管理器时，将按以下顺序进行检查：

1. **环境变量 (Environment variable)**: `CLAUDE_PACKAGE_MANAGER`
2. **项目配置 (Project config)**: `.claude/package-manager.json`
3. **package.json**: `packageManager` 字段
4. **锁定文件 (Lock file)**: 是否存在 package-lock.json、yarn.lock、pnpm-lock.yaml 或 bun.lockb
5. **全局配置 (Global config)**: `~/.claude/package-manager.json`
6. **后备方案 (Fallback)**: 第一个可用的包管理器 (pnpm > bun > yarn > npm)

## 配置文件 (Configuration Files)

### 全局配置
```json
// ~/.claude/package-manager.json
{
  "packageManager": "pnpm"
}
```

### 项目配置
```json
// .claude/package-manager.json
{
  "packageManager": "bun"
}
```

### package.json
```json
{
  "packageManager": "pnpm@8.6.0"
}
```

## 环境变量 (Environment Variable)

设置 `CLAUDE_PACKAGE_MANAGER` 以覆盖所有其他检测方法：

```bash
# Windows (PowerShell)
$env:CLAUDE_PACKAGE_MANAGER = "pnpm"

# macOS/Linux
export CLAUDE_PACKAGE_MANAGER=pnpm
```

## 运行检测 (Run the Detection)

若要查看当前的包管理器检测结果，请运行：

```bash
node scripts/setup-package-manager.js --detect
```
