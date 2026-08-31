from __future__ import annotations
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
from canonical_json import canonical_sha256
SCHEMA=ROOT/'schemas/v0.1'; BASE=ROOT/'scenarios/v0.1'; EXPECTED=ROOT/'expected/v0.1'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
schemas={p.name:load(p) for p in SCHEMA.glob('*.schema.json')}; reg=Registry()
for s in schemas.values(): reg=reg.with_resource(s['$id'],Resource.from_contents(s))
sv=Draft202012Validator(schemas['scenario.schema.json'],registry=reg,format_checker=FormatChecker()); rv=Draft202012Validator(schemas['operation-request.schema.json'],registry=reg,format_checker=FormatChecker()); ev=Draft202012Validator(schemas['expected-result.schema.json'],registry=reg,format_checker=FormatChecker())
folders=sorted(p for p in BASE.glob('S*') if p.is_dir()); assert [p.name for p in folders]==[f'S{i:03d}' for i in range(1,11)]
for folder in folders:
    s=load(folder/'scenario.json'); assert not list(sv.iter_errors(s)),folder.name
    epath=ROOT/s['expected_result_ref']; e=load(epath); assert not list(ev.iter_errors(e)),folder.name; assert e['scenario_id']==s['scenario_id']
    steps=[a['step'] for a in s['actions']]; assert steps==list(range(1,len(steps)+1))
    for a in s['actions']:
        req=load(ROOT/a['request_ref']); assert not list(rv.iter_errors(req)),a['request_ref']; assert req['actor_id']==a['actor_id']; assert req['operation']==a['operation']; assert req['target_id']==a['target_id']; assert req['occurred_at']==a['occurred_at']; assert canonical_sha256(req['payload'])==req['payload_hash'],a['request_ref']
assert len(load(BASE/'S003/scenario.json')['actions'])==3
assert load(EXPECTED/'S004.json')['authorized'] is False
assert load(EXPECTED/'S005.json')['expected_hash_match'] is False
assert load(EXPECTED/'S006.json')['expected_spatial_conflicts']
assert load(EXPECTED/'S007.json')['expected_spatial_conflicts']
assert load(EXPECTED/'S008.json')['expected_error_code']=='MISSING_SIGNATURE'
assert load(EXPECTED/'S010.json')['expected_error_code']=='VERSION_CONFLICT'
print('PASS S001-S010 scenario/request/ground-truth contracts')
