from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "data" / "governance-v0.1" / "transaction-rules.json"


def main() -> int:
    rules = json.loads(RULES.read_text(encoding="utf-8"))
    assert rules["model"] == "optimistic_concurrency"
    assert rules["version_field"] == "version"
    assert rules["request_version_field"] == "expected_version"
    codes = {rule["code"] for rule in rules["rules"]}
    required = {
        "VERSION_CONFLICT",
        "UNAUTHORIZED",
        "INVALID_STATE_TRANSITION",
        "MISSING_DOCUMENT",
        "MISSING_SIGNATURE",
        "HASH_MISMATCH",
        "REQUEST_ID_REUSE",
    }
    assert required.issubset(codes)
    for rule in rules["rules"]:
        if rule["code"] in required:
            assert rule["accepted"] is False
            assert rule["state_changed"] is False
            assert rule["audit_required"] is True
    assert rules["idempotency"]["same_request_same_payload"] == "RETURN_ORIGINAL_RESULT"
    assert rules["idempotency"]["same_request_different_payload"] == "REQUEST_ID_REUSE"
    print("PASS optimistic concurrency and transaction failure contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
