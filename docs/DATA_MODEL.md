# ReferenceCity 数据模型 v0.x 设计约定

> 当前文件定义 Phase 1 的概念骨架，尚不是冻结 Schema。稳定机器 Schema 将在 `schemas/` 中单独版本化。

## 1. 五个核心数据域

### 1.1 Spatial State
描述城市“在哪里、有什么”。

首批对象：
- `city`
- `district`
- `subdistrict_or_town`
- `planning_unit`
- `parcel`
- `building`
- `road_segment`
- `waterbody`
- `facility`

核心字段建议：

```text
id
object_type
geometry
valid_from
valid_to
source_type
source_ref
version
```

### 1.2 Planning State
描述“规划允许、要求或限制什么”。

首批对象：
- `plan`
- `plan_version`
- `land_use_control`
- `development_control`
- `controlled_boundary`
- `planning_constraint`

控制字段按研究需要逐步加入，例如：

```text
planned_land_use
far_max
building_height_max_m
building_density_max
绿地率等指标（机器字段后续统一英文）
```

不在 Phase 1 追求完整复刻全国所有国土空间规划数据库字段。

### 1.3 Governance State
描述“谁能做什么”。

首批对象：
- `organization`
- `actor`
- `role`
- `permission`
- `planning_document`
- `approval`

权限不能只写在自然语言文档中；Phase 1 后续应形成机器可读矩阵。

### 1.4 Event History
描述“状态如何变化”。

统一事件至少包含：

```text
event_id
event_type
actor_id
target_id
occurred_at
previous_version
resulting_version
authority_basis
related_document_ids
payload_hash
```

初始 `event_type` 候选：

```text
CREATE
SUBMIT
REVIEW
APPROVE
REJECT
ACTIVATE
AMEND
WITHDRAW
SUPERSEDE
ATTEMPT_UNAUTHORIZED_CHANGE
VERIFY
```

### 1.5 Ground Truth
描述“正确结果是什么”。

Ground Truth 不与链实现绑定。每个场景至少应能够判断：

```text
authorized: true | false
accepted: true | false
state_changed: true | false
expected_state_version
expected_error_code
expected_audit_event
expected_hash_match
expected_spatial_conflicts
```

## 2. ID 设计原则

稳定 ID 应：
- 不包含可识别现实敏感对象的编码；
- 不随语言改变；
- 不因几何微调而改变；
- 对象与版本分离。

候选格式：

```text
RC:CITY:001
RC:DISTRICT:001
RC:PARCEL:000001
RC:PLAN:0001
RC:DOC:000001
RC:ORG:001
RC:ACTOR:001
RC:EVENT:000001
RC:SCENARIO:S001
```

版本另记：

```text
object_id = RC:PARCEL:000001
version = 3
```

而不是把版本写死进对象永久 ID。

## 3. 时间模型

Phase 1 使用明确的实验时间轴。机器日期时间统一 ISO 8601。应区分：

- `occurred_at`：事件发生时间；
- `recorded_at`：事件被系统记录时间；
- `valid_from` / `valid_to`：状态在规划语义上的有效时间。

这三者不得默认等同。

## 4. 空间参考与单位

正式 CRS 在生成核心城市时冻结。ReferenceCity 应采用**纯合成坐标或明确的非敏感实验坐标方案**，避免暗示对应现实敏感位置。

机器字段明确单位：

```text
area_m2
length_m
height_m
far
ratio
```

## 5. 数据来源分类

每个数据集或对象至少标记：

```text
SYNTHETIC
PUBLIC_REAL
DERIVED
MANUAL_ANNOTATION
```

ReferenceCity 核心 v1.0 原则上以 `SYNTHETIC` 为主。

## 6. 数据与链的边界

ReferenceCity 用于测试时，应允许两类模式：

1. **On-chain test payload**：小型、明确允许写链的测试对象；
2. **Off-chain asset + on-chain proof**：大型 GIS/文档留在外部存储，链仅记录标识、Hash、版本、权限与事件。

不应为了演示区块链而默认把完整空间数据库写入链。

## 7. 后续 Schema 顺序

建议按以下顺序冻结：

1. `common.schema.json`
2. `spatial-object.schema.json`
3. `plan.schema.json`
4. `governance.schema.json`
5. `event.schema.json`
6. `scenario.schema.json`
7. `expected-result.schema.json`

Schema 进入 v1.0 前允许破坏性修改；ReferenceCity v1.0 后采用显式版本策略。
