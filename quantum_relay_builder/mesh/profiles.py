import math


def box_profile(width, height):
    half_width = width / 2.0
    half_height = height / 2.0
    return [
        (-half_width, -half_height),
        (half_width, -half_height),
        (half_width, half_height),
        (-half_width, half_height),
    ]


def diamond_profile(width, height):
    return [
        (0.0, -height / 2.0),
        (width / 2.0, 0.0),
        (0.0, height / 2.0),
        (-width / 2.0, 0.0),
    ]


def hex_profile(width, height):
    half_width = width / 2.0
    half_height = height / 2.0
    shoulder = half_width * 0.52
    return [
        (-shoulder, -half_height),
        (shoulder, -half_height),
        (half_width, 0.0),
        (shoulder, half_height),
        (-shoulder, half_height),
        (-half_width, 0.0),
    ]


def regular_polygon_profile(radius, sides, rotation=0.0):
    if sides < 3:
        raise ValueError("A polygon profile requires at least three sides")

    return [
        (
            radius * math.cos(rotation + (2.0 * math.pi * index / sides)),
            radius * math.sin(rotation + (2.0 * math.pi * index / sides)),
        )
        for index in range(sides)
    ]


def get_profile(profile_id, width, height):
    profiles = {
        "BOX": box_profile,
        "DIAMOND": diamond_profile,
        "HEX": hex_profile,
    }

    try:
        factory = profiles[profile_id]
    except KeyError as exc:
        raise ValueError(f"Unknown beam profile: {profile_id}") from exc

    return factory(width, height)
