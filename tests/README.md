# Tests

本目录用于验证 ReferenceCity 自身的一致性，而不是替代被测可信链的测试套件。

Phase 1 计划检查：

- ID 唯一性；
- Schema 合法性；
- geometry validity；
- 引用完整性；
- event 前后版本连续性；
- Scenario 与 Expected Result 一一对应；
- Ground Truth 必需字段完整；
- 数据 manifest 不含未知来源/敏感性状态；
- 固定随机种子重复生成结果一致。

可信链仓库应消费 ReferenceCity 的发布版本并执行自己的集成测试。
