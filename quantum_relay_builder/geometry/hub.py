from .primitives import create_cylinder
from . import naming


def create_layered_hub(collection, origin, hub_radius, hub_height, ring_height,
                       core_radius, core_height, bevel_width,
                       titanium_material, dark_material, energy_material):
    z = origin.z
    return [
        create_cylinder(naming.hub("Base"), hub_radius, hub_height, (origin.x,origin.y,z),
                        collection, dark_material, bevel_width),
        create_cylinder(naming.hub("LowerRing"), hub_radius*1.08, ring_height,
                        (origin.x,origin.y,z-hub_height/2+ring_height/2),
                        collection, titanium_material, bevel_width),
        create_cylinder(naming.hub("UpperRing"), hub_radius*0.78, ring_height,
                        (origin.x,origin.y,z+hub_height/2+ring_height/2),
                        collection, titanium_material, bevel_width),
        create_cylinder("QR_Quantum_Core", core_radius, core_height,
                        (origin.x,origin.y,z+hub_height/2+ring_height+core_height/2),
                        collection, energy_material, min(bevel_width, core_radius*0.2)),
    ]
