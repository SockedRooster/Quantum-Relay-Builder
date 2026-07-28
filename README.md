# Quantum Relay Builder

Procedural Blender framework for generating Quantum Relay spacecraft parts.

## Current release

**v2.0.4 — Sprint 6.1.3 Strict Ring Attachment**

This release builds directly on Sprint 6.1.1 and changes only the support-arm
geometry and its attachment height.

## Sprint 6.1.2 changes

- Support arms terminate at the calculated structural-ring mount radius.
- Arms rise from the top of the hub to a configurable clearance above the ring.
- Arm bodies and energy channels follow the same slope.
- Mounts and gussets align with the actual outer arm height.
- Support-arm centre-lines are written to the diagnostic report.

## Diagnostic mode

Enable **Diagnostic Logging** in the Quantum Relay sidebar before building.
The JSON report is saved beside the current `.blend` file. For an unsaved file,
it is written to the operating system temporary directory.

The report includes beam coordinates and lengths, object transforms, parenting,
world-space bounds, effective arm length, and the calculated arm endpoint
heights.


## Sprint 6.1.3

- Purges stale `QR_` objects from every collection before each build.
- Removes duplicate `QuantumRelay_Generated.*` collections.
- Derives support-arm endpoints exclusively from the actual edge-ring midline.
- Uses the same authoritative attachment radius for arms, mounts and gussets.
- Hides the obsolete free-form arm-length control while retaining preset compatibility.
- Records reflector, ring, arm-start and attachment radii in diagnostic reports.
