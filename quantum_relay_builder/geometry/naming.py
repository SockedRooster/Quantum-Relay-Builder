ROOT = "QR_Assembly_Root"
COLLECTION = "QuantumRelay_Generated"


def panel_frame(index):
    return f"QR_Panel_{index:02d}_Frame"


def panel_reflector(index):
    return f"QR_Panel_{index:02d}_Reflector"


def arm(index, component):
    return f"QR_Arm_{index:02d}_{component}"


def hub(component):
    return f"QR_Hub_{component}"
