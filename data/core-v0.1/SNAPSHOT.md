# Core v0.1 Snapshot Policy

ReferenceCity Core `0.1.0` 已采用“**生成源 + Snapshot descriptor + CI artifact + release lock**”冻结，而不是人工维护数百个重复对象文件。

## 生成

```bash
pip install -r requirements-dev.txt
python tools/build_snapshot.py
```

输出 `spatial-objects.json`、`planning-objects.json`、`manifest.json`、`spatial-preview.geojson` 与 `snapshot.json`。

`spatial-preview.geojson` 使用 `RC-SYNTHETIC-1` 的米制笛卡尔坐标，仅供 QGIS 等软件可视检查；它不声明真实 WGS84 地理位置。

## Release lock

`release-lock.json` 固定：

- generator 文件 SHA-256；
- config SHA-256 与 random seed；
- 221 个空间对象和 65 个规划对象的数量；
- 核心 JSON 的 file SHA-256；
- 核心 JSON 的 RFC 8785 canonical SHA-256；
- preview 文件 SHA-256。

CI 每次从源重新生成 snapshot，并要求结果与 lock **逐字段完全一致**。任何改变核心城市的提交都必须显式更新 dataset 版本或 release lock，不能无声漂移。
