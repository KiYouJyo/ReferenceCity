# Exports

本目录用于保存或说明由 ReferenceCity 核心数据生成的交换格式。

计划支持：

```text
GeoJSON
GeoPackage
CSV / JSON
```

原则：
- `data/` 中的规范源数据与 `exports/` 中的派生交换文件必须区分；
- 可自动生成的导出文件优先由脚本重建，并记录生成版本；
- 导出不得改变稳定 ID、语义或 Ground Truth；
- 大型派生文件是否提交 Git，应根据体积与可重复生成性单独决定。
