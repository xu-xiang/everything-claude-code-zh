# 更新文档 (Update Documentation)

从单一事实来源（Source-of-truth）同步文档：

1. 读取 `package.json` 中的 `scripts` 章节
   - 生成脚本参考表
   - 包含来自注释的说明描述

2. 读取 `.env.example`
   - 提取所有环境变量
   - 记录变量用途与格式

3. 生成 `docs/CONTRIB.md`，内容包含：
   - 开发工作流（Development workflow）
   - 可用脚本
   - 环境搭建
   - 测试流程

4. 生成 `docs/RUNBOOK.md`，内容包含：
   - 部署流程
   - 监控与告警
   - 常见问题与修复
   - 回滚流程

5. 识别过时文档：
   - 查找 90 天以上未修改的文档
   - 列出清单以供人工核查

6. 显示差异（diff）摘要

单一事实来源（Single source of truth）：`package.json` 和 `.env.example`
