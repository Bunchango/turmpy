from constants import *
from grids.coord import Coordinate

class BaseCell:
    def __init__(self, coord: Coordinate, color=WHITE):
        self.coord = coord
        self.color = color

    def check_condition(self, new_color):
        if self.color != new_color:
            self.color = new_color  # Change to the new color
            return 1  # Color changed, award point
        return 0  # No change, no points awarded

