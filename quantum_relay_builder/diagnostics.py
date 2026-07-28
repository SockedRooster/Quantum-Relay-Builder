"""Opt-in diagnostic logging for the stable Sprint 6.1 geometry pipeline."""

from __future__ import annotations

import json
import math
import tempfile
from datetime import datetime
from pathlib import Path

import bpy
from mathutils import Vector


_enabled = False
_max_expected_beam_length = 0.0
_entries: list[dict] = []
_log_path = ""


def configure(enabled: bool, max_expected_beam_length: float = 0.0) -> None:
    global _enabled, _max_expected_beam_length, _entries, _log_path
    _enabled = bool(enabled)
    _max_expected_beam_length = max(0.0, float(max_expected_beam_length))
    _entries = []
    _log_path = ""


def enabled() -> bool:
    return _enabled


def _vector(values):
    return [round(float(value), 6) for value in values]


def log_beam(name, start, end, profile_id, width, height) -> None:
    if not _enabled:
        return

    start_v = Vector(start)
    end_v = Vector(end)
    delta = end_v - start_v
    length = delta.length
    flags = []

    if not all(math.isfinite(value) for value in (*start_v, *end_v, width, height)):
        flags.append("NON_FINITE_VALUE")
    if length <= 1.0e-6:
        flags.append("ZERO_LENGTH")
    if _max_expected_beam_length > 0.0 and length > _max_expected_beam_length:
        flags.append("UNEXPECTED_LENGTH")

    _entries.append({
        "type": "beam",
        "name": name,
        "start": _vector(start_v),
        "end": _vector(end_v),
        "delta": _vector(delta),
        "length": round(length, 6),
        "profile": profile_id,
        "width": round(float(width), 6),
        "height": round(float(height), 6),
        "flags": flags,
    })


def log_object(obj, root=None) -> None:
    if not _enabled:
        return

    world_corners = []
    if getattr(obj, "type", None) == "MESH":
        world_corners = [
            obj.matrix_world @ Vector(corner)
            for corner in obj.bound_box
        ]

    if world_corners:
        minimum = Vector((
            min(point.x for point in world_corners),
            min(point.y for point in world_corners),
            min(point.z for point in world_corners),
        ))
        maximum = Vector((
            max(point.x for point in world_corners),
            max(point.y for point in world_corners),
            max(point.z for point in world_corners),
        ))
        dimensions = maximum - minimum
    else:
        minimum = maximum = obj.matrix_world.translation.copy()
        dimensions = Vector((0.0, 0.0, 0.0))

    _entries.append({
        "type": "object",
        "name": obj.name,
        "object_type": obj.type,
        "parent": obj.parent.name if obj.parent else None,
        "expected_parent": root.name if root else None,
        "location": _vector(obj.location),
        "world_location": _vector(obj.matrix_world.translation),
        "rotation_euler": _vector(obj.rotation_euler),
        "scale": _vector(obj.scale),
        "bounds_min": _vector(minimum),
        "bounds_max": _vector(maximum),
        "bounds_dimensions": _vector(dimensions),
    })


def _default_log_path() -> Path:
    blend_directory = Path(bpy.path.abspath("//"))
    if bpy.data.filepath and blend_directory.exists():
        target_directory = blend_directory
    else:
        target_directory = Path(tempfile.gettempdir())

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return target_directory / f"quantum_relay_debug_{stamp}.json"


def write_report(build_data: dict) -> str:
    global _log_path
    if not _enabled:
        return ""

    path = _default_log_path()
    payload = {
        "build": build_data,
        "entry_count": len(_entries),
        "entries": _entries,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _log_path = str(path)
    return _log_path


def last_log_path() -> str:
    return _log_path
