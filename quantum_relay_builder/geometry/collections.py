import bpy
from .naming import COLLECTION, ROOT


GENERATED_OBJECT_PREFIX = "QR_"


def get_or_create_generated_collection(context):
    collection = bpy.data.collections.get(COLLECTION)
    if collection is None:
        collection = bpy.data.collections.new(COLLECTION)
        context.scene.collection.children.link(collection)
    elif collection.name not in context.scene.collection.children:
        # Blender collection membership is not safely tested by name through
        # `in`; link only when it has no scene parent.
        if not collection.users_scene:
            context.scene.collection.children.link(collection)
    return collection


def _is_generated_object(obj):
    return (
        obj.name == ROOT
        or obj.name.startswith(GENERATED_OBJECT_PREFIX)
        or bool(obj.get("quantum_relay_generated", False))
    )


def clear_generated_collection():
    """Remove every prior Quantum Relay object, including stale copies.

    Earlier builds could leave generated objects behind when Blender renamed a
    duplicate collection or when objects were moved to another collection.
    Removing by generated-object identity prevents old oversized arms from
    surviving into a fresh build.
    """
    for obj in list(bpy.data.objects):
        if _is_generated_object(obj):
            bpy.data.objects.remove(obj, do_unlink=True)

    for collection in list(bpy.data.collections):
        if collection.name == COLLECTION or collection.name.startswith(COLLECTION + "."):
            bpy.data.collections.remove(collection)
