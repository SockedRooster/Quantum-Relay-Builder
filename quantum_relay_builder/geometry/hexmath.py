import math


def axial_coordinates(rings):
    coordinates = []
    for q in range(-rings, rings + 1):
        for r in range(max(-rings, -q - rings), min(rings, -q + rings) + 1):
            coordinates.append((q, r))
    coordinates.sort(key=lambda item: (hex_distance(*item), math.atan2(item[1], item[0]) if item != (0, 0) else 0.0))
    return coordinates


def hex_distance(q, r):
    return max(abs(q), abs(r), abs(-q-r))


def axial_to_world(q, r, radius, gap):
    effective = radius + (gap / math.sqrt(3.0))
    return math.sqrt(3.0) * effective * (q + r / 2.0), 1.5 * effective * r


def parabolic_height(x, y, curvature):
    return curvature * (x*x + y*y)


def parabolic_normal(x, y, curvature):
    nx, ny, nz = -2.0*curvature*x, -2.0*curvature*y, 1.0
    length = math.sqrt(nx*nx + ny*ny + nz*nz)
    return nx/length, ny/length, nz/length
