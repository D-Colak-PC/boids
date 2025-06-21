from random import randint
import pygame as pg

from consts import *
from boid import Boid


def crete_boids() -> list[Boid]:
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


def get_neighbors(target: Boid, boids: list[Boid]) -> list[Boid]:
    neighbors = []
    for boid in boids:
        if boid != target and target.distance_to(boid) < VISION_RADIUS:
            neighbors.append(boid)
    return neighbors


def precompute_neighbors(boids: list[Boid]) -> dict[Boid, list[Boid]]:
    neighbor_map = {}
    for boid in boids:
        neighbor_map[boid] = get_neighbors(boid, boids)
    return neighbor_map


def simulate(boids: list[Boid]) -> None:
    neighbor_map = precompute_neighbors(boids)
    for boid in boids:
        boid.update(neighbor_map[boid])


def main() -> None:
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption(WINDOW_TITLE)
    clock = pg.time.Clock()

    boids = crete_boids()

    running = True
    while running:
        running = handle_events()
        simulate(boids)
        render_frame(screen, boids)
        clock.tick(FPS)

    pg.quit()


if __name__ == "__main__":
    main()
