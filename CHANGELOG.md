# Changelog

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
