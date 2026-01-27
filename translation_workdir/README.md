# Translation Workdir (翻译工作归档)

本目录包含 `everything-claude-code` 项目的自动化中文翻译工具链。它是非原项目内容，仅用于维护本仓库的中文化版本。

## 目录结构
- `scripts/`: 核心自动化脚本
    - `batch_processor.py`: 扫描全量 MD，比对指纹，执行 AI 翻译或从缓存恢复。
    - `apply_translations.py`: 将翻译好的预览文件覆盖回原位。
- `prompts/`: 翻译提示词模版，包含项目背景和术语保护规则。
- `cache/`: 翻译数据库
    - `translation_db.json`: 存储英文指纹及其对应的中文内容，实现一秒还原和零成本同步。

## 日常维护流程 (SOP)

### 1. 同步上游更新
当你发现原作者的英文仓库有更新时，先拉取并覆盖本地（建议在 `main` 分支）：
```bash
# 添加并获取上游仓库（仅需执行一次）
git remote add upstream https://github.com/affaan-m/everything-claude-code.git
git fetch upstream

# 拉取最新英文版并覆盖本地（此时本地会变回英文）
git checkout upstream/main -- .
```

### 2. 执行自动化翻译
运行脚本。它会自动对比 `translation_db.json`，秒速恢复未改动的文件，并仅对新增/修改的文件调用 AI 翻译：
```bash
python3 translation_workdir/scripts/batch_processor.py
```

### 3. 应用翻译并覆盖
检查 `_zh` 目录无误后，执行物理替换。这会将翻译后的文件移回原位，并清理临时目录：
```bash
python3 translation_workdir/scripts/apply_translations.py
```

### 4. 提交你的汉化版本
```bash
git add .
git commit -m "sync: update chinese translation to match upstream latest"
git push origin main
```

---
*注：本目录应提交至 Git 仓库以持久化翻译资产。*