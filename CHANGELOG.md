# Changelog

## 1.3.2 — Sprint 5.3

- Added `geometry/mounts.py`.
- Added arm-to-ring mounting blocks and upper clamps.
- Added `geometry/gussets.py`.
- Added paired triangular reinforcement gussets at every arm endpoint.
- Added `geometry/braces.py`.
- Added optional polygonal cross-bracing between neighbouring support arms.
- Added a Structure Detail panel with independent mount, gusset and brace controls.
- Added automatic mount positioning from structural edge-ring dimensions.
- Added semantic registry categories and object names for all new components.

## 1.3.1 — Sprint 5.2

- Added `geometry/edge_ring.py`.
- Added a segmented structural edge ring around the generated reflector.
- Added adjustable ring clearance, width, height and segment count.
- Added configurable angular expansion-joint gaps.
- Added raised reinforcement ribs to every ring segment.
- Added semantic registry categories for edge-ring segments and ribs.
- Updated reflector generation to return assembly dimensions.
- Updated Blender UI and build reporting.

## 1.3.0 — Sprint 5.1

- Doubled the default reflector panel radius.
- Updated QR-100 support proportions for the larger reflector.
- Added central version metadata.
- Added central object naming helpers.
- Expanded `PartRegistry` with name lookup, category counts and duplicate protection.
- Updated the UI and operator names for Sprint 5.
