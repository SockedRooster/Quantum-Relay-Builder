import bpy
from .primitives import add_bevel_modifier, assign_material


def create_prism_mesh(name, collection, bottom_loop, top_loop, bevel_width=0.0, material=None):
    if len(bottom_loop) != len(top_loop):
        raise ValueError("Bottom and top loops must contain the same number of points")

    count = len(bottom_loop)
    vertices = list(bottom_loop) + list(top_loop)
    faces = [
        tuple(range(count - 1, -1, -1)),
        tuple(range(count, count * 2)),
    ]
    for index in range(count):
        nxt = (index + 1) % count
        faces.append((index, nxt, count + nxt, count + index))

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    add_bevel_modifier(obj, bevel_width)
    assign_material(obj, material)
    return obj
