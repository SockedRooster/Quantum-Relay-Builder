from mathutils import Vector

from .prism import create_prism


def create_plate(
    name,
    collection,
    outline,
    thickness,
    normal=(0.0, 0.0, 1.0),
    bevel_width=0.0,
    material=None,
):
    if len(outline) < 3:
        raise ValueError("A plate outline requires at least three points")

    normal = Vector(normal).normalized()
    half_offset = normal * (thickness / 2.0)
    bottom = [tuple(Vector(point) - half_offset) for point in outline]
    top = [tuple(Vector(point) + half_offset) for point in outline]

    return create_prism(
        name=name,
        collection=collection,
        bottom_loop=bottom,
        top_loop=top,
        bevel_width=bevel_width,
        material=material,
    )
