"""Configuration constants for the boids simulation."""

from numpy import array, ndarray

# Display settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Boids Simulation"
FPS = 60
DT = 1 / FPS

# Colors
WHITE = "#ffffff"
BG = "#003a59"
GREEN = "#00ff00"
RED = "#ff0000"

# Boid appearance
BOID_SCALING_FACTOR = 1
BOID_POLYGON: ndarray = array(
    [
        [0, 0],
        [-4, -8],
        [0, -6],
        [4, -8],
    ],
    dtype=float,
)

# sim stuff
NUM_BOIDS = 200
MIN_SPEED = 1
MAX_SPEED = 500
MAX_STARTING_SPEED = 50
MAX_FORCE = 10
VISION_RADIUS_SQUARED = 50**2
SEPARATION_RADIUS_SQUARED = 20**2
DRAG_COEFFICIENT = 0.01

# weights
ALIGNMENT_WEIGHT = 5
COHESION_WEIGHT = 6
SEPARATION_WEIGHT = 10

# behavior flags
ENABLE_SEPARATION = True
ENABLE_ALIGNMENT = True
ENABLE_COHESION = True

# debug flags
SHOW_VISION_RADIUS = False
SHOW_VELOCITY_VECTORS = False
SHOW_FORCE_VECTORS = False

# other flags
ENABLE_BOUNDARY_WRAPPING = True

PERFORMANCE_MONITORING = True
