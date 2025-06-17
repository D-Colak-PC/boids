from pygame.math import Vector2
from pygame import Surface
from pygame.transform import scale
from consts import *


class Boid:
    def __init__(self, position: Vector2 = Vector2(0, 0)):
        self.position: Vector2 = position
        self.velocity: Vector2 = Vector2(0, 0)

    def draw(self, surface):
        height = int(BOID_BMP.get_height() * (BOID_WIDTH / BOID_BMP.get_width()))
        scaled_bmp = scale(BOID_BMP, (BOID_WIDTH, height))

        # Draw the bitmap centered at the boid's position
        position = (self.position.x - BOID_WIDTH // 2, self.position.y - height // 2)
        surface.blit(scaled_bmp, position)
