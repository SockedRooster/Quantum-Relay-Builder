from mathutils import Vector

from .meshbuilder import create_prism_mesh
from . import naming
from ..diagnostics import log_beam


def _quad_between(start, end, side, near_width, far_width, vertical_offset, lateral_offset=0.0):
    start = Vector(start) + side * lateral_offset
    end = Vector(end) + side * lateral_offset
    start.z += vertical_offset
    end.z += vertical_offset

    return [
        tuple(start + side * (near_width / 2.0)),
        tuple(start - side * (near_width / 2.0)),
        tuple(end - side * (far_width / 2.0)),
        tuple(end + side * (far_width / 2.0)),
    ]


def _create_rail(
    name,
    collection,
    start,
    end,
    side,
    near_width,
    far_width,
    thickness,
    lateral_offset,
    bevel_width,
    material,
):
    bottom = _quad_between(
        start, end, side, near_width, far_width,
        -thickness / 2.0, lateral_offset,
    )
    top = _quad_between(
        start, end, side, near_width, far_width,
        thickness / 2.0, lateral_offset,
    )
    return create_prism_mesh(
        name,
        collection,
        bottom,
        top,
        bevel_width,
        material,
    )


def create_arm_from_node(
    node,
    collection,
    near_width,
    far_width,
    thickness,
    channel_width,
    channel_height,
    bevel_width,
    dark_material,
    energy_material,
):
    index = node["index"]
    start = Vector(node["hub"])
    end = Vector(node["ring"])
    side = Vector(node["tangent"])

    vector = end - start
    if vector.length <= 1.0e-5:
        raise ValueError(f"Support arm {index} has coincident attachment nodes")

    log_beam(
        naming.arm(index, "Centreline"),
        start,
        end,
        "TWIN_RAIL_NODE_SUPPORT",
        near_width,
        thickness,
    )

    # Two separated structural rails make the support system visible from above
    # and leave the reflector surface unobstructed between them.
    rail_near_width = max(near_width * 0.28, 0.035)
    rail_far_width = max(far_width * 0.24, 0.035)
    rail_separation = max(near_width * 0.62, rail_near_width * 1.8)

    left = _create_rail(
        naming.arm(index, "LeftRail"),
        collection,
        start,
        end,
        side,
        rail_near_width,
        rail_far_width,
        thickness,
        rail_separation / 2.0,
        bevel_width,
        dark_material,
    )
    right = _create_rail(
        naming.arm(index, "RightRail"),
        collection,
        start,
        end,
        side,
        rail_near_width,
        rail_far_width,
        thickness,
        -rail_separation / 2.0,
        bevel_width,
        dark_material,
    )

    # Raised energy conduit follows the arm centreline.
    channel_start = start.lerp(end, 0.08)
    channel_end = start.lerp(end, 0.92)
    conduit_width = min(channel_width, near_width * 0.32)
    channel_bottom_offset = thickness / 2.0 + channel_height * 0.35

    channel_bottom = _quad_between(
        channel_start,
        channel_end,
        side,
        conduit_width,
        min(conduit_width * 1.12, far_width * 0.32),
        channel_bottom_offset,
    )
    channel_top = _quad_between(
        channel_start,
        channel_end,
        side,
        conduit_width,
        min(conduit_width * 1.12, far_width * 0.32),
        channel_bottom_offset + channel_height,
    )
    channel = create_prism_mesh(
        naming.arm(index, "EnergyConduit"),
        collection,
        channel_bottom,
        channel_top,
        min(bevel_width, channel_width * 0.15),
        energy_material,
    )

    return [left, right, channel]


def create_arm_array_from_nodes(
    collection,
    nodes,
    width_hub,
    width_outer,
    thickness,
    channel_width,
    channel_height,
    bevel_width,
    dark_material,
    energy_material,
):
    result = []
    for node in nodes:
        result.extend(create_arm_from_node(
            node=node,
            collection=collection,
            near_width=width_hub,
            far_width=width_outer,
            thickness=thickness,
            channel_width=channel_width,
            channel_height=channel_height,
            bevel_width=bevel_width,
            dark_material=dark_material,
            energy_material=energy_material,
        ))
    return result


def create_detailed_arm_array(
    collection, origin, arm_count, hub_radius, hub_gap, end_radius,
    width_hub, width_outer, thickness, rail_width, rail_height,
    channel_width, channel_height, bevel_width, titanium_material,
    dark_material, energy_material, near_centre_z, far_centre_z,
):
    """Compatibility wrapper for scripts written against Sprint 6."""
    from .support_nodes import build_support_nodes

    nodes = build_support_nodes(
        origin=origin,
        arm_count=arm_count,
        hub_attachment_radius=hub_radius + hub_gap,
        ring_attachment_radius=end_radius,
        hub_attachment_z=near_centre_z,
        ring_attachment_z=far_centre_z,
    )
    return create_arm_array_from_nodes(
        collection=collection,
        nodes=nodes,
        width_hub=width_hub,
        width_outer=width_outer,
        thickness=thickness,
        channel_width=channel_width,
        channel_height=channel_height,
        bevel_width=bevel_width,
        dark_material=dark_material,
        energy_material=energy_material,
    )
