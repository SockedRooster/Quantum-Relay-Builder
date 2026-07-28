from mathutils import Vector

from .meshbuilder import create_prism_mesh
from ..mesh.beam import create_profile_beam
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


def _truss_point(start, end, side, t, near_separation, far_separation, side_sign):
    centre = start.lerp(end, t)
    separation = near_separation + (far_separation - near_separation) * t
    return centre + side * (separation * 0.5 * side_sign)


def _beam(name, collection, start, end, width, height, bevel_width, material):
    return create_profile_beam(
        name=name,
        collection=collection,
        start=start,
        end=end,
        profile_id="BOX",
        width=width,
        height=height,
        bevel_width=min(bevel_width, min(width, height) * 0.18),
        material=material,
        up_hint=(0.0, 0.0, 1.0),
    )


def create_arm_from_node(
    node,
    collection,
    near_width,
    far_width,
    thickness,
    rail_width,
    rail_height,
    truss_bays,
    channel_width,
    channel_height,
    bevel_width,
    dark_material,
    titanium_material,
    energy_material,
):
    """Create a tapered Warren truss between explicit hub and ring nodes."""
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
        "WARREN_TRUSS_NODE_SUPPORT",
        near_width,
        thickness,
    )

    chord_width = max(rail_width, 0.025)
    chord_height = max(rail_height, 0.02)
    web_width = max(chord_width * 0.72, 0.018)
    web_height = max(chord_height * 0.72, 0.016)

    near_separation = max(near_width * 0.72, chord_width * 2.6)
    far_separation = max(far_width * 0.72, chord_width * 2.6)

    left_start = _truss_point(start, end, side, 0.0, near_separation, far_separation, 1.0)
    left_end = _truss_point(start, end, side, 1.0, near_separation, far_separation, 1.0)
    right_start = _truss_point(start, end, side, 0.0, near_separation, far_separation, -1.0)
    right_end = _truss_point(start, end, side, 1.0, near_separation, far_separation, -1.0)

    result = [
        _beam(
            naming.arm(index, "LeftChord"), collection,
            left_start, left_end, chord_width, chord_height,
            bevel_width, dark_material,
        ),
        _beam(
            naming.arm(index, "RightChord"), collection,
            right_start, right_end, chord_width, chord_height,
            bevel_width, dark_material,
        ),
    ]

    # Alternating diagonals form a Warren truss that remains clearly visible
    # from the working top view. End ties lock the truss into the brackets.
    bay_count = max(int(truss_bays), 2)
    for bay in range(bay_count):
        t0 = bay / bay_count
        t1 = (bay + 1) / bay_count
        if bay % 2 == 0:
            web_start = _truss_point(start, end, side, t0, near_separation, far_separation, 1.0)
            web_end = _truss_point(start, end, side, t1, near_separation, far_separation, -1.0)
        else:
            web_start = _truss_point(start, end, side, t0, near_separation, far_separation, -1.0)
            web_end = _truss_point(start, end, side, t1, near_separation, far_separation, 1.0)

        result.append(_beam(
            naming.arm(index, f"Web_{bay + 1:02d}"), collection,
            web_start, web_end, web_width, web_height,
            bevel_width, titanium_material,
        ))

    for component, t in (("HubTie", 0.0), ("RingTie", 1.0)):
        tie_left = _truss_point(start, end, side, t, near_separation, far_separation, 1.0)
        tie_right = _truss_point(start, end, side, t, near_separation, far_separation, -1.0)
        result.append(_beam(
            naming.arm(index, component), collection,
            tie_left, tie_right, web_width, web_height,
            bevel_width, titanium_material,
        ))

    # Raised energy conduit follows the arm centreline without hiding the web.
    channel_start = start.lerp(end, 0.08)
    channel_end = start.lerp(end, 0.92)
    conduit_width = min(channel_width, near_separation * 0.30)
    channel_bottom_offset = chord_height / 2.0 + channel_height * 0.45

    channel_bottom = _quad_between(
        channel_start, channel_end, side,
        conduit_width, min(conduit_width * 1.12, far_separation * 0.30),
        channel_bottom_offset,
    )
    channel_top = _quad_between(
        channel_start, channel_end, side,
        conduit_width, min(conduit_width * 1.12, far_separation * 0.30),
        channel_bottom_offset + channel_height,
    )
    result.append(create_prism_mesh(
        naming.arm(index, "EnergyConduit"),
        collection,
        channel_bottom,
        channel_top,
        min(bevel_width, channel_width * 0.15),
        energy_material,
    ))

    return result


def create_arm_array_from_nodes(
    collection,
    nodes,
    width_hub,
    width_outer,
    thickness,
    rail_width,
    rail_height,
    truss_bays,
    channel_width,
    channel_height,
    bevel_width,
    dark_material,
    titanium_material,
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
            rail_width=rail_width,
            rail_height=rail_height,
            truss_bays=truss_bays,
            channel_width=channel_width,
            channel_height=channel_height,
            bevel_width=bevel_width,
            dark_material=dark_material,
            titanium_material=titanium_material,
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
        rail_width=rail_width,
        rail_height=rail_height,
        truss_bays=5,
        channel_width=channel_width,
        channel_height=channel_height,
        bevel_width=bevel_width,
        dark_material=dark_material,
        titanium_material=titanium_material,
        energy_material=energy_material,
    )
