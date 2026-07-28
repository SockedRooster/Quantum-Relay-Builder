import math
from mathutils import Vector

from .meshbuilder import create_prism_mesh
from . import naming


def _beam_rectangle(start, end, width, z):
    direction = end - start
    length = direction.length
    if length <= 1.0e-6:
        raise ValueError("Cross-brace endpoints are coincident")

    direction.normalize()
    tangent = Vector((-direction.y, direction.x, 0.0))
    half_width = width / 2.0

    return [
        tuple(start + tangent * half_width)[:2] + (z,),
        tuple(start - tangent * half_width)[:2] + (z,),
        tuple(end - tangent * half_width)[:2] + (z,),
        tuple(end + tangent * half_width)[:2] + (z,),
    ]


def create_cross_brace_array(
    collection,
    origin,
    arm_count,
    brace_radius,
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
            Vector(origin)
            + Vector((
                math.cos(angle) * brace_radius,
                math.sin(angle) * brace_radius,
                0.0,
            ))
        )

    bottom_z = centre_z - (brace_height / 2.0)
    top_z = centre_z + (brace_height / 2.0)

    for index, start in enumerate(points):
        end = points[(index + 1) % arm_count]

        brace = create_prism_mesh(
            name=naming.brace(index + 1),
            collection=collection,
            bottom_loop=_beam_rectangle(start, end, brace_width, bottom_z),
            top_loop=_beam_rectangle(start, end, brace_width, top_z),
            bevel_width=min(bevel_width, brace_width * 0.18),
            material=material,
        )
        registry.add("cross_brace", brace)
