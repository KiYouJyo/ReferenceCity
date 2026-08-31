# ReferenceCity 规划治理模型 v0.1

> 中文源文本。English: `GOVERNANCE_MODEL.en.md` · 日本語: `GOVERNANCE_MODEL.ja.md`

Phase 1C 的目标不是复制某个现实部门的完整法定职权，而是建立一套**职责分离、权限可判定、结果可审计**的最小规划治理实验模型。

## 六类角色

| 角色 | 主要能力 | 明确禁止/缺失能力 |
|---|---|---|
| PLANNER | 创建、提交、发起调整 | 自行批准、生效 |
| REVIEWER | 审查、退回、拒绝 | 修改原成果、最终批准 |
| APPROVER | 批准、生效、废止旧版 | 代替编制者秘密改内容 |
| DISTRICT_MANAGER | 指定区范围的控制审查 | 越区处理 |
| APPLICANT | 提交建设项目申请 | 修改规划成果 |
| AUDITOR | 验证 Hash、版本、历史 | 改变业务状态 |

## 生命周期

```text
DRAFT ──SUBMIT_PLAN──> SUBMITTED
  │                       │
  │                       ├─REVIEW_PASS──> REVIEWED ──APPROVE_PLAN──> APPROVED ──ACTIVATE_PLAN──> EFFECTIVE
  │                       ├─RETURN_PLAN──> DRAFT
  │                       └─REJECT_PLAN──> REJECTED
  │
  └─WITHDRAW_PLAN──> WITHDRAWN

EFFECTIVE ──OPEN_AMENDMENT──> AMENDMENT ──SUBMIT_AMENDMENT──> SUBMITTED
EFFECTIVE ──SUPERSEDE_PLAN──> SUPERSEDED
```

每次状态迁移必须同时满足：当前状态正确、operation 存在、actor 的 role 被允许、所需文档/签名存在、版本前置条件正确。链实现输出必须留下 audit event。

## 研究边界

该模型是功能性实验抽象，不宣称这些角色与中国现实任何一级政府、审批机关或法定程序一一对应。后续制度研究需要把真实法规与地方实践作为独立证据层。
