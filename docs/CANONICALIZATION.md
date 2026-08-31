# ReferenceCity 内容规范化与 Hash v0.1

## 两种 Hash 必须区分

ReferenceCity 从 Phase 1B 起明确区分：

1. **File SHA-256**：对实际文件字节计算，用于发布包完整性、下载校验和 snapshot 固定；
2. **Canonical SHA-256**：先按 RFC 8785 JSON Canonicalization Scheme (JCS) 规范化 JSON 内容，再计算 SHA-256，用于跨语言/跨实现的内容身份与链上 proof。

因此仅改变 JSON 的缩进、空格或键输出顺序，可以改变 File SHA-256，但不应改变 Canonical SHA-256。

Canonical Hash 表示：

```text
sha256:<64 lowercase hexadecimal characters>
```

## 适用范围

核心 `spatial-objects.json`、`planning-objects.json` 和 `manifest.json` 同时记录 file hash 与 canonical hash。GeoJSON preview 仅作为可视检查产物，Phase 1B 不把其内容 Hash 当作链协议 Ground Truth。

## 数值规则

进入 canonicalization 前的数据必须已经满足 Schema：不得使用 NaN、Infinity 或实现私有数值类型。空间单位与比例规则见 `CONVENTIONS.md`。

## 跨实现要求

未来 C#、Rust、Go、JavaScript 等客户端如果参与链上内容指纹计算，必须实现兼容 RFC 8785 的 canonical JSON，不得简单对本地 `JSON.stringify` / serializer 默认输出直接 Hash。
