from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "v0.1"
EXAMPLE_DIR = ROOT / "examples" / "minimal"

EXAMPLES = {
    "spatial-object.json": "spatial-object.schema.json",
    "plan.json": "plan.schema.json",
    "governance-organization.json": "governance.schema.json",
    "event.json": "event.schema.json",
    "scenario-s001.json": "scenario.schema.json",
    "expected-s001.json": "expected-result.schema.json",
    "manifest.json": "dataset-manifest.schema.json",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    schemas = {path.name: load_json(path) for path in SCHEMA_DIR.glob("*.schema.json")}
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))

    failed = False
    for example_name, schema_name in EXAMPLES.items():
        schema = schemas[schema_name]
        instance = load_json(EXAMPLE_DIR / example_name)
        validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
        if errors:
            failed = True
            print(f"FAIL {example_name} -> {schema_name}")
            for error in errors:
                location = "/".join(str(part) for part in error.path) or "<root>"
                print(f"  {location}: {error.message}")
        else:
            print(f"PASS {example_name} -> {schema_name}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
