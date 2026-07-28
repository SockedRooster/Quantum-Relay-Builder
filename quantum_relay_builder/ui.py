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
        layout.label(text="Structural edge-ring milestone", icon='MESH_TORUS')

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
        structure.label(text="Support Structure")
        structure.prop(props, "generate_structure")

        column = structure.column()
        column.enabled = props.generate_structure
        column.prop(props, "arm_count")
        column.prop(props, "hub_radius")
        column.prop(props, "hub_height")
        column.prop(props, "hub_ring_height")
        column.prop(props, "core_radius")
        column.prop(props, "core_height")
        column.prop(props, "arm_length")
        column.prop(props, "arm_width_hub")
        column.prop(props, "arm_width_outer")
        column.prop(props, "arm_thickness")
        column.prop(props, "arm_gap")
        column.prop(props, "rail_width")
        column.prop(props, "rail_height")
        column.prop(props, "channel_width")
        column.prop(props, "channel_height")

        detail = layout.box()
        detail.label(text="Global Detail")
        detail.prop(props, "bevel_width")

        layout.separator()
        layout.operator("qr.build_sprint5", icon='MOD_BUILD')
        layout.operator("qr.clear_generated", icon='TRASH')
