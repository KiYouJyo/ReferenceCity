from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generators.core_city import generate  # noqa: E402

SCHEMA_DIR = ROOT / "schemas" / "v0.1"
CONFIG = ROOT / "data" / "core-v0.1" / "config.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(path.glob("*.json")):
        digest.update(file.name.encode("utf-8"))
        digest.update(file.read_bytes())
    return digest.hexdigest()


def registry_and_schemas() -> tuple[Registry, dict[str, dict]]:
    schemas = {path.name: load_json(path) for path in SCHEMA_DIR.glob("*.schema.json")}
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry, schemas


def validate_items(items: list[dict], schema: dict, registry: Registry) -> None:
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    for index, item in enumerate(items):
        errors = list(validator.iter_errors(item))
        if errors:
            messages = "; ".join(error.message for error in errors)
            raise AssertionError(f"item {index} failed schema validation: {messages}")


def main() -> int:
    registry, schemas = registry_and_schemas()
    with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
        first_path, second_path = Path(first), Path(second)
        result = generate(CONFIG, first_path)
        generate(CONFIG, second_path)

        counts: dict[str, int] = {}
        for item in result["spatial"]:
            counts[item["object_type"]] = counts.get(item["object_type"], 0) + 1

        expected_counts = {
            "city": 1,
            "district": 3,
            "subdistrict_or_town": 6,
            "parcel": 60,
            "building": 120,
            "road_segment": 18,
            "waterbody": 1,
            "facility": 12,
        }
        assert counts == expected_counts, (counts, expected_counts)
        assert len(result["spatial"]) == 221
        assert len(result["planning"]) == 65

        validate_items(result["spatial"], schemas["spatial-object.schema.json"], registry)
        validate_items(result["planning"], schemas["plan.schema.json"], registry)
        Draft202012Validator(
            schemas["dataset-manifest.schema.json"], registry=registry, format_checker=FormatChecker()
        ).validate(result["manifest"])

        first_digest = tree_digest(first_path)
        second_digest = tree_digest(second_path)
        assert first_digest == second_digest, (first_digest, second_digest)
        print(f"PASS core generator: 221 spatial, 65 planning, deterministic digest {first_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
