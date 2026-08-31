from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))

from build_snapshot import build  # noqa: E402

SCHEMA_DIR = ROOT / "schemas" / "v0.1"
CONFIG = ROOT / "data" / "core-v0.1" / "config.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def registry_and_schemas() -> tuple[Registry, dict[str, dict]]:
    schemas = {path.name: load_json(path) for path in SCHEMA_DIR.glob("*.schema.json")}
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry, schemas


def bbox(geometry: dict) -> tuple[float, float, float, float]:
    ring = geometry["coordinates"][0]
    xs = [point[0] for point in ring]
    ys = [point[1] for point in ring]
    return min(xs), min(ys), max(xs), max(ys)


def contains(outer: tuple[float, float, float, float], inner: tuple[float, float, float, float]) -> bool:
    return outer[0] <= inner[0] and outer[1] <= inner[1] and outer[2] >= inner[2] and outer[3] >= inner[3]


def main() -> int:
    registry, schemas = registry_and_schemas()
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory)
        snapshot = build(CONFIG, output)
        Draft202012Validator(
            schemas["snapshot.schema.json"], registry=registry, format_checker=FormatChecker()
        ).validate(snapshot)

        spatial = load_json(output / "spatial-objects.json")
        planning = load_json(output / "planning-objects.json")
        preview = load_json(output / "spatial-preview.geojson")

        ids = [item["id"] for item in spatial]
        assert len(ids) == len(set(ids)), "duplicate spatial IDs"
        by_id = {item["id"]: item for item in spatial}
        for item in spatial:
            parent_id = item.get("parent_id")
            if parent_id is not None:
                assert parent_id in by_id, f"missing parent {parent_id} for {item['id']}"

        city = by_id["RC:CITY:001"]
        city_area = city["area_m2"]
        parcels = [item for item in spatial if item["object_type"] == "parcel"]
        districts = [item for item in spatial if item["object_type"] == "district"]
        towns = [item for item in spatial if item["object_type"] == "subdistrict_or_town"]
        buildings = [item for item in spatial if item["object_type"] == "building"]
        assert sum(item["area_m2"] for item in parcels) == city_area
        assert sum(item["area_m2"] for item in districts) == city_area
        assert sum(item["area_m2"] for item in towns) == city_area

        for building in buildings:
            parcel = by_id[building["parent_id"]]
            assert contains(bbox(parcel["geometry"]), bbox(building["geometry"])), building["id"]

        controls = [item for item in planning if item["planning_object_type"] == "development_control"]
        assert len(controls) == len(parcels)
        assert {item["target_ids"][0] for item in controls} == {item["id"] for item in parcels}
        boundaries = [item for item in planning if item["planning_object_type"] == "controlled_boundary"]
        assert {item["constraint_code"] for item in boundaries} == {
            "urban_development_boundary",
            "ecological_constraint",
            "farmland_constraint",
        }

        assert preview["type"] == "FeatureCollection"
        assert preview["referencecity_crs"] == "RC-SYNTHETIC-1"
        assert len(preview["features"]) == len(spatial)
        print("PASS core snapshot topology, schema and preview checks")
        for asset in snapshot["assets"]:
            print(asset)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
