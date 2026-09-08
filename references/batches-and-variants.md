# Batch and controlled variants

A batch has four distinct counts: requested archetypes, structural variants, assemblies and exported files. Report each; do not count color swaps, duplicates or the assembly as additional requested archetypes.

## Plan the actual work

Create batch.json with batchId, requestedTypes, assets and assemblies. Each asset has id, archetype, familyId, specFile, generatorVersion, seed, parameters and status. A variant additionally has parentId and changedFields (parameter keys). Status is pending, modeled, structurally-verified, approved or blocked. Assembly members reference asset IDs plus transforms. Run batch_check.py before committing to the batch.

Group by construction grammar, not just use or color: repeated-floor slabs, large-span halls, shelters, sports surfaces. Reuse materials and compatible modules. A sawtooth studio and lecture hall need their own roof/section logic. Complete a representative shape before expanding its family. Schedule bounded export batches; record each result immediately and resume by stable ID rather than rerunning successful expensive work.

## Reference isolation

Build each prompt from styleLock + exactly one subjectBrief + that subject's views. Never append a conditional instruction naming another asset to every prompt. For a shop, explicitly require only the shop; for a running track, include its top view. Do not give each generation tool the whole unrelated asset roster.

Inspect subject, view consistency, counts, silhouette and unwanted objects. An unrelated background object may be excluded with an explicit note if the requested asset is unambiguous. If the wrong subject or an unusable main view is generated, retry that failed item once with a reduced isolated prompt; retain both provenance records, explain any remaining blocker and model from explicit rules only if useful. Do not repeatedly draw the whole batch.

## Variants and upgrades

Distinguish parameter variant (same grammar), style variant (new facade/roof/material rules), detail upgrade (same identity with revision), and new archetype (new grammar). Preserve approved originals. A parameter-only variant can reuse references; a new silhouette/style needs targeted reference work.

Record parentId, generatorVersion, base parameters, overrides and changedFields. State implemented ranges. Changing floors regenerates slabs/windows/stairs/roof; changing bays adjusts frontage; terraces alter the relevant upper mass and roof. Reject unsupported overrides rather than silently ignoring them. Seed is not a substitute for an explicit variant design; don't label ignored seed changes as diversity.

Check equal input yields equal geometry signatures; declared structural variants differ in geometry. Check range boundaries, doorway clearance, supports, roof closure, embedded materials and finite bounds individually. A passing parent never automatically passes its children.

## Assembly and delivery

Compute transformed footprint clearance, ground contact and access paths. Keep member transforms serialized. Validate large grounds/fields against placement bounds; never fit an oversized campus by silently scaling buildings. Assemblies do not automatically become editor-placeable assets.

Export each asset plus optional assembly, reproducible source/specs, prompts and reference files, per-asset QA, report and checksums. Approved requires actual visual/material/runtime evidence; structurally-verified and blocked remain useful delivery states. GLB can retain editable named parts; runtime loads merge by compatible material. Texture presence, mesh counts and CPU previews are not proof of GPU quality.

## Level chains are stricter than variants

A level chain is a detail-upgrade ancestry, not merely another variant family. When the requested output is L1/L2/L3 or otherwise progressive, create `progression.json` and use `scripts/progression_check.py` in addition to `batch_check.py`. The progression record must explain what the child adds in independent architectural and detail/content groups. A parameter variant may remain simple; a level upgrade may not.

Do not count the same change twice under different names. For example, a taller building plus stretched windows is still one massing change if the windows were only stretched as a side effect. If a child is supposed to add furniture, material fidelity or movable parts, record and verify those changes explicitly.
