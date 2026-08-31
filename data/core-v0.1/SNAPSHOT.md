# Core v0.1 Snapshot Policy

ReferenceCity Core `0.1.0` 采用“**生成源 + Snapshot descriptor + CI artifact + release lock**”冻结，而不是人工维护数百个重复对象文件。

## 生成

```bash
pip install -r requirements-dev.txt
python tools/build_snapshot.py
```

输出：

```text
generated/
├─ spatial-objects.json
├─ planning-objects.json
├─ manifest.json
├─ spatial-preview.geojson
└─ snapshot.json
```

`spatial-preview.geojson` 使用 `RC-SYNTHETIC-1` 的米制笛卡尔坐标，仅供 QGIS 等软件可视检查；它不声明真实 WGS84 地理位置。

## 冻结策略

Phase 1B 验收时提交 `release-lock.json`，固定生成器、config、对象数以及核心 asset 的 file/canonical SHA-256。CI 每次重新生成并与 lock 比对。

正式发布时，GitHub Actions 同时上传完整生成结果作为 artifact/release 输入。
