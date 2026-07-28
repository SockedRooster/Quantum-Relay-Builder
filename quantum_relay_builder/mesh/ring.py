import math

from .prism import create_prism


def annular_segment_loops(
    inner_radius,
    outer_radius,
    start_angle,
    end_angle,
    bottom_z,
    top_z,
    arc_steps,
):
    if inner_radius <= 0.0:
        raise ValueError("Inner radius must be positive")
    if outer_radius <= inner_radius:
        raise ValueError("Outer radius must exceed inner radius")
    if arc_steps < 1:
        raise ValueError("Arc steps must be at least one")

    outer = []
    inner = []

    for step in range(arc_steps + 1):
        factor = step / arc_steps
        angle = start_angle + ((end_angle - start_angle) * factor)
        outer.append((
            outer_radius * math.cos(angle),
            outer_radius * math.sin(angle),
            bottom_z,
        ))

    for step in range(arc_steps, -1, -1):
        factor = step / arc_steps
        angle = start_angle + ((end_angle - start_angle) * factor)
        inner.append((
            inner_radius * math.cos(angle),
            inner_radius * math.sin(angle),
            bottom_z,
        ))

    bottom = outer + inner
    top = [(x, y, top_z) for x, y, _ in bottom]
    return bottom, top


def create_annular_segment(
    name,
    collection,
    inner_radius,
    outer_radius,
    start_angle,
    end_angle,
    bottom_z,
    top_z,
    arc_steps=4,
    bevel_width=0.0,
    material=None,
):
    bottom, top = annular_segment_loops(
        inner_radius,
        outer_radius,
        start_angle,
        end_angle,
        bottom_z,
        top_z,
        arc_steps,
    )

    return create_prism(
        name=name,
        collection=collection,
        bottom_loop=bottom,
        top_loop=top,
        bevel_width=bevel_width,
        material=material,
    )
