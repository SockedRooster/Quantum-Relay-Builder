import bpy
from mathutils import Vector

from .collections import clear_generated_collection, get_or_create_generated_collection
from .registry import PartRegistry
from .materials import (
    get_titanium_material,
    get_dark_metal_material,
    get_quantum_energy_material,
    get_reflector_material,
)
from .reflector import create_reflector_array
from .edge_ring import create_structural_edge_ring
from .hub import create_layered_hub
from .arms import create_detailed_arm_array
from .mounts import create_mount_array
from .gussets import create_gusset_array
from .braces import create_cross_brace_array
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

    root = registry.add(
        "root",
        create_root(
            collection,
            cursor,
            max(props.panel_radius * 1.25, 0.25),
        ),
    )

    reflector_metrics = create_reflector_array(
        collection=collection,
        origin=cursor,
        rings=props.reflector_rings,
        panel_radius=props.panel_radius,
        panel_gap=props.panel_gap,
        panel_thickness=props.panel_thickness,
        frame_width=props.panel_frame_width,
        reflector_inset=props.reflector_inset,
        reflector_thickness=props.reflector_thickness,
        curvature=props.reflector_curvature,
        tilt_panels=props.tilt_panels,
        bevel_width=props.bevel_width,
        frame_material=titanium,
        reflector_material=reflector_material,
        registry=registry,
    )

    ring_metrics = None

    if props.generate_edge_ring:
        ring_metrics = create_structural_edge_ring(
            collection=collection,
            origin=cursor,
            reflector_outer_radius=reflector_metrics["outer_radius"],
            clearance=props.edge_ring_clearance,
            ring_width=props.edge_ring_width,
            ring_height=props.edge_ring_height,
            segment_count=props.edge_ring_segments,
            joint_gap_angle=props.edge_ring_gap_angle,
            rib_width=props.edge_ring_rib_width,
            rib_height=props.edge_ring_rib_height,
            bevel_width=props.bevel_width,
            ring_material=dark,
            rib_material=titanium,
            registry=registry,
        )

    if props.generate_structure:
        support_origin = cursor + Vector((
            0.0,
            0.0,
            -(props.panel_thickness / 2.0)
            - (props.hub_height / 2.0)
            - 0.10,
        ))

        registry.extend(
            "hub",
            create_layered_hub(
                collection,
                support_origin,
                props.hub_radius,
                props.hub_height,
                props.hub_ring_height,
                props.core_radius,
                props.core_height,
                props.bevel_width,
                titanium,
                dark,
                energy,
            ),
        )

        registry.extend(
            "arm",
            create_detailed_arm_array(
                collection,
                support_origin,
                props.arm_count,
                props.hub_radius,
                props.arm_gap,
                props.arm_length,
                props.arm_width_hub,
                props.arm_width_outer,
                props.arm_thickness,
                props.rail_width,
                props.rail_height,
                props.channel_width,
                props.channel_height,
                props.bevel_width,
                titanium,
                dark,
                energy,
            ),
        )

        arm_start_radius = props.hub_radius + props.arm_gap
        arm_end_radius = arm_start_radius + props.arm_length

        if ring_metrics is not None:
            mount_radius = (
                ring_metrics["inner_radius"]
                + ring_metrics["outer_radius"]
            ) / 2.0
            ring_top_z = cursor.z + (props.edge_ring_height / 2.0)
        else:
            mount_radius = arm_end_radius
            ring_top_z = cursor.z

        arm_top_z = support_origin.z + (props.arm_thickness / 2.0)
        mount_width = props.arm_width_outer * props.mount_width_scale

        if props.generate_mounts:
            create_mount_array(
                collection=collection,
                origin=support_origin,
                arm_count=props.arm_count,
                mount_radius=mount_radius,
                arm_outer_width=props.arm_width_outer,
                mount_length=props.mount_length,
                mount_width_scale=props.mount_width_scale,
                mount_height=props.mount_height,
                clamp_height=props.clamp_height,
                arm_top_z=arm_top_z,
                ring_top_z=ring_top_z,
                bevel_width=props.bevel_width,
                base_material=dark,
                clamp_material=titanium,
                registry=registry,
            )

        if props.generate_gussets:
            create_gusset_array(
                collection=collection,
                origin=support_origin,
                arm_count=props.arm_count,
                mount_radius=mount_radius,
                arm_outer_width=props.arm_width_outer,
                mount_width=mount_width,
                gusset_length=props.gusset_length,
                gusset_height=props.gusset_height,
                gusset_thickness=props.gusset_thickness,
                arm_top_z=arm_top_z,
                bevel_width=props.bevel_width,
                material=titanium,
                registry=registry,
            )

        if props.generate_braces:
            brace_radius = (
                arm_start_radius
                + props.arm_length * props.brace_radius_scale
            )
            create_cross_brace_array(
                collection=collection,
                origin=support_origin,
                arm_count=props.arm_count,
                brace_radius=brace_radius,
                brace_profile=props.brace_profile,
                brace_width=props.brace_width,
                brace_height=props.brace_height,
                centre_z=support_origin.z,
                bevel_width=props.bevel_width,
                material=dark,
                registry=registry,
            )

    for obj in registry.all_objects():
        if obj is not root:
            obj.parent = root

    bpy.ops.object.select_all(action='DESELECT')
    root.select_set(True)
    context.view_layer.objects.active = root
    return registry
