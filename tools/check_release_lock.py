from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))

from build_snapshot import build  # noqa: E402
from generators.core_city import DEFAULT_CONFIG  # noqa: E402

LOCK = ROOT / "data" / "core-v0.1" / "release-lock.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    expected = load(LOCK)
    with tempfile.TemporaryDirectory() as directory:
        actual = build(DEFAULT_CONFIG, Path(directory))
    if actual != expected:
        print("FAIL ReferenceCity core-v0.1 release lock mismatch")
        print("EXPECTED")
        print(json.dumps(expected, ensure_ascii=False, indent=2, sort_keys=True))
        print("ACTUAL")
        print(json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    print("PASS ReferenceCity core-v0.1 release lock")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
