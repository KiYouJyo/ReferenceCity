# Core City Data

本目录只保存 ReferenceCity 的核心、可人工核验城市状态数据。

Phase 1 建议子域：

```text
base/
spatial/
planning/
governance/
documents/
manifests/
```

核心原则：
- v1.0 核心以 `SYNTHETIC` 数据为主；
- 每个数据包必须有 provenance / sensitivity manifest；
- 压力测试数据不得混入核心城市；
- 现实公开案例数据不得冒充 ReferenceCity Synthetic Core；
- 大型二进制数据加入 Git 前应单独评估版本管理方式。
