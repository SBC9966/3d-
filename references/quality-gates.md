# Evidence and quality gates

Track each gate as pending / pass / fail / blocked with a short reason and artifact paths. A script can validate files, not decide visual quality. Never derive “pass” merely from existence of a screenshot or from user praise of a different asset.

| Gate | Required evidence |
|---|---|
| structural | GLB parses; finite positions/normals/indices; valid index ranges; positive bounds; metre scale; named components; expected embedded textures; no unintended missing files |
| parameter | same spec/seed reproduces parameters/geometry; tested allowed ranges preserve openings, roof and positive sizes; family variants differ intentionally |
| visual | actual rendered front/side/three-quarter views; reference comparison of silhouette, scale, openings, repetition and grounded details |
| material | normal direction, UV scale, roughness/reflection, glass/alpha and shadow check; use project's lighting presets, including morning/noon/sunset/night in City Studio |
| performance | actual draw calls/frame time at relevant placement count and camera distance; include renderer/device; CPU mesh count is not GPU draw calls |
| integration | if requested: loader succeeds, correct footprint/pivot, placement/picking where supported, save/reload and undo, model ID survives edits |

Before exporting final assets, correct clear structural and dominant visual defects. Do not endlessly regenerate new references in place of fixing geometry. If the renderer is blocked, complete export/readback and label visual/material/performance blocked; retain a concrete next check. CPU rasterization must use depth handling rather than triangle-centroid painter sorting where intersecting surfaces would give false defects.

Deliver: GLB, authoritative spec, editable generator/source, reference prompts/files, manifest, geometry-derived thumbnail, validation report and actual preview where available. Include the tools/dependencies needed to rebuild. Never label an AI concept rendering “model preview”. Never inflate KTX2/Draco/WebGPU claims when absent.

For changes to existing assets, preserve old stable IDs where editing the same asset, create distinct IDs for requested siblings, and keep old files until new ones validate. Update manifest records by ID, do not replace the whole registry with only the current batch. Removing old/generated furniture must not erase user-placed assets.

## Progression evidence

For L1/L2/L3 work, the parameter and visual gates must include parent/child evidence. Run `progression_check.py` before approval. Record geometry signatures, triangle counts, named-part counts, material/texture metrics, furniture or animatable-part counts when declared, and at least three actual model-render preview paths per level. Compare matched cameras so the new massing, facade depth, interior/furniture and material detail are visible rather than inferred from metadata.

If a declared upgrade is not visible at the intended camera distance, mark the child fail or revise it even when the progression record is structurally valid.
