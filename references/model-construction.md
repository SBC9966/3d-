# Model construction contract

Keep BuildingAssetSpec as JSON. Link it to stable asset IDs and seed. Renderer objects and Three UUIDs belong only in implementation. Determine the valid ranges for this typology; fit repeated bays inside available length, preserve minimum opening/column dimensions, reject impossible combinations.

Build in this order because errors propagate from larger to smaller features:
1. Ground/pivot, footprint, massing and floor/roof heights.
2. Roof shape and connections; check front/side silhouette.
3. Structural columns, beams, slabs, wall panels and actual openings.
4. Facade modules, balconies, entrances, parapets and visible interior.
5. Roof equipment and grounded contextual components.
6. Material/UV detail and edge refinement for the intended camera distance.

Model tiers are configurable. A small civic prop may fit 5k–20k triangles; a reusable apartment or landmark needs a different budget. Do not turn these examples into universal limits. Use spec.budget for the current task and report exceptions; tune LOD only where there is measured benefit.

Use meaningful named components, e.g. roof-main, column-*, opening-*, slab-floor-*, balcony-*, door-*, planter-*. Export component geometry without losing normal transforms. Triangular/custom surfaces need normals, winding and UVs when textured. Avoid nonuniform normal errors and negative/zero dimensions. Combine reusable geometry/materials without stripping standalone editability.

Use instanced modules or facade shaders/atlases for repeated windows in city-scale buildings. Keep one scene object per window out of the runtime. Static named GLB components can be merged by material on loading, then instanced by placement; GLB editing and runtime performance are separate representations. Transparency sorting may require separate glass groups and cannot be approved from geometry counts.

Use processed PBR sources with provenance. glTF metallic-roughness uses G=roughness, B=metallic. Base color is sRGB; normals/roughness/metallic/AO are data textures. State generated/derived maps are approximations. Preserve metre-based texture scale: mapping a 20m wall and a 0.1m slat to the same full texture will visibly stretch detail. Use UV adjustment or module-local mapping and inspect it.

Source families should expose parameters rather than copy multiple entire generators. Compare two seeds and boundary floor counts. Preserve doors, stairs, roof closure and positive component dimensions after changes. New shapes are allowed to need additional authoring; the workflow provides repeatability, not an unconditional any-style modeling guarantee.

## Constructing L1/L2/L3 from one family

For progressive assets, expose explicit level-aware modules instead of duplicating the whole generator. Useful controls include `detailLevel`, `facadeProfile`, `interiorMode`, `furnitureDensity`, `roofEquipment`, `propSet`, `materialSet`, and `motionSet`. Keep the parent geometry path shared until a declared architectural delta requires a branch.

L1 should solve massing, structure, roof, major openings and basic material separation. L2 should add real facade depth and street-visible content. L3 should add close-camera geometry, visible interior/furniture, richer processed PBR/UV treatment, secondary props and optional movable parts. Use the exact progression contract for acceptance; do not infer that a higher triangle count alone means higher quality.
