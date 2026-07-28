def collect_mesh_statistics(registry):
    object_count = 0
    vertex_count = 0
    edge_count = 0
    polygon_count = 0

    for obj in registry.all_objects():
        if getattr(obj, "type", None) != 'MESH':
            continue

        object_count += 1
        mesh = obj.data
        vertex_count += len(mesh.vertices)
        edge_count += len(mesh.edges)
        polygon_count += len(mesh.polygons)

    return {
        "objects": object_count,
        "vertices": vertex_count,
        "edges": edge_count,
        "polygons": polygon_count,
    }
