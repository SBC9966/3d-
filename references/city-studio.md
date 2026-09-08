# Procedural City Studio adapter

Locate the actual project from the user's selected workspace or artifact; do not assume an absolute path. Read .project/PROJECT.md, STATUS.md, TASKS.md and DECISIONS.md and inspect the diff first. A .openai/hosting.json requires the available Sites workflow; preserve its identity. Asset work alone does not require a new site or audience change.

Current successful example files (inspect current contents before adapting):
- src/assets/pavilions.ts: named original café, greenhouse and pergola geometry.
- src/assets/batch-model.ts: static geometry merged by material while keeping bounds.
- scripts/assets/build-pavilions.ts: glTF Transform export, shared materials, embedded processed PBR maps, optimization, readback and thumbnails.
- scripts/assets/validate-model.ts: asset manifest/GLB checks.
- scripts/assets/preview-pavilions.py: CPU structural z-buffer preview; not GPU acceptance.
- src/engine/renderer/world-renderer.ts: model loading, instance placement, fallback prototypes.
- src/schemas/city.ts: PropSchema, BuildingSchema and serialized CityProject.
- src/editor/tools/actions.ts: placement/spacing checks, command history, preservation across furniture refresh.
- src/ui/App.tsx: asset browser, selection of prop type, actual download/reference links.
- scripts/export/city-glb.ts: offline whole-city geometry export; fidelity differs from standalone GLB.

Use these as proven examples, not universal generators. A new architectural family deserves its own generator/rules. Extending only the asset browser creates a fake feature: update schema, loader, fallback, geometry batching, placement footprint, persistence/export and manifests together. For many new types, prefer a validated asset registry over proliferating hardcoded enum/list copies, but do not restructure the whole editor unless needed.

Regeneration hazards: build-manifest.ts originally rebuilds the base registry; inspect it before running and preserve all unrelated/new entries. Do not assume earlier scripts are safe appenders. Model IDs should survive parcel/furniture refresh. Check whether new textured prototypes are parsable in Node's offline exporter; keep the standalone export authoritative for full PBR fidelity if the existing offline exporter only approximates it.

npm run verify currently includes TypeScript, lint, tests, build and asset smoke. New assets should add meaningful tests for geometry/batching/serialization rather than tests that merely mirror strings. Inspect in a real supported browser and save actual screenshots for visual features. Existing cloud WebGL-blocked evidence is a session-specific limitation, not a reason to skip testing on a later GPU-capable environment.

The 2026-09-06 pavilion batch produced 6,312 / 11,930 / 5,100 triangles and at most seven material batches per runtime prototype. These are example budgets, not measured FPS or a requirement for future buildings. The user liked those models; preserve their editable construction and reference-driven method while allowing different architectural styles.
