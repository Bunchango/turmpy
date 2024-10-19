class Coordinate:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, value):
        return self.x == value.x and self.y == value.y
    
    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def copy(self):
        return Coordinate(self.x, self.y)