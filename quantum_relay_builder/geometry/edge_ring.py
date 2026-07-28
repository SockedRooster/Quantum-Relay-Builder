import math

from .meshbuilder import create_prism_mesh
from . import naming


def _annular_segment_loops(
    inner_radius,
    outer_radius,
    start_angle,
    end_angle,
    bottom_z,
    top_z,
    arc_steps,
):
    """
    Build matching bottom and top loops for one annular structural segment.

    The loop travels along the outer arc and returns along the inner arc,
    producing a closed polygon suitable for prism extrusion.
    """
    outer_points = []
    inner_points = []

    for step in range(arc_steps + 1):
        factor = step / arc_steps
        angle = start_angle + ((end_angle - start_angle) * factor)

        outer_points.append((
            outer_radius * math.cos(angle),
            outer_radius * math.sin(angle),
            bottom_z,
        ))

    for step in range(arc_steps, -1, -1):
        factor = step / arc_steps
        angle = start_angle + ((end_angle - start_angle) * factor)

        inner_points.append((
            inner_radius * math.cos(angle),
            inner_radius * math.sin(angle),
            bottom_z,
        ))

    bottom = outer_points + inner_points
    top = [(x, y, top_z) for x, y, _ in bottom]
    return bottom, top


def _rib_loops(
    radius,
    angle,
    radial_width,
    tangential_width,
    bottom_z,
    top_z,
):
    radial = (
        math.cos(angle),
        math.sin(angle),
    )
    tangent = (
        -math.sin(angle),
        math.cos(angle),
    )

    centre_x = radius * radial[0]
    centre_y = radius * radial[1]

    half_radial = radial_width / 2.0
    half_tangent = tangential_width / 2.0

    corners = [
        (
            centre_x + radial[0] * half_radial + tangent[0] * half_tangent,
            centre_y + radial[1] * half_radial + tangent[1] * half_tangent,
        ),
        (
            centre_x + radial[0] * half_radial - tangent[0] * half_tangent,
            centre_y + radial[1] * half_radial - tangent[1] * half_tangent,
        ),
        (
            centre_x - radial[0] * half_radial - tangent[0] * half_tangent,
            centre_y - radial[1] * half_radial - tangent[1] * half_tangent,
        ),
        (
            centre_x - radial[0] * half_radial + tangent[0] * half_tangent,
            centre_y - radial[1] * half_radial + tangent[1] * half_tangent,
        ),
    ]

    bottom = [(x, y, bottom_z) for x, y in corners]
    top = [(x, y, top_z) for x, y in corners]
    return bottom, top


def create_structural_edge_ring(
    collection,
    origin,
    reflector_outer_radius,
    clearance,
    ring_width,
    ring_height,
    segment_count,
    joint_gap_angle,
    rib_width,
    rib_height,
    bevel_width,
    ring_material,
    rib_material,
    registry,
):
    inner_radius = reflector_outer_radius + clearance
    outer_radius = inner_radius + ring_width

    segment_angle = (2.0 * math.pi) / segment_count
    usable_angle = max(segment_angle - joint_gap_angle, segment_angle * 0.20)
    half_usable = usable_angle / 2.0

    bottom_z = origin.z - (ring_height / 2.0)
    top_z = origin.z + (ring_height / 2.0)

    arc_steps = max(2, int(24 / segment_count) + 2)

    for index in range(segment_count):
        centre_angle = segment_angle * index
        start_angle = centre_angle - half_usable
        end_angle = centre_angle + half_usable

        bottom_loop, top_loop = _annular_segment_loops(
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            start_angle=start_angle,
            end_angle=end_angle,
            bottom_z=bottom_z,
            top_z=top_z,
            arc_steps=arc_steps,
        )

        segment = create_prism_mesh(
            name=naming.edge_ring_segment(index + 1),
            collection=collection,
            bottom_loop=bottom_loop,
            top_loop=top_loop,
            bevel_width=min(bevel_width, ring_height * 0.20),
            material=ring_material,
        )
        segment.location = (origin.x, origin.y, 0.0)
        registry.add("edge_ring", segment)

        rib_bottom, rib_top = _rib_loops(
            radius=(inner_radius + outer_radius) / 2.0,
            angle=centre_angle,
            radial_width=ring_width * 1.12,
            tangential_width=rib_width,
            bottom_z=top_z,
            top_z=top_z + rib_height,
        )

        rib = create_prism_mesh(
            name=naming.edge_ring_rib(index + 1),
            collection=collection,
            bottom_loop=rib_bottom,
            top_loop=rib_top,
            bevel_width=min(bevel_width, rib_width * 0.20),
            material=rib_material,
        )
        rib.location = (origin.x, origin.y, 0.0)
        registry.add("edge_ring_rib", rib)

    return {
        "inner_radius": inner_radius,
        "outer_radius": outer_radius,
        "segment_count": segment_count,
    }
