# ReferenceCity 开发路线图

> 中文源文本。English: `ROADMAP.en.md` · 日本語: `ROADMAP.ja.md`

## Phase 1 — 国土空间可信链基准城市

### Phase 1A — 完成
三语基础、核心数据域、Schema v0.1、稳定 ID、时间/单位、provenance/sensitivity 与自动校验均已建立。

### Phase 1B — 工程冻结
- [x] 20 km × 20 km 合成城市、确定性生成器与 seed；
- [x] 221 spatial + 65 planning objects；
- [x] file SHA-256 + RFC 8785 canonical SHA-256；
- [x] snapshot descriptor、GeoJSON preview、拓扑检查、CI artifact；
- [x] `release-lock.json` 强制校验；
- [ ] 人工 GIS 视觉审阅（不阻塞后续开发）。

### Phase 1C — 工程完成
- [x] 5 个组织、6 类角色、6 actor、权限矩阵；
- [x] 生命周期 Schema 与状态迁移；
- [x] PlanningDocument / Approval / synthetic signature fixture；
- [x] PlanningDocument RFC 8785 canonical Hash 校验；
- [x] `expected_version` 乐观并发、request idempotency 与稳定错误码。

### Phase 1D — Benchmark Scenarios v0.1 — 已建立首版
- [x] S001 正常规划成果登记；
- [x] S002 合法版本更新；
- [x] S003 正常审批并生效；
- [x] S004 无权限主体修改；
- [x] S005 已批准文档篡改；
- [x] S006 规划约束冲突；
- [x] S007 项目跨越受控边界；
- [x] S008 缺少必要签名；
- [x] S009 历史版本验证；
- [x] S010 冲突更新；
- [x] 每个场景具有 operation request 与机器可读 Ground Truth；
- [x] CI 校验 scenario/request/expected Schema、步骤对应关系与 payload canonical Hash；
- [ ] 建立实现无关的 benchmark runner / adapter contract。

### Phase 1E — Trust Chain 对接与回归
下一步定义链适配器输入/输出协议，使任意实现只要实现 adapter contract 即可执行 S001–S010，并将 observed result 与 Ground Truth 自动比较。

---

## Phase 2 — 现实公开数据兼容性
公开数据作为外部 fixtures/cases 管理，不取代核心合成城市。

## Phase 3 — 规划研究形态扩展
预留传统街巷、单位大院、封闭式高层小区、小街区开放社区、城中村、工业区、TOD、新城、城乡结合部与村庄。

## Phase 4 — 研究型实验环境
支持控制实验、城市更新、人居形态指标与中日比较；不得把预设研究结论编码进生成规则。

## Phase 5 — Scale / Stress Benchmarks
独立生成 10K、100K、1M+ 对象；压力数据不属于核心城市。
