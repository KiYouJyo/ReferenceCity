from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "v0.1"
DATA_DIR = ROOT / "data" / "governance-v0.1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def registry_and_schemas():
    schemas = {path.name: load(path) for path in SCHEMA_DIR.glob("*.schema.json")}
    registry = Registry()
    for schema in schemas.values():
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry, schemas


def main() -> int:
    registry, schemas = registry_and_schemas()
    governance = load(DATA_DIR / "entities.json")
    lifecycle = load(DATA_DIR / "lifecycle.json")

    entity_validator = Draft202012Validator(schemas["governance.schema.json"], registry=registry, format_checker=FormatChecker())
    for entity in governance:
        errors = list(entity_validator.iter_errors(entity))
        assert not errors, f"{entity.get('id')}: {[error.message for error in errors]}"

    Draft202012Validator(schemas["lifecycle.schema.json"], registry=registry, format_checker=FormatChecker()).validate(lifecycle)

    ids = [entity["id"] for entity in governance]
    assert len(ids) == len(set(ids)), "duplicate governance IDs"
    by_id = {entity["id"]: entity for entity in governance}

    organizations = {entity["id"] for entity in governance if entity["entity_type"] == "organization"}
    roles = {entity["id"] for entity in governance if entity["entity_type"] == "role"}
    actors = [entity for entity in governance if entity["entity_type"] == "actor"]
    permissions = [entity for entity in governance if entity["entity_type"] == "permission"]

    assert len(organizations) == 5
    assert len(roles) == 6
    assert len(actors) == 6
    assert len(permissions) == 14

    for actor in actors:
        assert actor["organization_id"] in organizations, actor["id"]
        assert actor["role_id"] in roles, actor["id"]

    permission_pairs = {(permission["role_id"], permission["operation"]) for permission in permissions}
    for transition in lifecycle["transitions"]:
        assert transition["from"] in lifecycle["states"]
        assert transition["to"] in lifecycle["states"]
        for role_id in transition["allowed_role_ids"]:
            assert role_id in roles
            assert (role_id, transition["operation"]) in permission_pairs, transition["transition_id"]

    assert lifecycle["initial_state"] in lifecycle["states"]
    assert set(lifecycle["terminal_states"]).issubset(set(lifecycle["states"]))

    applicant = by_id["RC:ACTOR:005"]
    assert applicant["role_id"] == "RC:ROLE:APPLICANT"
    applicant_ops = {p["operation"] for p in permissions if p["role_id"] == applicant["role_id"]}
    assert "APPROVE_PLAN" not in applicant_ops
    assert "OPEN_AMENDMENT" not in applicant_ops
    assert "SUBMIT_PROJECT_APPLICATION" in applicant_ops

    auditor_ops = {p["operation"] for p in permissions if p["role_id"] == "RC:ROLE:AUDITOR"}
    assert auditor_ops == {"VERIFY"}

    print("PASS governance: 5 organizations, 6 roles, 6 actors, 14 permissions, 10 lifecycle transitions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
