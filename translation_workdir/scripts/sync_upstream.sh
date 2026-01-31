#!/bin/bash
set -e

# 参数解析
AUTO_PUSH=false
for arg in "$@"; do
  case $arg in
    --push)
      AUTO_PUSH=true
      shift
      ;; 
  esac
done

# 配置
WORK_DIR="translation_workdir"
DATE_TAG=$(date +%Y%m%d-%H%M)
SYNC_BRANCH="sync/upstream-${DATE_TAG}"

echo ">>> [1/6] 准备环境..."
# 确保在 main 分支且是最新的
git checkout main
git pull origin main

# 获取上游最新状态
echo ">>> [2/6] 获取 Upstream 状态..."
if ! git remote | grep -q "upstream"; then
    echo "错误: 未找到远程仓库 'upstream'。请先添加 upstream。"
    exit 1
fi
git fetch upstream

# 创建同步分支
echo ">>> [3/6] 创建同步分支: ${SYNC_BRANCH}..."
git checkout -b "${SYNC_BRANCH}"

# 记录 Upstream SHA
UP_SHA=$(git rev-parse --short upstream/main)
echo "   Target Upstream SHA: ${UP_SHA}"

# 覆盖式拉取 (Overlay)
echo ">>> [4/6] 同步上游文件..."
# 1. 引入上游的新增和修改
git checkout upstream/main -- .
# 取消暂存，方便后续统一管理
git reset HEAD .

# 2. 清理上游已删除的文件 (Sync Deletions)
# 逻辑：找出 upstream/main 里没有，但当前 HEAD (基于原 main) 里有的文件
# 排除 translation_workdir, .git, .gitignore 等项目维护文件
echo "   Cleaning up deleted files..."
git diff --name-only --diff-filter=A upstream/main HEAD \
  | grep -v "^${WORK_DIR}/" \
  | grep -v "^.git" \
  | grep -v "README.md" \
  | while read -r file; do
      if [ -f "$file" ]; then
          echo "   Removing deleted file: $file"
          rm "$file"
      fi
  done

echo ">>> [5/6] 执行翻译流程..."
# 增量翻译
python3 "${WORK_DIR}/scripts/batch_processor.py"
# 应用翻译 (模拟交互输入 y)
yes | python3 "${WORK_DIR}/scripts/apply_translations.py"

echo ">>> [6/6] 准备提交..."
git add .
COMMIT_MSG="chore: sync with upstream ${UP_SHA} + update zh translations"
echo "   Commit Message: ${COMMIT_MSG}"

git commit -m "${COMMIT_MSG}"

echo ""
echo "--------------------------------------------------------"
echo "✅ 同步完成！分支: ${SYNC_BRANCH}"

if [ "$AUTO_PUSH" = true ]; then
    echo ">>> 检测到 --push 参数，正在推送到远程..."
    git push origin "${SYNC_BRANCH}"
    echo "✅ 已推送到 origin/${SYNC_BRANCH}"
    echo "请前往 GitHub 发起 Pull Request。"
else
    echo "请检查文件变更，确认无误后推送到 origin 并发起 PR。"
    echo "命令参考: git push origin ${SYNC_BRANCH}"
fi
echo "--------------------------------------------------------"
