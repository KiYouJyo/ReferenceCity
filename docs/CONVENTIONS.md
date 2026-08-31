# ReferenceCity 机器约定 v0.1

## 时间

所有机器时间使用 ISO 8601 RFC 3339 兼容时间戳并显式包含时区，例如：

```text
2030-01-15T09:00:00+08:00
```

严格区分：

- `occurred_at`：业务事件发生时间；
- `recorded_at`：系统记录时间；
- `valid_from` / `valid_to`：规划或空间状态的语义有效期。

## 坐标参考

ReferenceCity v0.x 核心城市采用 `SYNTHETIC_CARTESIAN`，单位为米，不绑定真实经纬度。正式核心城市生成时冻结具体原点与范围。

## 单位

机器字段显式写单位：

- 长度：`*_m`；
- 面积：`*_m2`；
- 容积率：`far` / `far_max`，无量纲；
- 比率：0–1 小数，不使用百分数字符串。

## Hash

内容指纹统一表示为：

```text
sha256:<64 lowercase hexadecimal characters>
```

Hash 的规范化序列化规则将在 Phase 1B 冻结；在该规则冻结前，不得把不同程序计算出的 JSON Hash 当作跨实现 Ground Truth。

## 语言

机器字段、枚举和错误码使用英文稳定标识。面向人的核心名称和场景说明使用：

```json
{
  "zh-Hans": "中文",
  "en": "English",
  "ja": "日本語"
}
```

三种语言是显示层，不改变对象身份与业务判断。
