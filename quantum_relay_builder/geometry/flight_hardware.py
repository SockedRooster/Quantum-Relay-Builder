import math
import bpy
from mathutils import Vector

from .primitives import create_cylinder, add_bevel_modifier, assign_material
from ..mesh.beam import create_profile_beam


def _move_to_collection(obj, collection):
    for source in list(obj.users_collection):
        source.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def _create_cone(name, collection, radius1, radius2, depth, location, material, bevel_width, vertices=48):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        end_fill_type='NGON',
        location=location,
    )
    obj = bpy.context.active_object
    obj.name = name
    _move_to_collection(obj, collection)
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    add_bevel_modifier(obj, min(bevel_width, min(radius1, max(radius2, 0.01)) * 0.18))
    assign_material(obj, material)
    return obj


def _beam(name, collection, start, end, width, material, bevel_width):
    return create_profile_beam(
        name=name,
        collection=collection,
        start=start,
        end=end,
        profile_id='BOX',
        width=width,
        height=width,
        bevel_width=min(bevel_width, width * 0.20),
        material=material,
        up_hint=(0.0, 0.0, 1.0),
    )


def create_mounting_interface(
    collection, origin, hub_radius, hub_height, flange_radius_scale,
    flange_height, bolt_count, bolt_radius, bolt_circle_scale,
    bevel_width, dark_material, titanium_material, registry,
):
    """Create a self-contained KSP-style attachment flange below the relay."""
    flange_radius = hub_radius * flange_radius_scale
    flange_z = origin.z - hub_height * 0.5 - flange_height * 0.5

    flange = create_cylinder(
        'QR_Relay_Base_MountingFlange', flange_radius, flange_height,
        (origin.x, origin.y, flange_z), collection, dark_material, bevel_width,
    )
    registry.add('mounting_interface', flange)

    collar_height = flange_height * 0.55
    collar = create_cylinder(
        'QR_Relay_Base_AdapterCollar', hub_radius * 0.82, collar_height,
        (origin.x, origin.y, flange_z - flange_height * 0.5 - collar_height * 0.5),
        collection, titanium_material, bevel_width,
    )
    registry.add('mounting_interface', collar)

    count = max(int(bolt_count), 4)
    circle_radius = flange_radius * bolt_circle_scale
    bolt_depth = flange_height * 0.34
    for index in range(count):
        angle = (math.tau * index) / count
        x = origin.x + math.cos(angle) * circle_radius
        y = origin.y + math.sin(angle) * circle_radius
        z = flange_z + flange_height * 0.5 + bolt_depth * 0.35
        bolt = create_cylinder(
            f'QR_Relay_Base_Bolt_{index + 1:02d}', bolt_radius, bolt_depth,
            (x, y, z), collection, titanium_material,
            min(bevel_width, bolt_radius * 0.25), vertices=24,
        )
        registry.add('fastener', bolt)

    # Two compact umbilical ports make the base read as a spacecraft payload.
    for index, lateral in enumerate((-1.0, 1.0), start=1):
        port = create_cylinder(
            f'QR_Relay_Base_Umbilical_{index:02d}',
            bolt_radius * 1.65, flange_height * 0.42,
            (origin.x + lateral * flange_radius * 0.48,
             origin.y - flange_radius * 0.46,
             flange_z + flange_height * 0.48),
            collection, titanium_material,
            min(bevel_width, bolt_radius * 0.25), vertices=24,
        )
        registry.add('umbilical', port)


def create_feed_assembly(
    collection, origin, hub_radius, hub_height, ring_height,
    feed_height, horn_radius, horn_length, strut_count, strut_width,
    bevel_width, dark_material, titanium_material, energy_material, registry,
):
    """Create an animation-ready feed horn and tripod above the central hub."""
    hub_top = origin.z + hub_height * 0.5 + ring_height
    mast_height = max(feed_height * 0.55, horn_length * 1.4)
    mast = create_cylinder(
        'QR_Feed_Waveguide', horn_radius * 0.28, mast_height,
        (origin.x, origin.y, hub_top + mast_height * 0.5),
        collection, titanium_material, min(bevel_width, horn_radius * 0.08), vertices=32,
    )
    registry.add('feed', mast)

    horn_z = hub_top + feed_height
    horn = _create_cone(
        'QR_Feed_Horn', collection,
        horn_radius * 0.42, horn_radius, horn_length,
        (origin.x, origin.y, horn_z), energy_material, bevel_width,
    )
    registry.add('feed', horn)

    secondary = create_cylinder(
        'QR_Feed_SecondaryReflector', horn_radius * 0.68, horn_length * 0.14,
        (origin.x, origin.y, horn_z + horn_length * 0.62),
        collection, dark_material, min(bevel_width, horn_radius * 0.08), vertices=48,
    )
    registry.add('feed', secondary)

    tripod_radius = hub_radius * 0.66
    strut_top = Vector((origin.x, origin.y, horn_z - horn_length * 0.18))
    for index in range(max(int(strut_count), 3)):
        angle = math.tau * index / max(int(strut_count), 3)
        start = Vector((
            origin.x + math.cos(angle) * tripod_radius,
            origin.y + math.sin(angle) * tripod_radius,
            hub_top + ring_height * 0.18,
        ))
        strut = _beam(
            f'QR_Feed_Support_{index + 1:02d}', collection,
            start, strut_top, strut_width, titanium_material, bevel_width,
        )
        registry.add('feed_support', strut)


def create_cable_harness(
    collection, nodes, cable_radius, clamp_count,
    bevel_width, cable_material, clamp_material, registry,
):
    """Run one visible service harness along the first structural truss."""
    if not nodes:
        return
    node = nodes[0]
    start = Vector(node['hub'])
    end = Vector(node['ring'])
    tangent = Vector(node['tangent'])
    offset = tangent * cable_radius * 2.5 + Vector((0.0, 0.0, cable_radius * 2.2))
    cable_start = start.lerp(end, 0.05) + offset
    cable_end = start.lerp(end, 0.95) + offset

    cable = _beam(
        'QR_CableHarness_Main', collection, cable_start, cable_end,
        cable_radius * 2.0, cable_material, min(bevel_width, cable_radius * 0.4),
    )
    registry.add('cable', cable)

    count = max(int(clamp_count), 2)
    for index in range(count):
        t = (index + 1) / (count + 1)
        point = cable_start.lerp(cable_end, t)
        clamp = create_cylinder(
            f'QR_CableClamp_{index + 1:02d}', cable_radius * 1.55,
            cable_radius * 1.2, tuple(point), collection, clamp_material,
            min(bevel_width, cable_radius * 0.25), vertices=20,
        )
        registry.add('cable_clamp', clamp)
