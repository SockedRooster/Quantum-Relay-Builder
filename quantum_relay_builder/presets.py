PRESETS = {
    "QR100": {
        "label": "QR-100 Pathfinder",
        "reflector_rings": 1,
        "panel_radius": 1.24,
        "panel_gap": 0.10,
        "reflector_curvature": 0.022,
        "edge_ring_width": 0.26,
        "edge_ring_height": 0.18,
        "edge_ring_segments": 12,
        "arm_count": 6,
        "hub_radius": 0.72,
        "hub_height": 0.42,
        "arm_length": 4.80,
        "arm_width_hub": 0.34,
        "arm_width_outer": 0.54,
        "brace_radius_scale": 0.58,
    },
    "QR250": {
        "label": "QR-250 Voyager",
        "reflector_rings": 2,
        "panel_radius": 1.10,
        "panel_gap": 0.09,
        "reflector_curvature": 0.016,
        "edge_ring_width": 0.34,
        "edge_ring_height": 0.24,
        "edge_ring_segments": 18,
        "arm_count": 8,
        "hub_radius": 0.96,
        "hub_height": 0.54,
        "arm_length": 7.20,
        "arm_width_hub": 0.44,
        "arm_width_outer": 0.72,
        "brace_radius_scale": 0.62,
    },
    "QR500": {
        "label": "QR-500 Event Horizon",
        "reflector_rings": 3,
        "panel_radius": 1.00,
        "panel_gap": 0.08,
        "reflector_curvature": 0.011,
        "edge_ring_width": 0.44,
        "edge_ring_height": 0.32,
        "edge_ring_segments": 24,
        "arm_count": 12,
        "hub_radius": 1.28,
        "hub_height": 0.72,
        "arm_length": 10.60,
        "arm_width_hub": 0.58,
        "arm_width_outer": 0.94,
        "brace_radius_scale": 0.66,
    },
}


def apply_preset(props, preset_id):
    values = PRESETS.get(preset_id)
    if values is None:
        raise ValueError(f"Unknown Quantum Relay preset: {preset_id}")

    for property_name, value in values.items():
        if property_name == "label":
            continue
        setattr(props, property_name, value)

    props.preset = preset_id
    return values["label"]
