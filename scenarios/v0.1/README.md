# ReferenceCity Benchmark Scenarios v0.1

Phase 1D 的 10 个核心场景均由三部分组成：`scenario.json` 描述故事与执行顺序，`request*.json` 是符合 `operation-request.schema.json` 的机器请求，`expected/v0.1/Sxxx.json` 是与链实现无关的 Ground Truth。

S001–S010 覆盖正常登记、合法调整、审批生效、越权、文档篡改、规划约束冲突、空间边界冲突、缺少签名、历史验证与并发版本冲突。
