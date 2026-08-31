# ReferenceCity Planning Governance Model v0.1

> English mirror. 中文: `GOVERNANCE_MODEL.md` · 日本語: `GOVERNANCE_MODEL.ja.md`

Phase 1C defines a minimal experimental governance model with separation of duties, machine-decidable authority and auditable outcomes. It does not reproduce the complete statutory powers of any real government body.

Six roles are used: PLANNER creates/submits/amends drafts; REVIEWER reviews/returns/rejects submissions; APPROVER approves, activates and supersedes versions; DISTRICT_MANAGER reviews controls only within assigned district scope; APPLICANT submits development applications but cannot modify plans; AUDITOR verifies hashes, versions and history without changing business state.

The standard lifecycle is DRAFT → SUBMITTED → REVIEWED → APPROVED → EFFECTIVE, with return/rejection/withdrawal paths and an EFFECTIVE → AMENDMENT → SUBMITTED update loop. Each transition requires a valid current state, permitted operation and role, required documents/signatures, correct version preconditions and an audit event.

This is a functional research abstraction, not a claim that these roles map one-to-one to Chinese statutory planning procedures.
