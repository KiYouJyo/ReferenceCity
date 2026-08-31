# ReferenceCity 开发路线图

> 中文源文本。English: `ROADMAP.en.md` · 日本語: `ROADMAP.ja.md`

## Phase 1 — 国土空间可信链基准城市

### Phase 1A：文本、Schema 与最小骨架 — 完成

- [x] 三语项目主页；
- [x] 明确与 UrbanPlanningLab 的职责边界；
- [x] 定义核心数据域和场景思想；
- [x] 建立 Spatial / Planning / Governance / Event / Ground Truth Schema v0.1；
- [x] 建立稳定 ID 规则；
- [x] 定义坐标参考、单位、日期时间和版本规则；
- [x] 建立数据 provenance / sensitivity manifest；
- [x] 建立最小机器可读示例与自动 Schema 校验。

### Phase 1B：核心小城市 v0.1 — 进行中

- [x] 冻结合成空间范围、规模与生成 seed；
- [x] 建立确定性核心城市生成器；
- [x] 建立对象数量、Schema 与重复生成 Hash 的自动测试；
- [x] 建立三语核心城市 profile；
- [x] 引入 file SHA-256 与 RFC 8785 canonical SHA-256 双重内容指纹；
- [x] 建立 snapshot descriptor 与 CI artifact；
- [x] 建立 GeoJSON preview 与自动拓扑/父子关系检查；
- [ ] 提交并强制校验 `release-lock.json`；
- [ ] 完成首个正式 core dataset snapshot 人工 GIS 审阅。

### Phase 1C：规划治理模型 v0.1 — 进行中

- [x] 建立 5 个虚构组织；
- [x] 建立 PLANNER / REVIEWER / APPROVER / DISTRICT_MANAGER / APPLICANT / AUDITOR 六类角色；
- [x] 建立 6 个合成 actor；
- [x] 建立机器可读权限矩阵；
- [x] 建立规划成果生命周期 Schema；
- [x] 建立 DRAFT → SUBMITTED → REVIEWED → APPROVED → EFFECTIVE 主路径及退回、拒绝、撤回、调整、废止路径；
- [x] 建立权限—状态迁移一致性自动测试；
- [ ] 加入 PlanningDocument / Approval / signature fixtures；
- [ ] 加入版本前置条件与并发更新规则。

### Phase 1D：Benchmark Scenarios v0.1

至少建立：正常规划成果登记、合法版本更新、正常审批并生效、无权限主体修改、已批准文档篡改、地块用途与上位约束冲突、项目跨越受控边界、审批缺少必要主体/签名、历史版本验证、同一对象冲突更新。

每个场景必须同时具有 `input` 与 `expected`。

### Phase 1E：Trust Chain 对接与回归

为链提供稳定、与实现无关的测试输入；比较链执行输出与 Ground Truth；固定 ReferenceCity v1.0 基准；将性能测试与核心正确性测试分离。

### Phase 1 完成条件

Schema 稳定；核心城市可完整导出/导入；至少 10 个标准场景；每个场景具有机器可读 Ground Truth；生命周期可由可信链端到端执行；核心场景可确定性重复；数据清单不存在来源或敏感性不明内容。

---

## Phase 2 — 现实公开数据兼容性

公开数据作为外部 fixtures/cases 管理，不取代核心合成城市。

## Phase 3 — 规划研究形态扩展

为 UrbanPlanningLab 后续研究预留传统街巷、单位大院、封闭式高层商品房小区、小街区开放社区、城中村、工业区、TOD、新城、城乡结合部与村庄。

## Phase 4 — 研究型实验环境

支持控制实验、城市更新状态演化、人居形态指标、中日比较研究；不得把预设研究结论编码进生成规则。

## Phase 5 — Scale / Stress Benchmarks

独立生成 10K、100K、1M 及更大规模对象；压力数据不属于核心城市。
