from mathutils import Vector

from .meshbuilder import create_prism_mesh
from . import naming
from ..diagnostics import log_beam


def _quad_between(start, end, side, near_width, far_width, vertical_offset):
    start = Vector(start)
    end = Vector(end)
    start.z += vertical_offset
    end.z += vertical_offset

    return [
        tuple(start + side * (near_width / 2.0)),
        tuple(start - side * (near_width / 2.0)),
        tuple(end - side * (far_width / 2.0)),
        tuple(end + side * (far_width / 2.0)),
    ]


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
        naming.arm(index, "Base"),
        start,
        end,
        "EXPLICIT_NODE_SUPPORT_ARM",
        near_width,
        thickness,
    )

    bottom = _quad_between(
        start, end, side, near_width, far_width, -thickness / 2.0
    )
    top = _quad_between(
        start, end, side, near_width, far_width, thickness / 2.0
    )

    base = create_prism_mesh(
        naming.arm(index, "Base"),
        collection,
        bottom,
        top,
        bevel_width,
        dark_material,
    )

    channel_start = start.lerp(end, 0.05)
    channel_end = start.lerp(end, 0.95)
    near_channel_width = min(channel_width, near_width * 0.45)
    far_channel_width = min(channel_width * 1.18, far_width * 0.45)
    channel_bottom_offset = thickness / 2.0 + channel_height * 0.15

    channel_bottom = _quad_between(
        channel_start,
        channel_end,
        side,
        near_channel_width,
        far_channel_width,
        channel_bottom_offset,
    )
    channel_top = _quad_between(
        channel_start,
        channel_end,
        side,
        near_channel_width,
        far_channel_width,
        channel_bottom_offset + channel_height,
    )

    channel = create_prism_mesh(
        naming.arm(index, "EnergyChannel"),
        collection,
        channel_bottom,
        channel_top,
        min(bevel_width, channel_width * 0.15),
        energy_material,
    )

    return [base, channel]


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
