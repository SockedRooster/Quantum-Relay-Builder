from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import PropertyGroup


PRESET_ITEMS = (
    ("QR100", "QR-100", "Compact Pathfinder relay"),
    ("QR250", "QR-250", "Medium Voyager relay"),
    ("QR500", "QR-500", "Large Event Horizon relay"),
    ("CUSTOM", "Custom", "Manually edited parameters"),
)

PROFILE_ITEMS = (
    ("BOX", "Box Beam", "Rectangular solid beam"),
    ("DIAMOND", "Diamond Beam", "Rotated rectangular beam"),
    ("HEX", "Hex Beam", "Six-sided structural beam"),
)


class QRBuilderProperties(PropertyGroup):
    preset: EnumProperty(
        name="Relay Family",
        items=PRESET_ITEMS,
        default="QR100",
    )

    reflector_rings: IntProperty(
        name="Reflector Rings",
        description="Hex-grid ring count; 1 creates 7 panels, 2 creates 19 panels",
        default=1,
        min=0,
        max=5,
    )
    panel_radius: FloatProperty(
        name="Panel Radius", default=1.488, min=0.05, soft_max=10.0, unit='LENGTH'
    )
    panel_gap: FloatProperty(
        name="Panel Gap", default=0.10, min=0.0, soft_max=1.0, unit='LENGTH'
    )
    panel_thickness: FloatProperty(
        name="Panel Thickness", default=0.12, min=0.01, soft_max=1.0, unit='LENGTH'
    )
    panel_frame_width: FloatProperty(
        name="Frame Width", default=0.14, min=0.01, soft_max=1.0, unit='LENGTH'
    )
    reflector_inset: FloatProperty(
        name="Reflector Inset", default=0.05, min=0.0, soft_max=0.5, unit='LENGTH'
    )
    reflector_thickness: FloatProperty(
        name="Reflector Thickness", default=0.035, min=0.005, soft_max=0.5, unit='LENGTH'
    )
    reflector_curvature: FloatProperty(
        name="Curvature", default=0.022, min=-0.5, max=0.5
    )
    tilt_panels: BoolProperty(name="Aim Panels", default=True)

    generate_edge_ring: BoolProperty(name="Generate Edge Ring", default=True)
    edge_ring_clearance: FloatProperty(
        name="Ring Clearance", default=0.18, min=0.0, soft_max=2.0, unit='LENGTH'
    )
    edge_ring_width: FloatProperty(
        name="Ring Width", default=0.26, min=0.02, soft_max=2.0, unit='LENGTH'
    )
    edge_ring_height: FloatProperty(
        name="Ring Height", default=0.18, min=0.02, soft_max=2.0, unit='LENGTH'
    )
    edge_ring_segments: IntProperty(name="Ring Segments", default=12, min=6, max=96)
    edge_ring_gap_angle: FloatProperty(
        name="Joint Gap", default=0.018, min=0.0, max=0.20, subtype='ANGLE'
    )
    edge_ring_rib_width: FloatProperty(
        name="Rib Width", default=0.10, min=0.01, soft_max=1.0, unit='LENGTH'
    )
    edge_ring_rib_height: FloatProperty(
        name="Rib Height", default=0.08, min=0.0, soft_max=1.0, unit='LENGTH'
    )

    generate_structure: BoolProperty(name="Generate Hub and Arms", default=True)
    arm_count: IntProperty(name="Arm Count", default=6, min=3, max=24)
    hub_radius: FloatProperty(
        name="Hub Radius", default=0.72, min=0.05, soft_max=5.0, unit='LENGTH'
    )
    hub_height: FloatProperty(
        name="Hub Height", default=0.42, min=0.03, soft_max=5.0, unit='LENGTH'
    )
    hub_ring_height: FloatProperty(
        name="Hub Ring Height", default=0.15, min=0.01, soft_max=1.0, unit='LENGTH'
    )
    core_radius: FloatProperty(
        name="Core Radius", default=0.28, min=0.03, soft_max=2.0, unit='LENGTH'
    )
    core_height: FloatProperty(
        name="Core Height", default=0.20, min=0.02, soft_max=1.0, unit='LENGTH'
    )
    arm_length: FloatProperty(
        name="Legacy Arm Length",
        description="Retained for preset compatibility; support length is now derived from the ring",
        default=4.80,
        min=0.10,
        soft_max=30.0,
        unit='LENGTH',
        options={'HIDDEN'},
    )
    arm_width_hub: FloatProperty(
        name="Width at Hub", default=0.34, min=0.03, soft_max=3.0, unit='LENGTH'
    )
    arm_width_outer: FloatProperty(
        name="Width at Outer End", default=0.54, min=0.03, soft_max=3.0, unit='LENGTH'
    )
    arm_thickness: FloatProperty(
        name="Arm Thickness", default=0.18, min=0.02, soft_max=2.0, unit='LENGTH'
    )
    arm_gap: FloatProperty(
        name="Hub Gap", default=0.05, min=0.0, soft_max=1.0, unit='LENGTH'
    )
    arm_ring_clearance: FloatProperty(
        name="Arm Ring Clearance",
        description="Vertical clearance above the edge ring at the arm attachment",
        default=0.08,
        min=0.0,
        soft_max=1.0,
        unit='LENGTH',
    )
    rail_width: FloatProperty(
        name="Rail Width", default=0.085, min=0.01, soft_max=0.5, unit='LENGTH'
    )
    rail_height: FloatProperty(
        name="Rail Height", default=0.07, min=0.005, soft_max=0.5, unit='LENGTH'
    )
    channel_width: FloatProperty(
        name="Channel Width", default=0.14, min=0.02, soft_max=1.0, unit='LENGTH'
    )
    channel_height: FloatProperty(
        name="Channel Height", default=0.025, min=0.002, soft_max=0.2, unit='LENGTH'
    )

    generate_mounts: BoolProperty(name="Mount Blocks", default=True)
    mount_length: FloatProperty(
        name="Mount Length", default=0.42, min=0.05, soft_max=2.0, unit='LENGTH'
    )
    mount_width_scale: FloatProperty(
        name="Mount Width Scale", default=1.28, min=0.5, max=3.0
    )
    mount_height: FloatProperty(
        name="Mount Height", default=0.24, min=0.03, soft_max=1.0, unit='LENGTH'
    )
    clamp_height: FloatProperty(
        name="Clamp Height", default=0.10, min=0.01, soft_max=0.5, unit='LENGTH'
    )

    generate_gussets: BoolProperty(name="Gussets", default=True)
    gusset_length: FloatProperty(
        name="Gusset Length", default=0.62, min=0.05, soft_max=3.0, unit='LENGTH'
    )
    gusset_height: FloatProperty(
        name="Gusset Height", default=0.25, min=0.02, soft_max=2.0, unit='LENGTH'
    )
    gusset_thickness: FloatProperty(
        name="Gusset Thickness", default=0.07, min=0.01, soft_max=0.5, unit='LENGTH'
    )

    generate_braces: BoolProperty(name="Cross Braces", default=True)
    brace_profile: EnumProperty(
        name="Brace Profile",
        items=PROFILE_ITEMS,
        default="HEX",
    )
    brace_radius_scale: FloatProperty(
        name="Brace Radius", default=0.58, min=0.15, max=0.95
    )
    brace_width: FloatProperty(
        name="Brace Width", default=0.10, min=0.01, soft_max=1.0, unit='LENGTH'
    )
    brace_height: FloatProperty(
        name="Brace Height", default=0.10, min=0.01, soft_max=1.0, unit='LENGTH'
    )

    diagnostic_logging: BoolProperty(
        name="Diagnostic Logging",
        description="Write beam coordinates, transforms and bounds to a JSON log",
        default=False,
    )
    diagnostic_length_multiplier: FloatProperty(
        name="Beam Length Warning",
        description="Flag beams longer than this multiple of the calculated arm length",
        default=2.0,
        min=1.0,
        max=20.0,
    )

    bevel_width: FloatProperty(
        name="Bevel Width", default=0.035, min=0.0, soft_max=0.25, unit='LENGTH'
    )
