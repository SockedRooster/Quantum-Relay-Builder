import bpy
from mathutils import Vector

from .collections import clear_generated_collection, get_or_create_generated_collection
from .registry import PartRegistry
from .materials import (
    get_titanium_material, get_dark_metal_material,
    get_quantum_energy_material, get_reflector_material
)
from .reflector import create_reflector_array
from .hub import create_layered_hub
from .arms import create_detailed_arm_array
from .naming import ROOT


def create_root(collection, location, display_size):
    root = bpy.data.objects.new(ROOT, None)
    root.empty_display_type = 'CIRCLE'
    root.empty_display_size = display_size
    root.location = location
    collection.objects.link(root)
    return root


def build_sprint5_assembly(context, props):
    clear_generated_collection()
    collection = get_or_create_generated_collection(context)
    registry = PartRegistry()
    cursor = context.scene.cursor.location.copy()

    titanium = get_titanium_material()
    dark = get_dark_metal_material()
    energy = get_quantum_energy_material()
    reflector_material = get_reflector_material()

    root = registry.add("root", create_root(collection, cursor, max(props.panel_radius*1.25,0.25)))

    create_reflector_array(
        collection, cursor, props.reflector_rings, props.panel_radius, props.panel_gap,
        props.panel_thickness, props.panel_frame_width, props.reflector_inset,
        props.reflector_thickness, props.reflector_curvature, props.tilt_panels,
        props.bevel_width, titanium, reflector_material, registry
    )

    if props.generate_structure:
        support_origin = cursor + Vector((0,0,-props.panel_thickness/2-props.hub_height/2-0.10))
        registry.extend("hub", create_layered_hub(
            collection, support_origin, props.hub_radius, props.hub_height,
            props.hub_ring_height, props.core_radius, props.core_height,
            props.bevel_width, titanium, dark, energy
        ))
        registry.extend("arm", create_detailed_arm_array(
            collection, support_origin, props.arm_count, props.hub_radius,
            props.arm_gap, props.arm_length, props.arm_width_hub,
            props.arm_width_outer, props.arm_thickness, props.rail_width,
            props.rail_height, props.channel_width, props.channel_height,
            props.bevel_width, titanium, dark, energy
        ))

    for obj in registry.all_objects():
        if obj is not root:
            obj.parent = root

    bpy.ops.object.select_all(action='DESELECT')
    root.select_set(True)
    context.view_layer.objects.active = root
    return registry
