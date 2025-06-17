from os.path import join
from pygame.image import load

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Boids by Dennis Colak"
FPS = 60

# Colors
WHITE = "#ffffff"
BG = "#003a59"
BLACK = "#000000"

# Boids
BOID_BMP_PATH = join("assets", "boid.bmp")
BOID_BMP = load(BOID_BMP_PATH)
NUMBER_OF_BOIDS = 100
BOID_WIDTH = 15
