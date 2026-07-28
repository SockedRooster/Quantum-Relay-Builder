# Changelog

## 2.1.2 — Sprint 6.2.2

- Added visible twin-rail support arms.
- Added raised centreline energy conduits.
- Added explicit hub and ring attachment brackets.
- Increased support-framework clearance above the reflector.
- Kept all support hardware locked to the explicit attachment nodes.

## 2.1.1 — Sprint 6.2.1

- Added explicit hub/ring attachment-node generation.
- Rebuilt support arms directly between node pairs.
- Raised the support hub above the dish.
- Bound mount centres to the same ring nodes used by the arms.
- Added support-node coordinates to diagnostic output.
- Preserved compatibility with the previous public arm function.

## 2.0.4 — Sprint 6.1.3

- Added global stale generated-object cleanup.
- Added duplicate generated-collection cleanup.
- Added one authoritative support attachment calculation.
- Locked arm endpoints to the actual structural-ring midline.
- Added strict radius checks before geometry generation.
- Expanded diagnostic radius reporting.
- Hid the obsolete free-form arm-length control.

## 2.0.3 — Sprint 6.1.2

- Rebuilt support arms as tapered, sloped structural prisms.
- Anchored every arm directly between the hub and calculated ring mount radius.
- Added configurable arm-to-ring vertical clearance.
- Raised arm endpoints to the structural ring instead of leaving them flat beneath the dish.
- Updated mounts and gussets to align with the new outer arm height.
- Added support-arm centre-line diagnostics.

## 2.0.2 — Sprint 6.1.1

- Built directly from the stable Sprint 6.1 source.
- Added optional JSON diagnostic logging.
- Added beam coordinate and length instrumentation.
- Added object transform, parenting and world-bounds reporting.
- Added configurable unexpected-beam-length warnings.
- Left the Sprint 6.1 geometry-generation math unchanged.

## 2.0.1 — Sprint 6.1

- Fixed assembly parenting so generated world transforms are preserved.
- Auto-fitted radial support arms to the structural edge ring instead of using oversized preset lengths.
- Clamped gusset length to the available support-arm span.
- Added assembly-radius, empty-geometry and parenting validation.
- Added effective arm length and validation warning count to build reports.
