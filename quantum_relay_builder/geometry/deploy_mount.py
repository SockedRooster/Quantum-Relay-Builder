import math
import bpy
from mathutils import Vector

from .primitives import create_cylinder, add_bevel_modifier, assign_material
from ..mesh.beam import create_profile_beam


def _empty(name, collection, location, display='PLAIN_AXES', size=0.35):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = display
    obj.empty_display_size = size
    obj.location = location
    collection.objects.link(obj)
    return obj


def _parent_keep_world(obj, parent):
    world = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = world


def _box(name, collection, location, dimensions, material, bevel_width):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    for source in list(obj.users_collection):
        source.objects.unlink(obj)
    collection.objects.link(obj)
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    add_bevel_modifier(obj, min(bevel_width, min(dimensions) * 0.18))
    assign_material(obj, material)
    return obj


def _led_material():
    name = 'QR_StatusLED_Animated'
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
    material.use_nodes = True
    node = material.node_tree.nodes.get('Principled BSDF')
    if node:
        node.inputs['Base Color'].default_value = (0.03, 0.03, 0.03, 1.0)
        node.inputs['Metallic'].default_value = 0.0
        node.inputs['Roughness'].default_value = 0.24
        if 'Emission Color' in node.inputs:
            node.inputs['Emission Color'].default_value = (0.02, 0.02, 0.02, 1.0)
            node.inputs['Emission Strength'].default_value = 0.0
    return material


def _keyframe_led(material, deploy_end_frame, power_on_frame):
    node = material.node_tree.nodes.get('Principled BSDF')
    if not node or 'Emission Color' not in node.inputs:
        return

    colour = node.inputs['Emission Color']
    strength = node.inputs['Emission Strength']

    colour.default_value = (0.02, 0.02, 0.02, 1.0)
    strength.default_value = 0.0
    colour.keyframe_insert('default_value', frame=1)
    strength.keyframe_insert('default_value', frame=1)
    colour.keyframe_insert('default_value', frame=max(deploy_end_frame - 1, 1))
    strength.keyframe_insert('default_value', frame=max(deploy_end_frame - 1, 1))

    colour.default_value = (1.0, 0.28, 0.02, 1.0)
    strength.default_value = 2.5
    colour.keyframe_insert('default_value', frame=deploy_end_frame)
    strength.keyframe_insert('default_value', frame=deploy_end_frame)

    colour.default_value = (0.02, 1.0, 0.12, 1.0)
    strength.default_value = 5.0
    colour.keyframe_insert('default_value', frame=power_on_frame)
    strength.keyframe_insert('default_value', frame=power_on_frame)


def create_deployable_mount(
    collection, registry, relay_objects, support_origin,
    arm_length, arm_width, arm_height, hinge_radius,
    base_radius, base_height, deploy_angle,
    generate_braces, brace_width, brace_spread,
    generate_actuator, actuator_radius,
    deploy_start_frame, deploy_end_frame, power_on_frame,
    bevel_width, dark_material, titanium_material,
):
    """Create an animation-ready fold-out mount and parent the relay payload to it.

    The generated action has two stages:
      1. The player-triggered arm rotates from the stowed angle to 0 degrees.
      2. The status LED changes from off, to amber, to green.
    """
    origin = Vector(support_origin)
    length = max(float(arm_length), hinge_radius * 3.0)
    hinge_location = origin + Vector((-length, 0.0, -base_height * 0.25))

    base = create_cylinder(
        'Relay_Base', base_radius, base_height,
        tuple(hinge_location + Vector((0.0, 0.0, -base_height * 0.5))),
        collection, dark_material, bevel_width, vertices=64,
    )
    registry.add('deploy_mount', base)

    base_collar = create_cylinder(
        'Relay_Base_Collar', base_radius * 0.72, base_height * 0.62,
        tuple(hinge_location + Vector((0.0, 0.0, base_height * 0.18))),
        collection, titanium_material, bevel_width, vertices=48,
    )
    registry.add('deploy_mount', base_collar)

    hinge = _empty('Deploy_Hinge', collection, hinge_location, 'CIRCLE', hinge_radius * 1.5)
    registry.add('animation_pivot', hinge)

    hinge_body = create_cylinder(
        'Deploy_Hinge_Bearing', hinge_radius, arm_width * 1.45,
        tuple(hinge_location), collection, titanium_material, bevel_width, vertices=48,
    )
    hinge_body.rotation_euler.x = math.radians(90.0)
    registry.add('deploy_mount', hinge_body)

    gearbox = _box(
        'Deploy_Hinge_Gearbox', collection,
        tuple(hinge_location + Vector((0.0, -arm_width * 0.95, 0.0))),
        (hinge_radius * 1.25, arm_width * 0.62, hinge_radius * 1.05),
        dark_material, bevel_width,
    )
    registry.add('deploy_mount', gearbox)

    arm_pivot = _empty('Deploy_Arm', collection, hinge_location, 'ARROWS', hinge_radius)
    arm_pivot.parent = hinge
    registry.add('animation_pivot', arm_pivot)

    arm_start = hinge_location + Vector((hinge_radius * 0.9, 0.0, 0.0))
    arm_end = origin + Vector((-hinge_radius * 0.55, 0.0, 0.0))
    upper = create_profile_beam(
        'Deploy_Arm_Upper', collection,
        arm_start + Vector((0.0, 0.0, arm_height * 0.33)),
        arm_end + Vector((0.0, 0.0, arm_height * 0.33)),
        'BOX', arm_width, arm_height * 0.28,
        min(bevel_width, arm_width * 0.15), dark_material, (0.0, 0.0, 1.0),
    )
    lower = create_profile_beam(
        'Deploy_Arm_Lower', collection,
        arm_start - Vector((0.0, 0.0, arm_height * 0.33)),
        arm_end - Vector((0.0, 0.0, arm_height * 0.33)),
        'BOX', arm_width, arm_height * 0.28,
        min(bevel_width, arm_width * 0.15), dark_material, (0.0, 0.0, 1.0),
    )
    registry.add('deploy_arm', upper)
    registry.add('deploy_arm', lower)
    _parent_keep_world(upper, arm_pivot)
    _parent_keep_world(lower, arm_pivot)

    bay_count = 5
    for index in range(bay_count):
        t0 = index / bay_count
        t1 = (index + 1) / bay_count
        p0 = arm_start.lerp(arm_end, t0)
        p1 = arm_start.lerp(arm_end, t1)
        if index % 2 == 0:
            start = p0 + Vector((0.0, 0.0, -arm_height * 0.33))
            end = p1 + Vector((0.0, 0.0, arm_height * 0.33))
        else:
            start = p0 + Vector((0.0, 0.0, arm_height * 0.33))
            end = p1 + Vector((0.0, 0.0, -arm_height * 0.33))
        web = create_profile_beam(
            f'Deploy_Arm_Web_{index + 1:02d}', collection, start, end,
            'BOX', arm_width * 0.42, arm_width * 0.42,
            min(bevel_width, arm_width * 0.08), titanium_material, (0.0, 1.0, 0.0),
        )
        registry.add('deploy_arm', web)
        _parent_keep_world(web, arm_pivot)

    lock = _box(
        'Deploy_Lock', collection,
        tuple(origin + Vector((-hinge_radius * 0.28, 0.0, -arm_height * 0.46))),
        (hinge_radius * 0.75, arm_width * 1.5, arm_height * 0.42),
        titanium_material, bevel_width,
    )
    registry.add('deploy_lock', lock)
    _parent_keep_world(lock, arm_pivot)

    # Sprint 7.1: two visible folding support legs form a rigid triangular
    # load path beneath the arm in the deployed position. They are separate
    # named objects so they can receive dedicated KSP animation later.
    if generate_braces:
        side_offset = max(float(brace_spread), arm_width * 1.35) * 0.5
        leg_start_x = hinge_location.x + hinge_radius * 0.10
        leg_end_x = origin.x - hinge_radius * 0.78
        leg_start_z = hinge_location.z - hinge_radius * 0.72
        leg_end_z = origin.z - arm_height * 0.58
        for side_name, side in (('Left', 1.0), ('Right', -1.0)):
            start = Vector((leg_start_x, side * side_offset, leg_start_z))
            end = Vector((leg_end_x, side * side_offset * 0.72, leg_end_z))
            leg = create_profile_beam(
                f'Deploy_{side_name}_Lock_Brace', collection, start, end,
                'BOX', brace_width, brace_width,
                min(bevel_width, brace_width * 0.16), titanium_material,
                (0.0, 1.0, 0.0),
            )
            registry.add('deploy_brace', leg)
            leg['qr_animation_role'] = 'folding_lock_brace'
            _parent_keep_world(leg, arm_pivot)

            # Clevis blocks at both ends visually explain the pinned joints.
            for suffix, point in (('Base_Clevis', start), ('Arm_Clevis', end)):
                clevis = _box(
                    f'Deploy_{side_name}_{suffix}', collection, tuple(point),
                    (brace_width * 1.9, brace_width * 1.45, brace_width * 1.45),
                    dark_material, min(bevel_width, brace_width * 0.12),
                )
                registry.add('deploy_brace_joint', clevis)
                _parent_keep_world(clevis, arm_pivot)

        cross_tie = create_profile_beam(
            'Deploy_Brace_Cross_Tie', collection,
            Vector((leg_end_x, -side_offset * 0.72, leg_end_z)),
            Vector((leg_end_x, side_offset * 0.72, leg_end_z)),
            'BOX', brace_width * 0.72, brace_width * 0.72,
            min(bevel_width, brace_width * 0.10), dark_material,
            (0.0, 0.0, 1.0),
        )
        registry.add('deploy_brace', cross_tie)
        _parent_keep_world(cross_tie, arm_pivot)

    # Sprint 7.1: a compact screw-jack style actuator under the arm. The
    # housing and exposed rod are kept separate for later export animation.
    if generate_actuator:
        actuator_start = hinge_location + Vector((hinge_radius * 0.30, 0.0, -hinge_radius * 0.88))
        actuator_joint = arm_start.lerp(arm_end, 0.58) + Vector((0.0, 0.0, -arm_height * 0.46))
        split = actuator_start.lerp(actuator_joint, 0.58)
        housing = create_profile_beam(
            'Deploy_Actuator_Housing', collection, actuator_start, split,
            'HEX', actuator_radius * 2.35, actuator_radius * 2.35,
            min(bevel_width, actuator_radius * 0.18), dark_material,
            (0.0, 1.0, 0.0),
        )
        rod = create_profile_beam(
            'Deploy_Actuator_Rod', collection, split, actuator_joint,
            'HEX', actuator_radius * 1.12, actuator_radius * 1.12,
            min(bevel_width, actuator_radius * 0.10), titanium_material,
            (0.0, 1.0, 0.0),
        )
        registry.add('deploy_actuator', housing)
        registry.add('deploy_actuator', rod)
        housing['qr_animation_role'] = 'actuator_body'
        rod['qr_animation_role'] = 'actuator_rod'
        _parent_keep_world(housing, arm_pivot)
        _parent_keep_world(rod, arm_pivot)

        for name, point in (('Deploy_Actuator_Base_Pin', actuator_start), ('Deploy_Actuator_Arm_Pin', actuator_joint)):
            pin = create_cylinder(
                name, actuator_radius * 1.45, max(arm_width * 1.35, actuator_radius * 2.4),
                tuple(point), collection, titanium_material,
                min(bevel_width, actuator_radius * 0.15), vertices=32,
            )
            pin.rotation_euler.x = math.radians(90.0)
            registry.add('deploy_actuator_joint', pin)
            _parent_keep_world(pin, arm_pivot)

    payload = _empty('Relay_Payload', collection, origin, 'CIRCLE', base_radius * 0.75)
    payload.parent = arm_pivot
    registry.add('animation_pivot', payload)

    for obj in relay_objects:
        if obj and obj.name not in {'Relay_Base', 'Relay_Base_Collar'} and obj.parent is None:
            _parent_keep_world(obj, payload)

    electronics = _box(
        'Relay_Electronics_Box', collection,
        tuple(origin + Vector((-base_radius * 0.48, -base_radius * 0.48, -base_height * 0.08))),
        (base_radius * 0.65, base_radius * 0.42, base_height * 0.72),
        dark_material, bevel_width,
    )
    registry.add('electronics', electronics)
    _parent_keep_world(electronics, payload)

    led_material = _led_material()
    led = create_cylinder(
        'Relay_Status_LED', max(base_radius * 0.055, 0.018), max(base_height * 0.10, 0.018),
        tuple(origin + Vector((-base_radius * 0.48, -base_radius * 0.70, base_height * 0.02))),
        collection, led_material, min(bevel_width, base_radius * 0.02), vertices=32,
    )
    led.rotation_euler.x = math.radians(90.0)
    registry.add('indicator', led)
    _parent_keep_world(led, payload)

    stowed_radians = -abs(float(deploy_angle))
    arm_pivot.rotation_mode = 'XYZ'
    arm_pivot.rotation_euler.y = stowed_radians
    arm_pivot.keyframe_insert(data_path='rotation_euler', frame=int(deploy_start_frame))
    arm_pivot.rotation_euler.y = 0.0
    arm_pivot.keyframe_insert(data_path='rotation_euler', frame=int(deploy_end_frame))

    if arm_pivot.animation_data and arm_pivot.animation_data.action:
        arm_pivot.animation_data.action.name = 'QR_DeployRelay'
        for fcurve in arm_pivot.animation_data.action.fcurves:
            for key in fcurve.keyframe_points:
                key.interpolation = 'BEZIER'

    _keyframe_led(led_material, int(deploy_end_frame), int(power_on_frame))

    hinge['qr_animation'] = 'Deploy Relay'
    hinge['qr_stage_1'] = 'Player-triggered deploy arm extension with locking braces and actuator'
    led['qr_stage_2'] = 'Relay power indicator: off -> amber -> green'
    payload['qr_ksp_export_role'] = 'relay_payload'
    base['qr_ksp_attach_node'] = 'bottom'
    base['qr_ksp_animation_clip'] = 'QR_DeployRelay'

    return {
        'base': base,
        'hinge': hinge,
        'arm': arm_pivot,
        'payload': payload,
        'led': led,
    }
