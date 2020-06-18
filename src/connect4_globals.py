"""Contains the things global variables."""
# Colors
BLUE = (0, 0, 100)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
RED = (255, 3, 62)
TAN = (210, 180, 140)

# Board Dimensions
COLUMN_COUNT = 7
ROW_COUNT = 6
PADDING = 200
WIDTH = COLUMN_COUNT * PADDING
HEIGHT = (ROW_COUNT + 2) * PADDING
SIZE = (WIDTH, HEIGHT)

# Results
SUCCESS = 1
FAILURE = -1

# Numbers
ALPHA = -1000000
BETA = 1000000
INF = 1000000
N_INF = -INF
