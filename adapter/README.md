# ReferenceCity Adapter Contract v0.1

> 中文源文本。English: `README.en.md` · 日本語: `README.ja.md`

Phase 1E 不规定区块链必须使用哪种语言、进程协议或网络接口，而只规定**输入包与输出结果的数据契约**。

## 核心原则

```text
Benchmark Input Bundle
        ↓
   Chain Adapter
        ↓
Observed Result JSON
        ↓
Evaluator
        ↓
Ground Truth
```

适配器运行时得到的输入包**不包含 Ground Truth**。Ground Truth 只由 evaluator 在链执行完成后读取。这样可以避免把 `expected/` 当成实现逻辑的一部分。

## 输入

运行：

```bash
python tools/build_benchmark_input.py --output build/benchmark-input-v0.1
```

生成的隔离输入包包含：

- `benchmark-input.json`；
- ReferenceCity Core v0.1 的实际生成数据与 `snapshot.json`；
- `release-lock.json`；
- governance / lifecycle / transaction fixtures；
- S001–S010 的 scenario、operation request 与场景内部 fixture；
- v0.1 JSON Schema。

明确不复制：

```text
expected/
```

## 输出

每个场景输出一个符合 `schemas/v0.1/observed-result.schema.json` 的 JSON，例如：

```text
observed/S001.json
...
observed/S010.json
```

必须报告授权判断、是否接受、是否改变状态、最终版本、错误码、审计事件、Hash 判断和空间冲突。实现私有的交易 ID / state proof 可以放在 `evidence` 中，但 evaluator 不依赖这些字段判断核心 PASS/FAIL。

## 评测

```bash
python tools/compare_observed.py --observed observed/
```

Evaluator 将 observed result 与仓库内部 `expected/v0.1/` 比较。适配器不应读取 `expected/`。

## 进程接口

v0.1 **不强制** CLI、HTTP、gRPC、FFI 或某种 SDK。C#、Rust、Go、JavaScript 等实现只需要能够：

1. 消费隔离 benchmark bundle；
2. 顺序执行 scenario 中的 operation requests；
3. 生成符合 observed-result Schema 的结果。

后续如果多个链实现需要统一启动方式，再在不改变数据契约的前提下增加可选 runner profile。
