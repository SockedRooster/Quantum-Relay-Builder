import bmesh

from .core import create_bmesh_object


def create_cylinder(
    name,
    collection,
    radius,
    depth,
    segments=32,
    location=(0.0, 0.0, 0.0),
    bevel_width=0.0,
    material=None,
):
    if radius <= 0.0 or depth <= 0.0:
        raise ValueError("Cylinder radius and depth must be positive")

    def build(bm):
        bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=segments,
            radius1=radius,
            radius2=radius,
            depth=depth,
        )
        bmesh.ops.translate(
            bm,
            verts=list(bm.verts),
            vec=location,
        )

    return create_bmesh_object(
        name=name,
        collection=collection,
        build_geometry=build,
        bevel_width=bevel_width,
        material=material,
    )
