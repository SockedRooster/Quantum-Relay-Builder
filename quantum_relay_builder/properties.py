from bpy.props import BoolProperty, FloatProperty, IntProperty
from bpy.types import PropertyGroup


class QRBuilderProperties(PropertyGroup):
    reflector_rings: IntProperty(
        name="Reflector Rings",
        description="Hex-grid ring count; 1 creates 7 panels, 2 creates 19 panels",
        default=1,
        min=0,
        max=5,
    )

    panel_radius: FloatProperty(
        name="Panel Radius",
        description="Distance from panel centre to a hex corner",
        default=1.24,
        min=0.05,
        soft_max=10.0,
        unit='LENGTH',
    )

    panel_gap: FloatProperty(
        name="Panel Gap",
        description="Gap between neighbouring hex panels",
        default=0.10,
        min=0.0,
        soft_max=1.0,
        unit='LENGTH',
    )

    panel_thickness: FloatProperty(
        name="Panel Thickness",
        description="Thickness of the outer panel frame",
        default=0.12,
        min=0.01,
        soft_max=1.0,
        unit='LENGTH',
    )

    panel_frame_width: FloatProperty(
        name="Frame Width",
        description="Width of the visible panel frame",
        default=0.14,
        min=0.01,
        soft_max=1.0,
        unit='LENGTH',
    )

    reflector_inset: FloatProperty(
        name="Reflector Inset",
        description="Vertical recess of the reflective panel surface",
        default=0.05,
        min=0.0,
        soft_max=0.5,
        unit='LENGTH',
    )

    reflector_thickness: FloatProperty(
        name="Reflector Thickness",
        description="Thickness of each reflective insert",
        default=0.035,
        min=0.005,
        soft_max=0.5,
        unit='LENGTH',
    )

    reflector_curvature: FloatProperty(
        name="Curvature",
        description="Parabolic dish curvature; zero produces a flat reflector",
        default=0.022,
        min=-0.5,
        max=0.5,
    )

    tilt_panels: BoolProperty(
        name="Aim Panels",
        description="Tilt panel normals along the dish surface",
        default=True,
    )

    generate_edge_ring: BoolProperty(
        name="Generate Edge Ring",
        description="Create the segmented structural ring around the reflector",
        default=True,
    )

    edge_ring_clearance: FloatProperty(
        name="Ring Clearance",
        description="Radial clearance between the reflector panels and structural ring",
        default=0.18,
        min=0.0,
        soft_max=2.0,
        unit='LENGTH',
    )

    edge_ring_width: FloatProperty(
        name="Ring Width",
        description="Radial width of the structural edge ring",
        default=0.26,
        min=0.02,
        soft_max=2.0,
        unit='LENGTH',
    )

    edge_ring_height: FloatProperty(
        name="Ring Height",
        description="Vertical thickness of each structural ring segment",
        default=0.18,
        min=0.02,
        soft_max=2.0,
        unit='LENGTH',
    )

    edge_ring_segments: IntProperty(
        name="Ring Segments",
        description="Number of structural segments around the edge ring",
        default=12,
        min=6,
        max=96,
    )

    edge_ring_gap_angle: FloatProperty(
        name="Joint Gap",
        description="Angular gap between neighbouring edge-ring segments",
        default=0.018,
        min=0.0,
        max=0.20,
        subtype='ANGLE',
    )

    edge_ring_rib_width: FloatProperty(
        name="Rib Width",
        description="Tangential width of reinforcement ribs",
        default=0.10,
        min=0.01,
        soft_max=1.0,
        unit='LENGTH',
    )

    edge_ring_rib_height: FloatProperty(
        name="Rib Height",
        description="Height added by the outer reinforcement ribs",
        default=0.08,
        min=0.0,
        soft_max=1.0,
        unit='LENGTH',
    )

    generate_structure: BoolProperty(
        name="Generate Hub and Arms",
        description="Include the support assembly",
        default=True,
    )

    arm_count: IntProperty(
        name="Arm Count",
        description="Number of radial support arms",
        default=6,
        min=3,
        max=24,
    )

    hub_radius: FloatProperty(
        name="Hub Radius",
        default=0.72,
        min=0.05,
        soft_max=5.0,
        unit='LENGTH',
    )

    hub_height: FloatProperty(
        name="Hub Height",
        default=0.42,
        min=0.03,
        soft_max=5.0,
        unit='LENGTH',
    )

    hub_ring_height: FloatProperty(
        name="Hub Ring Height",
        default=0.15,
        min=0.01,
        soft_max=1.0,
        unit='LENGTH',
    )

    core_radius: FloatProperty(
        name="Core Radius",
        default=0.28,
        min=0.03,
        soft_max=2.0,
        unit='LENGTH',
    )

    core_height: FloatProperty(
        name="Core Height",
        default=0.20,
        min=0.02,
        soft_max=1.0,
        unit='LENGTH',
    )

    arm_length: FloatProperty(
        name="Arm Length",
        default=4.80,
        min=0.10,
        soft_max=30.0,
        unit='LENGTH',
    )

    arm_width_hub: FloatProperty(
        name="Width at Hub",
        default=0.34,
        min=0.03,
        soft_max=3.0,
        unit='LENGTH',
    )

    arm_width_outer: FloatProperty(
        name="Width at Outer End",
        default=0.54,
        min=0.03,
        soft_max=3.0,
        unit='LENGTH',
    )

    arm_thickness: FloatProperty(
        name="Arm Thickness",
        default=0.18,
        min=0.02,
        soft_max=2.0,
        unit='LENGTH',
    )

    arm_gap: FloatProperty(
        name="Hub Gap",
        default=0.05,
        min=0.0,
        soft_max=1.0,
        unit='LENGTH',
    )

    rail_width: FloatProperty(
        name="Rail Width",
        default=0.085,
        min=0.01,
        soft_max=0.5,
        unit='LENGTH',
    )

    rail_height: FloatProperty(
        name="Rail Height",
        default=0.07,
        min=0.005,
        soft_max=0.5,
        unit='LENGTH',
    )

    channel_width: FloatProperty(
        name="Channel Width",
        default=0.14,
        min=0.02,
        soft_max=1.0,
        unit='LENGTH',
    )

    channel_height: FloatProperty(
        name="Channel Height",
        default=0.025,
        min=0.002,
        soft_max=0.2,
        unit='LENGTH',
    )

    bevel_width: FloatProperty(
        name="Bevel Width",
        default=0.035,
        min=0.0,
        soft_max=0.25,
        unit='LENGTH',
    )
