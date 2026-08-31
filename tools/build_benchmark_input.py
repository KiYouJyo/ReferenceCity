from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from build_snapshot import build as build_snapshot

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_ROOT = ROOT / "scenarios" / "v0.1"
CORE_CONFIG = ROOT / "data" / "core-v0.1" / "config.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def copy_repo_file(relative: str, output: Path) -> None:
    source = ROOT / relative
    if not source.is_file():
        raise FileNotFoundError(relative)
    destination = output / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build(output: Path) -> dict:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    core_output = output / "data" / "core-v0.1" / "generated"
    build_snapshot(CORE_CONFIG, core_output)
    copy_repo_file("data/core-v0.1/release-lock.json", output)

    for relative in [
        "data/governance-v0.1/entities.json",
        "data/governance-v0.1/lifecycle.json",
        "data/governance-v0.1/transaction-rules.json",
        "data/governance-v0.1/documents-and-approvals.json",
        "data/governance-v0.1/documents/plan-v1-submission.json",
    ]:
        copy_repo_file(relative, output)

    schema_destination = output / "schemas" / "v0.1"
    schema_destination.mkdir(parents=True, exist_ok=True)
    for schema in (ROOT / "schemas" / "v0.1").glob("*.schema.json"):
        shutil.copy2(schema, schema_destination / schema.name)

    entries = []
    for number in range(1, 11):
        scenario_name = f"S{number:03d}"
        scenario_path = SCENARIO_ROOT / scenario_name / "scenario.json"
        scenario = load(scenario_path)
        scenario_ref = f"scenarios/v0.1/{scenario_name}/scenario.json"
        copy_repo_file(scenario_ref, output)

        request_refs = []
        for action in scenario["actions"]:
            request_ref = action["request_ref"]
            copy_repo_file(request_ref, output)
            request_refs.append(request_ref)

        fixture_refs = []
        for fixture in scenario["fixtures"]:
            copy_repo_file(fixture, output)
            fixture_refs.append(fixture)

        entries.append({
            "scenario_id": scenario["scenario_id"],
            "scenario_ref": scenario_ref,
            "request_refs": request_refs,
            "fixture_refs": fixture_refs,
        })

    manifest = {
        "benchmark_id": "RC:BENCHMARK:V01",
        "benchmark_version": "0.1.0",
        "protocol_version": "0.1",
        "ground_truth_included": False,
        "core_snapshot_ref": "data/core-v0.1/generated/snapshot.json",
        "scenario_count": 10,
        "scenarios": entries,
    }
    (output / "benchmark-input.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build isolated ReferenceCity benchmark input without Ground Truth")
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "benchmark-input-v0.1")
    args = parser.parse_args()
    manifest = build(args.output)
    print(f"Built {manifest['scenario_count']} scenarios at {args.output}; ground_truth_included=false")


if __name__ == "__main__":
    main()
