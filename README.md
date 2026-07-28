# Quantum Relay Builder

A procedural Blender framework for building the Quantum Relay KSP asset family.

## Current release

v2.0.0 — Sprint 6.0 Procedural Framework

## Sprint 6 architecture

The add-on now includes an operator-free BMesh mesh engine:

```text
quantum_relay_builder/
    mesh/
        core.py
        prism.py
        beam.py
        profiles.py
        plate.py
        cylinder.py
        ring.py
```

## Features

- Reusable BMesh object creation
- Prism, plate, cylinder, beam and annular-ring generators
- Box, diamond and hexagonal beam profiles
- Profile-based cross braces
- QR-100, QR-250 and QR-500 family presets
- Build-time object and topology statistics
- Existing reflector, hub, arms, mounts, gussets and edge-ring features
- No `bpy.ops` dependency during mesh construction

## Install

Install the release ZIP through Blender:

`Edit > Preferences > Add-ons > Install from Disk`

Open the `Quantum Relay` tab in the 3D Viewport sidebar.
