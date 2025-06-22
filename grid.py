import numpy as np
from math import isqrt
from boid import Boid
from utils import clamp
from consts import WINDOW_HEIGHT, WINDOW_WIDTH, VISION_RADIUS_SQUARED


class SpatialGrid:
    def __init__(self):
        self.cell_size: int = isqrt(VISION_RADIUS_SQUARED)
        self.cols: int = WINDOW_WIDTH // self.cell_size + 1
        self.rows: int = WINDOW_HEIGHT // self.cell_size + 1

        self.grid = np.empty((self.rows, self.cols), dtype=object)
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i, j] = []

    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i, j].clear()

    def get_cell_coords(self, x: float, y: float) -> tuple[int, int]:
        col = clamp(int(x // self.cell_size), 0, self.cols - 1)
        row = clamp(int(y // self.cell_size), 0, self.rows - 1)
        return col, row

    def add_boid(self, boid: Boid):
        col, row = self.get_cell_coords(boid.position.x, boid.position.y)
        self.grid[row, col].append(boid)

    def get_nearby_boids(self, boid: Boid) -> list:
        col, row = self.get_cell_coords(boid.position.x, boid.position.y)

        nearby_boids = []

        # check 3x3 grid around boid cell
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                check_row = row + row_offset
                check_col = col + col_offset
                if (
                    check_row < 0
                    or check_row >= self.rows
                    or check_col < 0
                    or check_col >= self.cols
                ):
                    continue  # skip cells out of the grid

                potential_boids = self.grid[check_row, check_col]

                for other_boid in potential_boids:
                    if boid == other_boid:  # boid cant be its own neighbor
                        continue

                    if boid.distance_to_squared(other_boid) < VISION_RADIUS_SQUARED:
                        nearby_boids.append(other_boid)

        return nearby_boids
