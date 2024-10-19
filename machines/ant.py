from machines.base import BaseMachine
from constants import *
from grids import Coordinate, BaseGrid

class LangtonAnt(BaseMachine):
    def __init__(self, coord: Coordinate, grid: BaseGrid, name: str, pattern: str = 'LR', colors=[WHITE, BLACK]):
        super().__init__(coord, grid, name)
        
        # Validate that the pattern contains only 'L' and 'R'
        if not pattern or not all(c in 'LR' for c in pattern):
            raise ValueError("Pattern must consist of 'L' and 'R' only.")
        self.pattern = pattern
        self.colors = colors  # List of colors the ant will cycle through
        self.direction = 0  # 0: Up, 1: Right, 2: Down, 3: Left
        
        # Use this dictionary to track which color corresponds to which pattern index
        self.color_to_pattern_index = {}  # Map colors to pattern indices
        self.next_color_index = 0  # The next color will map to this pattern index

    def move(self):
        # Fetch current cell
        cell = self.grid.get_cell(self.coord.x, self.coord.y)

        # Map any unseen colors to a pattern index
        if cell.color not in self.color_to_pattern_index:
            # Map the new color to the current pattern index
            self.color_to_pattern_index[cell.color] = self.next_color_index
            # Move to the next pattern index, using modulo to wrap around
            self.next_color_index = (self.next_color_index + 1) % len(self.pattern)

        # Fetch the pattern index for the current cell color
        pattern_index = self.color_to_pattern_index[cell.color]
        # Get the turn instruction from the pattern using the pattern index
        turn_instruction = self.pattern[pattern_index]

        # Change direction based on the turn instruction
        if turn_instruction == 'R':
            self.turn_right()
        elif turn_instruction == 'L':
            self.turn_left()

        # Change the cell color after moving
        # Cycle to the next color in the `colors` list
        current_color_index = self.colors.index(cell.color)
        next_color = self.colors[(current_color_index + 1) % len(self.colors)]  # Cycle through colors
        condition = cell.check_condition(next_color)
        
        if condition:
            self.score += condition  # Award a point if color changed

        # Move forward based on current direction
        self.move_forward()

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        self.direction = (self.direction - 1) % 4

    def move_forward(self):
        if self.direction == 0:  # Up
            self.coord.y -= 1
        elif self.direction == 1:  # Right
            self.coord.x += 1
        elif self.direction == 2:  # Down
            self.coord.y += 1
        elif self.direction == 3:  # Left
            self.coord.x -= 1
