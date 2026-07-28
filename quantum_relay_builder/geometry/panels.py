import math
from mathutils import Vector
from .meshbuilder import create_prism_mesh
from . import naming


def _hex_loop(radius, z):
    return [
        (radius*math.cos(math.radians(30+60*i)),
         radius*math.sin(math.radians(30+60*i)), z)
        for i in range(6)
    ]


def _orient(obj, location, normal):
    obj.location = location
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector((0,0,1)).rotation_difference(Vector(normal))


def create_hex_panel(index, collection, centre, normal, panel_radius, panel_thickness,
                     frame_width, reflector_inset, reflector_thickness, bevel_width,
                     frame_material, reflector_material):
    inner = max(panel_radius-frame_width, panel_radius*0.2)
    frame = create_prism_mesh(
        naming.panel_frame(index), collection,
        _hex_loop(panel_radius, -panel_thickness/2),
        _hex_loop(panel_radius, panel_thickness/2),
        min(bevel_width, panel_thickness*0.35), frame_material
    )
    top = panel_thickness/2-reflector_inset
    reflector = create_prism_mesh(
        naming.panel_reflector(index), collection,
        _hex_loop(inner, top-reflector_thickness),
        _hex_loop(inner, top),
        min(bevel_width, reflector_thickness*0.3), reflector_material
    )
    _orient(frame, centre, normal)
    _orient(reflector, centre, normal)
    return frame, reflector
