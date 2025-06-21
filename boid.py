from pygame.math import Vector2
from pygame import Surface
from pygame.draw import polygon
from consts import *
from random import uniform
from math import pi, cos, sin, radians
from numpy import array, ndarray, asarray


def clamp_magnitude(vector: Vector2, max_magnitude: float) -> Vector2:
    if vector.length() > max_magnitude:
        return vector.normalize() * max_magnitude
    return vector


class Boid:
    # these are static properties
    cohesion_enabled: bool = True
    alignment_enabled: bool = True
    repulsion_enabled: bool = True

    feature_flags: list[bool] = [
        cohesion_enabled,
        alignment_enabled,
        repulsion_enabled,
    ]

    def __init__(self, position: Vector2 = Vector2(0, 0)):
        self.position: Vector2 = position
        angle = uniform(0, 2 * pi)
        speed = uniform(MIN_SPEED, MAX_STARTING_SPEED)  # speed
        self.velocity: Vector2 = Vector2(cos(angle) * speed, sin(angle) * speed)
        self.acceleration: Vector2 = Vector2(0, 0)

    def draw(self, surface):
        if self.velocity.length() == 0:
            polygon_points = BOID_POLYGON * BOID_SCALING_FACTOR + asarray(
                self.position, dtype=float
            )
        else:
            angle = radians(
                self.velocity.angle_to(Vector2(0, 1))
            )  # get angle off North line in radians
            # rotation matrix (since in pygame positive y is down sign of sin (lol) is flipped)
            ROTATION_MATRIX: ndarray = array(
                [
                    [cos(angle), sin(angle)],
                    [-sin(angle), cos(angle)],
                ],
                dtype=float,
            )
            # rotate the polygon points and translate to position
            polygon_points = (
                (ROTATION_MATRIX @ BOID_POLYGON.T).T
            ) * BOID_SCALING_FACTOR + asarray(self.position, dtype=float)
        # draw the polygon on the surface
        polygon(surface, WHITE, polygon_points.astype(int), 0)

    def distance_to(self, other: "Boid") -> float:
        return self.position.distance_to(other.position)

    # logic
    def interact(self, neighbors: list["Boid"]) -> None:
        if not neighbors:  # length = 0
            return

        alignment_force: Vector2 = (
            self.alignment(neighbors) * ALIGNMENT_WEIGHT
            if self.alignment_enabled
            else Vector2(0, 0)
        )
        cohesion_force: Vector2 = (
            self.cohesion(neighbors) * COHESION_WEIGHT
            if self.cohesion_enabled
            else Vector2(0, 0)
        )
        separation_force: Vector2 = (
            self.separation(neighbors) * SEPARATION_WEIGHT
            if self.repulsion_enabled
            else Vector2(0, 0)
        )

        self.acceleration = alignment_force + cohesion_force + separation_force

    def separation(self, neighbors: list["Boid"]) -> Vector2:
        separation_force: Vector2 = Vector2(0, 0)
        for neighbor in neighbors:
            difference = self.position - neighbor.position
            distance_squared = (
                difference.length_squared() or 1e-5
            )  # avoid singularity or smth
            strength = 1 / distance_squared  # inverse square law
            separation_force += difference.normalize() * strength

        separation_force /= len(neighbors)

        # steer towards the desired velocity
        desired_velocity = separation_force.normalize() * MAX_SPEED
        steering = desired_velocity - self.velocity
        return clamp_magnitude(steering, MAX_ACCELERATION)

    def cohesion(self, neighbors: list["Boid"]) -> Vector2:
        center_of_mass: Vector2 = Vector2(0, 0)
        for neighbor in neighbors:
            center_of_mass += neighbor.position
        center_of_mass /= len(neighbors)

        # steer towards the center of mass
        desired_velocity = (center_of_mass - self.position).normalize() * MAX_SPEED
        steering = desired_velocity - self.velocity
        return clamp_magnitude(steering, MAX_ACCELERATION)

    def alignment(self, neighbors: list["Boid"]) -> Vector2:
        average_velocity: Vector2 = Vector2(0, 0)
        for neighbor in neighbors:
            average_velocity += neighbor.velocity

        average_velocity /= len(neighbors)

        # steer towards the average velocity
        if average_velocity.length() > 0:
            desired_velocity = average_velocity.normalize() * MAX_SPEED
        else:
            desired_velocity = Vector2(0, 0)
        steering = desired_velocity - self.velocity
        return clamp_magnitude(steering, MAX_ACCELERATION)

    def update(self) -> None:
        # drag = k * speed^2
        # drag = -(k * ||V||^2 * unit(v))
        # drag = -(k * ||V||^2 * V / ||V||)
        # grad = -(k * ||V|| * V)
        # opbviously since we are subtracting we don't have to clamp again
        self.acceleration -= DRAG * self.velocity.length() * self.velocity

        # symplectic euler or whatever
        # update velocity
        self.velocity += self.acceleration * DT
        self.velocity = clamp_magnitude(self.velocity, MAX_SPEED)

        # update position
        self.position += self.velocity * DT

        # wrap around edges
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = WINDOW_HEIGHT
        elif self.position.y > WINDOW_HEIGHT:
            self.position.y = 0

        # reset acceleration
        self.acceleration = Vector2(0, 0)
