import bpy


def _material(name, base, metallic, roughness, emission=None):
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
    material.use_nodes = True
    node = material.node_tree.nodes.get("Principled BSDF")
    if node:
        node.inputs["Base Color"].default_value = (*base, 1.0)
        node.inputs["Metallic"].default_value = metallic
        node.inputs["Roughness"].default_value = roughness
        if emission and "Emission Color" in node.inputs:
            node.inputs["Emission Color"].default_value = (*emission, 1.0)
            node.inputs["Emission Strength"].default_value = 4.0
    return material


def get_titanium_material():
    return _material("QR_Titanium", (0.18, 0.21, 0.25), 0.90, 0.26)


def get_dark_metal_material():
    return _material("QR_DarkMetal", (0.035, 0.045, 0.06), 0.72, 0.34)


def get_quantum_energy_material():
    return _material("QR_QuantumEnergy", (0.01, 0.18, 0.30), 0.10, 0.18, (0.0, 0.45, 1.0))


def get_reflector_material():
    return _material("QR_Reflector", (0.08, 0.17, 0.23), 0.55, 0.16)
