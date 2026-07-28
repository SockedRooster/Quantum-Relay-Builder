import bpy


def add_bevel_modifier(obj, width, segments=3):
    if width <= 0:
        return
    modifier = obj.modifiers.new(name="QR_Bevel", type='BEVEL')
    modifier.width = width
    modifier.segments = segments
    modifier.limit_method = 'ANGLE'


def assign_material(obj, material):
    if obj.type == 'MESH' and material is not None:
        obj.data.materials.append(material)


def create_cylinder(name, radius, depth, location, collection, material=None, bevel_width=0.0, vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth,
        end_fill_type='NGON', location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    for source in list(obj.users_collection):
        source.objects.unlink(obj)
    collection.objects.link(obj)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    add_bevel_modifier(obj, bevel_width)
    assign_material(obj, material)
    return obj
