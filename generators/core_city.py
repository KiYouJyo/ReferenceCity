from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "data" / "core-v0.1" / "config.json"
DEFAULT_OUTPUT = ROOT / "data" / "core-v0.1" / "generated"
VALID_FROM = "2030-01-01T00:00:00+08:00"


def localized(zh: str, en: str, ja: str) -> dict:
    return {"zh-Hans": zh, "en": en, "ja": ja}


def provenance(seed: int, generator: str = "generators/core_city.py") -> dict:
    return {
        "source_type": "SYNTHETIC",
        "source_ref": "ReferenceCity deterministic generator",
        "sensitivity": "SYNTHETIC_SAFE",
        "generated_by": generator,
        "random_seed": seed,
        "notes": None,
    }


def polygon(x0: float, y0: float, x1: float, y1: float) -> dict:
    return {
        "type": "Polygon",
        "coordinates": [[[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]],
    }


def line(points: list[list[float]]) -> dict:
    return {"type": "LineString", "coordinates": points}


def point(x: float, y: float) -> dict:
    return {"type": "Point", "coordinates": [x, y]}


def boundaries(length: int, parts: int) -> list[int]:
    return [round(length * i / parts) for i in range(parts + 1)]


def spatial_object(
    object_id: str,
    object_type: str,
    geometry: dict,
    seed: int,
    *,
    name: dict | None = None,
    parent_id: str | None = None,
    area_m2: float | None = None,
    length_m: float | None = None,
    properties: dict | None = None,
) -> dict:
    item = {
        "id": object_id,
        "object_type": object_type,
        "geometry": geometry,
        "version": 1,
        "valid_from": VALID_FROM,
        "valid_to": None,
        "properties": properties or {},
        "provenance": provenance(seed),
    }
    if name is not None:
        item["name"] = name
    if parent_id is not None:
        item["parent_id"] = parent_id
    if area_m2 is not None:
        item["area_m2"] = area_m2
    if length_m is not None:
        item["length_m"] = length_m
    return item


def build_spatial(config: dict) -> list[dict]:
    width = config["width_m"]
    height = config["height_m"]
    seed = config["random_seed"]
    rng = random.Random(seed)
    district_bounds = boundaries(width, config["district_count"])
    town_bounds = boundaries(height, config["towns_per_district"])
    parcel_x = boundaries(width, config["parcel_columns"])
    parcel_y = boundaries(height, config["parcel_rows"])

    items: list[dict] = []
    items.append(
        spatial_object(
            "RC:CITY:001",
            "city",
            polygon(0, 0, width, height),
            seed,
            name=localized("参考城", "Reference City", "リファレンスシティ"),
            area_m2=width * height,
            properties={"synthetic_population": 600000},
        )
    )

    for d in range(config["district_count"]):
        district_id = f"RC:DISTRICT:{d + 1:03d}"
        x0, x1 = district_bounds[d], district_bounds[d + 1]
        items.append(
            spatial_object(
                district_id,
                "district",
                polygon(x0, 0, x1, height),
                seed,
                name=localized(f"第{d + 1}区", f"District {d + 1}", f"第{d + 1}区"),
                parent_id="RC:CITY:001",
                area_m2=(x1 - x0) * height,
            )
        )
        for t in range(config["towns_per_district"]):
            town_no = d * config["towns_per_district"] + t + 1
            y0, y1 = town_bounds[t], town_bounds[t + 1]
            items.append(
                spatial_object(
                    f"RC:TOWN:{town_no:03d}",
                    "subdistrict_or_town",
                    polygon(x0, y0, x1, y1),
                    seed,
                    name=localized(f"第{town_no}镇街", f"Town Unit {town_no}", f"第{town_no}地区"),
                    parent_id=district_id,
                    area_m2=(x1 - x0) * (y1 - y0),
                )
            )

    parcel_records: list[tuple[dict, tuple[int, int, int, int]]] = []
    parcel_no = 0
    for row in range(config["parcel_rows"]):
        for col in range(config["parcel_columns"]):
            parcel_no += 1
            x0, x1 = parcel_x[col], parcel_x[col + 1]
            y0, y1 = parcel_y[row], parcel_y[row + 1]
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            district_index = min(int(cx * config["district_count"] / width), config["district_count"] - 1)
            town_side = min(int(cy * config["towns_per_district"] / height), config["towns_per_district"] - 1)
            town_no = district_index * config["towns_per_district"] + town_side + 1
            current_use = "commercial" if col in (4, 5) else ("industrial" if row in (0, 5) else "residential")
            parcel = spatial_object(
                f"RC:PARCEL:{parcel_no:06d}",
                "parcel",
                polygon(x0, y0, x1, y1),
                seed,
                name=localized(f"地块 {parcel_no}", f"Parcel {parcel_no}", f"街区 {parcel_no}"),
                parent_id=f"RC:TOWN:{town_no:03d}",
                area_m2=(x1 - x0) * (y1 - y0),
                properties={"current_land_use": current_use, "grid_row": row + 1, "grid_column": col + 1},
            )
            items.append(parcel)
            parcel_records.append((parcel, (x0, y0, x1, y1)))

            for building_index in range(config["buildings_per_parcel"]):
                margin_x = 120 + rng.randint(0, 60)
                margin_y = 160 + rng.randint(0, 80)
                mid_x = (x0 + x1) / 2
                if building_index == 0:
                    bx0, bx1 = x0 + margin_x, mid_x - 60
                else:
                    bx0, bx1 = mid_x + 60, x1 - margin_x
                by0, by1 = y0 + margin_y, y1 - margin_y
                building_no = (parcel_no - 1) * config["buildings_per_parcel"] + building_index + 1
                items.append(
                    spatial_object(
                        f"RC:BUILDING:{building_no:06d}",
                        "building",
                        polygon(bx0, by0, bx1, by1),
                        seed,
                        parent_id=parcel["id"],
                        area_m2=max(0, (bx1 - bx0) * (by1 - by0)),
                        properties={"floors": 6 + (building_no % 13)},
                    )
                )

    road_no = 0
    for x in parcel_x:
        road_no += 1
        items.append(
            spatial_object(
                f"RC:ROAD:{road_no:04d}",
                "road_segment",
                line([[x, 0], [x, height]]),
                seed,
                parent_id="RC:CITY:001",
                length_m=height,
                properties={"class": "grid_vertical"},
            )
        )
    for y in parcel_y:
        road_no += 1
        items.append(
            spatial_object(
                f"RC:ROAD:{road_no:04d}",
                "road_segment",
                line([[0, y], [width, y]]),
                seed,
                parent_id="RC:CITY:001",
                length_m=width,
                properties={"class": "grid_horizontal"},
            )
        )

    river_points = [[width * 0.47, 0], [width * 0.49, height * 0.25], [width * 0.46, height * 0.5], [width * 0.50, height * 0.75], [width * 0.48, height]]
    items.append(
        spatial_object(
            "RC:WATER:0001",
            "waterbody",
            line(river_points),
            seed,
            name=localized("参考河", "Reference River", "リファレンス川"),
            parent_id="RC:CITY:001",
            length_m=height,
            properties={"kind": "synthetic_river_centerline"},
        )
    )

    facility_no = 0
    interval = config["facility_interval_parcels"]
    for parcel, (x0, y0, x1, y1) in parcel_records:
        numeric = int(parcel["id"].split(":")[-1])
        if numeric % interval != 0:
            continue
        facility_no += 1
        items.append(
            spatial_object(
                f"RC:FACILITY:{facility_no:04d}",
                "facility",
                point((x0 + x1) / 2, (y0 + y1) / 2),
                seed,
                name=localized(f"公共设施 {facility_no}", f"Public Facility {facility_no}", f"公共施設 {facility_no}"),
                parent_id=parcel["id"],
                properties={"facility_type": ["school", "clinic", "community_service"][facility_no % 3]},
            )
        )

    return items


def build_planning(config: dict) -> list[dict]:
    seed = config["random_seed"]
    width = config["width_m"]
    height = config["height_m"]
    items: list[dict] = [
        {
            "id": "RC:PLAN:0001",
            "planning_object_type": "plan",
            "name": localized("参考城国土空间规划", "Reference City Territorial Spatial Plan", "リファレンスシティ国土空間計画"),
            "plan_id": None,
            "status": "EFFECTIVE",
            "version": 1,
            "valid_from": VALID_FROM,
            "valid_to": None,
            "target_ids": ["RC:CITY:001"],
            "constraint_code": None,
            "provenance": provenance(seed),
        },
        {
            "id": "RC:PLANVER:0001",
            "planning_object_type": "plan_version",
            "name": localized("基准版本 1", "Baseline Version 1", "基準バージョン 1"),
            "plan_id": "RC:PLAN:0001",
            "status": "EFFECTIVE",
            "version": 1,
            "valid_from": VALID_FROM,
            "valid_to": None,
            "target_ids": ["RC:CITY:001"],
            "constraint_code": None,
            "provenance": provenance(seed),
        },
    ]

    for parcel_no in range(1, config["parcel_columns"] * config["parcel_rows"] + 1):
        col = (parcel_no - 1) % config["parcel_columns"]
        row = (parcel_no - 1) // config["parcel_columns"]
        if col in (4, 5):
            use, far, height_max, density, green = "C2", 3.0, 80.0, 0.40, 0.25
        elif row in (0, config["parcel_rows"] - 1):
            use, far, height_max, density, green = "M1", 1.5, 36.0, 0.45, 0.20
        else:
            use, far, height_max, density, green = "R2", 2.0, 45.0, 0.30, 0.35
        items.append(
            {
                "id": f"RC:CONTROL:{parcel_no:04d}",
                "planning_object_type": "development_control",
                "plan_id": "RC:PLAN:0001",
                "status": "EFFECTIVE",
                "version": 1,
                "valid_from": VALID_FROM,
                "valid_to": None,
                "target_ids": [f"RC:PARCEL:{parcel_no:06d}"],
                "constraint_code": None,
                "controls": {
                    "planned_land_use": use,
                    "far_max": far,
                    "building_height_max_m": height_max,
                    "building_density_max": density,
                    "green_ratio_min": green,
                },
                "provenance": provenance(seed),
            }
        )

    boundaries_data = [
        ("RC:BOUNDARY:DEV001", "urban_development_boundary", polygon(width * 0.1, height * 0.1, width * 0.9, height * 0.9)),
        ("RC:BOUNDARY:ECO001", "ecological_constraint", polygon(0, 0, width * 0.12, height)),
        ("RC:BOUNDARY:FARM001", "farmland_constraint", polygon(width * 0.88, 0, width, height)),
    ]
    for boundary_id, code, geometry in boundaries_data:
        items.append(
            {
                "id": boundary_id,
                "planning_object_type": "controlled_boundary",
                "plan_id": "RC:PLAN:0001",
                "status": "EFFECTIVE",
                "version": 1,
                "valid_from": VALID_FROM,
                "valid_to": None,
                "target_ids": ["RC:CITY:001"],
                "boundary_geometry": geometry,
                "constraint_code": code,
                "provenance": provenance(seed),
            }
        )
    return items


def serialized(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_json(path: Path, data: object) -> str:
    payload = serialized(data)
    path.write_bytes(payload)
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def generate(config_path: Path, output_dir: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    spatial = build_spatial(config)
    planning = build_planning(config)

    spatial_hash = write_json(output_dir / "spatial-objects.json", spatial)
    planning_hash = write_json(output_dir / "planning-objects.json", planning)

    manifest = {
        "dataset_id": "RC:DATASET:COREV01",
        "title": localized("ReferenceCity 核心城市 v0.1", "ReferenceCity Core City v0.1", "ReferenceCity コア都市 v0.1"),
        "dataset_version": config["dataset_version"],
        "generated_at": "2030-01-01T00:00:00+08:00",
        "random_seed": config["random_seed"],
        "crs": {
            "kind": "SYNTHETIC_CARTESIAN",
            "identifier": config["crs_identifier"],
            "description": "Synthetic Cartesian plane in metres; no real-world geolocation",
        },
        "units": {"length": "m", "area": "m2", "ratio": "decimal"},
        "assets": [
            {"path": "spatial-objects.json", "hash": spatial_hash, "source_type": "SYNTHETIC", "sensitivity": "SYNTHETIC_SAFE", "source_ref": "generators/core_city.py"},
            {"path": "planning-objects.json", "hash": planning_hash, "source_type": "SYNTHETIC", "sensitivity": "SYNTHETIC_SAFE", "source_ref": "generators/core_city.py"},
        ],
    }
    write_json(output_dir / "manifest.json", manifest)
    return {"spatial": spatial, "planning": planning, "manifest": manifest}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic ReferenceCity core v0.1 data")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = generate(args.config, args.output)
    print(f"Generated {len(result['spatial'])} spatial objects and {len(result['planning'])} planning objects in {args.output}")


if __name__ == "__main__":
    main()
