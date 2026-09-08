"""Validate batch records; does not inspect geometry, render quality or runtime."""
import json,sys
from pathlib import Path

def check(b):
 assert isinstance(b.get('batchId'),str) and b['batchId'], 'batchId required'
 requested=b['requestedTypes'];assert requested and len(set(requested))==len(requested), 'requestedTypes must be unique'
 assets=b['assets'];ids=[a['id'] for a in assets];assert len(ids)==len(set(ids)), 'duplicate asset ID'
 by_id={a['id']:a for a in assets}
 assert set(requested)<=set(a['archetype'] for a in assets), 'missing requested archetype'
 for a in assets:
  assert a['archetype'] in requested, 'unrequested archetype'
  assert a.get('familyId') and a.get('specFile') and a.get('generatorVersion'), 'missing provenance'
  assert type(a.get('seed')) is int and a['seed']>=0, 'invalid seed'
  assert isinstance(a.get('parameters'),dict), 'parameters required'
  assert a.get('status') in ['pending','modeled','structurally-verified','approved','blocked'], 'invalid status'
  if a.get('parentId'):
   seen={a['id']};cursor=a
   while cursor.get('parentId'):
    parent=cursor['parentId'];assert parent in by_id and parent not in seen, 'invalid ancestry'
    seen.add(parent);cursor=by_id[parent]
   base=by_id[a['parentId']];assert base['archetype']==a['archetype'], 'variant archetype mismatch'
   fields=a.get('changedFields',[]);assert fields and len(fields)==len(set(fields)), 'variant changes required'
   for k in fields:assert k in a['parameters'] and a['parameters'][k]!=base['parameters'].get(k), 'unchanged declared field'
 for assembly in b.get('assemblies',[]):
  assert assembly['id'] not in by_id, 'assembly ID collision'
  assert assembly['members'], 'empty assembly'
  for m in assembly['members']:
   assert m['assetId'] in by_id, 'unknown assembly member'
   if 'rotation' in m:assert type(m['rotation']) in (int,float) and abs(m['rotation'])<1e9, 'invalid rotation'
   if 'scale' in m:assert len(m['scale'])==3 and all(type(n) in (int,float) and 0<n<1e9 for n in m['scale']), 'invalid scale'
   assert len(m['position'])==3 and all(type(n) in (int,float) and abs(n)<1e9 for n in m['position']), 'invalid position'
 return {'archetypes':len(requested),'assets':len(assets),'variants':sum(bool(a.get('parentId')) for a in assets),'assemblies':len(b.get('assemblies',[])),'note':'Record validity only; geometry and QA require separate evidence.'}
if __name__=='__main__':
 try:print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())),indent=2))
 except (AssertionError,KeyError,TypeError,ValueError) as e:sys.exit('Batch invalid: '+str(e))
