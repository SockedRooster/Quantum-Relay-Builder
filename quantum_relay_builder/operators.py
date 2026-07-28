from bpy.types import Operator

from .geometry.assembly import build_sprint5_assembly
from .geometry.collections import clear_generated_collection
from .geometry.stats import collect_mesh_statistics
from .presets import apply_preset
from .diagnostics import configure


class QR_OT_apply_preset(Operator):
    bl_idname = "qr.apply_preset"
    bl_label = "Apply Relay Preset"
    bl_description = "Load the selected Quantum Relay family dimensions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.qr_builder

        if props.preset == "CUSTOM":
            self.report({'INFO'}, "Custom mode leaves current dimensions unchanged")
            return {'FINISHED'}

        try:
            label = apply_preset(props, props.preset)
        except Exception as exc:
            self.report({'ERROR'}, f"Preset failed: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Applied {label}")
        return {'FINISHED'}


class QR_OT_build_sprint6(Operator):
    bl_idname = "qr.build_sprint6"
    bl_label = "Build Quantum Relay"
    bl_description = "Generate the relay using the Sprint 6 BMesh framework"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.qr_builder

        try:
            expected_beam_length = max(
                props.arm_length,
                props.panel_radius * (props.reflector_rings * 2 + 3),
            ) * props.diagnostic_length_multiplier
            configure(props.diagnostic_logging, expected_beam_length)
            registry = build_sprint5_assembly(context, props)
            stats = collect_mesh_statistics(registry)
            warnings = getattr(registry, 'build_warnings', [])
        except Exception as exc:
            self.report({'ERROR'}, f"Quantum Relay build failed: {exc}")
            return {'CANCELLED'}

        log_path = getattr(registry, "diagnostic_log_path", "")
        message = (
                f"Generated {stats['objects']} mesh objects, "
                f"{stats['vertices']} vertices and "
                f"{stats['polygons']} polygons; "
                f"arm length {getattr(registry, 'effective_arm_length', 0.0):.2f}; "
                f"{len(warnings)} warning(s)"
        )
        if log_path:
            message += f"; diagnostic log: {log_path}"
        self.report({'INFO'}, message)
        return {'FINISHED'}


class QR_OT_clear_generated(Operator):
    bl_idname = "qr.clear_generated"
    bl_label = "Clear Generated Assembly"
    bl_description = "Delete only the generated Quantum Relay collection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        clear_generated_collection()
        self.report({'INFO'}, "Generated assembly cleared")
        return {'FINISHED'}
