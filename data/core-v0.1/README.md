# ReferenceCity Core v0.1

Phase 1B 的确定性核心城市配置。

当前先版本化**生成参数与生成器**，不手工维护成百上千个重复 JSON 对象。运行：

```bash
python generators/core_city.py
```

默认输出到 `data/core-v0.1/generated/`。生成结果必须满足：

- 1 city；
- 3 districts；
- 6 subdistrict/town units；
- 60 parcels；
- 120 buildings；
- 18 road segments；
- 1 synthetic river；
- 12 facilities；
- 1 plan + 1 plan version + 60 development controls + 3 controlled boundaries。

生成是确定性的：相同版本、配置和 `random_seed` 必须产生相同文件 Hash。

> `generated/` 在 Phase 1B 验收前仍视为可重建产物；正式 ReferenceCity 基准发布时再冻结生成结果与 release checksum。
