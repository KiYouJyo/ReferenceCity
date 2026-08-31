# Benchmark Scenario 规范

## 1. 目的

Scenario 是 ReferenceCity 的核心研究资产。它描述一个可重复发生的规划/治理操作，并配套独立的 Expected Result / Ground Truth。

场景不应该依赖某条链、某种智能合约语言或某个客户端实现。

## 2. 建议目录

```text
scenarios/
└─ S001-plan-registration/
   ├─ scenario.yaml
   ├─ input/
   │  ├─ state.json
   │  ├─ event.json
   │  └─ documents.json
   └─ README.md

expected/
└─ S001.json
```

## 3. Scenario 最小字段

```yaml
scenario_id: RC:SCENARIO:S001
name:
  zh-CN: 正常规划成果登记
  en: Normal plan registration
  ja: 正常な計画成果登録
category: lifecycle
reference_city_version: 0.x
initial_state_ref: ...
actions:
  - actor_id: RC:ACTOR:001
    event_type: SUBMIT
    target_id: RC:PLAN:0001
expected_ref: ../../expected/S001.json
deterministic: true
```

## 4. Expected Result 最小字段

```json
{
  "scenario_id": "RC:SCENARIO:S001",
  "authorized": true,
  "accepted": true,
  "state_changed": true,
  "expected_error_code": null,
  "expected_audit_event": true
}
```

具体状态、Hash 和空间冲突结果根据场景增加。

## 5. Phase 1 场景目录

| ID | 场景 | 类型 | 核心预期 |
|---|---|---|---|
| S001 | 正常规划成果登记 | lifecycle | ACCEPT |
| S002 | 合法版本更新 | lifecycle | ACCEPT + version increment |
| S003 | 正常审批并生效 | governance | ACCEPT + effective state |
| S004 | 无权限主体修改 | authorization | DENY + no state change |
| S005 | 已批准文档被篡改 | integrity | HASH_MISMATCH |
| S006 | 地块用途与规划约束冲突 | spatial | CONFLICT |
| S007 | 项目跨越受控边界 | spatial | CONFLICT / rule-dependent reject |
| S008 | 审批缺少必要主体或签名 | governance | INCOMPLETE_APPROVAL |
| S009 | 历史版本验证 | history | MATCH expected historical state |
| S010 | 并发/冲突更新 | versioning | VERSION_CONFLICT |

## 6. Ground Truth 原则

- Expected Result 由实验设计确定，不由被测链运行后“反推”。
- 对具有制度解释空间的规则，必须明确 ReferenceCity 的实验规则来源/假设，不声称其自动代表现实法律结论。
- 一个 Scenario 尽量只验证一个主要机制，避免失败后无法定位原因。
- 场景应可以在不同链实现、普通数据库实现或纯本地参考实现上执行。

## 7. 正常与异常场景都要保留

仅测试失败案例无法证明正常流程正确；仅测试正常流程也无法证明可信机制有效。Phase 1 的场景集至少同时覆盖：

```text
happy path
permission failure
integrity failure
spatial-rule failure
version conflict
history verification
```

## 8. 后续研究扩展

人居形态、城市更新、TOD 等研究进入后，应建立新的 scenario family，而不是修改 Phase 1 已冻结的可信链场景来迎合新研究。
