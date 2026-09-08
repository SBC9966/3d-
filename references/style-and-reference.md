# Style and reference contract

Describe style as construction choices, not a color preset. Separate:

| Layer | Choices to make explicit |
|---|---|
| Massing | courtyard/slab/tower/pavilion, wings, setbacks, roof silhouette |
| Facade | bay width, floor rhythm, openings, balcony/arcade depth, entrance emphasis |
| Roof | flat/pitched/hip/sawtooth/custom; slope, ridge, eaves, parapet |
| Materials | masonry/timber/metal/glass response, palette, weathering, UV scale |
| Context | street frontage, park footprint, ground access, local scale |

Examples are grammar starting points, not historical claims or implemented generators:
- Warm brick apartments: repeated vertical bays, recessed windows, balcony rails, distinct entrance/base, roof/parapet detail.
- Courtyard residence: connected wings, an actual open court, roof junctions, veranda depth and aligned doors; require plan/top view.
- Glass office tower: podium and tower, modular curtain wall, setbacks, mechanical crown; keep facade rendering batched.
- Timber lodge: pitched roof and deep eaves, real porch, exposed beam rhythm, wood direction; review roof intersections.
- Curvilinear museum: section profiles, wall/roof continuity and tessellation quality; a custom mesh/Blender pass may be warranted.

Generate a single-asset reference sheet using this shape:

“Original [use + architectural style], architectural modeling sheet, the SAME design in front orthographic, right orthographic and three-quarter view; [width × depth × height metres; floors]; [massing/roof]; [facade and entrance rules]; [materials]; neutral background and readable neutral lighting; [project visual direction]. Consistent openings and structural bays between views, no labels, logos or city background.”

Do not encode exact data as trusted image text. If the image disagrees with the spec, choose/document a consistent design in the spec and rule record. For complex roofs add top view; for courtyard connections add plan; for ornament add one local detail. Keep one visual direction after lock, revise only to resolve a concrete problem.

Record each extracted rule as:
`reference ID → visible observation → parameter/geometry rule → implemented component → actual QA evidence`.
Example: REF-06 front shows an open service hatch → counterWidth=5.25m, openingHeight=1.5m → front wall split into side/header/sill geometry → front/street screenshot verifies the interior is not occluded.

The user's approval of the original pavilion batch establishes a useful workflow and taste example; it does not automatically approve later assets or require every building to resemble a pavilion.

## Upgrade-chain references

For the same-building L1/L2/L3 workflow, lock the base identity first. Use the approved parent model and its renders as the identity anchor. Generate only the additional references needed to clarify new massing, facade, interior, roof, material or prop decisions. Prefer an aligned same-building evolution sheet or targeted detail sheets over three independent concept images.

If an L2/L3 concept image drifts into a different building, keep the parent geometry identity and extract only the local detail idea. Reference images suggest detail; the accepted parent plus progression spec controls ancestry.
