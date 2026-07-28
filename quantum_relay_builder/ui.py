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
        layout.label(text="Large-scale QR-100 baseline", icon='OUTLINER_OB_SURFACE')

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
