from bpy.types import Panel
from .version import BUILD_LABEL


class QR_PT_builder(Panel):
    bl_label = "Quantum Relay Builder"
    bl_idname = "QR_PT_builder"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Quantum Relay"

    def draw(self, context):
        layout = self.layout
        props = context.scene.qr_builder

        layout.label(text=BUILD_LABEL)
        layout.label(text="BMesh framework milestone", icon='MESH_DATA')

        family = layout.box()
        family.label(text="Relay Family")
        family.prop(props, "preset")
        family.operator("qr.apply_preset", icon='PRESET')

        reflector = layout.box()
        reflector.label(text="Reflector")
        reflector.prop(props, "reflector_rings")
        reflector.prop(props, "panel_radius")
        reflector.prop(props, "panel_gap")
        reflector.prop(props, "panel_thickness")
        reflector.prop(props, "panel_frame_width")
        reflector.prop(props, "reflector_inset")
        reflector.prop(props, "reflector_thickness")
        reflector.prop(props, "reflector_curvature")
        reflector.prop(props, "tilt_panels")

        edge_ring = layout.box()
        edge_ring.label(text="Structural Edge Ring")
        edge_ring.prop(props, "generate_edge_ring")
        ring_column = edge_ring.column()
        ring_column.enabled = props.generate_edge_ring
        ring_column.prop(props, "edge_ring_clearance")
        ring_column.prop(props, "edge_ring_width")
        ring_column.prop(props, "edge_ring_height")
        ring_column.prop(props, "edge_ring_segments")
        ring_column.prop(props, "edge_ring_gap_angle")
        ring_column.prop(props, "edge_ring_rib_width")
        ring_column.prop(props, "edge_ring_rib_height")

        structure = layout.box()
        structure.label(text="Hub and Support Arms")
        structure.prop(props, "generate_structure")
        column = structure.column()
        column.enabled = props.generate_structure
        column.prop(props, "arm_count")
        column.prop(props, "hub_radius")
        column.prop(props, "hub_height")
        column.prop(props, "hub_ring_height")
        column.prop(props, "core_radius")
        column.prop(props, "core_height")
        column.label(text="Arm length: derived from support ring", icon='DRIVER_DISTANCE')
        column.prop(props, "arm_width_hub")
        column.prop(props, "arm_width_outer")
        column.prop(props, "arm_thickness")
        column.prop(props, "arm_gap")
        column.prop(props, "arm_ring_clearance")
        column.prop(props, "channel_width")
        column.prop(props, "channel_height")

        integration = layout.box()
        integration.label(text="Structure Detail")
        integration.prop(props, "generate_mounts")
        mounts = integration.column()
        mounts.enabled = props.generate_structure and props.generate_mounts
        mounts.prop(props, "mount_length")
        mounts.prop(props, "mount_width_scale")
        mounts.prop(props, "mount_height")
        mounts.prop(props, "clamp_height")

        integration.separator()
        integration.prop(props, "generate_gussets")
        gussets = integration.column()
        gussets.enabled = props.generate_structure and props.generate_gussets
        gussets.prop(props, "gusset_length")
        gussets.prop(props, "gusset_height")
        gussets.prop(props, "gusset_thickness")

        integration.separator()
        integration.prop(props, "generate_braces")
        braces = integration.column()
        braces.enabled = props.generate_structure and props.generate_braces
        braces.prop(props, "brace_profile")
        braces.prop(props, "brace_radius_scale")
        braces.prop(props, "brace_width")
        braces.prop(props, "brace_height")

        detail = layout.box()
        detail.label(text="Global Detail")
        detail.prop(props, "bevel_width")

        diagnostics = layout.box()
        diagnostics.label(text="Diagnostics", icon='INFO')
        diagnostics.prop(props, "diagnostic_logging")
        diagnostic_column = diagnostics.column()
        diagnostic_column.enabled = props.diagnostic_logging
        diagnostic_column.prop(props, "diagnostic_length_multiplier")
        diagnostic_column.label(text="Log saves beside the .blend file")
        diagnostic_column.label(text="Unsaved files use the system temp folder")

        layout.separator()
        layout.operator("qr.build_sprint6", icon='MOD_BUILD')
        layout.operator("qr.clear_generated", icon='TRASH')
