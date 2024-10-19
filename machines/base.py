from grids import Coordinate, BaseGrid
from constants import *
from game.game import *

class BaseMachine: 
    def __init__(self, coord: Coordinate, grid: BaseGrid, name: str):
        self.coord: Coordinate = coord
        self.grid: BaseGrid = grid
        self.score: float = 0
        self.name: str = name

    def move(self):
        raise NotImplementedError("move() not implemented")
