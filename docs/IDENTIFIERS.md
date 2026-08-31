# ReferenceCity 稳定 ID 规则 v0.1

## 1. 原则

ID 是机器身份，不是展示名称。它必须：

- 与中文、英文、日文展示文本无关；
- 与几何坐标和属性值解耦；
- 与对象版本解耦；
- 不编码现实敏感地理信息；
- 在同一 ReferenceCity 主版本内保持稳定。

## 2. 格式

```text
RC:<NAMESPACE>:<LOCAL_ID>
```

首批命名空间：

```text
CITY DISTRICT TOWN UNIT PARCEL BUILDING ROAD WATER FACILITY
PLAN PLANVER CONTROL BOUNDARY CONSTRAINT
ORG ACTOR ROLE PERMISSION DOC APPROVAL
EVENT SCENARIO DATASET
```

示例：

```text
RC:CITY:001
RC:PARCEL:000001
RC:PLAN:0001
RC:ACTOR:001
RC:SCENARIO:S001
```

## 3. 版本

版本永远单独保存：

```json
{
  "id": "RC:PARCEL:000001",
  "version": 3
}
```

禁止使用 `RC:PARCEL:000001:V3` 作为永久对象 ID。

## 4. 删除与重建

已进入发布版或 benchmark 的 ID 不重用。删除对象保留历史记录；新对象获得新 ID。
