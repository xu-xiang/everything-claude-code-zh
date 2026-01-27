# 测试覆盖率 (Test Coverage)

分析测试覆盖率并生成缺失的测试用例：

1. 运行带覆盖率报告的测试：npm test --coverage 或 pnpm test --coverage

2. 分析覆盖率报告 (coverage/coverage-summary.json)

3. 识别覆盖率低于 80% 阈值的文件

4. 针对每个覆盖率不足的文件：
   - 分析未测试的代码路径
   - 为函数生成单元测试 (Unit Tests)
   - 为 API 生成集成测试 (Integration Tests)
   - 为关键流程生成端到端测试 (E2E Tests)

5. 验证新测试已通过

6. 展示覆盖率指标的前后对比

7. 确保项目整体覆盖率达到 80% 以上

重点关注：
- 正常路径 (Happy path) 场景
- 错误处理 (Error handling)
- 边缘情况 (Edge cases) (null, undefined, empty)
- 边界条件 (Boundary conditions)
