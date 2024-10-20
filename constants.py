WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WINDOW_SIZE = (1500, 750)
CELL_SIZE = 4

# Constants for the layout
GRID_PERCENTAGE = 0.7
SIDEBAR_WIDTH = WINDOW_SIZE[0] * (1 - GRID_PERCENTAGE)
GRID_WIDTH_PX = int(WINDOW_SIZE[0] * GRID_PERCENTAGE)
BORDER_COLOR = (159, 159, 159)  # Dimmer color for borders
CLEAR_BUTTON_COLOR = (200, 50, 50)
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 20
ADD_STEP = 10

GRID_WIDTH = GRID_WIDTH_PX // CELL_SIZE
GRID_HEIGHT = WINDOW_SIZE[1] // CELL_SIZE