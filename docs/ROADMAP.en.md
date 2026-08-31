# ReferenceCity Roadmap

> English mirror of the Chinese source `ROADMAP.md`.

## Phase 1 — Benchmark city for Territorial Spatial Trust Chain research

### Phase 1A: documentation, schemas and minimum skeleton

Goal: define ReferenceCity consistently for both researchers and machines before drawing a large city.

- [x] Trilingual project overview.
- [x] Repository boundary with UrbanPlanningLab.
- [x] Core data domains and benchmark-scenario concept.
- [ ] Spatial / Planning / Governance / Event / Ground Truth Schema v0.1.
- [ ] Stable identifier rules.
- [ ] CRS, unit, date-time and version conventions.
- [ ] Provenance and sensitivity manifest.

### Phase 1B: inspectable core city v0.1

Build one small city that can be checked object by object: 1 city, 3 district-level units, 6–10 lower-level units, 50–100 parcels, 100–300 buildings/facilities/features, basic roads and waterways, plus internally consistent current-land-use and planning-control layers.

All objects require stable IDs. Geometry must be inspectable. The city must not reproduce precise coordinates or sensitive data from a real city. Generation parameters, manual edits and random seeds must be traceable.

### Phase 1C: planning-governance model v0.1

Create planning-preparation bodies, approval authorities, municipal/district roles, applicant actors, a permission matrix, Plan / PlanVersion / PlanningDocument / Approval objects and a lifecycle state machine.

Initial lifecycle:

```text
Draft → Submitted → Reviewed → Approved → Effective
                                      ↓
                                  Amendment
                                      ↓
                               New Effective Version
```

### Phase 1D: benchmark scenarios v0.1

At minimum: normal registration, legal version update, normal approval, unauthorized modification, tampered approved document, land-use conflict, controlled-boundary crossing, missing approval actor/signature, historical-version verification, and conflicting updates.

Every scenario must contain both machine-readable input and expected output.

### Phase 1E: trust-chain integration and regression

- Provide implementation-independent test inputs.
- Compare chain outputs with Ground Truth.
- Freeze a ReferenceCity v1.0 benchmark.
- Re-run the same benchmark against later trust-chain versions.
- Keep correctness tests separate from performance tests.

### Phase 1 completion criteria

Release ReferenceCity v1.0 when schemas are stable, the core city can be exported/imported, at least 10 standard scenarios have machine-readable Ground Truth, the lifecycle executes end-to-end through the trust chain, core scenarios are deterministic, and the data manifest contains no unknown provenance or sensitivity status.

## Phase 2 — Real public-data compatibility

Add public-data import and mapping fixtures to test compatibility with real GIS data without contaminating the synthetic core Ground Truth.

## Phase 3 — Planning-research morphology extensions

Reserve archetypes for traditional street fabrics, work-unit compounds, gated high-rise housing, open small-block neighborhoods, urban villages, industrial districts, TOD districts, new towns, urban-rural fringes and villages.

## Phase 4 — Research experimental environment

Support controlled experiments, urban-renewal state transitions, housing-morphology indicators and China-Japan comparative studies. New archetypes must not encode predetermined research conclusions into the generation rules.

## Phase 5 — Scale / Stress Benchmarks

Generate separate 10K, 100K, 1M and larger datasets for performance, scalability and distributed-processing experiments. Stress data is not part of the human-verifiable ReferenceCity core.
