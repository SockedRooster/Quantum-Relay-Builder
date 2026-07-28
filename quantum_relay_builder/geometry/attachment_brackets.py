"""Visible attachment hardware for explicit support nodes."""

from mathutils import Vector

from .meshbuilder import create_prism_mesh
from . import naming


def _oriented_box(centre, radial, tangent, radial_length, width, bottom_z, top_z):
    centre = Vector(centre)
    radial = Vector(radial)
    tangent = Vector(tangent)
    half_length = radial_length / 2.0
    half_width = width / 2.0

    footprint = [
        centre - radial * half_length + tangent * half_width,
        centre - radial * half_length - tangent * half_width,
        centre + radial * half_length - tangent * half_width,
        centre + radial * half_length + tangent * half_width,
    ]
    bottom = [(point.x, point.y, bottom_z) for point in footprint]
    top = [(point.x, point.y, top_z) for point in footprint]
    return bottom, top


def create_attachment_brackets(
    collection,
    nodes,
    arm_width_hub,
    arm_width_outer,
    arm_thickness,
    bevel_width,
    hub_material,
    ring_material,
    registry,
):
    """Create one hub saddle and one ring saddle for every support arm."""
    result = []

    for node in nodes:
        index = node["index"]
        radial = node["radial"]
        tangent = node["tangent"]

        hub_centre = node["hub"]
        hub_bottom = hub_centre.z - arm_thickness * 0.70
        hub_top = hub_centre.z + arm_thickness * 0.70
        hub_loops = _oriented_box(
            hub_centre,
            radial,
            tangent,
            radial_length=max(arm_width_hub * 0.90, arm_thickness * 1.8),
            width=arm_width_hub * 1.35,
            bottom_z=hub_bottom,
            top_z=hub_top,
        )
        hub_bracket = create_prism_mesh(
            naming.arm(index, "HubBracket"),
            collection,
            hub_loops[0],
            hub_loops[1],
            min(bevel_width, arm_thickness * 0.18),
            hub_material,
        )
        registry.add("hub_bracket", hub_bracket)
        result.append(hub_bracket)

        ring_centre = node["ring"]
        ring_bottom = ring_centre.z - arm_thickness * 0.65
        ring_top = ring_centre.z + arm_thickness * 0.85
        ring_loops = _oriented_box(
            ring_centre,
            radial,
            tangent,
            radial_length=max(arm_width_outer * 0.85, arm_thickness * 1.8),
            width=arm_width_outer * 1.30,
            bottom_z=ring_bottom,
            top_z=ring_top,
        )
        ring_bracket = create_prism_mesh(
            naming.arm(index, "RingBracket"),
            collection,
            ring_loops[0],
            ring_loops[1],
            min(bevel_width, arm_thickness * 0.18),
            ring_material,
        )
        registry.add("ring_bracket", ring_bracket)
        result.append(ring_bracket)

    return result
