# ReferenceCity Schema v0.1

Phase 1A 的机器契约，采用 JSON Schema Draft 2020-12。

## 文件

- `common.schema.json`：稳定 ID、时间、Hash、来源、敏感性、三语文本、基础几何；
- `spatial-object.schema.json`：空间状态；
- `plan.schema.json`：规划状态；
- `governance.schema.json`：组织、人员、角色、权限、规划文档与审批；
- `event.schema.json`：状态变化与审计事件；
- `scenario.schema.json`：可执行 benchmark 输入；
- `expected-result.schema.json`：与链实现无关的 Ground Truth；
- `dataset-manifest.schema.json`：数据 provenance、敏感性、CRS、单位与资产清单。

## 稳定性

`v0.1` 在 ReferenceCity v1.0 前允许破坏性修改。机器字段固定使用英文，不随 README 语言变化。

## 设计边界

这些 Schema 只冻结跨研究可复用的最小语义，不试图复刻任何具体地区完整规划数据库字段，也不把链实现细节写入数据模型。
