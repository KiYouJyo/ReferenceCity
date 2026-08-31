# Generators

本目录用于保存可重复生成 ReferenceCity 空间对象、规划状态及压力数据的代码。

生成器必须优先支持：

```text
explicit parameters
fixed random seed
versioned algorithm
reproducible output
```

核心城市生成与压力数据生成必须分离。未来建议：

```text
core-city/
terrain/
roads/
parcels/
buildings/
planning/
stress/
```

任何人工修正应记录为可追踪 patch/override，而不是只在 GIS 软件中静默修改最终文件。
