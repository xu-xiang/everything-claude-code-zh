### 插件清单注意事项（Plugin Manifest Gotchas）

如果你计划编辑 `.claude-plugin/plugin.json`，请注意 Claude 插件验证器（plugin validator）强制执行了一些**未公开但严格的约束**，这些约束可能导致安装失败并显示模糊的错误（例如，`agents: Invalid input`）。特别是，组件字段必须是数组（arrays），`agents` 必须使用明确的文件路径而非目录，且为了实现可靠的验证和安装，必须包含 `version` 字段。

这些约束在公开示例中并不明显，且在过去曾多次导致安装失败。它们在 `.claude-plugin/PLUGIN_SCHEMA_NOTES.md` 中有详细记录，在对插件清单（plugin manifest）进行任何更改之前，应仔细阅读该文档。
