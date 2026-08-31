# ReferenceCity

> 合成国土空间规划基准城市 · Synthetic Territorial Spatial Planning Benchmark City · 合成国土空間計画ベンチマーク都市

[中文](README.md) | [English](README.en.md) | [日本語](README.ja.md)

ReferenceCity 是 UrbanPlanningLab 的标准合成实验城市。它不是现实城市的复制品，也不用于替代现实案例研究；它通过可控、可重复、Ground Truth 已知的空间与治理场景，为国土空间规划相关算法、可信链、数据模型和研究方法提供稳定测试对象。

## 当前任务：Phase 1

**第一阶段只服务国土空间可信链研究。**

当前目标是建立一座规模较小、能够人工检查、但具备完整规划生命周期的实验城市，用于验证：

- 空间对象登记与稳定 ID；
- 规划成果及版本管理；
- 编制、提交、审批、生效、调整等事件；
- 机构、角色、权限与多主体操作；
- 数据指纹 / Hash 与文档完整性；
- 越权修改、文档篡改、空间冲突等异常场景；
- 历史状态与可重复回归测试。

Phase 1 不追求真实城市的视觉逼真，也不追求百万级要素规模。

## ReferenceCity 不是“一张假地图”

它由五类互相关联的数据组成：

1. **Spatial State** — 行政区、道路、水系、地块、建筑等空间对象；
2. **Planning State** — 规划单元、用途、控制指标、边界与约束；
3. **Governance State** — 机构、角色、权限、文件与审批关系；
4. **Event History** — 编制、提交、审批、修改、撤回、异常操作等时间序列；
5. **Ground Truth** — 每个基准场景预先定义的正确结果。

因此，一个测试场景不仅要描述“哪里有什么”，还要描述“谁在什么时候依据什么规则做了什么，以及正确结果应该是什么”。

## Phase 1 初始规模目标

第一版优先保持小而可检查：

- 1 个城市；
- 3 个区级单元；
- 6–10 个街镇级单元；
- 约 50–100 个规划地块；
- 约 100–300 个建筑/设施等空间对象；
- 5–10 个机构与角色；
- 20–40 个规划生命周期事件；
- 10–20 个正常/异常基准场景。

后续性能测试数据通过生成器单独扩展，不污染人工可核验的核心城市。

## 仓库结构

```text
ReferenceCity/
├─ docs/          # 方法、数据模型、路线图、数据政策
├─ schemas/       # 稳定机器 Schema
├─ data/          # 核心城市状态数据
├─ scenarios/     # 输入事件与测试场景
├─ expected/      # Ground Truth / Expected Result
├─ generators/    # 合成与压力数据生成器
├─ exports/       # 可交换格式导出（后续）
└─ tests/         # 一致性与回归测试（后续）
```

## 与 UrbanPlanningLab 的关系

- [UrbanPlanningLab](https://github.com/KiYouJyo/UrbanPlanningLab) 定义通用研究语义、术语与长期研究基础设施。
- ReferenceCity 实现这些通用规范的一个标准化合成城市实例。
- ReferenceCity 不应反向定义通用研究模型。
- 国土空间可信链核心不得硬编码 ReferenceCity 特例。

## 长期远景

在 Phase 1 稳定后，ReferenceCity 可逐步增加单位大院、封闭式高层小区、小街区、传统街巷、城中村、TOD、新城、工业区、城乡结合部和村庄等城市形态原型，用于人居形态、城市更新、TOD、城乡治理等研究。

这些远景只作为兼容性目标记录，当前开发仍以国土空间可信链研究为最高优先级。

## 文档

- [开发路线图](docs/ROADMAP.md)
- [数据模型](docs/DATA_MODEL.md)
- [场景规范](docs/SCENARIOS.md)
- [数据来源与安全政策](docs/DATA_POLICY.md)
- [多语言规则](docs/I18N.md)
- [变更记录](CHANGELOG.md)

## 状态

项目处于基础设施初始化阶段。当前尚未声明任何现实城市数据为 ReferenceCity 的组成部分。
