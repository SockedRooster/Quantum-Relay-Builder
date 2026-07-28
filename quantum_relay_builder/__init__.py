bl_info = {
    "name": "Quantum Relay Builder",
    "author": "SockedRooster / OpenAI",
    "version": (2, 0, 2),
    "blender": (5, 2, 0),
    "location": "3D Viewport > Sidebar > Quantum Relay",
    "description": "Procedural modelling framework for Quantum Relay parts",
    "category": "Add Mesh",
}

import bpy

from .properties import QRBuilderProperties
from .operators import (
    QR_OT_apply_preset,
    QR_OT_build_sprint6,
    QR_OT_clear_generated,
)
from .ui import QR_PT_builder


CLASSES = (
    QRBuilderProperties,
    QR_OT_apply_preset,
    QR_OT_build_sprint6,
    QR_OT_clear_generated,
    QR_PT_builder,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.qr_builder = bpy.props.PointerProperty(
        type=QRBuilderProperties
    )


def unregister():
    if hasattr(bpy.types.Scene, "qr_builder"):
        del bpy.types.Scene.qr_builder

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
