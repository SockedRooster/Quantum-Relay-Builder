from mathutils import Vector

from .core import build_indexed_geometry, create_bmesh_object
from .profiles import get_profile


def _beam_frame(start, end, up_hint):
    start = Vector(start)
    end = Vector(end)
    axis = end - start

    if axis.length <= 1.0e-6:
        raise ValueError("Beam start and end points must differ")

    axis.normalize()
    up = Vector(up_hint)

    if abs(axis.dot(up.normalized())) > 0.995:
        up = Vector((0.0, 1.0, 0.0))

    side = axis.cross(up).normalized()
    normal = side.cross(axis).normalized()
    return start, end, side, normal


def profile_beam_geometry(start, end, profile_points, up_hint=(0.0, 0.0, 1.0)):
    start, end, side, normal = _beam_frame(start, end, up_hint)
    count = len(profile_points)

    if count < 3:
        raise ValueError("Beam profile requires at least three points")

    start_loop = [
        tuple(start + side * x + normal * y)
        for x, y in profile_points
    ]
    end_loop = [
        tuple(end + side * x + normal * y)
        for x, y in profile_points
    ]

    vertices = start_loop + end_loop
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


def create_profile_beam(
    name,
    collection,
    start,
    end,
    profile_id,
    width,
    height,
    bevel_width=0.0,
    material=None,
    up_hint=(0.0, 0.0, 1.0),
):
    profile = get_profile(profile_id, width, height)
    vertices, faces = profile_beam_geometry(start, end, profile, up_hint)

    return create_bmesh_object(
        name=name,
        collection=collection,
        build_geometry=lambda bm: build_indexed_geometry(bm, vertices, faces),
        bevel_width=bevel_width,
        material=material,
    )
