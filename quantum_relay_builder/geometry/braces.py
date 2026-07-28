import math
from mathutils import Vector

from ..mesh.beam import create_profile_beam
from . import naming


def create_cross_brace_array(
    collection,
    origin,
    arm_count,
    brace_radius,
    brace_profile,
    brace_width,
    brace_height,
    centre_z,
    bevel_width,
    material,
    registry,
):
    points = []

    for index in range(arm_count):
        angle = (2.0 * math.pi * index) / arm_count
        points.append(
            Vector((
                origin.x + math.cos(angle) * brace_radius,
                origin.y + math.sin(angle) * brace_radius,
                centre_z,
            ))
        )

    for index, start in enumerate(points):
        end = points[(index + 1) % arm_count]

        brace = create_profile_beam(
            name=naming.brace(index + 1),
            collection=collection,
            start=start,
            end=end,
            profile_id=brace_profile,
            width=brace_width,
            height=brace_height,
            bevel_width=min(bevel_width, brace_width * 0.18),
            material=material,
        )
        registry.add("cross_brace", brace)
