"""Create/check a building asset job; does not generate images, geometry or approve QA."""
import argparse
import json
import math
import re
from pathlib import Path

GATES = ['structural', 'parameter', 'visual', 'material', 'performance', 'integration']

def require(condition, message):
    if not condition:
        raise ValueError(message)

def number(value, name, minimum=0, integer=False):
    require(type(value) in (int, float) and math.isfinite(value) and value > minimum,
            name + ' must be a finite number greater than ' + str(minimum))
    if integer:
        require(type(value) is int, name + ' must be an integer')

def validate_spec(s):
    require(isinstance(s, dict), 'spec must be an object')
    require(s.get('schemaVersion') == '1.0', 'schemaVersion must be 1.0')
    require(isinstance(s.get('id'), str) and re.fullmatch(r'[a-z][a-z0-9-]{2,79}', s['id']), 'id must be a safe lowercase asset ID')
    for field in ['name', 'use']:
        require(isinstance(s.get(field), str) and bool(s[field].strip()), field + ' is required')
    style = s.get('style', {})
    require(isinstance(style, dict) and bool(style.get('name')), 'style.name is required')
    require(isinstance(style.get('traits'), list) and len(style['traits']) >= 2 and all(isinstance(x, str) and x.strip() for x in style['traits']), 'describe at least two structural style traits')
    d = s.get('dimensions', {})
    for key in ['width', 'depth', 'floorHeight']:
        number(d.get(key), 'dimensions.' + key)
    number(d.get('floors'), 'dimensions.floors', integer=True)
    for field in ['massing', 'roof']:
        require(isinstance(s.get(field), dict) and bool(s[field].get('type')), field + '.type is required')
    if s['massing']['type'] == 'courtyard':
        for key, outer in [('courtyardWidth', 'width'), ('courtyardDepth', 'depth')]:
            number(s['massing'].get(key), 'massing.' + key)
            require(s['massing'][key] < d[outer], key + ' must fit inside the footprint')
    require(isinstance(s.get('facade'), dict) and bool(s['facade']), 'facade rules are required')
    materials = s.get('materials', [])
    require(isinstance(materials, list) and bool(materials), 'materials are required')
    require(all(isinstance(m, dict) and isinstance(m.get('id'), str) and m['id'] and m.get('role') for m in materials), 'every material needs id and role')
    require(len({m['id'] for m in materials}) == len(materials), 'material IDs must be unique')
    require(type(s.get('seed')) is int and 0 <= s['seed'] <= 2147483647, 'seed must be an integer from 0 through 2147483647')
    number(s.get('variants', 1), 'variants', integer=True)
    target = s.get('target', {})
    require(target.get('format') == 'glb' and target.get('units') == 'm', 'target must use GLB and metres')
    require(target.get('upAxis') == 'Y' and target.get('frontAxis') == '+Z', 'template convention is Y up, +Z front; convert explicitly for other engines')
    require(target.get('integration') in ['standalone', 'city'], 'integration must be standalone or city')
    for field in ['triangles', 'materialBatches', 'textureResolution']:
        number(s.get('budget', {}).get(field), 'budget.' + field, integer=True)
    return s

def init(spec_path, out):
    s = validate_spec(json.loads(spec_path.read_text()))
    require(not out.exists(), 'output already exists; edit the existing job deliberately or choose a new path')
    out.mkdir(parents=True)
    for name in ['references', 'models', 'previews', 'source']:
        (out / name).mkdir()
    (out / 'spec.json').write_text(json.dumps(s, ensure_ascii=False, indent=2) + '\n')
    d = s['dimensions']
    prompt = (f"Original {s['name']} ({s['use']}), {s['style']['name']}. Architectural modeling sheet: "
              f"the same design in front orthographic, side orthographic and three-quarter views. "
              f"{d['width']}m wide, {d['depth']}m deep, {d['floors']} floors at {d['floorHeight']}m floor height. "
              f"Massing: {json.dumps(s['massing'], ensure_ascii=False)}. Roof: {json.dumps(s['roof'], ensure_ascii=False)}. "
              f"Structural traits: {', '.join(s['style']['traits'])}. Facade: {json.dumps(s['facade'], ensure_ascii=False)}. "
              f"Materials: {json.dumps(s['materials'], ensure_ascii=False)}. Neutral studio background, "
              "readable lighting, consistent entrances, openings and structural bays. No labels, logos or city background. "
              f"Avoid: {', '.join(s['style'].get('avoid', []))}. Reconcile views against the dimensional spec.")
    (out / 'references/prompts.md').write_text('# Reference prompt draft\n\n' + prompt + '\n\nImage generation has not run. Register actual tool, prompt, file and inspection result after generation.\n')
    qa = {g: {'status': 'pending', 'reason': '', 'evidence': []} for g in GATES}
    if s['target']['integration'] == 'standalone':
        qa['integration'] = {'status': 'not-required', 'reason': 'Standalone asset requested', 'evidence': []}
    (out / 'qa.json').write_text(json.dumps(qa, indent=2) + '\n')
    (out / 'references/manifest.json').write_text('[]\n')
    return {'job': str(out.resolve()), 'specValid': True, 'modelsGenerated': False, 'qaPassed': False}

def check(job, require_ready=False):
    s = validate_spec(json.loads((job / 'spec.json').read_text()))
    qa = json.loads((job / 'qa.json').read_text())
    require(isinstance(qa, dict) and set(qa) == set(GATES), 'qa.json must contain exactly the six documented gates')
    for name, gate in qa.items():
        require(isinstance(gate, dict), name + ' gate must be an object')
        status = gate.get('status')
        require(status in ['pending', 'pass', 'fail', 'blocked', 'not-required'], name + ' has invalid status')
        require(isinstance(gate.get('evidence'), list), name + ' needs an evidence list')
        if status == 'not-required':
            require(name == 'integration' and s['target']['integration'] == 'standalone', 'only standalone integration may be not-required')
        if status in ['pass', 'fail', 'blocked', 'not-required']:
            require(isinstance(gate.get('reason'), str) and gate['reason'].strip(), name + ' needs an explanation')
        if status == 'pass':
            require(bool(gate['evidence']), name + ' pass requires actual evidence paths')
        for entry in gate['evidence']:
            require(isinstance(entry, str) and entry, 'evidence path must be a string')
            path = (job / entry).resolve()
            require(path.is_relative_to(job.resolve()), 'evidence must remain within this job')
            require(path.is_file() and path.stat().st_size > 0, 'missing or empty evidence: ' + entry)
    ready = all(g['status'] in ['pass', 'not-required'] for g in qa.values())
    if require_ready:
        require(ready, 'QA is incomplete; pending/blocked/failed gates cannot be promoted automatically')
    return {'specValid': True, 'recordedGatesComplete': ready, 'gateStatus': {k:v['status'] for k,v in qa.items()},
            'note': 'Checks records and file presence only; does not judge visual evidence, GLB geometry or measured performance.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('init'); create.add_argument('--spec', type=Path, required=True); create.add_argument('--out', type=Path, required=True)
    verify = sub.add_parser('check'); verify.add_argument('--job', type=Path, required=True); verify.add_argument('--require-ready', action='store_true')
    args = parser.parse_args()
    try:
        result = init(args.spec, args.out) if args.command == 'init' else check(args.job, args.require_ready)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as error:
        parser.exit(1, 'Asset job validation failed: ' + str(error) + '\n')

if __name__ == '__main__':
    main()
