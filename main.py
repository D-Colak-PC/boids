import pygame as pg
from random import randint
from consts import *
from boid import Boid


def init_pygame() -> pg.Surface:
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption(WINDOW_TITLE)
    return screen


def handle_events() -> None:
    pass  # placeholder


def simulate(boids: list[Boid]) -> list[Boid]:
    for i, boid_i in enumerate(boids):
        neighbors: list[Boid] = []
        for j, boid_j in enumerate(boids):
            if i == j:
                continue

            if boid_i.distance_to(boid_j) < VISION_RADIUS:
                neighbors.append(boid_j)

        boid_i.interact(neighbors)

    for boid in boids:
        boid.update()

    return boids


def init_boids() -> list[Boid]:
    boids: list[Boid] = []
    for _ in range(NUMBER_OF_BOIDS):
        position = pg.Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        boids.append(Boid(position))

    return boids


def draw_boids(boids: list[Boid], surface: pg.Surface) -> None:
    for boid in boids:
        boid.draw(surface)
        # pg.draw.circle(
        #     surface,
        #     WHITE,
        #     (int(boid.position.x), int(boid.position.y)),
        #     VISION_RADIUS,
        #     1,
        # )

        # pg.draw.line(
        #     surface,
        #     GREEN,
        #     (int(boid.position.x), int(boid.position.y)),
        #     (
        #         int(boid.position.x + boid.velocity.x / 2),
        #         int(boid.position.y + boid.velocity.y / 2),
        #     ),
        # )


def main() -> None:

    boids = init_boids()
    screen = init_pygame()
    clock = pg.time.Clock()

    # typical pygame loop
    running = True
    while running:
        for event in pg.event.get():
            handle_events()
            if event.type == pg.QUIT:
                running = False

        screen.fill(BG)  # clear screen

        boids = simulate(boids)
        draw_boids(boids, screen)

        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
