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
from .arms import create_arm_array_from_nodes
from .mounts import create_mount_array
from .gussets import create_gusset_array
from .braces import create_cross_brace_array
from .validation import validate_generated_assembly
from .support_geometry import calculate_support_attachment
from .support_nodes import build_support_nodes
from .attachment_brackets import create_attachment_brackets
from .naming import ROOT
from ..diagnostics import log_object, write_report


def create_root(collection, location, display_size):
    root = bpy.data.objects.new(ROOT, None)
    root.empty_display_type = 'CIRCLE'
    root.empty_display_size = display_size
    root.location = location
    collection.objects.link(root)
    return root


def _parent_keep_world(obj, root):
    world_matrix = obj.matrix_world.copy()
    obj.parent = root
    obj.matrix_world = world_matrix


def build_sprint5_assembly(context, props):
    clear_generated_collection()
    collection = get_or_create_generated_collection(context)
    registry = PartRegistry()
    cursor = context.scene.cursor.location.copy()

    titanium = get_titanium_material()
    dark = get_dark_metal_material()
    energy = get_quantum_energy_material()
    reflector_material = get_reflector_material()

    root = registry.add("root", create_root(collection, cursor, max(props.panel_radius * 1.25, 0.25)))

    reflector_metrics = create_reflector_array(
        collection=collection, origin=cursor, rings=props.reflector_rings,
        panel_radius=props.panel_radius, panel_gap=props.panel_gap,
        panel_thickness=props.panel_thickness, frame_width=props.panel_frame_width,
        reflector_inset=props.reflector_inset, reflector_thickness=props.reflector_thickness,
        curvature=props.reflector_curvature, tilt_panels=props.tilt_panels,
        bevel_width=props.bevel_width, frame_material=titanium,
        reflector_material=reflector_material, registry=registry,
    )

    ring_metrics = None
    if props.generate_edge_ring:
        ring_metrics = create_structural_edge_ring(
            collection=collection, origin=cursor,
            reflector_outer_radius=reflector_metrics["outer_radius"],
            clearance=props.edge_ring_clearance, ring_width=props.edge_ring_width,
            ring_height=props.edge_ring_height, segment_count=props.edge_ring_segments,
            joint_gap_angle=props.edge_ring_gap_angle, rib_width=props.edge_ring_rib_width,
            rib_height=props.edge_ring_rib_height, bevel_width=props.bevel_width,
            ring_material=dark, rib_material=titanium, registry=registry,
        )

    expected_radius = reflector_metrics["outer_radius"]

    if props.generate_structure:
        # The support hub is intentionally above the reflector. Its lower face
        # clears the panel surface so the hub and arm roots remain visible.
        panel_top_z = cursor.z + (props.panel_thickness / 2.0)
        support_origin = cursor + Vector((
            0.0,
            0.0,
            (props.panel_thickness / 2.0) + 0.32 + (props.hub_height / 2.0),
        ))

        support_metrics = calculate_support_attachment(
            reflector_outer_radius=reflector_metrics["outer_radius"],
            ring_metrics=ring_metrics,
            hub_radius=props.hub_radius,
            hub_gap=props.arm_gap,
        )
        arm_start_radius = support_metrics["arm_start_radius"]
        mount_radius = support_metrics["attachment_radius"]
        effective_arm_length = support_metrics["effective_arm_length"]

        if ring_metrics is not None:
            ring_top_z = cursor.z + (props.edge_ring_height / 2.0)
        else:
            ring_top_z = cursor.z

        expected_radius = support_metrics["structural_outer_radius"] + props.mount_length

        # Fail loudly rather than generating another visually misleading build.
        if mount_radius > expected_radius:
            raise ValueError(
                f"Support attachment radius {mount_radius:.3f} exceeds "
                f"expected assembly radius {expected_radius:.3f}"
            )
        arm_near_centre_z = support_origin.z + (props.hub_height * 0.08)
        arm_far_centre_z = max(
            ring_top_z + props.arm_ring_clearance + (props.arm_thickness / 2.0),
            panel_top_z + 0.20 + (props.arm_thickness / 2.0),
        )

        support_nodes = build_support_nodes(
            origin=support_origin,
            arm_count=props.arm_count,
            hub_attachment_radius=arm_start_radius,
            ring_attachment_radius=mount_radius,
            hub_attachment_z=arm_near_centre_z,
            ring_attachment_z=arm_far_centre_z,
        )

        registry.extend("hub", create_layered_hub(
            collection, support_origin, props.hub_radius, props.hub_height,
            props.hub_ring_height, props.core_radius, props.core_height,
            props.bevel_width, titanium, dark, energy,
        ))

        registry.extend("arm", create_arm_array_from_nodes(
            collection=collection,
            nodes=support_nodes,
            width_hub=props.arm_width_hub,
            width_outer=props.arm_width_outer,
            thickness=props.arm_thickness,
            channel_width=props.channel_width,
            channel_height=props.channel_height,
            bevel_width=props.bevel_width,
            dark_material=dark,
            energy_material=energy,
        ))

        create_attachment_brackets(
            collection=collection,
            nodes=support_nodes,
            arm_width_hub=props.arm_width_hub,
            arm_width_outer=props.arm_width_outer,
            arm_thickness=props.arm_thickness,
            bevel_width=props.bevel_width,
            hub_material=titanium,
            ring_material=dark,
            registry=registry,
        )

        arm_top_z = arm_far_centre_z + (props.arm_thickness / 2.0)
        mount_width = props.arm_width_outer * props.mount_width_scale

        if props.generate_mounts:
            create_mount_array(
                collection=collection, origin=support_origin, arm_count=props.arm_count,
                mount_radius=mount_radius, arm_outer_width=props.arm_width_outer,
                mount_length=props.mount_length, mount_width_scale=props.mount_width_scale,
                mount_height=props.mount_height, clamp_height=props.clamp_height,
                arm_top_z=arm_top_z, ring_top_z=ring_top_z, bevel_width=props.bevel_width,
                base_material=dark, clamp_material=titanium, registry=registry,
                attachment_nodes=support_nodes,
            )

        if props.generate_gussets:
            create_gusset_array(
                collection=collection, origin=support_origin, arm_count=props.arm_count,
                mount_radius=mount_radius, arm_outer_width=props.arm_width_outer,
                mount_width=mount_width, gusset_length=min(props.gusset_length, effective_arm_length * 0.45),
                gusset_height=props.gusset_height, gusset_thickness=props.gusset_thickness,
                arm_top_z=arm_top_z, bevel_width=props.bevel_width,
                material=titanium, registry=registry,
            )

        if props.generate_braces:
            brace_radius = arm_start_radius + effective_arm_length * props.brace_radius_scale
            create_cross_brace_array(
                collection=collection, origin=support_origin, arm_count=props.arm_count,
                brace_radius=brace_radius, brace_profile=props.brace_profile,
                brace_width=props.brace_width, brace_height=props.brace_height,
                centre_z=support_origin.z, bevel_width=props.bevel_width,
                material=dark, registry=registry,
            )

    for obj in registry.all_objects():
        if obj is not root:
            _parent_keep_world(obj, root)

    warnings = validate_generated_assembly(registry, root, expected_radius)
    registry.build_warnings = warnings
    registry.effective_arm_length = locals().get("effective_arm_length", 0.0)

    for generated_object in registry.all_objects():
        log_object(generated_object, root)

    registry.diagnostic_log_path = write_report({
        "version": "2.1.2",
        "sprint": "6.2.2",
        "expected_radius": float(expected_radius),
        "effective_arm_length": float(registry.effective_arm_length),
        "arm_start_radius": float(locals().get("arm_start_radius", 0.0)),
        "arm_attachment_radius": float(locals().get("mount_radius", 0.0)),
        "support_radius_source": locals().get("support_metrics", {}).get("source", ""),
        "reflector_outer_radius": float(reflector_metrics["outer_radius"]),
        "ring_inner_radius": float(ring_metrics["inner_radius"]) if ring_metrics else None,
        "ring_outer_radius": float(ring_metrics["outer_radius"]) if ring_metrics else None,
        "arm_near_centre_z": float(locals().get("arm_near_centre_z", 0.0)),
        "arm_far_centre_z": float(locals().get("arm_far_centre_z", 0.0)),
        "support_node_count": len(locals().get("support_nodes", [])),
        "support_hub_points": [
            [float(value) for value in node["hub"]]
            for node in locals().get("support_nodes", [])
        ],
        "support_ring_points": [
            [float(value) for value in node["ring"]]
            for node in locals().get("support_nodes", [])
        ],
        "object_count": len(registry.all_objects()),
        "warnings": list(warnings),
        "cursor": [float(value) for value in cursor],
        "preset": props.preset,
        "arm_count": int(props.arm_count),
        "reflector_rings": int(props.reflector_rings),
    })

    bpy.ops.object.select_all(action='DESELECT')
    root.select_set(True)
    context.view_layer.objects.active = root
    return registry
