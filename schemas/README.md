# Schemas

本目录保存 ReferenceCity 的稳定机器 Schema。概念定义来自 UrbanPlanningLab；ReferenceCity 只实现和测试这些 Schema 的具体实例。

Phase 1 计划顺序：

```text
common.schema.json
spatial-object.schema.json
plan.schema.json
governance.schema.json
event.schema.json
scenario.schema.json
expected-result.schema.json
```

规则：
- Schema 标识符和字段名使用英文；
- Schema 本身版本化；
- 破坏性修改必须显式提升 Schema 版本；
- ReferenceCity v1.0 发布后，不允许无版本说明地改变既有字段语义；
- 三语展示文本不得改变机器稳定值。
