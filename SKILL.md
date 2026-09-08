---
name: reference-to-building
description: Generate architectural reference views and turn building briefs or reference images into original, parameterized 3D buildings, houses and civic props with PBR materials, editable source, GLB exports and city-editor integration. Use for reference-to-model workflows, new architectural styles, controlled families of building variants, and level-based upgrade chains such as L1/L2/L3 where the same building gains real massing, facade, interior, furniture, material and functional detail; not for image-only requests or unrelated website design.
---

# Reference to Building — 参考图建筑工坊

Deliver a reproducible asset, not just an attractive concept. Preserve the user's requested architecture and existing project. Use the successful café / greenhouse / pergola method: reference views → explicit structural rules → named geometry → processed PBR → GLB → render batches → actual QA.

## 1. Resolve the brief and destination

Inspect the selected project's instructions, art direction, asset manifest and existing export code. Preserve its established stack. If no project is selected, produce a standalone asset package without silently creating or deploying a website.

Translate natural language into `BuildingAssetSpec`; use [the example](assets/building-spec.example.json) and the validation contract in `scripts/asset_job.py`. Infer routine dimensions and material choices, record assumptions, and ask only if conflicting goals materially change the result. Do not force coastal modern style on every future request.

Choose the scope: a single asset, a parameterized family, or an edit of an existing asset. A new style requires new structural/facade/roof rules when needed. A specification scaffold alone is never a finished model or an automatic text-to-3D service.

Create a job without overwriting existing work:

```sh
python3 <skill>/scripts/asset_job.py init --spec <spec.json> --out <new-job-directory>
```

## Batch and variant routing

For multiple requested models or variant upgrades, read [batch and variant contract](references/batches-and-variants.md). Inventory distinct archetypes separately from variants and assemblies. Use `scripts/batch_check.py batch.json` to validate coverage, variant ancestry, unique IDs and explicit parameter changes before generation and again before delivery. It validates records, not models. Preserve existing assets; resume unfinished items without regenerating accepted references.

## Level progression routing

When the user asks for L1/L2/L3, base/developed/hero, an upgraded version of the same model, or progressively richer building detail, read [level progression contract](references/level-progression.md). Treat this as ancestry, not as three random variants. Create `progression.json` from [the example](assets/progression.example.json), lock the building identity, and declare explicit upgrade deltas before modeling.

Run `scripts/progression_check.py progression.json --mode plan` before generation. By default, each child level must change at least four independent groups, include at least one architectural change and one detail/content change, and remain visibly recognizable as the same building. Do not use global scaling, seed changes, color swaps, texture-only replacement, or extra subdivisions as the upgrade by themselves.

Build the levels from one modular family generator whenever practical. L1 establishes the correct game-ready shell; L2 adds street-level architectural depth and usable interior/content; L3 adds hero-level facade, interior/furniture, PBR/UV, roof/prop detail and optional movable or data-driven parts when useful. Preserve the accepted parent and create a child ID for each level.

## 2. Generate and lock useful references

For new appearance requests, call the available image generation tool directly, applying its skill when available. Generate one consistent front/side/three-quarter reference sheet per distinct archetype; reuse the approved parent reference for parameter-only variants; add rear/top/details only where modeling ambiguity warrants them. Use [reference and style rules](references/style-and-reference.md). If the user provides adequate references, reuse them; do not generate unnecessary alternatives. If image generation is unavailable, state the limit and continue useful modeling from supplied references or an explicit written design if possible; do not claim generated references exist.

Inspect each output before approving it. Ensure the named subject is present and exclude unrelated campus objects. Do not include conditional references to other asset types in a shared prompt (e.g. athletics instructions in a dormitory prompt). Keep the positive subject and view instructions asset-specific; put only style constraints in the shared prefix. Extract silhouette, opening positions, load-bearing rhythm, roof topology and material separation. Reconcile inconsistent views against the dimensional spec. Register exact prompts, tool, files and purpose. Approve reference direction using reasonable judgment unless the user requests a review checkpoint. Reference approval is distinct from model/visual approval.

## 3. Build the model as an editable system

Read [model construction](references/model-construction.md). Use metre units, explicit up/front axes, a ground pivot, named parts and shared materials. Build the interior/openings visible to the intended camera; avoid a closed cube behind a supposedly open window. Keep seed and parameters separate from renderer objects.

Choose procedural Three.js geometry for repeated architectural components; use Blender or another available modeling tool when curved/custom forms justify it. Do not promise any style can be produced by the three existing pavilion generators. Implement/adapt a generator for the requested grammar; keep code and spec with the asset.

For a family, first complete a representative asset, then vary valid parameters with a deterministic seed. Rebuild bays, floors, roofs and stairs from parameters; do not use global scaleY as floor editing. Reuse compatible structure, not unrelated silhouettes.

For a level chain, inherit the parent generator and add explicit modules or parameter changes for the declared deltas. If massing changes, regenerate dependent slabs, openings, stairs, facade modules and roof edges instead of stretching the old mesh. Higher detail must be visible at the intended camera distance; hidden subdivisions do not count as an upgrade.

## 4. Materials, export and integration

Use processed texture sources, not full reference images as material maps. Preserve UV scale, color space, normal convention, roughness and metallic response. Keep editor GLB components named; batch/instance separately for runtime. Read [quality and export gates](references/quality-gates.md).

Export GLB with embedded or correctly resolved textures, inspect readback and bounds, create thumbnails from actual geometry, and upsert stable manifest IDs without deleting unrelated entries. Integrate with a city's existing placement/persistence/renderer path only when requested or already in scope. For Procedural City Studio specifically, read [its adapter](references/city-studio.md); do not assume that checkout exists in another session.

## 5. Verify, correct, deliver

Run structural and deterministic checks, then inspect the actual model in a supported 3D renderer from at least front, side and street/aerial distances. Compare against reference rules; correct silhouette, scale, openings and major proportions before optional microdetail. Inspect glass, shadows and materials under the required lighting presets. Measure runtime rather than guessing FPS.

If GPU/browser QA is unavailable, deliver useful structurally verified assets with the blocked gates recorded; a CPU structural preview is allowed only with a clear label. Never substitute AI imagery for model evidence or call blocked visual gates passed.

Validate the job record:

```sh
python3 <skill>/scripts/asset_job.py check --job <job-directory>
```

For an upgrade chain, also record actual per-level metrics and matched-camera model previews in `progression.json`, then validate:

```sh
python3 <skill>/scripts/progression_check.py progression.json --mode delivery --root <job-root>
```

A passing progression record is not visual approval. Compare parent and child renders from matched cameras and reject any L2/L3 whose added value is not clearly visible or whose identity drifts into a different archetype.

Return the asset(s), source/spec, reference provenance, actual model preview and concise limits. Follow the environment's artifact persistence mechanism. Creating an asset does not authorize publishing a website or changing access. Update project status/tasks when working in an existing managed project.
