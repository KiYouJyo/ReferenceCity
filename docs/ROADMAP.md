# ReferenceCity 开发路线图

> 中文源文本。English: `ROADMAP.en.md` · 日本語: `ROADMAP.ja.md`

## Phase 1 — 国土空间可信链基准城市

### Phase 1A：文本、Schema 与最小骨架 — 完成
- [x] 三语项目主页、核心数据域、Schema v0.1、稳定 ID、时间/单位、provenance/sensitivity 与自动校验。

### Phase 1B：核心小城市 v0.1 — 工程冻结
- [x] 20 km × 20 km 合成城市、seed 与确定性生成器；
- [x] 221 spatial + 65 planning objects；
- [x] file SHA-256 + RFC 8785 canonical SHA-256；
- [x] snapshot descriptor、GeoJSON preview、拓扑检查与 CI artifact；
- [x] `release-lock.json` 强制逐字段校验；
- [ ] 人工 GIS 视觉审阅（不阻塞后续开发）。

### Phase 1C：规划治理模型 v0.1 — 接近完成
- [x] 5 个虚构组织、6 类角色、6 个 actor、14 条权限；
- [x] 生命周期 Schema 与 10 个状态迁移；
- [x] 权限—状态迁移一致性自动测试；
- [x] PlanningDocument / Approval / synthetic signature presence fixtures；
- [x] `expected_version` 乐观并发控制与事务失败错误码；
- [x] request idempotency 规则；
- [ ] 冻结 PlanningDocument canonical content hash；
- [ ] 将操作请求 fixture 接入 S001–S010。

### Phase 1D：Benchmark Scenarios v0.1
建立 S001–S010：正常登记、合法版本更新、正常审批生效、无权限修改、批准文档篡改、规划约束冲突、跨受控边界、缺少审批/签名、历史版本验证、冲突更新。每个场景必须同时具有 `input` 与 `expected`。

### Phase 1E：Trust Chain 对接与回归
链只消费公开 Schema/fixture；执行输出与 Ground Truth 比较；固定 ReferenceCity v1.0；性能测试与核心正确性测试分离。

---

## Phase 2 — 现实公开数据兼容性
公开数据作为外部 fixtures/cases 管理，不取代核心合成城市。

## Phase 3 — 规划研究形态扩展
预留传统街巷、单位大院、封闭式高层小区、小街区开放社区、城中村、工业区、TOD、新城、城乡结合部与村庄。

## Phase 4 — 研究型实验环境
支持控制实验、城市更新、人居形态指标与中日比较；不得把预设研究结论编码进生成规则。

## Phase 5 — Scale / Stress Benchmarks
独立生成 10K、100K、1M+ 对象；压力数据不属于核心城市。
