from bpy.types import Operator

from .geometry.assembly import build_sprint5_assembly
from .geometry.collections import clear_generated_collection


class QR_OT_build_sprint5(Operator):
    bl_idname = "qr.build_sprint5"
    bl_label = "Build Sprint 5 Relay"
    bl_description = "Generate the integrated relay structure"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.qr_builder

        try:
            registry = build_sprint5_assembly(context, props)
        except Exception as exc:
            self.report({'ERROR'}, f"Quantum Relay build failed: {exc}")
            return {'CANCELLED'}

        counts = registry.counts()
        self.report(
            {'INFO'},
            (
                f"Generated {counts.get('panel_frame', 0)} panels, "
                f"{counts.get('mount', 0)} mounts, "
                f"{counts.get('gusset', 0)} gussets and "
                f"{counts.get('cross_brace', 0)} braces"
            ),
        )
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
