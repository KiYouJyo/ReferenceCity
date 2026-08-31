# ReferenceCity Adapter Contract v0.1

> English mirror. 中文: `README.md` · 日本語: `README.ja.md`

Phase 1E does not mandate a programming language, process protocol, or network API. It defines only an implementation-independent **input bundle and observed-result contract**.

The flow is: Benchmark Input Bundle → Chain Adapter → Observed Result JSON → Evaluator → Ground Truth. The isolated bundle supplied to an adapter does **not** contain Ground Truth; `expected/` is read only by the evaluator after execution.

Build an isolated input with `python tools/build_benchmark_input.py --output build/benchmark-input-v0.1`. It contains the generated core dataset, release lock, governance/lifecycle/transaction fixtures, S001–S010 scenario inputs, and v0.1 Schemas, but no `expected/` directory.

Each scenario produces one JSON document conforming to `observed-result.schema.json`, normally `observed/S001.json` through `observed/S010.json`. Evaluate them with `python tools/compare_observed.py --observed observed/`.

CLI, HTTP, gRPC, FFI, or an SDK may all be used. The adapter only needs to consume the isolated bundle, execute requests in scenario order, and emit the standard observed result.
