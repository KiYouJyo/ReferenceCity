# ReferenceCity Adapter Contract v0.1

> 日本語ミラー。中文: `README.md` · English: `README.en.md`

Phase 1E ではプログラミング言語、プロセス通信方式、ネットワーク API を強制せず、実装から独立した**入力 bundle と observed result のデータ契約**だけを定義します。

流れは Benchmark Input Bundle → Chain Adapter → Observed Result JSON → Evaluator → Ground Truth です。Adapter に渡す隔離入力 bundle には Ground Truth を含めず、`expected/` は実行後に evaluator だけが読み取ります。

`python tools/build_benchmark_input.py --output build/benchmark-input-v0.1` で、Core データ、release lock、governance/lifecycle/transaction fixture、S001–S010 入力、v0.1 Schema を含む bundle を生成します。ただし `expected/` は含みません。

各シナリオは `observed-result.schema.json` に適合する JSON を 1 件出力し、通常 `observed/S001.json` ～ `S010.json` とします。`python tools/compare_observed.py --observed observed/` で Ground Truth と比較できます。

CLI、HTTP、gRPC、FFI、SDK のいずれも利用可能です。Adapter は隔離 bundle を消費し、scenario の順序で request を実行し、標準 observed result を生成できればよいものとします。
