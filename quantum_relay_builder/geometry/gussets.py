import math
from mathutils import Vector

from .meshbuilder import create_prism_mesh
from . import naming


def _triangular_plate_loops(
    origin,
    radial,
    tangent,
    mount_radius,
    arm_outer_width,
    mount_width,
    gusset_length,
    gusset_height,
    gusset_thickness,
    base_z,
    side_sign,
):
    tangent_offset = (
        (arm_outer_width * 0.50)
        + (gusset_thickness * 0.65)
    ) * side_sign

    outer = Vector(origin) + radial * mount_radius + tangent * tangent_offset
    inner = outer - radial * gusset_length
    upper = outer + Vector((0.0, 0.0, gusset_height))

    thickness_offset = tangent * (gusset_thickness / 2.0)

    first = [
        tuple(inner - thickness_offset),
        tuple(outer - thickness_offset),
        tuple(upper - thickness_offset),
    ]
    second = [
        tuple(inner + thickness_offset),
        tuple(outer + thickness_offset),
        tuple(upper + thickness_offset),
    ]

    # Keep the lower edge level with the arm top.
    first = [(x, y, base_z if i < 2 else z) for i, (x, y, z) in enumerate(first)]
    second = [(x, y, base_z if i < 2 else z) for i, (x, y, z) in enumerate(second)]
    return first, second


def create_gusset_array(
    collection,
    origin,
    arm_count,
    mount_radius,
    arm_outer_width,
    mount_width,
    gusset_length,
    gusset_height,
    gusset_thickness,
    arm_top_z,
    bevel_width,
    material,
    registry,
):
    for index in range(arm_count):
        angle = (2.0 * math.pi * index) / arm_count
        radial = Vector((math.cos(angle), math.sin(angle), 0.0))
        tangent = Vector((-math.sin(angle), math.cos(angle), 0.0))

        for side_sign, side_name in ((-1.0, "Left"), (1.0, "Right")):
            first, second = _triangular_plate_loops(
                origin=origin,
                radial=radial,
                tangent=tangent,
                mount_radius=mount_radius,
                arm_outer_width=arm_outer_width,
                mount_width=mount_width,
                gusset_length=gusset_length,
                gusset_height=gusset_height,
                gusset_thickness=gusset_thickness,
                base_z=arm_top_z,
                side_sign=side_sign,
            )

            gusset = create_prism_mesh(
                name=naming.gusset(index + 1, side_name),
                collection=collection,
                bottom_loop=first,
                top_loop=second,
                bevel_width=min(bevel_width, gusset_thickness * 0.18),
                material=material,
            )
            registry.add("gusset", gusset)
