import math
from mathutils import Vector

from .meshbuilder import create_prism_mesh
from . import naming


def _oriented_rectangle(
    centre,
    radial,
    tangent,
    radial_length,
    tangential_width,
    z,
):
    half_length = radial_length / 2.0
    half_width = tangential_width / 2.0

    return [
        tuple(centre - radial * half_length + tangent * half_width)[:2] + (z,),
        tuple(centre - radial * half_length - tangent * half_width)[:2] + (z,),
        tuple(centre + radial * half_length - tangent * half_width)[:2] + (z,),
        tuple(centre + radial * half_length + tangent * half_width)[:2] + (z,),
    ]


def create_mount_array(
    collection,
    origin,
    arm_count,
    mount_radius,
    arm_outer_width,
    mount_length,
    mount_width_scale,
    mount_height,
    clamp_height,
    arm_top_z,
    ring_top_z,
    bevel_width,
    base_material,
    clamp_material,
    registry,
):
    mount_width = arm_outer_width * mount_width_scale

    for index in range(arm_count):
        angle = (2.0 * math.pi * index) / arm_count
        radial = Vector((math.cos(angle), math.sin(angle), 0.0))
        tangent = Vector((-math.sin(angle), math.cos(angle), 0.0))
        centre = Vector(origin) + radial * mount_radius

        base_bottom = arm_top_z
        base_top = max(base_bottom + mount_height, ring_top_z)

        base = create_prism_mesh(
            name=naming.mount(index + 1, "Base"),
            collection=collection,
            bottom_loop=_oriented_rectangle(
                centre,
                radial,
                tangent,
                mount_length,
                mount_width,
                base_bottom,
            ),
            top_loop=_oriented_rectangle(
                centre,
                radial,
                tangent,
                mount_length,
                mount_width,
                base_top,
            ),
            bevel_width=min(bevel_width, mount_height * 0.18),
            material=base_material,
        )
        registry.add("mount", base)

        clamp_length = mount_length * 0.78
        clamp_width = mount_width * 1.08
        clamp_bottom = base_top
        clamp_top = clamp_bottom + clamp_height

        clamp = create_prism_mesh(
            name=naming.mount(index + 1, "Clamp"),
            collection=collection,
            bottom_loop=_oriented_rectangle(
                centre,
                radial,
                tangent,
                clamp_length,
                clamp_width,
                clamp_bottom,
            ),
            top_loop=_oriented_rectangle(
                centre,
                radial,
                tangent,
                clamp_length,
                clamp_width,
                clamp_top,
            ),
            bevel_width=min(bevel_width, clamp_height * 0.18),
            material=clamp_material,
        )
        registry.add("mount_clamp", clamp)
