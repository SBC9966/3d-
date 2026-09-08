# Level progression contract

Use this contract when the user asks for an upgrade chain such as L1/L2/L3, base/developed/hero, a more refined version of the same building, or a family whose members visibly evolve in quality.

The goal is not to create several loosely related variants. The goal is to preserve one building identity while each child level introduces a deliberate, inspectable increase in architectural resolution, usable content, material fidelity, or functional behavior.

## 1. Treat levels as ancestry, not random variants

Create `progression.json` from `assets/progression.example.json` before modeling. Every level after L1 must point to the immediately previous level with `parentId`. Keep a stable `familyId` and an `identityLock` describing the cues that make the building recognizably the same design.

Identity locks should usually preserve items such as the entrance side, roof direction, dominant facade rhythm, primary material family, courtyard/opening logic, and signature silhouette. A higher level may expand or articulate the mass, but it must not silently become a different archetype.

Do not use seed changes, global scale, a color swap, texture replacement, or denser subdivisions as a level upgrade by itself.

## 2. Plan explicit upgrade deltas

Use the following delta groups. Only declare groups that will produce real source/model changes:

- `massing`: floors, bays, wings, setbacks, terraces, podium/crown, height or footprint composition.
- `structure`: columns, beams, slabs, braces, trusses, stairs, structural depth.
- `facade`: recesses, frames, louvers, balconies, canopies, cornices, mullions, facade layering.
- `roof`: eaves, parapets, dormers, skylights, roof equipment, junction refinement.
- `openings`: doors, windows, shopfronts, loading/service openings, reveal depth and frames.
- `interior`: visible rooms, counters, partitions, stairs, ceilings, service zones.
- `furniture`: tables, chairs, shelving, desks, fixtures, display units and other placed interior assets.
- `materials`: additional material separation, processed PBR maps, improved UV scale, higher justified texture resolution, trim/material variation.
- `props`: signage hardware, lighting fixtures, railings, planters, gutters, vents, utility details.
- `animation`: named pivots or separate movable parts such as doors, shutters, fans, elevators, gates or data-driven display surfaces.
- `landscape`: attached planters, decks, steps, ramps, retaining edges or other building-owned ground detail.
- `performance`: LOD, instancing, atlas/batching, collision simplification or runtime representation changes.

By default, every child level must change at least four independent groups, including at least one architecture group (`massing`, `structure`, `facade`, `roof`, `openings`) and at least one detail/content group (`interior`, `furniture`, `materials`, `props`, `animation`, `landscape`). Adjust the threshold only when the user's asset is too small for that rule to make sense.

## 3. Default three-level ladder

Use this ladder unless the user specifies a different progression.

### L1 - Base / game-ready shell

Establish the correct silhouette, footprint, roof, major openings, structural rhythm, primary entrance and basic material separation. Include only the visible interior needed to prevent fake closed windows. Keep components editable and named.

### L2 - Developed / street-detail asset

Preserve L1 identity and add meaningful facade depth plus usable content. Typical upgrades include one massing or roof articulation, richer entrance/facade modules, visible interior zoning, a first furniture set, secondary props, improved material separation and better UV/PBR treatment. Do not merely increase polygon density.

### L3 - Hero / close-camera asset

Preserve the same design while adding hero-level articulation. Typical upgrades include a refined upper mass or terrace/crown, detailed openings and trims, complete visible public interior zones, denser furniture/fixtures, roof/mechanical details, richer processed PBR sets, edge refinement, and optional movable/data-driven parts. L3 should survive close street views without exposing placeholder geometry.

For a landmark or cinematic asset, add L4 only if the use case justifies it. Do not manufacture extra levels to satisfy a count.

## 4. Build levels from one modular generator

Prefer one family generator with additive modules or parameterized stages over copied generators. A useful pattern is:

1. Build core massing and structure shared by all levels.
2. Apply level-specific massing/roof modules.
3. Add facade/opening modules appropriate to the level.
4. Add visible interior and furniture modules.
5. Add material/UV and prop modules.
6. Add optional movable/runtime modules.

Keep level logic explicit, for example `detailLevel`, `interiorMode`, `furnitureDensity`, `facadeProfile`, `roofEquipment`, and `motionSet`. Avoid a single `scale` or `detailMultiplier` that hides what actually changes.

If a higher level changes floors, bays or a wing, regenerate dependent slabs, openings, stairs, roof edges and facade modules from parameters. Never stretch the parent mesh to imitate new construction.

## 5. Reference strategy for upgrade chains

Lock the base design first. Parent geometry and its approved renders are the source of truth for identity. For L2/L3, generate only references needed to clarify new design decisions.

When image generation is useful, prefer either:

- an aligned same-building evolution sheet showing L1/L2/L3 from the same three-quarter camera, or
- targeted detail sheets for the facade, entrance, interior, roof or materials being added.

Do not generate three unrelated buildings and call them levels. If generated images drift from the locked parent, keep the parent identity and use only the relevant local detail ideas.

## 6. Budget progression

A higher level should spend more geometry/texture budget only where the added detail is visible and useful. Record per-level budgets in the progression manifest. Triangle growth is a useful default anti-copy check, but it is not permission to add invisible subdivisions.

Use LOD or a separate runtime representation when L3 would otherwise make city-scale placement too expensive. The editable hero GLB and the optimized runtime asset may be different representations of the same level.

## 7. Validate before modeling and before approval

Run:

```sh
python3 <skill>/scripts/progression_check.py progression.json --mode plan
```

This rejects broken ancestry, copy-like levels with too few independent delta groups, and upgrades missing architecture/detail changes.

Before delivery, record actual per-level metrics and evidence in `progression.json`, then run:

```sh
python3 <skill>/scripts/progression_check.py progression.json --mode delivery --root <job-root>
```

Delivery validation checks declared changes against recorded geometry/material/furniture/animation metrics and preview evidence. It does not judge whether a render is beautiful; actual visual QA is still required.

## 8. Visual acceptance of a level chain

Compare parent and child from matched cameras. A child level should make its new value obvious without losing the family identity. Verify at least:

- matched three-quarter view for silhouette and facade depth;
- front or street view for entrance/opening/furniture visibility;
- side or aerial view for roof/massing changes;
- close detail view for L3 material and trim quality when relevant.

If L2 or L3 is not visibly distinguishable at the intended camera distance, it is not an accepted upgrade even if its record passes validation.
