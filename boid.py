from math import pi, cos, sin, radians
from random import uniform
import numpy as np
from pygame import Surface
from pygame.draw import polygon, circle, line
from pygame.math import Vector2

from consts import *
from utils import clamp_magnitude


class Boid:
    def __init__(self, position: Vector2 = Vector2(0, 0)) -> None:
        self.position = position
        self.acceleration = Vector2(0, 0)

        # use angle and speed to set velocity randomly and also easily limit speed
        angle = uniform(0, 2 * pi)
        speed = uniform(MIN_SPEED, MAX_STARTING_SPEED)
        self.velocity = Vector2(cos(angle) * speed, sin(angle) * speed)

    def distance_to(self, other: "Boid") -> float:
        return self.position.distance_to(other.position)

    # used in some calculations, much faster than distance_to
    def distance_to_squared(self, other: "Boid") -> float:
        return self.position.distance_squared_to(other.position)

    # Separation: steer to avoid crowding local flockmates
    def separation(self, neighbors: list["Boid"]) -> Vector2:
        separation_force = Vector2(0, 0)
        for neighbor in neighbors:
            distance_squared = max(self.distance_to_squared(neighbor), 1e-5)
            if distance_squared <= SEPARATION_RADIUS_SQUARED:
                difference = self.position - neighbor.position
                strength = 1 / distance_squared
                separation_force += difference.normalize() * strength

        if separation_force == Vector2(0, 0):
            return Vector2(0, 0)

        separation_force /= len(neighbors)

        desired_velocity = separation_force.normalize() * MAX_SPEED
        steering = desired_velocity - self.velocity
        return clamp_magnitude(steering, MAX_FORCE)

    # Alignment: steer towards the average heading of local flockmates
    def alignment(self, neighbors: list["Boid"]) -> Vector2:
        average_velocity = Vector2(0, 0)
        for neighbor in neighbors:
            average_velocity += neighbor.velocity
        average_velocity /= len(neighbors)

        if average_velocity.length() > 0:
            desired_velocity = average_velocity.normalize() * MAX_SPEED
        else:
            desired_velocity = Vector2(0, 0)

        steering = desired_velocity - self.velocity
        return clamp_magnitude(steering, MAX_FORCE)

    # Cohesion: steer to move toward the average position of local flockmates
    def cohesion(self, neighbors: list["Boid"]) -> Vector2:
        center_of_mass = Vector2(0, 0)
        for neighbor in neighbors:
            center_of_mass += neighbor.position
        center_of_mass /= len(neighbors)

        desired_velocity = (center_of_mass - self.position).normalize() * MAX_SPEED
        steering = desired_velocity - self.velocity
        return clamp_magnitude(steering, MAX_FORCE)

    def interact(self, neighbors: list["Boid"]) -> None:
        if not neighbors:
            return

        total_force = Vector2(0, 0)

        if ENABLE_SEPARATION:
            separation_force = self.separation(neighbors) * SEPARATION_WEIGHT
            total_force += separation_force

        if ENABLE_ALIGNMENT:
            alignment_force = self.alignment(neighbors) * ALIGNMENT_WEIGHT
            total_force += alignment_force

        if ENABLE_COHESION:
            cohesion_force = self.cohesion(neighbors) * COHESION_WEIGHT
            total_force += cohesion_force

        self.acceleration = total_force

    def apply_drag(self) -> None:
        self.acceleration += -DRAG_COEFFICIENT * self.velocity.length() * self.velocity

    def move(self) -> None:
        self.velocity += self.acceleration * DT
        self.velocity = clamp_magnitude(self.velocity, MAX_SPEED)
        self.position += self.velocity * DT

    def wrap_around_screen(self) -> None:
        if ENABLE_BOUNDARY_WRAPPING:
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            elif self.position.x > WINDOW_WIDTH:
                self.position.x = 0

            if self.position.y < 0:
                self.position.y = WINDOW_HEIGHT
            elif self.position.y > WINDOW_HEIGHT:
                self.position.y = 0

    def update(self, neighbors: list["Boid"]) -> None:
        self.interact(neighbors)
        self.apply_drag()
        self.move()
        self.wrap_around_screen()

        self.acceleration = Vector2(0, 0)

    def draw(self, surface: Surface) -> None:
        if self.velocity.length() == 0:
            polygon_points = BOID_POLYGON * BOID_SCALING_FACTOR + np.asarray(
                self.position, dtype=float
            )
        else:
            angle = radians(self.velocity.angle_to(Vector2(0, 1)))

            rotation_matrix = np.array(
                [
                    [cos(angle), sin(angle)],
                    [-sin(angle), cos(angle)],
                ],
                dtype=float,
            )

            rotated_points = (rotation_matrix @ BOID_POLYGON.T).T
            polygon_points = rotated_points * BOID_SCALING_FACTOR + np.asarray(
                self.position, dtype=float
            )

        polygon(surface, WHITE, polygon_points.astype(int))

        # debug stuff
        integer_position = (int(self.position.x), int(self.position.y))

        if SHOW_VISION_RADIUS:
            circle(surface, WHITE, integer_position, VISION_RADIUS_SQUARED, 1)

        if SHOW_VELOCITY_VECTORS and self.velocity.length() > 0:
            velocity_end = (
                int(self.position.x + self.velocity.x / 10),
                int(self.position.y + self.velocity.y / 10),
            )
            line(surface, GREEN, integer_position, velocity_end, 2)

        if SHOW_FORCE_VECTORS and self.acceleration.length() > 0:
            # Scale acceleration for visibility
            force_end = (
                int(self.position.x + self.acceleration.x * 5),
                int(self.position.y + self.acceleration.y * 5),
            )
            line(surface, RED, integer_position, force_end, 2)
