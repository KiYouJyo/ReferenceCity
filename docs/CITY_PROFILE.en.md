# ReferenceCity Core City v0.1 — City Profile

> English mirror. 中文: `CITY_PROFILE.md` · 日本語: `CITY_PROFILE.ja.md`

ReferenceCity v0.1 is a fully synthetic, deterministically reproducible experimental city in the context of Chinese territorial spatial planning. Its Phase 1 purpose is to test trust-chain correctness: identity, versions, authority, approval, hashes, audit events, and spatial constraints.

## Spatial extent

- Synthetic extent: 20,000 m × 20,000 m;
- Area: 400 km²;
- CRS identifier: `RC-SYNTHETIC-1`;
- No real-world longitude, latitude, or administrative location is implied.

## Phase 1B baseline scale

The generated core contains 1 city, 3 districts, 6 town/subdistrict units, 60 parcels, 120 buildings, 18 grid road centerlines, 1 synthetic river centerline, 12 public facilities, 1 plan and baseline version, 60 parcel development controls, and 3 controlled boundaries.

## Why v0.1 is deliberately regular

The first city is intentionally simple and visually auditable. It answers whether the system behaves correctly, not whether it resembles a specific real Chinese city. Complex morphologies such as urban villages, work-unit compounds, gated high-rise estates and TOD districts are reserved for later research layers.

## Reproducibility

`data/core-v0.1/config.json` and `generators/core_city.py` are the generation sources. Identical code, configuration and seed must produce identical asset hashes. CI validates counts, Schema compliance and deterministic regeneration.
