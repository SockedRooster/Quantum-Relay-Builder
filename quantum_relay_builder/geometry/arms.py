import math
from mathutils import Vector
from .meshbuilder import create_prism_mesh
from . import naming


def _quad(origin, direction, side, start, length, near_width, far_width, z):
    near = Vector(origin)+direction*start
    far = near+direction*length
    return [
        tuple(near+side*(near_width/2))[:2]+(z,),
        tuple(near-side*(near_width/2))[:2]+(z,),
        tuple(far-side*(far_width/2))[:2]+(z,),
        tuple(far+side*(far_width/2))[:2]+(z,),
    ]


def create_arm(index, collection, origin, angle, start, length, near_width, far_width,
               thickness, rail_width, rail_height, channel_width, channel_height,
               bevel, titanium, dark, energy):
    d = Vector((math.cos(angle), math.sin(angle), 0))
    s = Vector((-math.sin(angle), math.cos(angle), 0))
    bottom, top = origin.z-thickness/2, origin.z+thickness/2

    base = create_prism_mesh(naming.arm(index,"Base"), collection,
        _quad(origin,d,s,start,length,near_width,far_width,bottom),
        _quad(origin,d,s,start,length,near_width,far_width,top), bevel, dark)

    channel = create_prism_mesh(naming.arm(index,"EnergyChannel"), collection,
        _quad(origin,d,s,start+length*0.03,length*0.94,
              min(channel_width,near_width*0.45),min(channel_width*1.18,far_width*0.45),top+channel_height*0.15),
        _quad(origin,d,s,start+length*0.03,length*0.94,
              min(channel_width,near_width*0.45),min(channel_width*1.18,far_width*0.45),top+channel_height*1.15),
        min(bevel,channel_width*0.15), energy)

    return [base, channel]


def create_detailed_arm_array(collection, origin, arm_count, hub_radius, hub_gap,
                              arm_length, width_hub, width_outer, thickness,
                              rail_width, rail_height, channel_width, channel_height,
                              bevel_width, titanium_material, dark_material, energy_material):
    result = []
    start = hub_radius + hub_gap
    for i in range(arm_count):
        result.extend(create_arm(
            i+1, collection, origin, 2*math.pi*i/arm_count, start, arm_length,
            width_hub, width_outer, thickness, rail_width, rail_height,
            channel_width, channel_height, bevel_width,
            titanium_material, dark_material, energy_material
        ))
    return result
