from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from canonical_json import canonical_sha256
content=json.loads((ROOT/'data/governance-v0.1/documents/plan-v1-submission.json').read_text(encoding='utf-8'))
entities=json.loads((ROOT/'data/governance-v0.1/documents-and-approvals.json').read_text(encoding='utf-8'))
doc=next(x for x in entities if x['id']=='RC:DOC:000001')
actual=canonical_sha256(content)
assert actual==doc['content_hash'],(actual,doc['content_hash'])
print('PASS planning document canonical hash',actual)
