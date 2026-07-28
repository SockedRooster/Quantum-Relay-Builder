"""Explicit hub and ring attachment nodes for the support system."""

from __future__ import annotations

import math
from mathutils import Vector


def build_support_nodes(
    origin,
    arm_count,
    hub_attachment_radius,
    ring_attachment_radius,
    hub_attachment_z,
    ring_attachment_z,
):
    """Build matching 3D hub/ring attachment points.

    Each arm receives one hub point and one ring point at the same polar angle.
    No arm mesh function derives or modifies these locations.
    """
    if arm_count < 3:
        raise ValueError("At least three support nodes are required")
    if ring_attachment_radius <= hub_attachment_radius:
        raise ValueError(
            "Ring attachment radius must be greater than hub attachment radius"
        )

    origin = Vector(origin)
    nodes = []

    for index in range(arm_count):
        angle = (2.0 * math.pi * index) / arm_count
        radial = Vector((math.cos(angle), math.sin(angle), 0.0))
        tangent = Vector((-radial.y, radial.x, 0.0))

        hub_point = origin + radial * hub_attachment_radius
        hub_point.z = hub_attachment_z

        ring_point = origin + radial * ring_attachment_radius
        ring_point.z = ring_attachment_z

        nodes.append({
            "index": index + 1,
            "angle": angle,
            "radial": radial,
            "tangent": tangent,
            "hub": hub_point,
            "ring": ring_point,
        })

    return nodes
