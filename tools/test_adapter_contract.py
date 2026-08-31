from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_benchmark_input import build as build_input  # noqa: E402
from compare_observed import evaluate  # noqa: E402

EXPECTED = ROOT / "expected" / "v0.1"
SCHEMA_DIR = ROOT / "schemas" / "v0.1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def observed_from_expected(expected: dict) -> dict:
    audit = expected["expected_audit_event"]
    return {
        "scenario_id": expected["scenario_id"],
        "protocol_version": "0.1",
        "adapter": {
            "name": "referencecity-harness-self-test",
            "version": "0.1.0",
            "implementation": "TEST_ONLY_NOT_A_CHAIN",
            "commit": None,
        },
        "executed_at": "2030-04-01T00:00:00+08:00",
        "authorized": expected["authorized"],
        "accepted": expected["accepted"],
        "state_changed": expected["state_changed"],
        "state_version": expected["expected_state_version"],
        "error_code": expected["expected_error_code"],
        "audit_events": [] if audit is None else [audit],
        "hash_match": expected["expected_hash_match"],
        "spatial_conflicts": expected["expected_spatial_conflicts"],
        "evidence": {"transaction_id": None, "state_proof": None, "log_ref": None},
    }


def manifest_validator():
    schemas = {path.name: load(path) for path in SCHEMA_DIR.glob("*.schema.json")}
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return Draft202012Validator(
        schemas["benchmark-input.schema.json"], registry=registry, format_checker=FormatChecker()
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as bundle_tmp, tempfile.TemporaryDirectory() as observed_tmp:
        bundle = Path(bundle_tmp)
        manifest = build_input(bundle)
        manifest_validator().validate(manifest)
        assert manifest["ground_truth_included"] is False
        assert manifest["scenario_count"] == 10
        assert not (bundle / "expected").exists(), "Ground Truth leaked into adapter input bundle"
        assert (bundle / "data/core-v0.1/generated/spatial-objects.json").exists()
        assert (bundle / "data/core-v0.1/generated/planning-objects.json").exists()
        assert (bundle / "data/core-v0.1/generated/snapshot.json").exists()

        observed_dir = Path(observed_tmp)
        for number in range(1, 11):
            name = f"S{number:03d}"
            value = observed_from_expected(load(EXPECTED / f"{name}.json"))
            (observed_dir / f"{name}.json").write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )

        passing = evaluate(observed_dir)
        assert passing["all_passed"] and passing["passed"] == 10

        broken = load(observed_dir / "S010.json")
        broken["state_version"] = 999
        (observed_dir / "S010.json").write_text(json.dumps(broken, ensure_ascii=False) + "\n", encoding="utf-8")
        failing = evaluate(observed_dir)
        assert failing["all_passed"] is False
        assert failing["passed"] == 9
        assert any("state_version" in item for item in failing["results"][-1]["mismatches"])

    print("PASS adapter contract: isolated input, 10/10 comparator pass, intentional mismatch detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
