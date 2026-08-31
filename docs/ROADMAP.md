# ReferenceCity 开发路线图

> 中文源文本。English: `ROADMAP.en.md` · 日本語: `ROADMAP.ja.md`

## Phase 1 — 国土空间可信链基准城市

### Phase 1A — 完成
三语基础、核心数据域、Schema v0.1、稳定 ID、时间/单位、provenance/sensitivity 与自动校验均已建立。

### Phase 1B — 工程冻结
- [x] 20 km × 20 km 合成城市、确定性生成器与 seed；
- [x] 221 spatial + 65 planning objects；
- [x] file SHA-256 + RFC 8785 canonical SHA-256；
- [x] snapshot、GeoJSON preview、拓扑检查、CI artifact 与 release lock；
- [ ] 人工 GIS 视觉审阅（非阻塞）。

### Phase 1C — 工程完成
- [x] 5 个组织、6 类角色、6 actor、权限矩阵；
- [x] 生命周期、PlanningDocument / Approval / signature fixture；
- [x] canonical document Hash、乐观并发、幂等与稳定错误码。

### Phase 1D — Benchmark Scenarios v0.1 — 完成首版
- [x] S001–S010 scenario + operation request + Ground Truth；
- [x] scenario/request/expected Schema 和 canonical payload Hash 自动验证；
- [x] 正常、授权、审批、篡改、规划冲突、空间冲突、签名、历史和并发场景覆盖。

### Phase 1E — Trust Chain Adapter / Evaluator — 进行中
- [x] `observed-result.schema.json`；
- [x] 实现无关 adapter contract，中英日三语；
- [x] 隔离 benchmark input builder；
- [x] adapter 输入包物理排除 `expected/` Ground Truth；
- [x] observed vs expected evaluator；
- [x] evaluator self-test：10/10 正确输出 PASS，并能识别故意注入的 mismatch；
- [ ] 对接实际国土空间可信链实现；
- [ ] 由真实链运行 S001–S010 并产出 observed results；
- [ ] 固定 ReferenceCity v1.0。

---

## Phase 2 — 现实公开数据兼容性
公开数据作为外部 fixtures/cases 管理，不取代核心合成城市。

## Phase 3 — 规划研究形态扩展
预留传统街巷、单位大院、封闭式高层小区、小街区开放社区、城中村、工业区、TOD、新城、城乡结合部与村庄。

## Phase 4 — 研究型实验环境
支持控制实验、城市更新、人居形态指标与中日比较；不得把预设研究结论编码进生成规则。

## Phase 5 — Scale / Stress Benchmarks
独立生成 10K、100K、1M+ 对象；压力数据不属于核心城市。
