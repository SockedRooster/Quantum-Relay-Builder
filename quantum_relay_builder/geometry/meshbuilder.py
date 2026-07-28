"""
Compatibility layer for the Sprint 5 geometry modules.

The public function remains stable while construction is now handled by the
operator-free BMesh framework in quantum_relay_builder.mesh.
"""

from ..mesh.prism import create_prism


def create_prism_mesh(
    name,
    collection,
    bottom_loop,
    top_loop,
    bevel_width=0.0,
    material=None,
):
    return create_prism(
        name=name,
        collection=collection,
        bottom_loop=bottom_loop,
        top_loop=top_loop,
        bevel_width=bevel_width,
        material=material,
    )
