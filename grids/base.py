from cells import BaseCell
from grids.coord import Coordinate
from conditions.borders import BaseBorder

class BaseGrid:
    def __init__(self, width, height, border: BaseBorder):
        self.width = width
        self.height = height
        self.cells = self.generate_cells()
        self.border = border

    def get_cell(self, x, y):
        return self.cells[x][y]
    
    def check_border(self, machine):
        return self.border.check_border(machine)
    
    def change_border_type(self, new_border: BaseBorder):
        self.border = new_border
        
    def generate_cells(self):
        return [[BaseCell(coord=Coordinate(x, y)) for y in range(self.height)] for x in range(self.width)]