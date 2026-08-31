from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from canonical_json import canonical_sha256

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT))

from generators.core_city import DEFAULT_CONFIG, generate  # noqa: E402

DEFAULT_OUTPUT = ROOT / "data" / "core-v0.1" / "generated"
GENERATOR_PATH = ROOT / "generators" / "core_city.py"


def file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def flat_feature(item: dict) -> dict:
    name = item.get("name") or {}
    props = {
        "id": item["id"],
        "object_type": item["object_type"],
        "parent_id": item.get("parent_id"),
        "version": item["version"],
        "area_m2": item.get("area_m2"),
        "length_m": item.get("length_m"),
        "name_zh": name.get("zh-Hans"),
        "name_en": name.get("en"),
        "name_ja": name.get("ja"),
    }
    props.update(item.get("properties", {}))
    return {"type": "Feature", "id": item["id"], "geometry": item["geometry"], "properties": props}


def write_pretty(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build(config_path: Path, output_dir: Path) -> dict:
    result = generate(config_path, output_dir)
    config = json.loads(config_path.read_text(encoding="utf-8"))

    preview = {
        "type": "FeatureCollection",
        "name": "ReferenceCity Core v0.1 spatial preview",
        "referencecity_crs": config["crs_identifier"],
        "referencecity_note": "Synthetic Cartesian coordinates in metres; not RFC 7946 WGS84 geolocation.",
        "features": [flat_feature(item) for item in result["spatial"]],
    }
    preview_path = output_dir / "spatial-preview.geojson"
    write_pretty(preview_path, preview)

    counts: dict[str, int] = {}
    for item in result["spatial"]:
        counts[item["object_type"]] = counts.get(item["object_type"], 0) + 1

    snapshot = {
        "snapshot_id": "RC:DATASET:COREV01SNAPSHOT",
        "dataset_version": config["dataset_version"],
        "schema_version": "0.1",
        "generator": {
            "path": "generators/core_city.py",
            "sha256": file_sha256(GENERATOR_PATH),
        },
        "config": {
            "path": "data/core-v0.1/config.json",
            "sha256": file_sha256(config_path),
            "random_seed": config["random_seed"],
        },
        "counts": {
            "spatial_objects": len(result["spatial"]),
            "planning_objects": len(result["planning"]),
            "by_spatial_type": dict(sorted(counts.items())),
        },
        "assets": [
            {
                "path": "spatial-objects.json",
                "file_sha256": file_sha256(output_dir / "spatial-objects.json"),
                "canonical_sha256": canonical_sha256(result["spatial"]),
                "media_type": "application/json",
            },
            {
                "path": "planning-objects.json",
                "file_sha256": file_sha256(output_dir / "planning-objects.json"),
                "canonical_sha256": canonical_sha256(result["planning"]),
                "media_type": "application/json",
            },
            {
                "path": "manifest.json",
                "file_sha256": file_sha256(output_dir / "manifest.json"),
                "canonical_sha256": canonical_sha256(result["manifest"]),
                "media_type": "application/json",
            },
            {
                "path": "spatial-preview.geojson",
                "file_sha256": file_sha256(preview_path),
                "media_type": "application/geo+json",
            },
        ],
    }
    write_pretty(output_dir / "snapshot.json", snapshot)
    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the ReferenceCity core v0.1 reproducible snapshot")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    snapshot = build(args.config, args.output)
    print(json.dumps(snapshot, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
