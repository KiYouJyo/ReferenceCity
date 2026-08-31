# ReferenceCity 开发路线图

> 中文源文本。English: `ROADMAP.en.md` · 日本語: `ROADMAP.ja.md`

## Phase 1 — 国土空间可信链基准城市

### Phase 1A：文本、Schema 与最小骨架

目标：不急于画城市，先让“什么是 ReferenceCity”可以被机器和研究者一致理解。

- [x] 三语项目主页；
- [x] 明确与 UrbanPlanningLab 的职责边界；
- [x] 定义核心数据域和场景思想；
- [x] 建立 Spatial / Planning / Governance / Event / Ground Truth Schema v0.1；
- [x] 建立稳定 ID 规则；
- [x] 定义坐标参考、单位、日期时间和版本规则；
- [x] 建立数据 provenance / sensitivity manifest；
- [x] 建立最小机器可读示例与自动 Schema 校验。

### Phase 1B：核心小城市 v0.1

目标：建设一个可人工逐对象检查的核心城市，而不是追求规模。

建议规模：
- 1 city；
- 3 district-level units；
- 6–10 township/subdistrict units；
- 50–100 parcels；
- 100–300 buildings/facilities/other features；
- 基础道路、水系与公共设施；
- 一套简化但内部一致的现状土地利用和规划控制数据。

要求：
- 空间对象具有稳定 ID；
- 几何关系可人工检查；
- 不对应现实城市的精确坐标和敏感数据；
- 生成过程、人工修改和随机种子可追踪。

### Phase 1C：规划治理模型 v0.1

建立：
- 规划编制机构；
- 审批主体；
- 区级/市级管理角色；
- 建设/申请主体；
- 权限矩阵；
- Plan / PlanVersion / PlanningDocument / Approval；
- 生命周期状态机。

首个标准生命周期：

```text
Draft → Submitted → Reviewed → Approved → Effective
                                      ↓
                                  Amendment
                                      ↓
                               New Effective Version
```

### Phase 1D：Benchmark Scenarios v0.1

至少建立以下场景：

1. 正常规划成果登记；
2. 合法版本更新；
3. 正常审批并生效；
4. 无权限主体修改；
5. 已批准文档内容被篡改；
6. 地块用途与上位约束冲突；
7. 项目跨越受控边界；
8. 审批缺少必要主体/签名；
9. 历史版本恢复与验证；
10. 同一对象发生冲突更新。

每个场景必须同时具有 `input` 与 `expected`，不能只保存故事描述。

### Phase 1E：Trust Chain 对接与回归

- 为链提供稳定、与实现无关的测试输入；
- 比较链执行输出和 Ground Truth；
- 固定 ReferenceCity v1.0 基准；
- 后续链版本始终能够重跑同一基准；
- 将性能测试与核心正确性测试分离。

### Phase 1 完成条件

满足以下条件后发布 ReferenceCity v1.0：

- Schema 稳定；
- 核心城市可完整导出/导入；
- 至少 10 个标准场景；
- 每个场景具有机器可读 Ground Truth；
- 生命周期可由可信链端到端执行；
- 全部核心场景能够确定性重复；
- 数据清单不存在来源或敏感性不明内容。

---

## Phase 2 — 现实公开数据兼容性

在不污染 ReferenceCity 核心 Ground Truth 的前提下，建立公开数据导入与映射测试，用于回答“现实 GIS 数据能否进入同一模型”。现实公开数据作为外部 fixtures/cases 管理，不取代核心合成城市。

## Phase 3 — 规划研究形态扩展

为 UrbanPlanningLab 后续研究预留：
- 传统街巷；
- 单位大院；
- 封闭式高层商品房小区；
- 小街区开放社区；
- 城中村；
- 工业区；
- TOD 地区；
- 新城；
- 城乡结合部；
- 村庄。

## Phase 4 — 研究型实验环境

支持控制实验、城市更新状态演化、人居形态指标、中日比较研究等。任何新增形态都必须避免把预设研究结论编码进数据生成规则。

## Phase 5 — Scale / Stress Benchmarks

独立生成 10K、100K、1M 及更大规模对象，用于性能、扩展性和分布式处理实验。压力数据不作为 ReferenceCity 核心城市的组成部分。
