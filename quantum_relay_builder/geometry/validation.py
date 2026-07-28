from mathutils import Vector


def validate_generated_assembly(registry, root, expected_radius=None):
    warnings = []
    mesh_objects = [obj for obj in registry.all_objects() if getattr(obj, "type", None) == 'MESH']

    disconnected = [obj.name for obj in registry.all_objects() if obj is not root and obj.parent is not root]
    if disconnected:
        warnings.append(f"{len(disconnected)} generated objects are not parented to the assembly root")

    zero_geometry = [obj.name for obj in mesh_objects if len(obj.data.vertices) == 0 or len(obj.data.polygons) == 0]
    if zero_geometry:
        warnings.append(f"{len(zero_geometry)} mesh objects contain no usable geometry")

    if expected_radius is not None and expected_radius > 0.0:
        limit = expected_radius * 1.35
        oversized = []
        for obj in mesh_objects:
            for vertex in obj.data.vertices:
                world = obj.matrix_world @ vertex.co
                if (Vector((world.x, world.y, root.location.z)) - root.location).length > limit:
                    oversized.append(obj.name)
                    break
        if oversized:
            warnings.append(f"{len(set(oversized))} objects extend beyond the expected assembly radius")

    return warnings
