from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from canonical_json import canonical_sha256  # noqa: E402

DOCUMENT = ROOT / "data" / "governance-v0.1" / "documents" / "plan-v1-submission.json"


def main() -> int:
    content = json.loads(DOCUMENT.read_text(encoding="utf-8"))
    print(f"RC:DOC:000001 canonical_sha256={canonical_sha256(content)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
