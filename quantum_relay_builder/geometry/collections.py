import bpy
from .naming import COLLECTION


def get_or_create_generated_collection(context):
    collection = bpy.data.collections.get(COLLECTION)
    if collection is None:
        collection = bpy.data.collections.new(COLLECTION)
        context.scene.collection.children.link(collection)
    return collection


def clear_generated_collection():
    collection = bpy.data.collections.get(COLLECTION)
    if collection is None:
        return
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)
