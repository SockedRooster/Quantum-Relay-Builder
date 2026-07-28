"""Authoritative support attachment calculations for Sprint 6.1.3."""


def calculate_support_attachment(
    reflector_outer_radius,
    ring_metrics,
    hub_radius,
    hub_gap,
):
    """Return validated radii used by arms, mounts, gussets and braces.

    The arm endpoint is derived only from actual reflector/ring dimensions.
    The legacy `arm_length` setting is intentionally not used as an endpoint.
    """
    arm_start_radius = max(0.0, float(hub_radius) + float(hub_gap))

    if ring_metrics is not None:
        inner = float(ring_metrics["inner_radius"])
        outer = float(ring_metrics["outer_radius"])
        if outer < inner:
            inner, outer = outer, inner
        attachment_radius = inner + ((outer - inner) * 0.5)
        structural_outer_radius = outer
        source = "edge_ring_midline"
    else:
        attachment_radius = float(reflector_outer_radius)
        structural_outer_radius = attachment_radius
        source = "reflector_outer_edge"

    minimum_span = 0.05
    attachment_radius = max(attachment_radius, arm_start_radius + minimum_span)

    return {
        "arm_start_radius": arm_start_radius,
        "attachment_radius": attachment_radius,
        "structural_outer_radius": structural_outer_radius,
        "effective_arm_length": attachment_radius - arm_start_radius,
        "source": source,
    }
