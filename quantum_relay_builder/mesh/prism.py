from .core import build_indexed_geometry, create_bmesh_object


def prism_geometry(bottom_loop, top_loop):
    if len(bottom_loop) != len(top_loop):
        raise ValueError("Bottom and top loops must contain the same number of points")
    if len(bottom_loop) < 3:
        raise ValueError("A prism requires at least three points per loop")

    count = len(bottom_loop)
    vertices = list(bottom_loop) + list(top_loop)
    faces = [
        tuple(range(count - 1, -1, -1)),
        tuple(range(count, count * 2)),
    ]

    for index in range(count):
        next_index = (index + 1) % count
        faces.append((
            index,
            next_index,
            count + next_index,
            count + index,
        ))

    return vertices, faces


def create_prism(
    name,
    collection,
    bottom_loop,
    top_loop,
    bevel_width=0.0,
    material=None,
):
    vertices, faces = prism_geometry(bottom_loop, top_loop)

    return create_bmesh_object(
        name=name,
        collection=collection,
        build_geometry=lambda bm: build_indexed_geometry(bm, vertices, faces),
        bevel_width=bevel_width,
        material=material,
    )
