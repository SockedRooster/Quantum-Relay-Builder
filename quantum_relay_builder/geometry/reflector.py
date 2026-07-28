from .hexmath import axial_coordinates, axial_to_world, parabolic_height, parabolic_normal
from .panels import create_hex_panel


def create_reflector_array(
    collection,
    origin,
    rings,
    panel_radius,
    panel_gap,
    panel_thickness,
    frame_width,
    reflector_inset,
    reflector_thickness,
    curvature,
    tilt_panels,
    bevel_width,
    frame_material,
    reflector_material,
    registry,
):
    centres = []

    for index, (q, r) in enumerate(axial_coordinates(rings), start=1):
        x, y = axial_to_world(q, r, panel_radius, panel_gap)
        z = parabolic_height(x, y, curvature)
        normal = parabolic_normal(x, y, curvature) if tilt_panels else (0, 0, 1)
        centre = (origin.x + x, origin.y + y, origin.z + z)

        frame, reflector = create_hex_panel(
            index,
            collection,
            centre,
            normal,
            panel_radius,
            panel_thickness,
            frame_width,
            reflector_inset,
            reflector_thickness,
            bevel_width,
            frame_material,
            reflector_material,
        )

        registry.add("panel_frame", frame)
        registry.add("reflector", reflector)
        centres.append((x, y, z))

    maximum_centre_radius = max(
        ((x * x) + (y * y)) ** 0.5
        for x, y, _ in centres
    )

    return {
        "panel_count": len(centres),
        "maximum_centre_radius": maximum_centre_radius,
        "outer_radius": maximum_centre_radius + panel_radius,
    }
