# Quantum Relay Builder

Procedural Blender framework for generating Quantum Relay spacecraft parts.

## Current release

**v2.0.2 — Sprint 6.1.1 Diagnostic Build**

This release is built directly on the stable Sprint 6.1 repository. It does not
change the generated geometry.

### Diagnostic mode

Enable **Diagnostic Logging** in the Quantum Relay sidebar before building.

The add-on records:

- Every beam start and end coordinate
- Calculated beam direction and length
- Profile dimensions
- Unexpected-length and invalid-value flags
- Object location, rotation and scale
- World-space bounding boxes
- Parenting information
- Calculated arm length and expected assembly radius

The JSON report is saved beside the current `.blend` file. For an unsaved file,
it is written to the operating system's temporary directory.
