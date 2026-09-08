# Reference to Building

A reusable ChatGPT/Codex Skill for turning architectural briefs or reference images into reproducible, parameterized 3D building assets.

The workflow is designed around evidence rather than concept-only output:

`brief/reference -> BuildingAssetSpec -> modeling references -> editable geometry -> PBR materials -> GLB export -> render QA`

## Highlights

- Reference-to-model workflow for buildings and civic props.
- Stable `BuildingAssetSpec` contract with meter-based dimensions and explicit axes.
- Batch and controlled-variant validation.
- L1/L2/L3 progression for the same building identity.
- Progression checks that reject fake upgrades such as seed-only, color-only, texture-only, global-scale-only, or subdivision-only changes.
- Named GLB parts, material/UV guidance, and structural/visual/material/performance QA gates.
- City Studio integration guidance when a compatible project is in scope.
- Blender or other modeling backends may be used when available and justified by geometry complexity; procedural geometry remains valid for repeated architectural systems.

## L1 / L2 / L3 progression

A progression is ancestry, not three random variants.

- **L1 Base**: correct massing, roof, openings, structural rhythm, basic game-ready materials.
- **L2 Developed**: visible architectural depth plus usable interior/content, furniture, facade modules, and richer materials.
- **L3 Hero**: hero-level facade/interior detail, denser furniture and props, refined PBR/UV work, roof equipment, and optional movable/data-driven parts.

By default each child level must change at least four independent groups and include both an architectural change and a detail/content change.

Validate a progression plan:

```bash
python3 scripts/progression_check.py progression.json --mode plan
```

Validate recorded delivery evidence:

```bash
python3 scripts/progression_check.py progression.json --mode delivery --root <job-root>
```

## Main files

- `SKILL.md` - workflow and routing rules.
- `references/level-progression.md` - L1/L2/L3 progression contract.
- `references/model-construction.md` - geometry and material construction rules.
- `references/quality-gates.md` - delivery evidence requirements.
- `references/batches-and-variants.md` - batch and variant behavior.
- `scripts/asset_job.py` - asset job validation scaffold.
- `scripts/batch_check.py` - batch record validation.
- `scripts/progression_check.py` - progression anti-fake-upgrade checks.
- `assets/building-spec.example.json` - example building specification.
- `assets/progression.example.json` - example level progression.
- `dist/skill.zip` - packaged Skill for installation/distribution.

## Quick use

Example request:

> Build a warm-brick corner cafe for a Three.js city game. Produce L1, L2 and L3 versions of the same building. L2 must add visible massing/facade/interior/furniture improvements. L3 must inherit L2 and become a hero asset with richer roof, facade, interior, PBR/UV and optional movable parts. Create and validate progression.json before modeling, then export GLBs and matched-camera previews for all levels.

## Notes

This Skill defines a reproducible modeling workflow and validation contract. It does not claim that a modeling backend, GPU renderer, Blender installation, or browser runtime is available in every execution environment. Blocked QA gates must be reported rather than silently passed.
