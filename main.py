from random import randint
import pygame as pg

from consts import *
from boid import Boid
from monitor import PerformanceMonitor
from grid import SpatialGrid


def create_boids() -> list[Boid]:
    boids = []
    for _ in range(NUM_BOIDS):
        position = pg.Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        boids.append(Boid(position))

    return boids


def handle_events() -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

    return True


def render_frame(surface: pg.Surface, boids: list[Boid]) -> None:
    surface.fill(BG)  # clear screen
    for boid in boids:
        boid.draw(surface)

    pg.display.flip()  # update the display


def populate_grid(boids: list[Boid], spatial_grid: SpatialGrid) -> SpatialGrid:
    for boid in boids:
        spatial_grid.add_boid(boid)
    return spatial_grid


def precompute_neighbors(
    boids: list[Boid], spatial_grid: SpatialGrid
) -> dict[Boid, list[Boid]]:
    neighbor_map = {}
    for boid in boids:
        neighbor_map[boid] = spatial_grid.get_nearby_boids(boid)

    return neighbor_map


def simulate(boids: list[Boid], spatial_grid: SpatialGrid) -> None:
    spatial_grid.reset()
    spatial_grid = populate_grid(boids, spatial_grid)
    neighbor_map = precompute_neighbors(boids, spatial_grid)
    for boid in boids:
        boid.update(neighbor_map[boid])


def main() -> None:
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption(WINDOW_TITLE)
    clock = pg.time.Clock()

    monitor = PerformanceMonitor()

    boids = create_boids()

    spatial_grid = SpatialGrid()

    running = True
    while running:
        monitor.start_frame()

        running = handle_events()

        monitor.start_simulation()
        simulate(boids, spatial_grid)
        monitor.end_simulation()

        monitor.start_rendering()
        render_frame(screen, boids)
        monitor.end_rendering()

        monitor.end_frame()
        monitor.print_performance()

        clock.tick(FPS)

    pg.quit()


if __name__ == "__main__":
    main()
