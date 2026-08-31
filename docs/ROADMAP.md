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

目标：建设一个可人工逐对象检查的核心城市，而不是追求规模。

- [x] 冻结合成空间范围、规模与生成 seed；
- [x] 建立确定性核心城市生成器；
- [x] 建立对象数量、Schema 与重复生成 Hash 的自动测试；
- [x] 建立三语核心城市 profile；
- [ ] 冻结生成文件的 canonical serialization / release checksum；
- [ ] 生成并审阅首个正式 core dataset snapshot；
- [ ] 在 QGIS/GeoJSON 导出层人工检查空间关系。

基准规模：1 city、3 district-level units、6 town/subdistrict units、60 parcels、120 buildings、18 road segments、1 synthetic river、12 facilities，以及一套简化但内部一致的规划控制数据。

### Phase 1C：规划治理模型 v0.1

建立规划编制机构、审批主体、区级/市级管理角色、建设/申请主体、权限矩阵、Plan / PlanVersion / PlanningDocument / Approval 与生命周期状态机。

首个标准生命周期：

```text
Draft → Submitted → Reviewed → Approved → Effective
                                      ↓
                                  Amendment
                                      ↓
                               New Effective Version
```

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
