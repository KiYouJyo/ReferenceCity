# ReferenceCity

> Synthetic Territorial Spatial Planning Benchmark City

[中文](README.md) | [English](README.en.md) | [日本語](README.ja.md)

ReferenceCity is the standardized synthetic experimental city of UrbanPlanningLab. It is not a replica of any real city and is not a substitute for empirical case studies. It provides a stable, controlled, reproducible environment with known Ground Truth for testing territorial-spatial-planning data models, algorithms, trust-chain mechanisms and research methods.

## Current task: Phase 1

**Phase 1 serves only the Territorial Spatial Trust Chain research track.**

The first target is a small, manually inspectable city with a complete planning lifecycle, supporting validation of:

- spatial-object registration and stable identifiers;
- plan outputs and version management;
- preparation, submission, approval, activation and amendment events;
- organizations, roles, permissions and multi-actor operations;
- data fingerprints/hashes and document integrity;
- abnormal scenarios such as unauthorized edits, document tampering and spatial conflicts;
- historical states and reproducible regression tests.

Phase 1 does not aim for photorealistic urban form or million-feature scale.

## More than a synthetic map

ReferenceCity consists of five linked data domains:

1. **Spatial State** — administrative units, roads, water, parcels, buildings and other spatial objects;
2. **Planning State** — planning units, land-use rules, control indicators, boundaries and constraints;
3. **Governance State** — organizations, roles, permissions, documents and approval relations;
4. **Event History** — chronological preparation, submission, approval, amendment, withdrawal and abnormal operations;
5. **Ground Truth** — predefined correct outcomes for each benchmark scenario.

A benchmark scenario must therefore describe not only *what exists where*, but also *who did what, when, under which rule, and what the correct result should be*.

## Initial Phase 1 scale

The first version should remain small and inspectable:

- 1 city;
- 3 district-level units;
- 6–10 subdistrict/town-level units;
- approximately 50–100 planning parcels;
- approximately 100–300 buildings, facilities and other spatial objects;
- 5–10 organizations/roles;
- 20–40 planning-lifecycle events;
- 10–20 normal and abnormal benchmark scenarios.

Large performance datasets will later be generated separately so the human-verifiable core city remains clean.

## Repository structure

```text
ReferenceCity/
├─ docs/
├─ schemas/
├─ data/
├─ scenarios/
├─ expected/
├─ generators/
├─ exports/
└─ tests/
```

## Relationship with UrbanPlanningLab

- [UrbanPlanningLab](https://github.com/KiYouJyo/UrbanPlanningLab) defines reusable research semantics, terminology and long-term infrastructure.
- ReferenceCity implements those shared conventions as one standardized synthetic city instance.
- ReferenceCity must not define the generic research model in reverse.
- Trust-chain core implementations must never hard-code ReferenceCity-specific exceptions.

## Long-term vision

After Phase 1 stabilizes, the city may progressively include work-unit compounds, gated high-rise compounds, small-block forms, traditional street fabrics, urban villages, TOD districts, new towns, industrial areas, urban-rural fringes and villages for housing morphology, urban renewal, TOD and urban-rural governance research.

These are compatibility goals only; trust-chain research remains the highest current priority.

## Documentation

- [Roadmap](docs/ROADMAP.en.md)
- [Data model](docs/DATA_MODEL.md)
- [Scenario specification](docs/SCENARIOS.md)
- [Data provenance and safety policy](docs/DATA_POLICY.md)
- [Multilingual policy](docs/I18N.md)
- [Changelog](CHANGELOG.md)

## Status

Infrastructure initialization. No real-world city dataset is currently declared part of ReferenceCity.
