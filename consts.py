from os.path import join
from pygame.image import load
from numpy import array, ndarray
from pygame.math import Vector2

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Boids by Dennis Colak"
FPS = 60
DT = 1 / FPS  # Delta time in seconds

# Colors
WHITE = "#ffffff"
BG = "#003a59"
BLACK = "#000000"
GREEN = "#00ff00"

# Boids
BOID_BMP_PATH = join("assets", "boid.bmp")
BOID_BMP = load(BOID_BMP_PATH)
BOID_SCALING_FACTOR = 1
NUMBER_OF_BOIDS = 200
BOID_POLYGON: ndarray = array(
    [
        [0, 0],
        [-4, -8],
        [0, -6],
        [4, -8],
    ],
    dtype=float,
)
MIN_SPEED = 1
MAX_SPEED = 500
MAX_STARTING_SPEED = 50
MAX_ACCELERATION = 10
VISION_RADIUS = 150

ALIGNMENT_WEIGHT = 6
COHESION_WEIGHT = 9
SEPARATION_WEIGHT = 10

DRAG = 0.01
