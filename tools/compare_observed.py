from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "v0.1"
DEFAULT_EXPECTED = ROOT / "expected" / "v0.1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_conflicts(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda item: (
        item.get("conflict_type", ""), item.get("target_id", ""),
        item.get("constraint_id", ""), item.get("severity", "")
    ))


def compare_one(expected: dict, observed: dict) -> list[str]:
    mismatches: list[str] = []
    pairs = [
        ("authorized", "authorized"),
        ("accepted", "accepted"),
        ("state_changed", "state_changed"),
        ("expected_state_version", "state_version"),
        ("expected_error_code", "error_code"),
        ("expected_hash_match", "hash_match"),
    ]
    for expected_key, observed_key in pairs:
        if expected[expected_key] != observed[observed_key]:
            mismatches.append(f"{observed_key}: expected {expected[expected_key]!r}, observed {observed[observed_key]!r}")

    audit = expected["expected_audit_event"]
    if audit is not None and audit not in observed["audit_events"]:
        mismatches.append(f"audit_events: expected event {audit!r} not present")

    if normalize_conflicts(expected["expected_spatial_conflicts"]) != normalize_conflicts(observed["spatial_conflicts"]):
        mismatches.append("spatial_conflicts: expected and observed conflict sets differ")
    return mismatches


def validator():
    schemas = {path.name: load(path) for path in SCHEMA_DIR.glob("*.schema.json")}
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return Draft202012Validator(
        schemas["observed-result.schema.json"], registry=registry, format_checker=FormatChecker()
    )


def evaluate(observed_dir: Path, expected_dir: Path = DEFAULT_EXPECTED) -> dict:
    observed_validator = validator()
    results = []
    passed = 0
    for number in range(1, 11):
        name = f"S{number:03d}"
        expected = load(expected_dir / f"{name}.json")
        observed_path = observed_dir / f"{name}.json"
        if not observed_path.exists():
            results.append({"scenario": name, "pass": False, "mismatches": ["missing observed result"]})
            continue
        observed = load(observed_path)
        schema_errors = sorted(observed_validator.iter_errors(observed), key=lambda error: list(error.path))
        if schema_errors:
            results.append({"scenario": name, "pass": False, "mismatches": [f"schema: {error.message}" for error in schema_errors]})
            continue
        mismatches = []
        if observed["scenario_id"] != expected["scenario_id"]:
            mismatches.append("scenario_id mismatch")
        mismatches.extend(compare_one(expected, observed))
        ok = not mismatches
        if ok:
            passed += 1
        results.append({"scenario": name, "pass": ok, "mismatches": mismatches})
    return {"passed": passed, "total": 10, "all_passed": passed == 10, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare implementation observed results with ReferenceCity Ground Truth")
    parser.add_argument("--observed", type=Path, required=True)
    parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = evaluate(args.observed, args.expected)
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(text)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + "\n", encoding="utf-8")
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
