from pygame.math import Vector2


def clamp_magnitude(vector: Vector2, max_magnitude: float) -> Vector2:
    if vector.length() > max_magnitude:
        return vector.normalize() * max_magnitude
    return vector


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))
