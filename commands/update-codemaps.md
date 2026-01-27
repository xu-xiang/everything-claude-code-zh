# 更新代码映射表（Update Codemaps）

分析代码库结构并更新架构文档：

1. 扫描所有源文件中的导入（imports）、导出（exports）和依赖关系
2. 生成符合以下格式的 Token 精简版代码映射表（Codemaps）：
   - `codemaps/architecture.md` - 整体架构
   - `codemaps/backend.md` - 后端结构  
   - `codemaps/frontend.md` - 前端结构
   - `codemaps/data.md` - 数据模型与模式（Schemas）

3. 计算与上一版本的差异百分比
4. 如果变更超过 30%，在更新前请求用户批准
5. 为每个代码映射表（Codemap）添加更新时间戳
6. 将报告保存至 `.reports/codemap-diff.txt`

使用 TypeScript/Node.js 进行分析。侧重于高层级结构，而非实现细节。
