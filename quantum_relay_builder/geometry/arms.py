import math
from mathutils import Vector

from .meshbuilder import create_prism_mesh
from . import naming
from ..diagnostics import log_beam


def _sloped_quad(origin, direction, side, start_radius, end_radius,
                 near_width, far_width, near_z, far_z):
    near_centre = Vector(origin) + direction * start_radius
    far_centre = Vector(origin) + direction * end_radius

    return [
        tuple(near_centre + side * (near_width / 2.0))[:2] + (near_z,),
        tuple(near_centre - side * (near_width / 2.0))[:2] + (near_z,),
        tuple(far_centre - side * (far_width / 2.0))[:2] + (far_z,),
        tuple(far_centre + side * (far_width / 2.0))[:2] + (far_z,),
    ]


def create_arm(index, collection, origin, angle, start_radius, end_radius,
               near_width, far_width, thickness, rail_width, rail_height,
               channel_width, channel_height, bevel, titanium, dark, energy,
               near_centre_z, far_centre_z):
    direction = Vector((math.cos(angle), math.sin(angle), 0.0))
    side = Vector((-math.sin(angle), math.cos(angle), 0.0))

    start_point = Vector(origin) + direction * start_radius
    start_point.z = near_centre_z
    end_point = Vector(origin) + direction * end_radius
    end_point.z = far_centre_z

    log_beam(
        naming.arm(index, "Base"),
        start_point,
        end_point,
        "TAPERED_SUPPORT_ARM",
        near_width,
        thickness,
    )

    bottom = _sloped_quad(
        origin, direction, side, start_radius, end_radius,
        near_width, far_width,
        near_centre_z - thickness / 2.0,
        far_centre_z - thickness / 2.0,
    )
    top = _sloped_quad(
        origin, direction, side, start_radius, end_radius,
        near_width, far_width,
        near_centre_z + thickness / 2.0,
        far_centre_z + thickness / 2.0,
    )

    base = create_prism_mesh(
        naming.arm(index, "Base"), collection,
        bottom, top, bevel, dark,
    )

    span = end_radius - start_radius
    channel_start = start_radius + span * 0.03
    channel_end = end_radius - span * 0.03
    channel_near_z = near_centre_z + thickness / 2.0 + channel_height * 0.15
    channel_far_z = far_centre_z + thickness / 2.0 + channel_height * 0.15

    channel_bottom = _sloped_quad(
        origin, direction, side, channel_start, channel_end,
        min(channel_width, near_width * 0.45),
        min(channel_width * 1.18, far_width * 0.45),
        channel_near_z,
        channel_far_z,
    )
    channel_top = _sloped_quad(
        origin, direction, side, channel_start, channel_end,
        min(channel_width, near_width * 0.45),
        min(channel_width * 1.18, far_width * 0.45),
        channel_near_z + channel_height,
        channel_far_z + channel_height,
    )

    channel = create_prism_mesh(
        naming.arm(index, "EnergyChannel"), collection,
        channel_bottom, channel_top,
        min(bevel, channel_width * 0.15), energy,
    )

    return [base, channel]


def create_detailed_arm_array(collection, origin, arm_count, hub_radius, hub_gap,
                              end_radius, width_hub, width_outer, thickness,
                              rail_width, rail_height, channel_width, channel_height,
                              bevel_width, titanium_material, dark_material,
                              energy_material, near_centre_z, far_centre_z):
    result = []
    start_radius = hub_radius + hub_gap
    safe_end_radius = max(start_radius + 0.05, end_radius)

    if safe_end_radius <= start_radius:
        raise ValueError("Support arm endpoint must be outside the hub attachment")
    if safe_end_radius > max(end_radius, start_radius + 0.05) + 1.0e-6:
        raise ValueError("Support arm endpoint validation failed")

    for i in range(arm_count):
        result.extend(create_arm(
            i + 1,
            collection,
            origin,
            2.0 * math.pi * i / arm_count,
            start_radius,
            safe_end_radius,
            width_hub,
            width_outer,
            thickness,
            rail_width,
            rail_height,
            channel_width,
            channel_height,
            bevel_width,
            titanium_material,
            dark_material,
            energy_material,
            near_centre_z,
            far_centre_z,
        ))

    return result
