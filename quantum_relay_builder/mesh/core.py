import bmesh
import bpy

from ..geometry.primitives import add_bevel_modifier, assign_material


def create_bmesh_object(
    name,
    collection,
    build_geometry,
    bevel_width=0.0,
    material=None,
):
    """
    Create a Blender object without bpy.ops.

    build_geometry receives an empty BMesh and must populate it.
    """
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    bm = bmesh.new()

    try:
        build_geometry(bm)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(mesh)
        mesh.update()
    finally:
        bm.free()

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    add_bevel_modifier(obj, bevel_width)
    assign_material(obj, material)
    return obj


def build_indexed_geometry(bm, vertices, faces):
    bm_vertices = [bm.verts.new(coordinate) for coordinate in vertices]
    bm.verts.ensure_lookup_table()

    for indices in faces:
        try:
            bm.faces.new([bm_vertices[index] for index in indices])
        except ValueError:
            # Duplicate faces are ignored; invalid topology should still fail
            # during normal validation rather than through operator context.
            continue
